"""
Voice Manager
-------------
High-level interface combining STT and TTS.

This module does NOT modify or interfere with existing AI_OS logic.
It is only used when explicitly imported.
"""

from voice.stt import WhisperSTT, record_audio
from voice.tts import PiperTTS


class VoiceManager:
    """
    Orchestrates Speech-to-Text and Text-to-Speech.
    """

    def __init__(self):
        """
        Initialize STT and TTS engines.
        Models load only when this class is instantiated.
        """
        self.stt = WhisperSTT()
        self.tts = PiperTTS()

    # -------------------------
    # LISTEN
    # -------------------------
    def listen(self, duration: int = 5) -> str:
        """
        Records audio from mic and converts to text.

        Args:
            duration (int): recording duration in seconds

        Returns:
            str: recognized speech text
        """
        audio_path = record_audio(duration=duration)

        if not audio_path:
            return ""

        return self.stt.transcribe(audio_path)

    # -------------------------
    # SPEAK
    # -------------------------
    def speak(self, text: str):
        """
        Converts text to speech and plays it.
        """
        self.tts.speak(text)
