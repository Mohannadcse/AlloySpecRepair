import matplotlib.pyplot as plt
import pandas as pd
import sys


def plot_bug_fixes(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Plotting
    ax = df.plot(x="Setting", kind="bar", stacked=False, figsize=(10, 6))
    # plt.title("Bug Fixes by Setting")
    plt.ylabel("Count", fontsize=16)
    # plt.xlabel("Setting No")
    plt.xticks(rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(title="Bug Type", fontsize=14, title_fontsize=16)
    plt.tight_layout()  # Adjust layout to not cut off labels

    ax.set_xlabel("")  # Remove x-axis label
    plt.savefig("bug_types_fixes_by_setting.pdf", format="pdf")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv_file>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    plot_bug_fixes(csv_file_path)
