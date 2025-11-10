import os
from fastapi import APIRouter, Body, Response

from helpers.audio.ha_text_to_speech_api import HATextToSpeechAPI
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

        return Response(content=tts_result["content"], media_type=f"audio/{tts_result['format']}")
    except Exception as e:
        return Response(content=str(e), status_code=500)
