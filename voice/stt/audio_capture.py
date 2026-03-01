"""
Audio Capture Module
--------------------
Records microphone input and saves as WAV file.

Standalone utility.
Does NOT interfere with existing AI_OS system.
"""

import sounddevice as sd
import soundfile as sf
from .config import SAMPLE_RATE


def record_audio(
    filename: str = "temp.wav",
    duration: int = 5,
) -> str:
    """
    Records microphone audio.

    Args:
        filename (str): Output file name
        duration (int): Recording duration in seconds

    Returns:
        str: Path to saved audio file
    """

    try:
        print("🎙 Recording...")

        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )

        sd.wait()

        sf.write(filename, audio, SAMPLE_RATE)

        print("✅ Recording complete")

        return filename

    except Exception as e:
        print(f"Audio Capture Error: {e}")
        return ""
