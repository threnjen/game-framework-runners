from abc import ABC, abstractmethod


class RunnerServerABC(ABC):

    async def poll_for_message_from_client(self) -> None: ...

    async def push_message_to_client(self, player_id: str, payload: dict) -> None: ...
