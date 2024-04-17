import pandas as pd
import sys
import os
from pathlib import Path


def count_solved_bugs(xlsx_file_path, csv_file_path, setting_no):
    # Read the XLSX and CSV files
    xlsx_df = pd.read_excel(xlsx_file_path)
    csv_df = pd.read_csv(csv_file_path)

    # Merge the DataFrames on the FileName/fileName column
    merged_df = pd.merge(csv_df, xlsx_df, left_on="fileName", right_on="FileName")

    # Filter rows where bugs are solved (fixed == 'YES')
    solved_df = merged_df[merged_df["fixed"] == "YES"]

    # Count how many single_line and multi_line bugs are solved
    solved_count = solved_df["BugType"].value_counts()
    single_count = solved_count.get("single_line", 0)
    multi_count = solved_count.get("multi_line", 0)

    # Preparing the result DataFrame
    result_df = pd.DataFrame(
        {
            "Setting": [setting_no],
            "SingleCount": [single_count],
            "MultiCount": [multi_count],
        }
    )
    csv_file_name = "single_multi_bug_analysis.csv"
    # Check if the CSV file exists to append or write new
    if os.path.exists(csv_file_name):
        result_df.to_csv(csv_file_name, mode="a", header=False, index=False)
    else:
        result_df.to_csv(csv_file_name, index=False)

    print("Results saved to " + csv_file_name)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python script.py <path_to_xlsx_file> <path_to_csv_file> <SettingNo>"
        )
        sys.exit(1)

    xlsx_file_path = sys.argv[1]
    csv_file_path = sys.argv[2]
    # setting_no = sys.argv[3]
    setting_no = Path(csv_file_path).parent.name.split("_")[-1]
    count_solved_bugs(xlsx_file_path, csv_file_path, setting_no)
