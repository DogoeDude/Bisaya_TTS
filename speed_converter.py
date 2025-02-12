import os
import librosa
import soundfile as sf
import numpy as np
from tqdm import tqdm  # For progress bar

# Input and output directories
input_folder = "outputs/slowdown"   # Change this to your folder path
output_folder = "outputs/mixed" # Change this to where you want the output

os.makedirs(output_folder, exist_ok=True)
speed_factor = 1.5 #recent

# Process all WAV files
for file in tqdm(os.listdir(input_folder), desc="Processing Audio"):
    if file.endswith(".wav"):
        file_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)
        y, sr = librosa.load(file_path, sr=None)
        y_slow = librosa.effects.time_stretch(y, rate=speed_factor)
        sf.write(output_path, y_slow, sr)

print(f"Slowed-down audio files saved in: {output_folder}")
