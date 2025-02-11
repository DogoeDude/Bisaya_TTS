import os
import wave
import pandas as pd
import scipy.io.wavfile as wav
import numpy as np

# Folder containing WAV files
folder_path = "custom_data"
output_csv = "tts_metadata.csv"

# Dictionary to map filenames to their transcriptions (you need to fill this manually or from a dataset)
transcriptions = {
    "01_maayong_buntag.wav": "Maayong buntag",
    "02_maayong_hapon.wav": "Maayong hapon",
    # Add more mappings here
}

# List to store metadata
metadata = []

# Process each WAV file in the folder
for file in os.listdir(folder_path):
    if file.endswith(".wav"):
        file_path = os.path.join(folder_path, file)
        file_size = os.path.getsize(file_path)
        transcription = transcriptions.get(file, "")  # Get transcription (if available)

        # Open the audio file
        with wave.open(file_path, "rb") as audio:
            sample_rate = audio.getframerate()
            num_channels = audio.getnchannels()
            bit_depth = audio.getsampwidth() * 8
            num_frames = audio.getnframes()
            duration = num_frames / float(sample_rate)

        # Read WAV data to compute peak and RMS amplitude
        sample_rate, data = wav.read(file_path)
        peak_amplitude = np.max(np.abs(data))
        rms_amplitude = np.sqrt(np.mean(data**2))

        # Append metadata to list
        metadata.append({
            "Filename": file,
            "Transcription": transcription,
            "Sample Rate (Hz)": sample_rate,
            "Channels": num_channels,
            "Bit Depth": bit_depth,
            "Number of Samples": num_frames,
            "Duration (s)": round(duration, 2),
            "File Size (bytes)": file_size,
            "Peak Amplitude": peak_amplitude,
            "RMS Amplitude": round(rms_amplitude, 2)
        })

# Convert to DataFrame
df = pd.DataFrame(metadata)

df.to_csv(output_csv, index=False)

print(f"TTS Metadata extracted and saved to {output_csv}!")
