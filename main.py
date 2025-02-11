from TTS.api import TTS
import gradio as gr
import torch
import os

# Set up the device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Ensure output directory exists
os.makedirs("outputs", exist_ok=True)

# Load TTS model once to avoid reloading each time
tts = TTS(model_name='tts_models/en/ljspeech/fast_pitch').to(device)

def get_unique_filename(base_path="outputs/output.wav"):
    """Generate a unique filename by appending numbers if the file exists."""
    if not os.path.exists(base_path):
        return base_path  # Return original name if it doesn't exist

    filename, ext = os.path.splitext(base_path)
    counter = 1

    while os.path.exists(f"{filename}_{counter}{ext}"):
        counter += 1

    return f"{filename}_{counter}{ext}"

def gen_aud(text="Hello world"):
    output_path = get_unique_filename()  # Generate unique filename
    tts.tts_to_file(text=text, file_path=output_path)
    
    if os.path.exists(output_path):
        return output_path  # Return the unique file path

print(gen_aud("Test ni siya na binisaya"))