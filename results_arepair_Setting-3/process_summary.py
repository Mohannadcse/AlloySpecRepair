import pandas as pd

def process_summary_file(input_file, output_file):
    # Attempt to read the CSV file while handling bad lines
    df = pd.read_csv(input_file, on_bad_lines='skip')  # Use on_bad_lines instead of error_bad_lines

    # Initialize a list to hold the rows for the final DataFrame
    final_data = []

    # Loop through the DataFrame to find .als files
    for i in range(1, len(df)):
        if df['fileName'].iloc[i].endswith('.als'):
            # Get the row above the .als entry
            previous_row = df.iloc[i - 1]
            # Check if the previous row's status is one of the desired statuses
            if previous_row['status'] in ["FIXED", "NOT_FIXED", "SYNTAX_ERROR", "TYPE_ERROR"]:
                # Append the previous row to the final data list
                final_data.append({
                    'fileName': previous_row['fileName'],
                    'iterations': previous_row['iterations'],
                    'status': previous_row['status']
                })

    # Convert the final data list to a DataFrame
    final_df = pd.DataFrame(final_data)

    # Save the result to a new CSV file
    final_df.to_csv(output_file, index=False)

# Specify your input and output file paths
input_file_path = 'summary.csv'  # Change this to your actual input file path
output_file_path = 'final_summary.csv'

# Process the summary file
process_summary_file(input_file_path, output_file_path)
