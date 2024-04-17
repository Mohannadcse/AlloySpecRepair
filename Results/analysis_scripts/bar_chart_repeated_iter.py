import pandas as pd
import matplotlib.pyplot as plt
import sys


def generate_bar_chart(csv_file_path):
    # Load the dataset
    data = pd.read_csv(csv_file_path)

    # Extract relevant data
    settings = data["Setting"]
    num_entries_true = data[
        "Number of entries where fst_iter_repeated_init_spec is True"
    ]

    # Creating the bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(settings, num_entries_true, color="#3333FF")

    # plt.title("Entries with fst_iter_repeated_init_spec True by Setting")
    # plt.xlabel("Setting")
    plt.ylabel("Count", fontsize=16)
    plt.xticks(rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    # Save or show the chart
    plt.tight_layout()
    plt.savefig("bar_chart_fst_iter_repeated_init_spec.pdf", format="pdf")
    plt.show()  # Uncomment this line if you prefer to display the chart instead


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_consolidated_ANALYSIS.csv>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    generate_bar_chart(csv_file_path)
