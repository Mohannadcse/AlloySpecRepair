import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Import NumPy
import sys


def plot_box_whisker(csv_path):
    df = pd.read_csv(csv_path)

    settings = df["Setting"]
    boxplot_data = [
        [
            x
            for x in df.loc[
                i,
                [
                    "Min number of iterations to fix",
                    "Q1 (25th percentile)",
                    "Median number of iterations to fix",
                    "Q3 (75th percentile)",
                    "Max number of iterations to fix",
                ],
            ].values.tolist()
        ]
        for i in df.index
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    bplot = ax.boxplot(
        boxplot_data,
        patch_artist=True,
        labels=settings,
        medianprops=dict(color="yellow", linewidth=2),
        whiskerprops=dict(color="black"),
        boxprops=dict(facecolor="lightgrey"),
    )

    # Plotting a distinctive marker at the median position for each box
    medians = [np.median(data) for data in boxplot_data]
    for i, median in enumerate(medians):
        ax.plot(
            i + 1,
            median,
            marker="X",
            markersize=12,
            markeredgecolor="red",
            markerfacecolor="gold",
        )

    # plt.ylim(1, 5)
    # plt.yticks([i for i in range(1,7)], fontsize=16)
    plt.ylabel("Number of Iterations", fontsize=16)
    plt.xticks(rotation=45, fontsize=16)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()

    plt.savefig("box-whisker-plot.pdf", format="pdf")

    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_consolidated_ANALYSIS.csv>")
    else:
        csv_path = sys.argv[1]
        plot_box_whisker(csv_path)
