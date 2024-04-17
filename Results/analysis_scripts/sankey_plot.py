import pandas as pd
import plotly.graph_objects as go

# Load the CSV data
df = pd.read_csv("/Users/moh/Downloads/repos/repair-sw-spec/setting6-iter1-6.csv")

# Initialize a list to store all unique statuses
unique_statuses = ["Defective_Model"]

# Initialize dictionaries to store the flow between statuses for each iteration
iteration_flows = {}

# Iterate over each row in the dataframe
for i in range(1, 7):
    # Extract iteration statuses
    iteration_statuses = df[f"iteration_{i}_status"].dropna().unique()

    # Append the iteration number to each status label
    iteration_statuses = [f"{status}_iteration_{i}" for status in iteration_statuses]

    # Update unique_statuses list, excluding NaN values
    unique_statuses.extend(iteration_statuses)

    # Initialize the flow dictionary for the current iteration
    iteration_flows[i] = {}

    # Iterate over each row again to collect the flow between statuses for the current iteration
    for index, row in df.iterrows():
        if i == 1:
            # For the first iteration, the source is the Defective_Model block
            source = "Defective_Model"
        else:
            # For subsequent iterations, the source is the status from the previous iteration
            source = f"{row[f'iteration_{i-1}_status']}_iteration_{i-1}"

        # Extract the current status for the current iteration
        current_status = f"{row[f'iteration_{i}_status']}_iteration_{i}"

        # Skip if current_status is NaN
        if pd.isna(row[f"iteration_{i}_status"]):
            continue

        # Update flow counts for the current iteration
        if source not in iteration_flows[i]:
            iteration_flows[i][source] = {}
        if current_status not in iteration_flows[i][source]:
            iteration_flows[i][source][current_status] = 0
        iteration_flows[i][source][current_status] += 1

# Filter out NaN values from unique_statuses
nodes = [status for status in unique_statuses if status not in [None, "nan"]]

# Create lists to store link data for the Sankey plot
link_data = []

# Iterate over each iteration's flow data to create links
for iteration, flow_data in iteration_flows.items():
    for source, targets in flow_data.items():
        for target, value in targets.items():
            if target in [None, "nan"]:
                continue  # Skip if target is NaN or not in nodes

            link_data.append(
                {
                    "source": nodes.index(source),
                    "target": nodes.index(target),
                    "value": value,
                }
            )

# Calculate total flows out of each node for percentages
total_flows_out = [
    0 for _ in nodes
]  # Initialize total flows out for each node as zeros

# Update total flows out based on the source index in link_data
for link in link_data:
    total_flows_out[link["source"]] += link["value"]

# Adjust link data to include custom data for hover information
for link in link_data:
    source_flow_total = total_flows_out[link["source"]]
    flow_percentage = (
        (link["value"] / source_flow_total) * 100 if source_flow_total else 0
    )
    link["customdata"] = [f"{flow_percentage:.2f}%"]

# Define a color mapping for statuses
color_mapping = {
    "Defective_Model": "lightgray",
    "Fixed": "green",
    "counterexample": "darkorange",
    "SyntaxError": "skyblue",
    "NoInstance": "lightgreen",
    "Repitation": "darkviolet",
}

# Apply color mapping to nodes
node_colors = [color_mapping.get(status.split("_")[0], "gray") for status in nodes]

# Create the Sankey plot with hovertemplate
fig = go.Figure(
    data=[
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color=node_colors,
            ),
            link=dict(
                source=[link["source"] for link in link_data],
                target=[link["target"] for link in link_data],
                value=[link["value"] for link in link_data],
                customdata=[link["customdata"] for link in link_data],
                hovertemplate="%{source.label} to %{target.label}: %{value}<br>%{customdata[0]}<extra></extra>",
            ),
        )
    ]
)

# Update layout
fig.update_layout(font=dict(size=10))

# Show the plot
fig.show()
