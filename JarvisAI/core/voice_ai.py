import sounddevice as sd
import soundfile as sf
import numpy as np
from openai import OpenAI
import tempfile
import os

client = OpenAI()

def speak(text: str, voice="alloy"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        audio_path = f.name

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,   # calm, deep, Jarvis-like
        input=text
    )

    response.stream_to_file(audio_path)

    data, samplerate = sf.read(audio_path, dtype="float32")
    sd.play(data, samplerate)
    sd.wait()

    os.remove(audio_path)
