import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def process_csv(file_path, setting_index):
    """
    Process a single CSV file to compute the sum of analyzer_agent_cost and prompt_agent_cost
    for each row and filter based on the 'fixed' column's value.
    Uses setting_index to label the setting as "Setting-{index}".
    Returns DataFrames for 'YES' and 'reached_max_iter' conditions along with the setting label.
    """
    # Label the setting as "Setting-{index}"
    setting_label = f"Setting-{setting_index}"

    # Read CSV file
    df = pd.read_csv(file_path)

    # Compute sum of analyzer_agent_cost and prompt_agent_cost
    df["total_cost"] = df["analyzer_agent_cost"] + df["prompt_agent_cost"]

    # Filter based on the 'fixed' column's value
    df_yes = df[df["fixed"] == "YES"]
    df_reached_max_iter = df[df["fixed"] == "reached_max_iter"]

    return (
        df_yes[["fileName", "total_cost"]],
        df_reached_max_iter[["fileName", "total_cost"]],
        setting_label,
    )


def plot_violin(data, save_path):
    """
    Generate and save a violin plot for the given data without an x-axis label, but with the setting names
    as part of the plot directly. The font size for the y-axis label is set to 16.
    """
    plt.figure(figsize=(8, 6))
    violin_plot = sns.violinplot(
        x="setting", y="total_cost", data=data, cut=0, width=0.8
    )
    violin_plot.set_xlabel("")  # Remove the x-axis label
    violin_plot.set_ylabel(
        "Total Cost (USD)", fontsize=14
    )  # Set font size for y-axis label only
    violin_plot.tick_params(
        axis="x", labelsize=16
    )  # Ensure setting names (ticks) are readable
    violin_plot.tick_params(axis="y", labelsize=16)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path, format="pdf", dpi=300)
    plt.close()


if __name__ == "__main__":
    # List to hold data for plotting
    data_yes = []
    data_reached_max_iter = []

    # Process each CSV file provided as a command-line argument
    for index, file_path in enumerate(sys.argv[1:], start=1):
        df_yes, df_reached_max_iter, setting_label = process_csv(file_path, index)
        if not df_yes.empty:
            df_yes["setting"] = setting_label
            data_yes.append(df_yes)
        if not df_reached_max_iter.empty:
            df_reached_max_iter["setting"] = setting_label
            data_reached_max_iter.append(df_reached_max_iter)

    # Concatenate DataFrames
    data_yes_concat = pd.concat(data_yes, ignore_index=True)
    data_reached_max_iter_concat = pd.concat(data_reached_max_iter, ignore_index=True)

    # Plot and save violin plots
    # Plot and save violin plots
    plot_violin(data_yes_concat, "total_cost_yes.pdf")
    plot_violin(data_reached_max_iter_concat, "total_cost_reached_max_iter.pdf")
