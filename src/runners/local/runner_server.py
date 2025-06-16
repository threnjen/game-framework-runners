import requests
import time
from game_contracts.runner_server_abc import RunnerServerABC


class LocalRunnerServer(RunnerServerABC):
    def __init__(self, fastapi_url="http://localhost:8000"):
        self.fastapi_url = fastapi_url

    def poll_for_message_from_client(self) -> dict:
        """Poll the FastAPI server for incoming messages from client"""
        while True:
            try:
                res = requests.get(f"{self.fastapi_url}/poll_from_server")
                if res.status_code == 200:
                    return res.json()
            except Exception as e:
                print("Error polling for message:", e)
            time.sleep(0.5)

    def push_message_to_client(self, player_id: str, payload: dict) -> None:
        """Send a message to a specific client (they poll for it)"""
        res = requests.post(
            f"{self.fastapi_url}/push_to_client",
            params={"player_id": player_id},
            json=payload,
        )
        res.raise_for_status()
