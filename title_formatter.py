import pandas as pd

def format_transcriptions(csv_file):
    try:
        # Read CSV with correct delimiter (comma)
        df = pd.read_csv(csv_file)

        # Ensure 'Filename' column exists
        if 'Filename' not in df.columns:
            print("Error: 'Filename' column not found in CSV.")
            return

        # Extract transcription from filename
        df['Transcription'] = df['Filename'].apply(lambda x: ' '.join(word.capitalize() for word in x.split('_')[1:]).replace('.wav', ''))

        title = "tts_slowed_metadata_cleaned.csv"
        # Save the updated CSV
        df.to_csv(f"{title}", index=False)
        print(f"CSV successfully formatted and saved as {title}")

    except Exception as e:
        print(f"Error processing CSV: {e}")

# Run the function
format_transcriptions("cleansed_metadata/tts_slowed_metadata_cleaned.csv")
