import requests


class HomeAssistantAPI:
    """Home Assistant API integration base class"""

    def __init__(self, ha_url: str, access_token: str) -> None:
        self._ha_url: str = ha_url
        self._access_token: str = access_token

    @property
    def _authorization_header(self) -> dict:
        """Return authorization header for requests."""
        return {"Authorization": f"Bearer {self._access_token}"}

    def _call_service(
        self, domain: str, service: str, payload: dict = {}, extra_headers: dict = {}
    ) -> requests.Response:
        """Call a Home Assistant service.

        Args:
            domain: Service domain (e.g., "light", "media_player").
            service: Service name (e.g., "turn_on", "play_media").
            payload: JSON payload to send with the request.
            extra_headers: Additional headers to include in the request.
        """

        headers = {
            **self._authorization_header,
            "Content-Type": "application/json",
            **extra_headers,
        }

        return requests.post(f"{self._ha_url}/api/services/{domain}/{service}", json=payload, headers=headers)
