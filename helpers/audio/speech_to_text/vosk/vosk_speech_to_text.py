#!/usr/bin/env python3
"""
Local Speech-to-Text Helper using Vosk
Provides offline speech recognition without internet connection
"""

import json
import logging
import os

from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)
logger = logging.getLogger(__name__)


class VoskSpeechToText:
    """
    Local speech-to-text recognition using Vosk
    - Fully offline (no internet required)
    - Low latency
    - Supports multiple languages
    """

    def __init__(self, model_path: str):
        """
        Initialize the speech-to-text helper

        Args:
            model_path: Path to Vosk model directory. Can also be a name of a pre-downloaded model in the "models/audio/vosk/" directory
        """
        if not os.path.exists(model_path):
            model_path = os.path.join("models", "audio", "vosk", model_path)

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Vosk model not found at {model_path}\n"
                f"Download models from: https://alphacephei.com/vosk/models\n"
                f"Extract to: models/audio/vosk/"
            )

        self._model = Model(model_path)
        self._recognizer = KaldiRecognizer(self._model, 16000)

    def convert_speech_to_text(self, audio_bytes: bytes) -> dict:
        """
        Convert speech audio bytes to text transcription

        Args:
            audio_bytes: Audio data in bytes (WAV format, mono, 16kHz)

        Returns:
            Transcribed text
        """
        if not audio_bytes:
            return {"text": "", "is_partial": False}

        if not self._recognizer.AcceptWaveform(audio_bytes):
            result = self._recognizer.PartialResult()
        else:
            result = self._recognizer.Result()

        result_dict: dict = json.loads(result)
        speech_as_text: str = result_dict.get("text", "")

        if not speech_as_text:
            speech_as_text = result_dict.get("partial", "")

        return {"text": speech_as_text, "is_partial": result_dict.get("partial", "") != ""}
