import os
from fastapi import APIRouter, File, Form, Response, UploadFile

from helpers.audio.speech_to_text.vosk.vosk_speech_to_text_helper import VoskSpeechToTextHelper
from middleware.auth import require_auth

router = APIRouter()


@router.post("/")
def speech_to_text(token: str = require_auth(), model: str = Form(None), file: UploadFile = File(...)):
    """
    Endpoint to convert speech audio to text.
    """
    model = model or os.getenv("SPEECH_TO_TEXT_DEFAULT_MODEL", "")

    try:
        speech_to_text_helper: VoskSpeechToTextHelper = VoskSpeechToTextHelper(model)
        audio_bytes = file.file.read()
        speech_as_text: dict = speech_to_text_helper.convert_speech_to_text(audio_bytes)

        return speech_as_text
    except Exception as e:
        return Response(content=str(e), status_code=500)


@router.get("/models")
def list_models(token: str = require_auth()):
    """
    Endpoint to list available Vosk speech-to-text models.
    """
    models_dir = os.path.join("models", "audio", "vosk")
    try:
        models = [name for name in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, name))]
        return {"available_models": models}
    except Exception as e:
        return Response(content=str(e), status_code=500)
