import os
import librosa
import soundfile as sf
import numpy as np
from tqdm import tqdm

input_folder = "custom_data" 
output_folder = "outputs/high_tone"

os.makedirs(output_folder, exist_ok=True)
pitch_semitones = 2  # Change to -2 to lower the pitch

# Process all WAV files
for file in tqdm(os.listdir(input_folder), desc="Modifying Pitch"):
    if file.endswith(".wav"):
        file_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)  
        y, sr = librosa.load(file_path, sr=None)  
        y_pitch = librosa.effects.pitch_shift(y, sr, n_steps=pitch_semitones)
        sf.write(output_path, y_pitch, sr)

print(f"Modified audio files saved in: {output_folder}")
