"""
 python3.11 repair_alloy_spec/repair_chat.py -db="/path/to/dataset"
"""

import typer
import os
import time
import logging
from rich import print
from dotenv import load_dotenv

from utility import (
    CLIOptions,
    check_result_dir,
    CustomLogger,
    ModelOption,
    FeedbackOption,
    ModelSource,
)

from langroid.agent.chat_agent import ChatAgentConfig
from langroid.language_models.azure_openai import AzureConfig
from langroid.language_models.openai_gpt import OpenAIGPTConfig
from langroid.agent.task import Task
from langroid.utils.configuration import Settings, set_global
from langroid.utils.logging import setup_colored_logging
from alloy_verification_tool import AlloyAnalzerAgent, VerifierMessage
from langroid.language_models.openai_gpt import OpenAIChatModel

app = typer.Typer()
setup_colored_logging()


def determine_setting(feedback: FeedbackOption, model: ModelOption) -> str:
    if feedback == FeedbackOption.NO_FEEDBACK and model in (
        ModelOption.GPT3_5_TURBO,
        ModelOption.GPT4_32K,
    ):
        return "Setting-1"
    elif feedback == FeedbackOption.GENERIC_FEEDBACK and model in (
        ModelOption.GPT3_5_TURBO,
        ModelOption.GPT4_32K,
    ):
        return "Setting-2"
    elif feedback == FeedbackOption.AUTO_FEEDBACK and model in (
        ModelOption.GPT3_5_TURBO,
        ModelOption.GPT4_32K,
    ):
        return "Setting-3"
    elif feedback == FeedbackOption.NO_FEEDBACK and model == ModelOption.GPT4_TURBO:
        return "Setting-4"
    elif (
        feedback == FeedbackOption.GENERIC_FEEDBACK and model == ModelOption.GPT4_TURBO
    ):
        return "Setting-5"
    elif feedback == FeedbackOption.AUTO_FEEDBACK and model == ModelOption.GPT4_TURBO:
        return "Setting-6"
    elif feedback == FeedbackOption.NO_FEEDBACK and model == ModelOption.GPT4o:
        return "Setting-7"
    elif feedback == FeedbackOption.GENERIC_FEEDBACK and model == ModelOption.GPT4o:
        return "Setting-8"
    elif feedback == FeedbackOption.AUTO_FEEDBACK and model == ModelOption.GPT4o:
        return "Setting-9"
    else:
        return None


def chat(opts: CLIOptions) -> None:
    # figure out setting number
    setting = determine_setting(opts.feedback, opts.model)
    if setting is None:
        raise ValueError("Invalid combination of options or missing options.")

    custom_logger = CustomLogger()
    logging.getLogger().addHandler(custom_logger)
    logging.getLogger().setLevel(logging.ERROR)  # Only capture ERROR level logs
    print("[blue] Welcome to the Specification Repair chatbot!\n")
    load_dotenv()

    llm_config = None
    if opts.source == ModelSource.OPENAI:
        llm_config = OpenAIGPTConfig(
            chat_model=opts.model.value,
            timeout=50,
            stream=True,
            temperature=0.2,
            max_output_tokens=4000,
        )
    elif opts.source == ModelSource.AZURE:
        llm_config = AzureConfig(
            timeout=50,
            stream=True,
            temperature=0.2,
            max_output_tokens=4000,
        )

    opts.result_path = f"results_{os.path.basename(opts.dataset_path)}" + f"_{setting}"

    check_result_dir(opts.result_path)

    files_to_skip = set()
    dir_path = opts.dataset_path
    for spec_file in os.scandir(dir_path):
        if any(
            os.path.splitext(spec_file.name)[0] in skip_file
            for skip_file in files_to_skip
        ):
            continue
        if spec_file.is_file() and os.path.splitext(spec_file.name)[1] == ".als":
            print(spec_file.name)
            try:
                with open(spec_file, "r") as file:
                    spec = file.read()
                    lines = spec.splitlines()
                    cleaned_lines = [line.replace("\t", "").strip() for line in lines]
                    cleaned_spec = "\n".join(cleaned_lines)

                agent = AlloyAnalzerAgent(
                    config=ChatAgentConfig(
                        name="SpecificationRepair",
                        use_tools=not opts.fn_api,
                        use_functions_api=opts.fn_api,
                        vecdb=None,
                        llm=llm_config,
                        user_message=f"Here is the <Faulty_SPECIFICATIONS>: \n{cleaned_spec}",
                    )
                )
                agent.system_message = agent.sys_instructions
                agent.enable_message(VerifierMessage)
                agent.orig_spec_content = cleaned_spec
                agent.orig_spec_file = spec_file
                agent.setting_name = setting
                agent.spec_file_dir_res = os.path.splitext(
                    os.path.basename(agent.orig_spec_file)
                )[0]
                agent.opts = opts
                agent.start_time = time.time()
                task = Task(
                    agent,
                    name="SpecificationRepairTask",
                    llm_delegate=True,
                    single_round=False,
                    default_human_response="",
                    interactive=False,
                    max_stalled_steps=5,
                    only_user_quits_root=False,
                )
                task.run()
            except Exception as e:
                # this means there will be a duplicated record for the same file
                # because by the end a report
                row = (
                    spec_file.name,
                    agent.repair_iterations + 1,
                    "Exception",
                    agent.num_repeated_fixes,
                    agent.num_repeated_init_spec,
                    agent.fst_iter_repeated_init_spec,
                    agent.wrong_format_msg,
                    agent.analyzer_agent_tokens,
                    agent.analyzer_agent_cost,
                    agent.prompt_agent_tokens,
                    agent.prompt_agent_cost,
                    "NA",
                    e,
                )
                agent._write_summary_csv(row)
                continue
            finally:
                logs = "&".join(custom_logger.log_messages)
                if logs:
                    row = (
                        spec_file.name,
                        agent.repair_iterations + 1,
                        "Error_finally_section",
                        agent.num_repeated_fixes,
                        agent.num_repeated_init_spec,
                        agent.fst_iter_repeated_init_spec,
                        agent.wrong_format_msg,
                        agent.analyzer_agent_tokens,
                        agent.analyzer_agent_cost,
                        agent.prompt_agent_tokens,
                        agent.prompt_agent_cost,
                        "NA",
                        logs,
                    )
                    agent._write_summary_csv(row)
                    custom_logger.log_messages.clear()  # Clear logs for next iteration


@app.command()
def main(
    dataset_path: str = typer.Option(
        "", "--dataset_path", "-db", help="path to Alloy dataset"
    ),
    feedback: FeedbackOption = typer.Option(
        FeedbackOption.NO_FEEDBACK,
        "--feedback",
        "-fb",
        help="""Specify the feedback option:
             No-Feedback - Do not send any feedback.
             Generic-Feedback - Send generic feedback.
             Auto-Feedback - Automatically generate and send feedback.""",
    ),
    source: ModelSource = typer.Option(
        ModelSource.OPENAI,
        "--source",
        "-s",
        help="""Specify the model source:
             OpenAI - Use the OpenAI model.
             Azure - Use the Azure model
             """,
    ),
    model: ModelOption = typer.Option(
        ModelOption.GPT4_32K,
        "--model",
        "-mo",
        help="""Select the model option:
             GPT-4-32-k - Use the GPT-4 model with 32k tokenizer.
             GPT-4-Turbo - Use the GPT-4 Turbo model.
             GPT-3.5-Turbo - Use the GPT-3.5 Turbo model.
             GPT4o - Use the gpt-4o model.""",
    ),
    bug_rep_hist: bool = typer.Option(
        False, "--bug_hist", "-bg", help="send bug/repair history"
    ),
    max_iter: int = typer.Option(5, "--max", "-m", help="max number of iterations"),
    debug: bool = typer.Option(False, "--debug", "-d", help="debug mode"),
    fn_api: bool = typer.Option(False, "--fn_api", "-f", help="use functions api"),
    result_path: str = typer.Option(
        "./results/", "--result_path", "-r", help="path to analysis results"
    ),
) -> None:
    set_global(
        Settings(
            debug=debug,
            cache=False,
            stream=True,
        )
    )

    opts = CLIOptions(
        dataset_path=dataset_path,
        bug_rep_hist=bug_rep_hist,
        result_path=result_path,
        fn_api=fn_api,
        max_iter=max_iter,
        feedback=feedback,
        model=model,
        source=source,
    )

    chat(opts)


if __name__ == "__main__":
    app()
