from game_contracts.runner_server_abc import RunnerServerABC
from fastapi import FastAPI, Request
import uvicorn
import asyncio

app = FastAPI()


class LocalRunnerServer(RunnerServerABC):

    def __init__(self) -> None:
        self.pending_actions = {}
        self.pending_responses = {}

    @app.get("/poll_for_input")
    async def poll_for_input(self, player_id: str):
        while player_id not in self.pending_responses:
            await asyncio.sleep(0.5)
        return {"action": self.pending_responses.pop(player_id)}

    @app.post("/post_action")
    async def receive_action(self, player_id: str, request: Request):
        action = await request.json()
        self.pending_responses[player_id] = action
        return {"status": "received"}

    @app.get("/get_available_actions")
    async def get_actions(self, player_id: str):
        # Polling: return actions if available
        actions = self.pending_actions.pop(player_id, None)
        return {"available_actions": actions or []}

    @app.post("/set_actions")
    async def push_response(self, player_id: str, request: Request):
        actions = await request.json()
        self.pending_actions[player_id] = actions
        return {"status": "actions set"}
