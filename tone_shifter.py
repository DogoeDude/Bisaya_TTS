import os
import librosa
import soundfile as sf
import numpy as np
from tqdm import tqdm

def process_audio_file(input_path, output_path, pitch_semitones):
    try:
        y, sr = librosa.load(input_path, sr=None)
        y_pitch = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=pitch_semitones)
        sf.write(output_path, y_pitch, sr)
        return True
    except Exception as e:
        print(f"\nError processing {input_path}: {str(e)}")
        return False

# Setup folders
input_folder = "custom_data"
output_folder = "outputs/low_tone"
os.makedirs(output_folder, exist_ok=True)

# Pitch shift settings
pitch_semitones = -2  # Change to -2 to lower the pitch

# Count successful and failed conversions
successful = 0
failed = 0

# Process all WAV files
for file in tqdm(os.listdir(input_folder), desc="Modifying Pitch"):
    if file.endswith(".wav"):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)
        
        if process_audio_file(input_path, output_path, pitch_semitones):
            successful += 1
        else:
            failed += 1

# Print summary
print(f"\nProcessing complete!")
print(f"Successfully processed: {successful} files")
print(f"Failed to process: {failed} files")
print(f"Modified audio files saved in: {output_folder}")