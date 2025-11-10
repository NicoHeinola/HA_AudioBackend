import requests

from helpers.home_assistant.home_assistant_api import HomeAssistantAPI


class HATextToSpeechAPI(HomeAssistantAPI):
    """Home Assistant Text-to-Speech integration"""

    def __init__(self, ha_url: str, access_token: str):
        super().__init__(ha_url, access_token)

    def _generate_tts_file_url(self, engine_id: str, message: str) -> requests.Response:
        """Get TTS URL from Home Assistant."""

        payload = {"engine_id": f"tts.{engine_id}", "message": message}
        headers = {
            **self._authorization_header,
            "Content-Type": "application/json",
        }

        response = requests.post(f"{self._ha_url}/api/tts_get_url", json=payload, headers=headers)
        return response

    def convert_text_to_speech(self, engine_id: str, message: str) -> dict:
        """Generate TTS file and retrieve its content and format."""

        response = self._generate_tts_file_url(engine_id, message)

        if response.status_code != 200:
            raise Exception(f"TTS generation failed: {response.text}")

        tts_url = response.json().get("url")
        if not tts_url:
            raise Exception("TTS URL not found in response.")

        tts_response = requests.get(f"{self._ha_url}{tts_url}", headers=self._authorization_header)
        if tts_response.status_code != 200:
            raise Exception(f"Failed to retrieve TTS audio file: {tts_response.text}")

        format: str = tts_response.headers.get("Content-Type", "audio/mpeg").split("/")[-1]

        return {"content": tts_response.content, "format": format}
