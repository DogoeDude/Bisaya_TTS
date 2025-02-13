import pandas as pd
import re

# File path
file_path = "cleansed_metadata/tts_mixed_metadata_cleaned.csv" # Change this to your actual CSV file

# Read CSV (adjust delimiter if needed)
df = pd.read_csv(file_path, delimiter=",", header=None)  # Use "," if it's a comma-separated file

# Function for natural sorting
def natural_sort_key(text):
    return [int(num) if num.isdigit() else num for num in re.split(r'(\d+)', str(text))]

# Sort the entire dataframe by the first column (filenames/numbers)
df = df.sort_values(by=0, key=lambda col: col.map(natural_sort_key))

# Save changes back to the same file
df.to_csv(file_path, index=False, sep=",", header=False)

print(f"CSV file '{file_path}' has been sorted and updated properly.")
