import csv
import os
import re
import subprocess
import json
import time

from rich import print
from typing import List, Tuple, Dict
from utility import (
    CLIOptions,
    process_Alloy_json_report,
    repeated_spec,
    _replace_newlines_except_specific_statement,
    _modify_string,
    FeedbackOption,
)
from langroid.parsing.parse_json import extract_top_level_json
from langroid.mytypes import Entity
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.agent.tool_message import ToolMessage
from langroid.agent.chat_document import ChatDocument
from langroid.language_models.azure_openai import AzureConfig


class VerifierMessage(ToolMessage):
    request: str = "run_alloy_analyzer"
    purpose: str = """
        To show a <FIXED_SPECIFICATIONS> to the user. Use this tool whenever you
        want to SHOW or VALIDATE the <FIXED_SPECIFICATIONS>. NEVER list out a
        <FIXED_SPECIFICATIONS> without using this tool.
    """
    specification: str

    @staticmethod
    def handle_message_fallback(
        agent: ChatAgent, msg: str | ChatDocument
    ) -> str | ChatDocument | None:
        print("[red]RecipientTool: Recipient not specified, asking LLM to clarify.")
        from alloy_verification_tool import AlloyAnalzerAgent

        assert isinstance(agent, AlloyAnalzerAgent)
        diff_s_escaped = False
        current_s_escaped = msg.content
        if isinstance(msg, ChatDocument) and msg.metadata.sender == Entity.LLM:
            resp = _modify_string(msg.content)
            s_escaped = _replace_newlines_except_specific_statement(resp)
            if s_escaped != current_s_escaped:
                diff_s_escaped = True
                current_s_escaped = s_escaped
            # check if extract_top_level_json is not empty
            if len(extract_top_level_json(s_escaped)) > 0 and diff_s_escaped:
                msg.content = s_escaped
                return agent.agent_response(msg)
            else:
                token, cost = agent._extract_tokens_cost(agent.token_stats_str)
                agent.analyzer_agent_tokens += token
                agent.analyzer_agent_cost = cost
                return agent.handle_next_iteration(True, False, False, None)


class AlloyAnalzerAgent(ChatAgent):
    orig_spec_content: str = None
    orig_spec_file: str = None
    spec_file_dir_res: str = None
    setting_name: str = None
    repair_iterations: int = 0
    wrong_format_msg: int = 0
    detailed_fixes: Dict[int, Tuple[List[str], List[str]]] = {}
    history_bug_fix: List[Tuple[List[str], List[str]]] = []
    num_repeated_fixes: int = 0
    num_repeated_init_spec: int = 0
    fst_iter_repeated_init_spec: bool = False
    opts: CLIOptions = None
    prompt_agent_tokens: int = 0
    prompt_agent_cost: float = 0.0
    analyzer_agent_tokens: int = 0
    analyzer_agent_cost: float = 0.0
    start_time: float = 0.0

    sys_instructions = (
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

    def _extract_tokens_cost(self, token_stats_str):
        pattern = r"in=(\d+), out=(\d+), .* now=\$(\d+\.\d+), cumul=\$(\d+\.\d+)"
        match = re.search(pattern, token_stats_str)
        if match:
            in_tokens, out_tokens, now_cost, cumul_cost = match.groups()
            return int(in_tokens) + int(out_tokens), float(cumul_cost)

    def _write_summary_csv(self, row):
        # Column headers
        columns = [
            "fileName",
            "iterations",
            "fixed",
            "repeated_fixes",
            "repeated_init_spec",
            "fst_iter_repeated_init_spec",
            "wrong_format_msg",
            "analyzer_agent_tokens",
            "analyzer_agent_cost",
            "prompt_agent_tokens",
            "prompt_agent_cost",
            "running_time",
            "Error_msg",
        ]
        file_path = os.path.join(self.opts.result_path, "summary.csv")

        # Determine whether to write the header
        write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0

        # Append data to a CSV file (or create a new one if it doesn't exist)
        with open(file_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write the header only if the file did not exist before
            if write_header:
                writer.writerow(columns)
            # Write the row
            writer.writerow(row)

    def _write_bug_fix_pair_csv(self, bugs, fixes, file_path):
        columns = ["Iteration", "Bugs", "Bugs_len", "Fixes", "Fixes_len"]
        with open(file_path, "a", newline="") as csvfile:
            file_exists = os.path.isfile(file_path)
            writer = csv.writer(csvfile)

            # Join the lists into single strings for each column using '&' as a separator
            bugs_str = "&".join(bugs)
            fixes_str = "&".join(fixes)
            if not file_exists:
                writer.writerow(columns)
            writer.writerow(
                [self.repair_iterations + 1, bugs_str, len(bugs), fixes_str, len(fixes)]
            )

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

    def handle_next_iteration(
        self,
        wrong_format: bool,
        repeated_bug_fix: bool,
        repeated_init_spec: bool,
        json_data: Dict,
    ):
        if wrong_format:
            self.wrong_format_msg += 1
        # terminate if reach iteration limit
        if self.repair_iterations == self.opts.max_iter:
            end_time = time.time()
            running_time = round(end_time - self.start_time, 2)
            row = (
                self.spec_file_dir_res,
                self.repair_iterations + 1,
                "reached_max_iter",
                self.num_repeated_fixes,
                self.num_repeated_init_spec,
                self.fst_iter_repeated_init_spec,
                self.wrong_format_msg,
                self.analyzer_agent_tokens,
                self.analyzer_agent_cost,
                self.prompt_agent_tokens,
                self.prompt_agent_cost,
                running_time,
            )
            self._write_summary_csv(row)
            return "DONE"
        else:
            self.repair_iterations += 1

            if repeated_init_spec:
                msg_to_llm = """the proposed <FIXED_SPECIFICATIONS> is IDENTICAL to
                 Alloy <Faulty_SPECIFICATIONS> that I sent you.
                 **DO NOT** send Alloy specifications that I sent you again.
                ALWAYS USE the tool `run_alloy_analyzer` to send me a new <FIXED_SPECIFICATIONS>.
                """

            # share bug/fix pairs
            elif repeated_bug_fix:
                if self.opts.bug_rep_hist:
                    msg_to_llm = f"""**IMPORTANT: DO NOT REPEAT** these PAIRS of
                        **Bug Statements** and **Fix Statements** in your next responses:
                        {self._print_history_bug_fix(self.history_bug_fix)}"""
                else:
                    msg_to_llm = "This is a repeated bug/fix pair. DON'T send it again."
            
            elif self.opts.feedback == FeedbackOption.NO_FEEDBACK:
                msg_to_llm = "The proposed specification DID NOT fix the bug."
            
            elif (
                json_data is not None
            ):
                report_msg = process_Alloy_json_report(json_data)
                formatted_report_msg = [line.strip() for line in report_msg]
                formatted_report_msg = "\n".join(formatted_report_msg)
                if self.opts.feedback == FeedbackOption.GENERIC_FEEDBACK:
                    alloy_msg = (
                        "Below are the results from the Alloy Analyzer."
                        "Fix all Errors and Counterexamples before sending me the next "
                        "<FIXED_SPECIFICATIONS>."
                    )

                    msg_to_llm = f"{alloy_msg} {formatted_report_msg}"
                elif (
                    self.opts.feedback == FeedbackOption.AUTO_FEEDBACK
                ):
                    # llm_config = AzureConfig(
                    #     timeout=50, stream=True, temperature=0.2, max_output_tokens=3000
                    # )
                    # llm_config = self.llm

                    prompt_agent_cfg = ChatAgentConfig(llm=self.config.llm)
                    prompt_agent = ChatAgent(prompt_agent_cfg)
                    response = prompt_agent.llm_response(
                        "You are Expert in Analyzing Alloy Analyzer reports."
                        + "Can you describe concisly and precisly the modifications needed to fix the error"
                        + "in at most 2 sentences?"
                        + f"based on this report from Alloy Analyzer: {formatted_report_msg}?"
                        + f"After running this Alloy Model is: {self.proposed_spec}"
                    )
                    tokens, cost = self._extract_tokens_cost(prompt_agent.token_stats_str)
                    self.prompt_agent_tokens += tokens
                    self.prompt_agent_cost = cost
                    msg_to_llm = f"\n\n{response.content}"
            elif wrong_format:
                msg_to_llm = (
                    "You must use the CORRECT format described in the tool "
                    + "`run_alloy_analyzer` to send me the fixed specifications. "
                    + "You either forgot to use it, or you used it with the WRONG format."
                    + "Make sure all fields are filled out."
                )
            # else:
            #     return "The proposed specification DID NOT fix the bug."

            return msg_to_llm

    def run_alloy_analyzer(self, msg: VerifierMessage) -> str:
        """
        This tool runs the proposed fixed_spec and returns the output of Alloy
        Analyzer
        """
        token, cost = self._extract_tokens_cost(self.token_stats_str)
        self.analyzer_agent_tokens += token
        self.analyzer_agent_cost = cost

        alloy_analyzer_path = "repair_alloy_spec/AlloyGPTverifier.jar"

        self.proposed_spec = msg.specification
        repeated_init_spec = repeated_spec(self.proposed_spec, self.orig_spec_content)
        if repeated_init_spec:
            self.num_repeated_init_spec += 1
            if self.repair_iterations == 0:
                self.fst_iter_repeated_init_spec = True

            return_str = self.handle_next_iteration(False, False, True, None)

        repeated_fix = False

        if not repeated_fix and not repeated_init_spec:
            # now we can process the specificiation if it's not repeated spec or fix
            res_path = os.path.join(self.opts.result_path, self.spec_file_dir_res)
            if res_path and not os.path.exists(res_path):
                os.makedirs(res_path)
            proposed_spec_file_no_ext = os.path.join(
                res_path,
                self.spec_file_dir_res
                + "_"
                + str(self.repair_iterations)
                + "_"
                + str(repeated_init_spec),
            )
            proposed_spec_file = proposed_spec_file_no_ext + ".als"

            with open(proposed_spec_file, "w") as f:
                f.write(self.proposed_spec)

            command = [
                "java",
                "-jar",
                alloy_analyzer_path,
                proposed_spec_file,
            ]
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            _, _ = process.communicate()

            json_report = proposed_spec_file_no_ext + "_alloyAnalyzerReport.json"

            if os.path.exists(json_report):
                with open(json_report, "r") as file:
                    json_data = json.load(file)

                error_is_empty = not json_data.get("error", "").strip()
                instance_exists = any(
                    item.get("instances") == "Yes"
                    for item in json_data.get("instances", [])
                )
                all_counterexamples_no = all(
                    item.get("counterexample") == "no"
                    for item in json_data.get("counterexamples", [])
                )
                end_time = time.time()
                running_time = round(end_time - self.start_time, 2)
                if error_is_empty and instance_exists and all_counterexamples_no:
                    row = (
                        self.spec_file_dir_res,
                        self.repair_iterations + 1,
                        "YES",
                        self.num_repeated_fixes,
                        self.num_repeated_init_spec,
                        self.fst_iter_repeated_init_spec,
                        self.wrong_format_msg,
                        self.analyzer_agent_tokens,
                        self.analyzer_agent_cost,
                        self.prompt_agent_tokens,
                        self.prompt_agent_cost,
                        running_time,
                    )
                    self._write_summary_csv(row)
                    return "DONE"
                else:
                    return_str = self.handle_next_iteration(
                        False, False, False, json_data
                    )

        if return_str == "DONE":
            return "DONE"
        print("total Iterations: ", self.repair_iterations)
        self.message_history = self.message_history[:2]
        return f"{return_str}"
