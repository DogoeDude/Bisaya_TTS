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

def gen_aud(text="Hello world"):
    output_path = "outputs/output.wav"
    tts.tts_to_file(text=text, file_path=output_path)
    return output_path 

print(gen_aud("Hello world"))
