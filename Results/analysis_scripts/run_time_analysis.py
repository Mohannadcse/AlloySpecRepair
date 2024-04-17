import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path


def parse_csvs(csv_paths):
    # Initialize a list to store DataFrames
    df_list = []

    # Iterate over each provided CSV file path
    for path in csv_paths:
        # Determine the setting name from the file path
        setting_name = Path(path).parent.name.split("_")[-1]

        # Read the CSV into a DataFrame
        df = pd.read_csv(path)

        # Add a column to distinguish the setting for each CSV
        df["setting_name"] = setting_name

        # Append the DataFrame to our list
        df_list.append(df)

    # Concatenate all DataFrames into a single one
    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df


# def plot_violin_plots(combined_df, fixed_status):
#     # Filter the DataFrame based on the fixed status
#     filtered_df = combined_df[combined_df["fixed"] == fixed_status]

#     # Create a violin plot for each setting_name within the filtered DataFrame
#     plt.figure(figsize=(12, 9))
#     # plt.figure(figsize=(14, 10))
#     ax = sns.violinplot(
#         x="setting_name", y="running_time", data=filtered_df, cut=0
#     )  # Limit the range of the KDE
#     plt.ylabel("Running Time (Seconds)", fontsize=20)
#     ax.set_xlabel("", fontsize=12)
#     ax.tick_params(axis="x", labelsize=20)
#     ax.tick_params(axis="y", labelsize=20)
#     plt.xticks(rotation=45)
#     plt.savefig(f"run_time_groupb_by_{fixed_status}.pdf", format="pdf")
#     plt.show()


def identify_and_print_outliers(df, fixed_status):
    # Group by 'setting_name' and calculate Q1, Q3, and IQR for each group
    grouped = df.groupby("setting_name")["running_time"]
    Q1 = grouped.quantile(0.25)
    Q3 = grouped.quantile(0.75)
    IQR = Q3 - Q1

    # Define function to detect outliers within a group
    def outliers(group):
        cat = group.name
        return group[
            (group < (Q1[cat] - 1.5 * IQR[cat])) | (group > (Q3[cat] + 1.5 * IQR[cat]))
        ]

    # Apply the outlier detection
    outlier_values = grouped.apply(outliers).dropna()

    if not outlier_values.empty:
        print(f"Outliers for '{fixed_status}' status:")
        print(outlier_values)
    else:
        print(f"No outliers detected for '{fixed_status}' status.")


def plot_violin_plots(combined_df, fixed_status):
    # Filter the DataFrame based on the fixed status
    filtered_df = combined_df[combined_df["fixed"] == fixed_status]

    # Calculate and print medians for each setting within the filtered DataFrame
    # medians = filtered_df.groupby("setting_name")["running_time"].median()
    # print(f"Medians for '{fixed_status}' status:")
    # print(medians)

    # Identify and print outliers for each setting, considering fixed status
    # identify_and_print_outliers(filtered_df, fixed_status)

    # Adjust figure size for single column layout
    plt.figure(figsize=(8, 6))  # Adjusted from (12, 9) for a single-column layout
    ax = sns.violinplot(
        x="setting_name", y="running_time", data=filtered_df, cut=0, width=0.8
    )  # Adjust violin width for clarity
    plt.ylabel("Running Time (Seconds)", fontsize=14)  # Adjusted font size
    ax.set_xlabel("", fontsize=12)
    ax.tick_params(axis="x", labelsize=16)  # Adjusted font size for clarity
    ax.tick_params(axis="y", labelsize=16)  # Adjusted font size for clarity
    plt.xticks(
        rotation=45
    )  # Consider reducing rotation if labels overlap or are unclear
    plt.tight_layout()  # Ensure nothing is cut off when saving
    plt.savefig(
        f"run_time_grouped_by_{fixed_status}.pdf", format="pdf", dpi=300
    )  # Save in high quality
    plt.show()


if __name__ == "__main__":
    # Extract the CSV file paths from the command line arguments
    csv_paths = sys.argv[1:]

    # Parse the CSVs and combine them into a single DataFrame
    combined_df = parse_csvs(csv_paths)

    # Plot violin plots for "YES" fixed status
    plot_violin_plots(combined_df, "YES")

    # Plot violin plots for "reached_max_iter" fixed status
    plot_violin_plots(combined_df, "reached_max_iter")
