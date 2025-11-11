import os
from pyexpat import model
from fastapi import APIRouter, File, Form, Response, UploadFile

from helpers.audio.mixing.audio_mixer import AudioMixer
from middleware.auth import require_auth

router = APIRouter()


@router.post("/speed-up")
def speech_to_text(token: str = require_auth(), speed: int = Form(...), file: UploadFile = File(...)):
    """
    Endpoint to convert speech audio to text.
    """

    sped_up_audio: bytes = AudioMixer.speed_up_audio(file.file.read(), speed)

    audio_format: str = "mp3"
    if file.filename is not None:
        file.filename.split(".")[-1]

    content_type: str = f"audio/{audio_format}"
    return Response(
        content=sped_up_audio,
        media_type=content_type,
        headers={
            "Content-Disposition": f"attachment; filename=tts_audio.{audio_format}",
            "Content-Length": str(len(sped_up_audio)),
        },
    )
