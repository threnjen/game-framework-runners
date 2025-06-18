import requests
import time
import asyncio
import httpx
from game_contracts.runner_client_abc import RunnerClientABC


class LocalRunnerClient(RunnerClientABC):
    def __init__(self, fastapi_url="http://localhost:8000", player_id="player1"):
        self.fastapi_url = fastapi_url
        self.player_id = player_id

    async def poll_for_server_response(self) -> dict:
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    res = await client.get(
                        f"{self.fastapi_url}/poll_to_client",
                        params={"player_id": self.player_id},
                        timeout=10.0,
                    )
                    if res.status_code == 200:
                        return res.json()
                except httpx.RequestError as e:
                    print(f"Request failed: {e}")
                await asyncio.sleep(0.5)

    def send_action_to_server(self, action: dict):
        requests.post(
            f"{self.fastapi_url}/post_from_client",
            json={**action, "player_id": self.player_id},
        )
