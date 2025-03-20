#This one converts the labels from categorical to numerical and also performs the summary statistics on it.
#will run overnight ot see results
#*****************************************************************************
#THIS IS THE BEST VERSION OF IT SO FAR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     *
# DONT PLAY WITH THIS ONE COPY FIRST !!!!!!!!!!!!!!!!                        *
#*****************************************************************************
import os
import pandas as pd

# Path to the folder containing the CSV files
folder_path = os.path.join(os.getcwd(), 'CIC')

# List of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Dictionaries to store intermediate summaries
num_chunks = {}              # Tracks the number of non-null rows processed per column
partial_sum = {}             # Accumulates the sum of values per column
partial_sum_squares = {}     # Accumulates the sum of squares of values per column (for variance)
max_values = {}              # Tracks the maximum value encountered per column
min_values = {}              # Tracks the minimum value encountered per column
value_counts = {}            # Stores frequency counts of unique values per column
label_mapping = {}           # Maps categorical labels to numerical values

#how many rows will be loaded at one time -> 500k seems to run okay with 16Gigs ram without maxing
# lower number will be slower, this seems like a good balance at least on my machine
chunksize = 500000

# Process each CSV file in the folder
for csv_file in csv_files:
    # Get the full path of the current CSV file
    csv_path = os.path.join(folder_path, csv_file)
    # Display progress by printing the current file being processed
    print(f'Processing file: {csv_file}')

    # Read the CSV file in chunks to avoid memory overload
    for chunk in pd.read_csv(csv_path, chunksize=chunksize):
        # Convert categorical labels to numerical
        if 'label' in chunk.columns:
            # Create label mapping if it doesnt exist
            if not label_mapping:
                unique_labels = chunk['label'].unique()
                label_mapping = {label: idx for idx, label in enumerate(unique_labels)}
            #Map categorical labels to numerical    
            chunk['label'] = chunk['label'].map(label_mapping)

        # Iterate through each column in the chunk
        for col in chunk.columns:
            # Skip non-numeric columns
            if not pd.api.types.is_numeric_dtype(chunk[col]):
                continue

            #initialize
            if col not in partial_sum:
                partial_sum[col] = 0
                partial_sum_squares[col] = 0
                num_chunks[col] = 0
                max_values[col] = float('-inf')
                min_values[col] = float('inf')
                value_counts[col] = pd.Series(dtype=int)

            # Accumulate sum and sum of squares for mean and variance calculations
            partial_sum[col] += chunk[col].sum()
            partial_sum_squares[col] += (chunk[col] ** 2).sum()
            # Update the number of non-null values processed
            num_chunks[col] += len(chunk[col].dropna())
            # Update max and min values
            max_values[col] = max(max_values[col], chunk[col].max())
            min_values[col] = min(min_values[col], chunk[col].min())
            # Update for mode calculation
            value_counts[col] = value_counts[col].add(chunk[col].value_counts(), fill_value=0)

# Calculate the statistics incrementally for each column
stats_summary = {}
print("\nCalculating statistics now")

for col in partial_sum:
    if num_chunks[col] > 0:
        # Calculate values
        mean = partial_sum[col] / num_chunks[col]
        variance = (partial_sum_squares[col] / num_chunks[col]) - (mean ** 2) if num_chunks[col] > 1 else 0
        stdev = variance ** 0.5
        mode_values = value_counts[col][value_counts[col] == value_counts[col].max()].index.tolist()
        mode = mode_values[0] if mode_values else None

        # Store calculated statistics for the current column
        stats_summary[col] = {
            'Mean': mean,
            'Mode': mode,
            'Max': max_values[col],
            'Min': min_values[col],
            'Standard Deviation': stdev,
        }

# Print the summary statistics for numeric columns
print('\nSummary Statistics Per Column')
for col, stats in stats_summary.items():
    print(f'\n{col}:')
    for stat_name, value in stats.items():
        print(f'  {stat_name}: {value}')

# Print the label mapping
print('\nLabel Mapping:')
for label, num in label_mapping.items():
    print(f'  {label} -> {num}')
