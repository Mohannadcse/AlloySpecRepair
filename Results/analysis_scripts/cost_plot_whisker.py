import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def process_csv(file_path):
    """
    Process a single CSV file to compute the sum of analyzer_agent_cost and prompt_agent_cost
    for each row. Returns a DataFrame with the sums and the setting name extracted from the file path.
    """
    # Extract setting name from file path
    setting_name = Path(file_path).parent.name.split("_")[-1]

    # Read CSV file
    df = pd.read_csv(file_path)

    # Compute sum of analyzer_agent_cost and prompt_agent_cost
    df["cost_sum"] = df["analyzer_agent_cost"] + df["prompt_agent_cost"]

    # Return DataFrame with necessary data and setting name
    return df[["cost_sum"]], setting_name


def plot_box_whisker(data, settings):
    """
    Plots a box-whisker chart for all settings together.
    :param data: Dictionary where keys are setting names and values are lists of sums.
    :param settings: List of setting names.
    """
    # Prepare data for plotting
    plot_data = [data[setting] for setting in settings]

    print("Total Cost of Each Setting:")
    for setting in settings:
        total_cost = sum(data[setting])
        print(f"{setting}: {total_cost:.2f}")

    print("\nMedian Cost of Each Setting:")
    for setting in settings:
        median_cost = np.median(data[setting])
        print(f"{setting}: {median_cost:.2f}")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.boxplot(plot_data, labels=settings)
    # plt.title("Box-Whisker Plot of Analyzer and Prompt Agent Costs Sum")
    # plt.xlabel("Settings")
    plt.ylabel("Cost(USD)", fontsize=16)
    plt.xticks(rotation=45, fontsize=16)
    plt.tight_layout()
    plt.tick_params(axis="y", labelsize=16)

    plt.savefig("cost_box-whisker-plot.pdf", format="pdf")

    plt.show()


if __name__ == "__main__":
    # Dictionary to hold the sum of costs for each setting
    setting_data = {}
    # files = [
    #         '/Users/moh/Downloads/repos/repair-sw-spec/new_results_arepair/results_arepair_Setting-1/summary.csv',
    #         '/Users/moh/Downloads/repos/repair-sw-spec/new_results_arepair/results_arepair_Setting-2/summary.csv',
    #         '/Users/moh/Downloads/repos/repair-sw-spec/new_results_arepair/results_arepair_Setting-3/summary.csv',
    #         '/Users/moh/Downloads/repos/repair-sw-spec/new_results_arepair/results_arepair_Setting-4/summary.csv',
    #         '/Users/moh/Downloads/repos/repair-sw-spec/new_results_arepair/results_arepair_Setting-5/summary.csv',
    #         '/Users/moh/Downloads/repos/repair-sw-spec/new_results_arepair/results_arepair_Setting-6/summary.csv'
    #         ]
    # Process each CSV file provided as a command-line argument
    for file_path in sys.argv[1:]:
        df, setting_name = process_csv(file_path)
        setting_data.setdefault(setting_name, []).extend(df["cost_sum"].tolist())

    # Extract settings for plotting
    settings = list(setting_data.keys())

    # Plot the box-whisker chart
    plot_box_whisker(setting_data, settings)
