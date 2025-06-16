from abc import ABC, abstractmethod


class RunnerServerABC(ABC):

    async def poll_for_message(self, player_id: str) -> None: ...

    async def push_message_to_client(self, player_id: str, request) -> None: ...
