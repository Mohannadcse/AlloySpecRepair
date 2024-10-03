import os
import re
import shutil
import logging
import difflib
from typing import List
from enum import Enum
from pydantic_settings import BaseSettings



def check_result_dir(directory_path):
    # Check if the directory exists
    if os.path.exists(directory_path):
        # Remove all its content
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
        # Create the directory
        os.makedirs(directory_path)


class FeedbackOption(Enum):
    NO_FEEDBACK = "No-Feedback"
    GENERIC_FEEDBACK = "Generic-Feedback"
    AUTO_FEEDBACK = "Auto-Feedback"


class ModelOption(Enum):
    GPT4_32K = "GPT-4-32-k"
    GPT4_TURBO = "GPT-4-Turbo"
    GPT3_5_TURBO = "GPT-3.5-Turbo"
    GPT4O = "GPT-4o"  # Added GPT-4o model option




from typing import ClassVar

class CLIOptions(BaseSettings):
    dataset_path: str = ""
    result_path: str = ""
    report: bool = False
    bug_rep_hist: bool = False  # Add type annotation
    fn_api: bool = False
    max_iter: int = 5
    model: ModelOption = ModelOption.GPT3_5_TURBO
    feedback: FeedbackOption = FeedbackOption.NO_FEEDBACK

    class Config:
        extra = "forbid"
        env_prefix = ""

#
# class CLIOptions(BaseSettings):
#     dataset_path: str = ""
#     result_path: str = ""
#     report: bool = False
#     bug_rep_hist = False
#     fn_api: bool = False
#     max_iter: int = 5
#     model: ModelOption = ModelOption.GPT3_5_TURBO
#     feedback: FeedbackOption = FeedbackOption.NO_FEEDBACK
#
#     class Config:
#         extra = "forbid"
#         env_prefix = ""


# Create a custom logger
class CustomLogger(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_messages = []

    def emit(self, record):
        self.log_messages.append(self.format(record))


def remove_dollar_sign(text):
    return text.replace("$", "")


def extract_line_column(error_message):
    # Regular expression pattern to find 'line x column y'
    match = re.search(r"at line (\d+) column (\d+)", error_message)
    if match:
        # Extracting line and column numbers
        line_number = match.group(1)
        column_number = match.group(2)
        return line_number, column_number
    else:
        return None, None


def remove_specification_part(line):
    # Check if the line contains "in" and "specification:"
    start_index = line.find(" in ")
    end_index = line.find("specification:")

    if start_index != -1 and end_index != -1:
        return line[:start_index] + line[end_index + len("specification:") :]
    else:
        return line


def remove_compilation_error_line(compilation_error_message):
    lines = compilation_error_message.split("\n")
    new_lines = []

    for line in lines:
        # Check if the line contains "in" and "specification:"
        line = remove_specification_part(line)

        # Check if the line starts with "in" and ends with "specification:"
        if line.startswith("in") and line.endswith("specification:"):
            continue

        # Replace "Warning" with "generates a compilation error at"
        line = line.replace("Warning", "generates a compilation error at")

        new_lines.append(line)

    return "\n".join(new_lines)


def _normalize_string(s):
    """Normalize a string by removing trailing whitespaces from each line."""
    return "\n".join(line.rstrip() for line in s.splitlines())


def normalize_list_of_strings(lst):
    """Normalize a list of strings by removing trailing whitespaces from each line in each string."""
    return [_normalize_string(s) for s in lst]


def process_Alloy_json_report(json_data) -> List[str]:
    output_lines = []

    # Helper function for adding lines to output
    def add_output_line(line):
        output_lines.append(line.strip())

    # Process counterexamples
    counterexamples = json_data.get("counterexamples", [])
    for item in counterexamples:
        cntr_cmd = item.get("cntr_cmd", "").replace("expect 0", "").strip()
        counterexample_msg = item.get("counterexample_msg", "")
        counterexample = item.get("counterexample", "").lower()
        assertion_name = remove_dollar_sign(cntr_cmd.replace("Check", "").strip())

        if counterexample == "no":
            add_output_line(
                f"Executing command [{cntr_cmd}] of the proposed Alloy model, "
                "Alloy analyzer found no counterexample, indicating assert "
                f"{assertion_name} is valid."
            )
        else:
            add_output_line(
                f"Executing command [{cntr_cmd}] of the proposed Alloy model, "
                "Alloy analyzer found a counterexample, indicating assert "
                f"{assertion_name} is violated by this counterexample:"
            )

            counterexample_msg_lines = [
                remove_dollar_sign(line.replace("this/", ""))
                for line in counterexample_msg.split("\n")
                if line and "Counterexample found which means that" not in line
            ]
            output_lines.extend(counterexample_msg_lines)

    # Process instances
    instances = json_data.get("instances", [])
    for item in instances:
        instance_cmd = item.get("instance_cmd", "").strip()
        instance_name = remove_dollar_sign(instance_cmd.replace("Run", "").strip())
        inst = item.get("instances", "").lower()

        if inst == "yes":
            add_output_line(
                f"Executing command [{instance_cmd}] of proposed Alloy model, "
                "Alloy analyzer generates a valid instance, indicating the model is "
                f"consistent and pred {instance_name} is satisfied."
            )
        else:
            add_output_line(
                f"Executing command [{instance_cmd}] of proposed Alloy model, "
                "Alloy analyzer does not generate a valid instance, indicating the model is "
                f"inconsistent and pred {instance_name} is not satisfied."
            )

    # Process error
    error = json_data.get("error", "")
    if error:
        lines_to_discard = ["als", "\tat edu.mit", "\tat alloyrepair"]
        if "Warning Line" in error:
            line_number, column_number = extract_line_column(error)
            compilation_error_message = remove_dollar_sign(
                " ".join(error.split(" ")[5:]).strip()
            )
            compilation_error_message = remove_compilation_error_line(
                compilation_error_message
            )
            error_lines = [
                line
                for line in compilation_error_message.split("\n")
                if "als" not in line
            ]
            add_output_line(
                f"Compiling the proposed Alloy model generates a compilation error at "
                f"Line {line_number}, Column {column_number}: {' '.join(error_lines)}"
            )
        elif error.startswith("Type error in"):
            line_number, column_number = extract_line_column(error)
            error_lines = [
                line
                for line in error.split("\n")
                if not any(discard in line for discard in lines_to_discard)
            ]
            add_output_line(
                f"Compiling the proposed Alloy model generates a type error at Line "
                f"{line_number}, Column {column_number}: {' '.join(error_lines)}"
            )
        else:
            syntax_error_message = remove_dollar_sign(
                " ".join(error.split(" ")[5:]).strip()
            ).split("\n")
            add_output_line(
                f"Compiling the proposed Alloy model generates a syntax error: "
                f"{' '.join(syntax_error_message)}"
            )
    return output_lines


def _preprocess_string(s):
    return [line.strip() for line in s.splitlines()]


def repeated_spec(str1, str2):
    # Create a Differ object
    differ = difflib.Differ()
    str1_processed = _preprocess_string(str1)
    str2_processed = _preprocess_string(str2)
    # Calculate the difference
    diff = differ.compare(str1_processed, str2_processed)

    # Check if there are any differences
    differences = any(line.startswith("-") or line.startswith("+") for line in diff)

    # Return True if there are no differences, otherwise False
    return not differences


def _replace_newlines_except_specific_statement(input_string):
    specific_statement = '\n{\n"request": "run_alloy_analyzer",\n"specification'

    # Check if the specific statement is in the string
    if specific_statement in input_string:
        # Split the input string into two parts around the specific statement
        before_statement, after_statement = input_string.split(specific_statement, 1)

        # Replace newlines in the parts before and after the specific statement
        before_statement = before_statement.replace("\n", "\\n")
        after_statement = after_statement.replace("\n", "\\n")

        # Reassemble the string
        return before_statement + specific_statement + after_statement
    else:
        # If the specific statement is not in the string, just replace all newlines
        return input_string.replace("\n", "\\n")


def _modify_string(input_string):
    if input_string.endswith("\n}"):
        return input_string[:-2] + "}"
    return input_string


# with open(
#     "/Users/moh/Downloads/repos/repair-sw-spec/results_GPT_Turbo/trash_inv6_31/trash_inv6_31_0_False_alloyAnalyzerReport.json",
#     "r",
# ) as file:
#     json_data = json.load(file)
# process_Alloy_json_report(json_data)
