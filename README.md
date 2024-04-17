## Overview
- This implementatin provides an LLM app that leverages [Langroid](https://github.com/langroid/langroid/tree/main) to build the LLM agent and its corresponding tool.

- The tool implemented as a python class and is called `AlloyAnalzerAgent`. It does several tasks like running the proposed Alloy specification, send back the feedback to `GPT`, recording bug/fix pairs, etc...

- The main system message that provides the instruction to `GPT` is assigned to the variable `sys_instructions`. Therefore, the main thing that we need to keep tune is **sys_instructions**. This message will be updated later on by inserting bug/fix pairs that `GPT` shouldn't repeat. See the variable `repair_history_msg`.

- If there any modifications to be made, they in general should be under the implemntation of the tool `AlloyAnalzerAgent`, specifically, the function `run_alloy_analyzer`, which orchestrates all the logic.


## Set up poetry env

Install [`poetry`](https://python-poetry.org/docs/#installation)
and use Python 3.11.

Create virtual env and install dependencies:

```bash
# clone the repo and cd into repo root
git clone 
cd 

# create a virtual env under project root, .venv directory
python3 -m venv .venv

# activate the virtual env
. .venv/bin/activate

# use poetry to install dependencies (these go into .venv dir)
poetry install
```

## Prerequesits
- The current implementation leverages Azure OpenAI. 
```python
llm_config = AzureConfig(
        chat_model=OpenAIChatModel.GPT4, timeout=50, stream=True, temperature=0.2
    )
```

To change to OpenAI, just enable the line 
```python
llm_config = OpenAIGPTConfig(chat_model=OpenAIChatModel.GPT4, stream=True)
```

- You need to make sure you have the required settings and API keys listed in `.env-template` for either Azure or OpenAI.  Here are the instructions to setup these keys:

In the root of the repo, copy the `.env-template` file to a new file `.env`: 
```bash
cp .env-template .env
```
Then insert your OpenAI API Key. 
Your `.env` file should look like this:
```bash
OPENAI_API_KEY=your-key-here-without-quotes
````

<summary><b>Setup instructions for Microsoft Azure OpenAI</b></summary> 

When using Azure OpenAI, additional environment variables are required in the 
`.env` file.
This page [Microsoft Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-python#environment-variables)
provides more information, and you can set each environment variable as follows:

- `AZURE_OPENAI_API_KEY`, from the value of `API_KEY`
- `AZURE_OPENAI_API_BASE` from the value of `ENDPOINT`, typically looks like `https://your.domain.azure.com`.
- For `AZURE_OPENAI_API_VERSION`, you can use the default value in `.env-template`, and latest version can be found [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/whats-new#azure-openai-chat-completion-general-availability-ga)
- `AZURE_OPENAI_DEPLOYMENT_NAME` is the name of the deployed model, which is defined by the user during the model setup 
- `AZURE_OPENAI_MODEL_NAME` GPT-3.5-Turbo or GPT-4 model names that you chose when you setup your Azure OpenAI account.


## Run
For example:
```bash
python3 repair_alloy_spec/repair_chat.py -db="/path/to/Alloy_dataset 
    -fb <feedback-level> -mo <model-name>
```

Add the flags:
- `db`: path to defective Alloy models
- `-fb`: feedback level `No-Feedback|Generic-Feedback|Auto-Feedback`.
- `mo`: pre-trained LLM `GPT-4-32-k|GPT-4-Turbo|GPT-3.5-Turbo`

## Output 
- A folder `results_<datasetName_SettingNumber>` will be created in the root directory. This folder will mantain a CSV file called `summary.csv`, which records the status of each Alloy file in the dataset. 

Following is a description of the columns in the CSV file:

- `fileName`: The name of the `.als` file being analyzed.

- `iterations`: The number of iterations that were performed to repair the als file. 

- `fixed`: This column indicates the final outcome. It can have values such as `YES` to signify that the issue was resolved or `reached_max_iter` to indicate that the process reached the maximum number of iterations without repairing the bug.

- `repeated_fixes`: The number of times fixes were applied repeatedly. A numeric value that shows how often an attempted fix was reapplied, suggesting potential challenges in reaching a resolution.

- `repeated_init_spec`: Indicates whether the initial specifications were repeated during the process. A numeric value (typically 0 or 1) that shows if there was a need to revisit or reapply the initial conditions or specifications.

- `fst_iter_repeated_init_spec`: A boolean-like value (`True` or `False` as strings in the CSV) indicating whether the buggy specifications were repeated in the first iteration. This can signal whether adjustments to the initial specifications were identified as necessary right from the beginning.

- `Error_msg`: Intended to contain error messages or codes related to the task or process. In the provided dataset, this column does not have any entries, suggesting that specific error messages were not recorded or applicable.
