import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy import stats

def clean_filename(filename):
    """Clean filename by removing quotes and special characters"""
    return str(filename).strip('"\'').replace(',', '')

def is_outlier(data):
    """Detect outliers using IQR method"""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (data < lower_bound) | (data > upper_bound)

def clean_data(input_file, output_file):
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Make a copy of original data
        df_cleaned = df.copy()
        
        # Define column types
        numeric_columns = [
            'Sample Rate (Hz)', 
            'Channels', 
            'Bit Depth', 
            'Number of Samples', 
            'Duration (s)', 
            'File Size (bytes)',
            'Peak Amplitude', 
            'RMS Amplitude'
        ]
        
        string_columns = ['Filename', 'Transcription']
        
        # Process string columns first
        for col in string_columns:
            if col in df_cleaned.columns:
                # Clean strings and handle empty values
                df_cleaned[col] = df_cleaned[col].apply(clean_filename)
                df_cleaned[col] = df_cleaned[col].replace('nan', '')
                
        # Process numeric columns
        for col in numeric_columns:
            if col in df_cleaned.columns:
                # Convert to numeric directly
                try:
                    # First attempt: direct conversion
                    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
                except:
                    # Second attempt: clean string values first
                    df_cleaned[col] = df_cleaned[col].apply(lambda x: str(x).strip('"\''))
                    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
                
                # Handle outliers
                mask = is_outlier(df_cleaned[col])
                if mask.any():
                    print(f"Found {mask.sum()} outliers in {col}")
                    # Replace outliers with median of non-outlier values
                    median_val = df_cleaned.loc[~mask, col].median()
                    df_cleaned.loc[mask, col] = median_val
                
                # Fill remaining NaN values with median
                median_val = df_cleaned[col].median()
                df_cleaned[col] = df_cleaned[col].fillna(median_val)
        
        # Save cleaned data without quoting numeric values
        df_cleaned.to_csv(output_file, index=False, float_format='%.6f')
        
        # Print summary statistics
        print("\nSummary of cleaned data:")
        print(f"Total rows: {len(df_cleaned)}")
        print("\nNumeric columns statistics:")
        print(df_cleaned[numeric_columns].describe())
        
        # Print data types of each column
        print("\nData types of columns:")
        print(df_cleaned.dtypes)
        
        return df_cleaned
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise  # This will show the full error traceback
        return None

# File paths
input_file = "tts_metadata1_plain.csv"
output_file = "cleansed_metadata/tts_plain_metadata_cleaned.csv"

# Clean the data
cleaned_data = clean_data(input_file, output_file)

if cleaned_data is not None:
    print(f"\nData cleaning completed successfully!")
    print(f"Cleaned data saved to: {output_file}")