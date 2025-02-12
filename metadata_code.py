import os
import soundfile as sf
import pandas as pd
import numpy as np

# Folder containing audio files
folder_path = "outputs/mixed"
output_csv = "tts_metadata_mixed.csv"

# Dictionary to map filenames to their transcriptions
transcriptions = {
    "01_maayong_buntag.wav": "Maayong buntag",
    "02_maayong_hapon.wav": "Maayong hapon",
    # Add more mappings here
}

# Dictionary to map soundfile subtypes to bit depths
subtype_to_bits = {
    'PCM_16': 16,
    'PCM_24': 24,
    'PCM_32': 32,
    'FLOAT': 32,
    'DOUBLE': 64,
    'PCM_U8': 8,
    'PCM_S8': 8
}

# List to store metadata
metadata = []

# Process each audio file in the folder
for file in os.listdir(folder_path):
    if file.endswith(('.wav', '.WAV')):
        try:
            file_path = os.path.join(folder_path, file)
            file_size = os.path.getsize(file_path)
            transcription = transcriptions.get(file, "")

            # Read audio file using soundfile
            data, sample_rate = sf.read(file_path)
            
            # Convert to mono if stereo
            if len(data.shape) > 1:
                data = np.mean(data, axis=1)

            # Calculate audio properties
            duration = len(data) / sample_rate
            peak_amplitude = np.max(np.abs(data))
            rms_amplitude = np.sqrt(np.mean(data**2))
            
            # Get audio file info
            info = sf.info(file_path)
            
            # Get bit depth from subtype
            bit_depth = subtype_to_bits.get(info.subtype, 'Unknown')

            # Append metadata to list
            metadata.append({
                "Filename": file,
                "Transcription": transcription,
                "Sample Rate (Hz)": sample_rate,
                "Channels": info.channels,
                "Bit Depth": bit_depth,
                "Number of Samples": len(data),
                "Duration (s)": round(duration, 2),
                "File Size (bytes)": file_size,
                "Peak Amplitude": round(peak_amplitude, 4),
                "RMS Amplitude": round(rms_amplitude, 4)
            })
            
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
            continue

# Convert to DataFrame
df = pd.DataFrame(metadata)

# Save to CSV
df.to_csv(output_csv, index=False)
print(f"TTS Metadata extracted and saved to {output_csv}!")