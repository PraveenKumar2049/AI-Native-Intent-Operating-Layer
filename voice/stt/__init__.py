"""
STT Package
-----------
Speech-to-Text utilities for AI_OS.

Safe import layer.
Does NOT execute model loading automatically.
"""

from .whisper_stt import WhisperSTT
from .audio_capture import record_audio
