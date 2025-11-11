import os
from fastapi import APIRouter, Body, File, Response, UploadFile

from helpers.audio.speech_to_text.vosk.vosk_speech_to_text_helper import VoskSpeechToTextHelper
from middleware.auth import require_auth

router = APIRouter()


@router.post("/")
def speech_to_text(token: str = require_auth(), body: dict = Body(...), file: UploadFile = File(...)):
    """
    Endpoint to convert speech audio to text.
    """

    model: str = body.get("model", os.getenv("SPEECH_TO_TEXT_DEFAULT_MODEL", ""))

    speech_to_text_helper: VoskSpeechToTextHelper = VoskSpeechToTextHelper(model)
    try:
        audio_bytes = file.file.read()
        speech_as_text: str = speech_to_text_helper.convert_speech_to_text(audio_bytes)

        return {"text": speech_as_text}
    except Exception as e:
        return Response(content=str(e), status_code=500)
