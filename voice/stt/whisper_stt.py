"""
Whisper STT Module
-------------------
Converts audio file -> text

Standalone module.
Does NOT interfere with existing AI_OS pipeline.
"""

from faster_whisper import WhisperModel
from .config import MODEL_SIZE, DEVICE, COMPUTE_TYPE


class WhisperSTT:
    """
    Speech-to-Text engine using Faster-Whisper.
    """

    def __init__(self):
        """
        Loads model once during initialization.
        """
        self.model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribes a WAV audio file to text.
        """
        try:
            segments, _ = self.model.transcribe(audio_path)

            text = ""
            for segment in segments:
                text += segment.text

            return text.strip()

        except Exception as e:
            print(f"STT Error: {e}")
            return ""
