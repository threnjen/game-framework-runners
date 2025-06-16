import requests
import time
from game_contracts.runner_server_abc import RunnerServerABC


class LocalRunnerServer(RunnerServerABC):
    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url

    def poll_for_message(self) -> dict:
        """Poll until a message is available from a client"""
        while True:
            try:
                res = requests.get(f"{self.server_url}/poll_from_server")
                if res.status_code == 200:
                    return res.json()
            except Exception:
                pass
            time.sleep(0.5)

    def push_message_to_client(self, player_id: str, payload: dict) -> None:
        """Push message to a specific client (they will poll for it)"""
        res = requests.post(
            f"{self.server_url}/push_to_client",
            params={"player_id": player_id},
            json=payload,
        )
        res.raise_for_status()
