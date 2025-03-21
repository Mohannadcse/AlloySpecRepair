import csv
import sys
import os
from pathlib import Path
import pandas as pd


def sum_wrong_format_msgs(csv_path):
    """
    Reads a CSV file from the given path and returns the sum of the 'wrong_format_msg' column values.

    Parameters:
    - csv_path: str, path to the CSV file.

    Returns:
    - int, sum of the 'wrong_format_msg' column values.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Compute the sum of the 'wrong_format_msg' column
    total_sum = df["wrong_format_msg"].sum()

    return total_sum


def count_categories(input_csv_file, summary_csv_file, setting):
    # Initialize counters for the input CSV
    errors_count = 0
    counterexamples_count = 0
    noinstances_count = 0

    # Process the input CSV file
    with open(input_csv_file, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Errors"] == "1":
                errors_count += 1
            if row["Counterexamples"] == "1":
                counterexamples_count += 1
            if row["NoInstances"] == "1":
                noinstances_count += 1

    # Initialize repetition count for the summary CSV
    repetition_count = 0

    # Process the summary CSV file to compute RepetitionCount
    with open(summary_csv_file, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            repetition_count += int(row.get("repeated_init_spec", 0))

    count_wrg_msg_format = sum_wrong_format_msgs(summary_csv_file)
    # Check if failures_counts.csv exists to decide on writing the header
    file_exists = os.path.isfile("failures_counts.csv")

    # Append the counts to 'failures_counts.csv'
    with open("failures_counts.csv", mode="a", newline="") as file:
        fieldnames = [
            "Setting",
            "ErrorsCount",
            "CounterexamplesCount",
            "NoInstancesCount",
            "RepetitionCount",
            "WrongMessageFormat",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if the file is being created (i.e., does not exist yet)
        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "Setting": setting,
                "ErrorsCount": errors_count,
                "CounterexamplesCount": counterexamples_count,
                "NoInstancesCount": noinstances_count,
                "RepetitionCount": repetition_count,
                "WrongMessageFormat": count_wrg_msg_format,
            }
        )


if __name__ == "__main__":
    # Check if both CSV file paths and setting are provided as command-line arguments
    if len(sys.argv) < 3:
        print(
            "Usage: python script.py <setting-char_csv_file> <summary_csv_file> <setting>"
        )
        sys.exit(1)

    setting_char_csv_file = sys.argv[
        1
    ]  # Get input CSV file path from command-line argument
    summary_csv_file = sys.argv[
        2
    ]  # Get summary CSV file path from command-line argument
    # setting = sys.argv[3]  # Get setting value from command-line argument
    setting = Path(summary_csv_file).parent.name.split("_")[-1]
    count_categories(setting_char_csv_file, summary_csv_file, setting)

    print("Results appended to counts.csv.")
