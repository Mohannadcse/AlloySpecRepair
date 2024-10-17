import typer
import os
import time
import csv
import re
import subprocess
import json
import shutil
import logging
import difflib
from enum import Enum
from pydantic import BaseSettings
from typing import List, Tuple, Dict
from rich import print
from openai import AzureOpenAI

# Azure OpenAI Settings
AZURE_OPENAI_API_KEY = 
AZURE_OPENAI_API_BASE = 
AZURE_OPENAI_DEPLOYMENT_NAME = 
AZURE_OPENAI_MODEL_NAME = 
AZURE_OPENAI_API_VERSION = 

app = typer.Typer()

class FeedbackOption(Enum):
    NO_FEEDBACK = "No-Feedback"
    GENERIC_FEEDBACK = "Generic-Feedback"
    AUTO_FEEDBACK = "Auto-Feedback"

class CLIOptions(BaseSettings):
    dataset_path: str = ""
    result_path: str = ""
    bug_rep_hist: bool = False
    max_iter: int = 5
    feedback: FeedbackOption = FeedbackOption.NO_FEEDBACK

    class Config:
        extra = "forbid"
        env_prefix = ""

def setup_logger(log_file_path):
    logger = logging.getLogger('AlloyRepair')
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def check_result_dir(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        os.makedirs(directory_path)

def remove_dollar_sign(text):
    return text.replace("$", "")

def extract_line_column(error_message):
    match = re.search(r"at line (\d+) column (\d+)", error_message)
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None

def remove_specification_part(line):
    start_index = line.find(" in ")
    end_index = line.find("specification:")
    if start_index != -1 and end_index != -1:
        return line[:start_index] + line[end_index + len("specification:"):]
    else:
        return line

def remove_compilation_error_line(compilation_error_message):
    lines = compilation_error_message.split("\n")
    new_lines = []
    for line in lines:
        line = remove_specification_part(line)
        if line.startswith("in") and line.endswith("specification:"):
            continue
        line = line.replace("Warning", "generates a compilation error at")
        new_lines.append(line)
    return "\n".join(new_lines)

def _normalize_string(s):
    return "\n".join(line.rstrip() for line in s.splitlines())

def normalize_list_of_strings(lst):
    return [_normalize_string(s) for s in lst]

def process_Alloy_json_report(json_data) -> List[str]:
    output_lines = []

    def add_output_line(line):
        output_lines.append(line.strip())

    counterexamples = json_data.get("counterexamples", [])
    for item in counterexamples:
        cntr_cmd = item.get("cntr_cmd", "").replace("expect 0", "").strip()
        counterexample_msg = item.get("counterexample_msg", "")
        counterexample = item.get("counterexample", "").lower()
        assertion_name = remove_dollar_sign(cntr_cmd.replace("Check", "").strip())

        if counterexample == "no":
            add_output_line(f"Executing command [{cntr_cmd}] of the proposed Alloy model, "
                            f"Alloy analyzer found no counterexample, indicating assert "
                            f"{assertion_name} is valid.")
        else:
            add_output_line(f"Executing command [{cntr_cmd}] of the proposed Alloy model, "
                            f"Alloy analyzer found a counterexample, indicating assert "
                            f"{assertion_name} is violated by this counterexample:")
            counterexample_msg_lines = [remove_dollar_sign(line.replace("this/", ""))
                                        for line in counterexample_msg.split("\n")
                                        if line and "Counterexample found which means that" not in line]
            output_lines.extend(counterexample_msg_lines)

    instances = json_data.get("instances", [])
    for item in instances:
        instance_cmd = item.get("instance_cmd", "").strip()
        instance_name = remove_dollar_sign(instance_cmd.replace("Run", "").strip())
        inst = item.get("instances", "").lower()

        if inst == "yes":
            add_output_line(f"Executing command [{instance_cmd}] of proposed Alloy model, "
                            f"Alloy analyzer generates a valid instance, indicating the model is "
                            f"consistent and pred {instance_name} is satisfied.")
        else:
            add_output_line(f"Executing command [{instance_cmd}] of proposed Alloy model, "
                            f"Alloy analyzer does not generate a valid instance, indicating the model is "
                            f"inconsistent and pred {instance_name} is not satisfied.")

    error = json_data.get("error", "")
    if error:
        lines_to_discard = ["als", "\tat edu.mit", "\tat alloyrepair"]
        if "Warning Line" in error:
            line_number, column_number = extract_line_column(error)
            compilation_error_message = remove_dollar_sign(" ".join(error.split(" ")[5:]).strip())
            compilation_error_message = remove_compilation_error_line(compilation_error_message)
            error_lines = [line for line in compilation_error_message.split("\n") if "als" not in line]
            add_output_line(f"Compiling the proposed Alloy model generates a compilation error at "
                            f"Line {line_number}, Column {column_number}: {' '.join(error_lines)}")
        elif error.startswith("Type error in"):
            line_number, column_number = extract_line_column(error)
            error_lines = [line for line in error.split("\n")
                           if not any(discard in line for discard in lines_to_discard)]
            add_output_line(f"Compiling the proposed Alloy model generates a type error at Line "
                            f"{line_number}, Column {column_number}: {' '.join(error_lines)}")
        else:
            syntax_error_message = remove_dollar_sign(" ".join(error.split(" ")[5:]).strip()).split("\n")
            add_output_line(f"Compiling the proposed Alloy model generates a syntax error: "
                            f"{' '.join(syntax_error_message)}")
    return output_lines

def _preprocess_string(s):
    return [line.strip() for line in s.splitlines()]

def repeated_spec(str1, str2):
    differ = difflib.Differ()
    str1_processed = _preprocess_string(str1)
    str2_processed = _preprocess_string(str2)
    diff = differ.compare(str1_processed, str2_processed)
    differences = any(line.startswith("-") or line.startswith("+") for line in diff)
    return not differences

def _replace_newlines_except_specific_statement(input_string):
    specific_statement = '\n{\n"request": "run_alloy_analyzer",\n"specification'
    if specific_statement in input_string:
        before_statement, after_statement = input_string.split(specific_statement, 1)
        before_statement = before_statement.replace("\n", "\\n")
        after_statement = after_statement.replace("\n", "\\n")
        return before_statement + specific_statement + after_statement
    else:
        return input_string.replace("\n", "\\n")

def _modify_string(input_string):
    if input_string.endswith("\n}"):
        return input_string[:-2] + "}"
    return input_string

class AlloyAnalyzerAgent:
    def __init__(self, client: AzureOpenAI, deployment_name: str, user_message: str, logger: logging.Logger):
        self.client = client
        self.deployment_name = deployment_name
        self.user_message = user_message
        self.logger = logger
        self.orig_spec_content: str = None
        self.orig_spec_file: str = None
        self.spec_file_dir_res: str = None
        self.setting_name: str = None
        self.repair_iterations: int = 0
        self.wrong_format_msg: int = 0
        self.detailed_fixes: Dict[int, Tuple[List[str], List[str]]] = {}
        self.history_bug_fix: List[Tuple[List[str], List[str]]] = []
        self.num_repeated_fixes: int = 0
        self.num_repeated_init_spec: int = 0
        self.fst_iter_repeated_init_spec: bool = False
        self.opts: CLIOptions = None
        self.total_tokens: int = 0
        self.total_cost: float = 0.0
        self.start_time: float = 0.0
        self.proposed_spec: str = None
        self.final_status = None
        self.final_iteration = 0
        self.final_error = ""
        self.last_json_file = None

    def get_system_instructions(self):
        return (
            "You are an expert in repairing Alloy declarative specifications.\n"
            "You will be presented with Alloy <Faulty_SPECIFICATIONS>.\n"
            "Your task is to FIX/REPAIR the <Faulty_SPECIFICATIONS>.\n"
            "Use the tool `run_alloy_analyzer` to demonstrate and validate the\n"
            "<FIXED_SPECIFICATIONS>. Wait for my feedback, which may include error\n"
            "messages or Alloy solver results. You will have 5 trials to fix the\n"
            "<Faulty_SPECIFICATIONS>.\n\n"
            "**Adhere to the Following Rules**:\n"
            "- The <FIXED_SPECIFICATIONS> should be consistent (having instances) and\n"
            "  all the assertions should be valid (no counterexample).\n"
            "- DO NOT REPEAT the <FIXED_SPECIFICATIONS> that I sent you.\n"
            "- DO NOT provide any commentary and always send me anything ONLY using the\n"
            "  tool `run_alloy_analyzer`.\n"
            "- The <FIXED_SPECIFICATIONS> MUST be different than the\n"
            "  <Faulty_SPECIFICATIONS>.\n"
        )

    def run(self):
        messages = [
            {"role": "system", "content": self.get_system_instructions()},
            {"role": "user", "content": self.user_message},
        ]
        
        self.logger.info(f"Initial user message: {self.user_message}")
        
        while self.repair_iterations < self.opts.max_iter:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.2,
                max_tokens=4000,
            )
            
            self.total_tokens += response.usage.total_tokens
            self.total_cost += (response.usage.prompt_tokens * 0.00003 + response.usage.completion_tokens * 0.00006)
            
            assistant_message = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_message})
            
            self.logger.info(f"Assistant response (iteration {self.repair_iterations + 1}):\n{assistant_message}")
            
            result = self.run_alloy_analyzer(assistant_message)
            if result == "DONE":
                self.logger.info("Repair process completed successfully.")
                break
            
            messages.append({"role": "user", "content": result})
            self.logger.info(f"Feedback to assistant (iteration {self.repair_iterations + 1}):\n{result}")

        self._write_summary_csv()

    def run_alloy_analyzer(self, msg: str) -> str:
        self.proposed_spec = self.filter_specifications(msg)
        repeated_init_spec = repeated_spec(self.proposed_spec, self.orig_spec_content)
        self.repair_iterations += 1
        
        if repeated_init_spec:
            self.num_repeated_init_spec += 1
            if self.repair_iterations == 1:
                self.fst_iter_repeated_init_spec = True
            return self.handle_next_iteration(False, False, True, None)

        res_path = os.path.join(self.opts.result_path, self.spec_file_dir_res)
        if res_path and not os.path.exists(res_path):
            os.makedirs(res_path)
        proposed_spec_file_no_ext = os.path.join(
            res_path,
            f"{self.spec_file_dir_res}_{self.repair_iterations}_{repeated_init_spec}"
        )
        proposed_spec_file = proposed_spec_file_no_ext + ".als"

        with open(proposed_spec_file, "w") as f:
            f.write(self.proposed_spec)

        alloy_analyzer_path = "./repair_alloy_spec/AlloyGPTverifier.jar"
        command = ["java", "-jar", alloy_analyzer_path, proposed_spec_file]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, _ = process.communicate()

        json_report = proposed_spec_file_no_ext + "_alloyAnalyzerReport.json"

        if os.path.exists(json_report):
            with open(json_report, "r") as file:
                json_data = json.load(file)

            error = json_data.get("error", "").strip()
            error_is_empty = not error
            instance_exists = any(item.get("instances") == "Yes" for item in json_data.get("instances", []))
            all_counterexamples_no = all(item.get("counterexample") == "no" for item in json_data.get("counterexamples", []))
            
            if error_is_empty and instance_exists and all_counterexamples_no:
                self.final_status = "FIXED"
                self.final_iteration = self.repair_iterations
                self.final_error = ""
                return "DONE"
            elif "Syntax error in" in error:
                self.final_status = "SYNTAX_ERROR"
            elif "Type error in" in error:
                self.final_status = "TYPE_ERROR"
            else:
                self.final_status = "NOT_FIXED"

            self.final_iteration = self.repair_iterations
            self.final_error = error

            if self.repair_iterations == self.opts.max_iter:
                return "DONE"
            else:
                return self.handle_next_iteration(False, False, False, json_data)
        else:
            return self.handle_next_iteration(True, False, False, None)

    def _write_summary_csv(self):
        columns = [
            "fileName", "finalIteration", "status", "repeated_fixes", "repeated_init_spec",
            "fst_iter_repeated_init_spec", "wrong_format_msg", "total_tokens",
            "total_cost", "running_time", "Error_msg"
        ]
        file_path = os.path.join(self.opts.result_path, "summary.csv")
        write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
        
        end_time = time.time()
        running_time = round(end_time - self.start_time, 2)

        row = (
            self.spec_file_dir_res, self.final_iteration, self.final_status,
            self.num_repeated_fixes, self.num_repeated_init_spec,
            self.fst_iter_repeated_init_spec, self.wrong_format_msg,
            self.total_tokens, self.total_cost, running_time, self.final_error
        )

        with open(file_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow(columns)
            writer.writerow(row)

    def _write_bug_fix_pair_csv(self, bugs, fixes, file_path):
        columns = ["Iteration", "Bugs", "Bugs_len", "Fixes", "Fixes_len"]
        with open(file_path, "a", newline="") as csvfile:
            file_exists = os.path.isfile(file_path)
            writer = csv.writer(csvfile)
            bugs_str = "&".join(bugs)
            fixes_str = "&".join(fixes)
            if not file_exists:
                writer.writerow(columns)
            writer.writerow([self.repair_iterations + 1, bugs_str, len(bugs), fixes_str, len(fixes)])

    def _print_history_bug_fix(self, pairs):
        result = ""
        for idx, (bugs, fixes) in enumerate(pairs, 1):
            result += f"Pair {idx}:\n\n"
            result += "- Bug Statements:\n"
            for bug in bugs:
                result += f"  {bug}\n"
            result += "\n- Fix Statements:\n"
            for fix in fixes:
                result += f"  {fix}\n"
            result += "\n---\n"
        return result

    def handle_next_iteration(self, wrong_format: bool, repeated_bug_fix: bool, repeated_init_spec: bool, json_data: Dict):
        if wrong_format:
            self.wrong_format_msg += 1
        if self.repair_iterations == self.opts.max_iter:
            end_time = time.time()
            running_time = round(end_time - self.start_time, 2)
            row = (
                self.spec_file_dir_res, self.repair_iterations + 1, "reached_max_iter",
                self.num_repeated_fixes, self.num_repeated_init_spec,
                self.fst_iter_repeated_init_spec, self.wrong_format_msg,
                self.total_tokens, self.total_cost, running_time, ""
            )
            self._write_summary_csv(row)
            return "DONE"
        else:
            self.repair_iterations += 1

            if repeated_init_spec:
                msg_to_llm = ("The proposed <FIXED_SPECIFICATIONS> is IDENTICAL to "
                              "Alloy <Faulty_SPECIFICATIONS> that I sent you. "
                              "**DO NOT** send Alloy specifications that I sent you again. "
                              "ALWAYS USE the tool `run_alloy_analyzer` to send me a new <FIXED_SPECIFICATIONS>.")
            elif repeated_bug_fix:
                if self.opts.bug_rep_hist:
                    msg_to_llm = (f"**IMPORTANT: DO NOT REPEAT** these PAIRS of "
                                  f"**Bug Statements** and **Fix Statements** in your next responses: "
                                  f"{self._print_history_bug_fix(self.history_bug_fix)}")
                else:
                    msg_to_llm = "This is a repeated bug/fix pair. DON'T send it again."
            elif self.opts.feedback == FeedbackOption.GENERIC_FEEDBACK and json_data is not None:
                alloy_msg = ("Below are the results from the Alloy Analyzer. "
                             "Fix all Errors and Counterexamples before sending me the next "
                             "<FIXED_SPECIFICATIONS>.")
                report_msg = process_Alloy_json_report(json_data)
                formatted_report_msg = "\n".join([line.strip() for line in report_msg])
                msg_to_llm = f"{alloy_msg} {formatted_report_msg}"
            elif self.opts.feedback == FeedbackOption.AUTO_FEEDBACK and json_data is not None:
                report_msg = process_Alloy_json_report(json_data)
                formatted_report_msg = "\n".join([line.strip() for line in report_msg])
                response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=[
                        {"role": "system", "content": "You are an Expert in Analyzing Alloy Analyzer reports."},
                        {"role": "user", "content": f"Can you describe concisely and precisely the modifications needed to fix the error in at most 2 sentences based on this report from Alloy Analyzer: {formatted_report_msg}? After running this Alloy Model is: {self.proposed_spec}"}
                    ],
                    temperature=0.2,
                    max_tokens=3000,
                )
                self.total_tokens += response.usage.total_tokens
                self.total_cost += (response.usage.prompt_tokens * 0.00003 + response.usage.completion_tokens * 0.00006)
                msg_to_llm = response.choices[0].message.content
            elif wrong_format:
                msg_to_llm = ("You must use the CORRECT format described in the tool "
                              "`run_alloy_analyzer` to send me the fixed specifications. "
                              "You either forgot to use it, or you used it with the WRONG format. "
                              "Make sure all fields are filled out.")
            else:
                msg_to_llm = "The proposed specification DID NOT fix the bug."

            return msg_to_llm

    def filter_specifications(self, specifications: str) -> str:
        # Remove code block markers
        specifications = specifications.replace('```', '')
        
        # Remove any instances of 'alloy' or 'run_alloy_analyzer'
        specifications = re.sub(r'\b(alloy|run_alloy_analyzer)\b', '', specifications, flags=re.IGNORECASE)
        
        # Remove any lines that start with 'run_alloy_analyzer'
        specifications = re.sub(r'^run_alloy_analyzer.*$', '', specifications, flags=re.MULTILINE)
        
        # Remove empty lines
        specifications = re.sub(r'^\s*$', '', specifications, flags=re.MULTILINE)
        
        # Strip leading and trailing whitespace
        filtered_spec = specifications.strip()
        
        return filtered_spec

    def run_alloy_analyzer(self, msg: str) -> str:
        self.proposed_spec = self.filter_specifications(msg)
        repeated_init_spec = repeated_spec(self.proposed_spec, self.orig_spec_content)
        if repeated_init_spec:
            self.num_repeated_init_spec += 1
            if self.repair_iterations == 0:
                self.fst_iter_repeated_init_spec = True
            return self.handle_next_iteration(False, False, True, None)

        res_path = os.path.join(self.opts.result_path, self.spec_file_dir_res)
        if res_path and not os.path.exists(res_path):
            os.makedirs(res_path)
        proposed_spec_file_no_ext = os.path.join(
            res_path,
            f"{self.spec_file_dir_res}_{self.repair_iterations}_{repeated_init_spec}"
        )
        proposed_spec_file = proposed_spec_file_no_ext + ".als"

        with open(proposed_spec_file, "w") as f:
            f.write(self.proposed_spec)

        alloy_analyzer_path = "./repair_alloy_spec/AlloyGPTverifier.jar"
        command = ["java", "-jar", alloy_analyzer_path, proposed_spec_file]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, _ = process.communicate()

        json_report = proposed_spec_file_no_ext + "_alloyAnalyzerReport.json"

        if os.path.exists(json_report):
            with open(json_report, "r") as file:
                json_data = json.load(file)

            error = json_data.get("error", "").strip()
            error_is_empty = not error
            instance_exists = any(item.get("instances") == "Yes" for item in json_data.get("instances", []))
            all_counterexamples_no = all(item.get("counterexample") == "no" for item in json_data.get("counterexamples", []))
            
            end_time = time.time()
            running_time = round(end_time - self.start_time, 2)
            
            if error_is_empty and instance_exists and all_counterexamples_no:
                status = "FIXED"
            elif "Syntax error in" in error:
                status = "SYNTAX_ERROR"
            elif "Type error in" in error:
                status = "TYPE_ERROR"
            else:
                status = "NOT_FIXED"

            row = (
                self.spec_file_dir_res, self.repair_iterations + 1, status,
                self.num_repeated_fixes, self.num_repeated_init_spec,
                self.fst_iter_repeated_init_spec, self.wrong_format_msg,
                self.total_tokens, self.total_cost, running_time, error
            )
            self._write_summary_csv(row)

            if status == "FIXED":
                return "DONE"
            else:
                return self.handle_next_iteration(False, False, False, json_data)
        else:
            return self.handle_next_iteration(True, False, False, None)

    def _write_summary_csv(self, row):
        columns = [
            "fileName", "iterations", "status", "repeated_fixes", "repeated_init_spec",
            "fst_iter_repeated_init_spec", "wrong_format_msg", "total_tokens",
            "total_cost", "running_time", "Error_msg"
        ]
        file_path = os.path.join(self.opts.result_path, "summary.csv")
        write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
        with open(file_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow(columns)
            writer.writerow(row)

def determine_setting(feedback: FeedbackOption) -> str:
    if feedback == FeedbackOption.NO_FEEDBACK:
        return "Setting-1"
    elif feedback == FeedbackOption.GENERIC_FEEDBACK:
        return "Setting-2"
    elif feedback == FeedbackOption.AUTO_FEEDBACK:
        return "Setting-3"
    else:
        return None

def chat(opts: CLIOptions) -> None:
    setting = determine_setting(opts.feedback)
    if setting is None:
        raise ValueError("Invalid feedback option.")

    print("[blue] Welcome to the Specification Repair chatbot!\n")

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_API_BASE
    )

    opts.result_path = f"results_{os.path.basename(opts.dataset_path)}_{setting}"
    check_result_dir(opts.result_path)

    log_file_path = os.path.join(opts.result_path, "interaction_log.txt")
    logger = setup_logger(log_file_path)

    files_to_skip = set()
    dir_path = opts.dataset_path
    for spec_file in os.scandir(dir_path):
        if any(os.path.splitext(spec_file.name)[0] in skip_file for skip_file in files_to_skip):
            continue
        if spec_file.is_file() and os.path.splitext(spec_file.name)[1] == ".als":
            print(spec_file.name)
            logger.info(f"Processing file: {spec_file.name}")
            try:
                with open(spec_file, "r") as file:
                    spec = file.read()
                    lines = spec.splitlines()
                    cleaned_lines = [line.replace("\t", "").strip() for line in lines]
                    cleaned_spec = "\n".join(cleaned_lines)

                agent = AlloyAnalyzerAgent(
                    client=client,
                    deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
                    user_message=f"Here is the <Faulty_SPECIFICATIONS>: \n{cleaned_spec}",
                    logger=logger
                )
                agent.orig_spec_content = cleaned_spec
                agent.orig_spec_file = spec_file
                agent.setting_name = setting
                agent.spec_file_dir_res = os.path.splitext(os.path.basename(agent.orig_spec_file))[0]
                agent.opts = opts
                agent.start_time = time.time()
                agent.run()
            except Exception as e:
                logger.error(f"Exception occurred: {str(e)}")
                row = (
                    spec_file.name, agent.repair_iterations + 1, "Exception",
                    agent.num_repeated_fixes, agent.num_repeated_init_spec,
                    agent.fst_iter_repeated_init_spec, agent.wrong_format_msg,
                    agent.total_tokens, agent.total_cost, "NA", str(e)
                )
                agent._write_summary_csv(row)
                continue
            finally:
                logger.info(f"Finished processing file: {spec_file.name}")

@app.command()
def main(
    dataset_path: str = typer.Option("", "--dataset_path", "-db", help="path to Alloy dataset"),
    feedback: FeedbackOption = typer.Option(
        FeedbackOption.NO_FEEDBACK,
        "--feedback",
        "-fb",
        help="Specify the feedback option: No-Feedback, Generic-Feedback, or Auto-Feedback",
    ),
    bug_rep_hist: bool = typer.Option(False, "--bug_hist", "-bg", help="send bug/repair history"),
    max_iter: int = typer.Option(5, "--max", "-m", help="max number of iterations"),
    result_path: str = typer.Option("./results/", "--result_path", "-r", help="path to analysis results"),
) -> None:
    opts = CLIOptions(
        dataset_path=dataset_path,
        bug_rep_hist=bug_rep_hist,
        result_path=result_path,
        max_iter=max_iter,
        feedback=feedback,
    )

    chat(opts)

if __name__ == "__main__":
    app()