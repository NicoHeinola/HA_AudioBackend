import os
from pyexpat import model
from fastapi import APIRouter, File, Form, Response, UploadFile

from helpers.audio.mixing.audio_mixer import AudioMixer
from middleware.auth import require_auth

router = APIRouter()


@router.post("/speed-up")
def speech_to_text(token: str = require_auth(), speed: str | float = Form(...), file: UploadFile = File(...)):
    """
    Endpoint to convert speech audio to text.
    """

    speed = float(speed)

    if speed < 1.0:
        return Response(
            content="Speed must be greater than or equal to 1.0",
            status_code=422,
        )

    try:
        audio_bytes = file.file.read()
        sped_up_audio: bytes = AudioMixer.speed_up_audio(audio_bytes, speed, output_format="wav")
    except ValueError as exc:
        print(exc)

        return Response(
            content=str(exc),
            status_code=422,
        )

    audio_format: str = "wav"
    if file.filename is not None:
        file.filename.split(".")[-1]

    content_type: str = f"audio/{audio_format}"
    return Response(
        content=sped_up_audio,
        media_type=content_type,
        headers={
            "Content-Disposition": f"attachment; filename=tts_audio_sped_up.{audio_format}",
            "Content-Length": str(len(sped_up_audio)),
        },
    )
