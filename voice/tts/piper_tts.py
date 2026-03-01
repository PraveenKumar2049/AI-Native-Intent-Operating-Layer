"""
Piper TTS Module
----------------
Windows-safe version.
No manual device forcing.
Uses system default output.
"""

import os
import numpy as np
import sounddevice as sd
from piper import PiperVoice
from .config import VOICE_MODEL_PATH, PLAY_AUDIO


class PiperTTS:
    def __init__(self):
        if not os.path.exists(VOICE_MODEL_PATH):
            raise FileNotFoundError(f"Piper model not found at: {VOICE_MODEL_PATH}")

        self.voice = PiperVoice.load(VOICE_MODEL_PATH)

    def speak(self, text: str):
        if not text.strip():
            return

        try:
            audio_chunks = []
            sample_rate = None

            for chunk in self.voice.synthesize(text):

                if hasattr(chunk, "audio_float_array"):
                    audio_chunks.append(chunk.audio_float_array)

                if hasattr(chunk, "sample_rate") and sample_rate is None:
                    sample_rate = chunk.sample_rate

            if not audio_chunks:
                print("No audio generated.")
                return

            audio = np.concatenate(audio_chunks).astype(np.float32)

            if sample_rate is None:
                sample_rate = 22050

            # 🔥 DO NOT FORCE DEVICE
            sd.play(audio, sample_rate)
            sd.wait()

        except Exception as e:
            print(f"TTS Error: {e}")
