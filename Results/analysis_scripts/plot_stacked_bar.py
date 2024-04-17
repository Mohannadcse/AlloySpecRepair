import pandas as pd
import matplotlib.pyplot as plt
import sys


def generate_stacked_bar_chart(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Calculate the number of fixed entries with iterations
    df["Number of fixed entries with iterations"] = (
        df["Number of fixed entries"]
        - df["Number of fixed entries with zero iterations"]
    )

    # Set 'Setting' column as index
    df.set_index("Setting", inplace=True)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(
        kind="bar",
        y=[
            "Number of fixed entries with iterations",
            "Number of fixed entries with zero iterations",
        ],
        stacked=True,
        ax=ax,
        color=["#1f77b4", "#ff7f0e"],
    )

    # Setting labels and title
    plt.ylabel("Count", fontsize=16)
    plt.legend(
        ["Fixed with two or more iterations", "Fixed from the first iterations"],
        fontsize=14,
    )
    plt.xticks(rotation=45, fontsize=16)
    plt.xlabel("")
    plt.yticks(fontsize=16)
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig("stacked_bar_chart.pdf", format="pdf")
    print("Stacked bar chart saved as 'stacked_bar_chart.pdf'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_csv_file>")
    else:
        csv_file = sys.argv[1]
        generate_stacked_bar_chart(csv_file)
