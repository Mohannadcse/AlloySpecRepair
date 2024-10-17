## Overview
- This repo provides a repair pipline for Alloy models using pre-trained LLMs. This pipeline comprises 2-agents and leverages [Azure OpenAI]([https://github.com/langroid/langroid/tree/main](https://github.com/retkowsky/Azure-OpenAI-demos/blob/main/GPT-4o/GPT-4o%20model%20with%20Azure%20OpenAI.ipynb ).

- The tool implemented as a python class and is called `AlloyAnalzerAgent`. It does several tasks like running the proposed Alloy specification, send back the feedback to `GPT`, recording bug/fix pairs, etc...

- This repo provides the artifacts of our empirical study using the implemented pipeline. 

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



<summary><b>Setup instructions for Microsoft Azure OpenAI</b></summary> 

When using Azure OpenAI, additional environment variables are required in the 
`/repair_alloy_spec/Alloy_Repair.py` file.
This page [Microsoft Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-python#environment-variables)
provides more information, and you can set each environment variable as follows:

- `AZURE_OPENAI_API_KEY`, from the value of `API_KEY`
- `AZURE_OPENAI_API_BASE` from the value of `ENDPOINT`, typically looks like `https://your.domain.azure.com`.
- `AZURE_OPENAI_MODEL_NAME` is the name of the deployed model, which is defined by the user during the model setup. 
- `AZURE_OPENAI_DEPLOYMENT_NAME` is the name of the deployed model, which is defined by the user during the model setup 
- `AZURE_OPENAI_API_VERSION` Current version of the Azure API, suppose "2024-05-01-preview"



## Run
For example:
```bash

python3 repair_alloy_spec/Alloy_Repair.py --dataset_path "<Location of the Dataset>" --feedback <feedback_type> --max [maximum_number_of_iterations]
```

Add the flags:
- `--dataset_path`: path to defective Alloy models
- `--feedback`: feedback level `No-Feedback|Generic-Feedback|Auto-Feedback`.
- `--max`: iteration number `we are considering 5 iterations`

## Output 
- A folder `results_<datasetName_SettingNumber>` will be created in the root directory. This folder will mantain a CSV file called `summary.csv`, which records the status of each Alloy file in the dataset.

- A file named `interaction_log.txt` contains all the real time interaction with LLM and output inside each results folder. 

Following is a description of the columns in the CSV file:

- `fileName`: The name of the `.als` file being analyzed.

- `iterations`: The number of iterations that were performed to repair the als file. 

- `fixed`: This column indicates the final outcome. It can have values such as `YES` to signify that the issue was resolved or `reached_max_iter` to indicate that the process reached the maximum number of iterations without repairing the bug.

- `repeated_fixes`: The number of times fixes were applied repeatedly. A numeric value that shows how often an attempted fix was reapplied, suggesting potential challenges in reaching a resolution.

- `repeated_init_spec`: Indicates whether the initial specifications were repeated during the process. A numeric value (typically 0 or 1) that shows if there was a need to revisit or reapply the initial conditions or specifications.

- `fst_iter_repeated_init_spec`: A boolean-like value (`True` or `False` as strings in the CSV) indicating whether the buggy specifications were repeated in the first iteration. This can signal whether adjustments to the initial specifications were identified as necessary right from the beginning.

- `Error_msg`: Intended to contain error messages or codes related to the task or process. In the provided dataset, this column does not have any entries, suggesting that specific error messages were not recorded or applicable.
