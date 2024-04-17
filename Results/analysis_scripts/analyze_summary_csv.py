import pandas as pd
import os
import argparse
from pathlib import Path


def analyze_csv(file_path, output_directory=None):
    parent_dir = os.path.basename(os.path.dirname(file_path))

    # Extract and print the last fragment of the parent directory name
    setting_name = Path(file_path).parent.name.split("_")[-1]

    # Construct the output file names for both analyses
    original_output_file_name = f"ANALYSIS_{parent_dir}.csv"
    new_output_file_name = f"ANALYSIS_COUNT_{parent_dir}.csv"

    if output_directory:
        original_output_file_path = os.path.join(
            output_directory, original_output_file_name
        )
        new_output_file_path = os.path.join(output_directory, new_output_file_name)
    else:
        original_output_file_path = original_output_file_name
        new_output_file_path = new_output_file_name

    # Read the CSV data into a DataFrame
    df = pd.read_csv(file_path)

    # Original analysis logic
    fixed_entries = df[df["fixed"] == "YES"]
    fst_iter_repeated_init_spec_count = df[
        df["fst_iter_repeated_init_spec"] == True
    ].shape[0]

    # Count the entries that are fixed and have zero iterations
    fixed_and_zero_iterations_count = df[
        (df["fixed"] == "YES") & (df["iterations"] == 1)
    ].shape[0]

    # Calculate quartiles, median, and identify any outliers if necessary
    if not fixed_entries.empty:
        Q1 = fixed_entries["iterations"].quantile(0.25)
        median = fixed_entries["iterations"].median()
        Q3 = fixed_entries["iterations"].quantile(0.75)
        min_value = fixed_entries["iterations"].min()
        max_value = fixed_entries["iterations"].max()
    else:
        Q1, median, Q3, min_value, max_value = "N/A", "N/A", "N/A", "N/A", "N/A"

    results = {
        "Setting": setting_name,
        "Number of fixed entries": fixed_entries.shape[0],
        "Number of entries that reached max iteration": df[
            df["fixed"] == "reached_max_iter"
        ].shape[0],
        "Average number of iterations for fixed entries": (
            fixed_entries["iterations"].mean() if not fixed_entries.empty else 0
        ),
        "Min number of iterations to fix": min_value,
        "Q1 (25th percentile)": Q1,
        "Median number of iterations to fix": median,
        "Q3 (75th percentile)": Q3,
        "Max number of iterations to fix": max_value,
        "Number of entries where fst_iter_repeated_init_spec is True": fst_iter_repeated_init_spec_count,
        "Number of fixed entries with zero iterations": fixed_and_zero_iterations_count,
    }
    pd.DataFrame([results]).to_csv(original_output_file_path, index=False)

    # group files
    df["fileName_clean"] = (
        df["fileName"]
        .str.replace("\d+", "", regex=True)
        .str.replace("_", "", regex=True)
    )
    result = (
        df.groupby("fileName_clean")["fixed"]
        .apply(lambda x: (x.size, x[x == "YES"].count()))
        .reset_index(name="count")
    )
    result["output"] = result.apply(
        lambda row: f"{row['fileName_clean']},{row['count'][0]}/{row['count'][1]}",
        axis=1,
    )
    result[["fileName_clean", "output"]].to_csv(new_output_file_path, index=False)

    # Print the paths of the output files
    print(f"Original analysis results saved to: {original_output_file_path}")
    print(f"New analysis results saved to: {new_output_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze CSV data and output two sets of statistics: original analysis including box-and-whisker plot details and counts of 'YES' for unique file names."
    )
    parser.add_argument("file_path", help="The path to the CSV file to analyze.")
    parser.add_argument(
        "--output_directory",
        help="The directory to save the output CSV files. Optional.",
        default=None,
    )

    args = parser.parse_args()

    analyze_csv(args.file_path, args.output_directory)
