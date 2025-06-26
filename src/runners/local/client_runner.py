import asyncio
import time

import httpx
import requests
from game_contracts.runner_client_abc import RunnerClientABC
from game_contracts.message import MessageEnvelope, MessageSource

from runners.utils.retries import safe_get, safe_post
from runners.utils.hmacsigner import HMACSigner


class LocalRunnerClient(RunnerClientABC):
    def __init__(self, fastapi_url="http://localhost:8000", player_id="player1"):
        self.fastapi_url = fastapi_url
        self.player_id = player_id
        self.sequence_number = 0
        self.signer = HMACSigner(secret="your_secret_key")

    def get_games_for_player(self, game_configs) -> dict:
        res = safe_get(
            f"{self.fastapi_url}/get_games_for_player",
            params={**game_configs},
        )
        if res.status_code == 200:
            return res.json()
        else:
            return {}

    def setup_new_game(self, game_configs: dict) -> dict:
        res = safe_post(
            f"{self.fastapi_url}/setup_new_game",
            payload={**game_configs},
        )
        if res.status_code == 200:
            return res.json()
        else:
            return {}

    def initialize_server(self, params) -> bool:
        res = safe_post(
            f"{self.fastapi_url}/initialize_server",
            payload={**params},
        )
        if res.status_code == 200:
            return True
        else:
            return False

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

    def post_to_server(self, game_id: str, client_id: str, payload: dict) -> None:

        envelope = MessageEnvelope(
            client_id=client_id,
            game_id=game_id,
            source=MessageSource.CLIENT,
            seq=self.sequence_number,
            payload={"move": "play_card", "card": "Surge"},
        )

        envelope.signature = self.signer.sign(envelope)

        safe_post(
            f"{self.fastapi_url}/post_from_client",
            payload=envelope.dict(),
        )

        self.sequence_number += 1
