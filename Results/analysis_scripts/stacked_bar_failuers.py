import pandas as pd
import matplotlib.pyplot as plt
import sys

# Check if the command line argument is provided
if len(sys.argv) < 2:
    print("Usage: script.py <csv_file>")
    sys.exit(1)

# Read the CSV file
csv_file = sys.argv[1]
data = pd.read_csv(csv_file)

# Set the 'Setting' column as the index
data.set_index("Setting", inplace=True)

# Define a list of easily distinguishable colors with more contrast
colors = [
    "#1f77b4",  # Muted Blue
    "#ff7f0e",  # Safety Orange
    # "#000000",  # Black
    "#00ff00",  # Lime Green
    "#9b59b6",  # Bright Purple
    "#f1c40f",  # Deep Yellow
]

# Plot with the custom colors
data.plot(kind="barh", stacked=True, figsize=(10, 7), color=colors)

plt.xlabel("Number of failures", fontsize=14)
plt.ylabel("")  # Set y-axis label to an empty string
plt.yticks(fontsize=14)
# Adjust the legend to be on top of the graph
plt.legend(
    [
        "SyntaxErrors",
        "Counterexamples",
        "NoInstances",
        "Repetition",
        "WrongMessageFormat",
    ],
    loc="lower center",
    bbox_to_anchor=(0.5, 1.0),
    ncol=5,
)

plt.tight_layout()
plt.savefig("stacked_bar_failures.pdf", format="pdf")  # Save the plot as a PDF file
plt.show()  # Display the plot
