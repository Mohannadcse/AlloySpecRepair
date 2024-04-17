import os
import shutil
import json
import csv
import sys
import tempfile


def copy_json_files(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".json"):
                shutil.copy(os.path.join(root, file), dst_dir)


def read_json_and_write_csv(json_dir, output_csv_path):
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["jsonFileName", "Errors", "Counterexamples", "NoInstances"])

        for filename in os.listdir(json_dir):
            if filename.endswith(".json"):
                with open(os.path.join(json_dir, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    errors = 1 if data.get("error") else 0
                    counterexamples = (
                        1
                        if any(
                            item.get("counterexample") == "Yes"
                            for item in data.get("counterexamples", [])
                        )
                        else 0
                    )
                    instances = (
                        1
                        if any(
                            item.get("instances") == "No"
                            for item in data.get("instances", [])
                        )
                        else 0
                    )
                    # Write to CSV only if any of the conditions are true
                    if errors or counterexamples or instances:
                        writer.writerow([filename, errors, counterexamples, instances])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <source_dir> <output_csv_path>")
    else:
        src_dir = sys.argv[1]
        # output_csv_path = sys.argv[2]
        output_csv_path = src_dir.split("/")[-1].split("_")[-1] + "_char_failures.csv"

        # Use a temporary directory for dst_dir
        with tempfile.TemporaryDirectory() as dst_dir:
            copy_json_files(src_dir, dst_dir)
            read_json_and_write_csv(dst_dir, output_csv_path)

        print("Process completed.")
