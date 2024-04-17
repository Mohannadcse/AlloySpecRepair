import pandas as pd
import matplotlib.pyplot as plt
import sys


def plot_box_whisker(csv_path):
    # Load the CSV file
    data = pd.read_csv(csv_path)

    # Filter the data where 'fixed' column is 'YES'
    filtered_data = data[data["fixed"] == "YES"]["iterations"]

    if len(filtered_data) > 0:
        # Calculate Q1, Q3, and median
        Q1 = filtered_data.quantile(0.25)
        Q3 = filtered_data.quantile(0.75)
        median = filtered_data.median()
        IQR = Q3 - Q1

        # Generate the box-whisker plot
        plt.figure(figsize=(10, 6))
        boxplot = plt.boxplot(
            filtered_data, vert=True, patch_artist=True, labels=["Iterations"]
        )

        # Optional: Annotate the plot with Q1, Q3, and median values
        plt.text(
            1,
            Q1,
            f"Q1: {Q1}",
            ha="center",
            va="center",
            fontweight="bold",
            color="blue",
        )
        plt.text(
            1, Q3, f"Q3: {Q3}", ha="center", va="center", fontweight="bold", color="red"
        )
        plt.text(
            1,
            median,
            f"Median: {median}",
            ha="center",
            va="center",
            fontweight="bold",
            color="green",
        )

        plt.title("Box-Whisker Plot for Iterations where Fixed is YES")
        plt.ylabel("Iterations")
        plt.show()
    else:
        print("No data available for 'fixed' column marked as 'YES'.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_box_whisker.py <path_to_csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    plot_box_whisker(csv_path)
