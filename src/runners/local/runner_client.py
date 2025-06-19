import requests
import time
import asyncio
import httpx
from game_contracts.runner_client_abc import RunnerClientABC


class LocalRunnerClient(RunnerClientABC):
    def __init__(self, fastapi_url="http://localhost:8000", player_id="player1"):
        self.fastapi_url = fastapi_url
        self.player_id = player_id

    def get_games_for_player(self, game_configs) -> list:
        res = requests.get(
            f"{self.fastapi_url}/get_games_for_player",
            json={**game_configs},
        )
        if res.status_code == 200:
            return res.json()
        else:
            return []

    def setup_new_game(self, game_configs: dict) -> dict:
        res = requests.post(
            f"{self.fastapi_url}/setup_new_game",
            json={**game_configs},
        )
        if res.status_code == 200:
            return res.json()
        else:
            return {}

    def initialize_server(self, game_id) -> dict:
        res = requests.post(
            f"{self.fastapi_url}/initialize_server",
            json={"game_id": game_id},
        )
        if res.status_code == 200:
            return res.json()
        else:
            return {}

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

    def post_to_server(self, payload: dict) -> None:
        requests.post(
            f"{self.fastapi_url}/post_from_client",
            json={**payload, "player_id": self.player_id},
        )
