import time

import requests
from game_contracts.runner_server_abc import RunnerServerABC

from runners.utils.retries import safe_get, safe_post


class LocalRunnerServer(RunnerServerABC):
    def __init__(self, fastapi_url="http://localhost:8000"):
        self.fastapi_url = fastapi_url

    def poll_for_message_from_client(self, game_id: str) -> dict:
        """Poll the FastAPI server for incoming messages from client"""
        while True:
            try:
                res = safe_get(
                    f"{self.fastapi_url}/poll_from_server", params={"game_id": game_id}
                )
                if res.status_code == 200:
                    return res.json()
            except Exception as e:
                print("Error polling for message:", e)
            time.sleep(0.5)

    def push_message_to_client(self, game_id: str, payload: dict) -> None:
        """Send a message to a specific client (they poll for it)"""
        res = safe_post(
            f"{self.fastapi_url}/push_to_client",
            payload=payload,
        )
        res.raise_for_status()

    def get_game_state(self, game_id: str) -> dict:
        """Fetch metadata for a specific game"""
        res = safe_get(f"{self.fastapi_url}/game_state", params={"game_id": game_id})
        if res.status_code == 200:
            return res.json()
        else:
            return {}
