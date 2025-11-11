import os
from fastapi import APIRouter, Body, Response

from helpers.audio.text_to_speech.ha_text_to_speech_api import HATextToSpeechAPI
from middleware.auth import require_auth

router = APIRouter()


@router.post("/")
def text_to_speech(token: str = require_auth(), body: dict = Body(...)):
    engine_id: str = body.get("engine_id", os.getenv("HOME_ASSISTANT_TTS_DEFAULT_VOICE_ENGINE_ID", ""))
    message: str = body.get("message", "")

    if not engine_id or not message:
        return Response(content="Invalid request", status_code=422)

    try:
        ha_host: str = os.getenv("HOME_ASSISTANT_HOST", "")
        ha_port: str = os.getenv("HOME_ASSISTANT_PORT", "")
        ha_url: str = f"{ha_host}:{ha_port}"
        ha_token: str = os.getenv("HOME_ASSISTANT_TOKEN", "")

        tts_api = HATextToSpeechAPI(ha_url, ha_token)
        tts_result = tts_api.convert_text_to_speech(engine_id, message)

        # Return the audio data as a proper Response with correct content type
        audio_content = tts_result.get("content", b"")
        audio_format = tts_result.get("format", "mpeg")

        # Set appropriate content type based on format
        content_type = f"audio/{audio_format}"

        return Response(
            content=audio_content,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename=tts_audio.{audio_format}",
                "Content-Length": str(len(audio_content)),
            },
        )
    except Exception as e:
        return Response(content=str(e), status_code=500)
