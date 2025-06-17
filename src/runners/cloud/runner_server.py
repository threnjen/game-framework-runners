from game_contracts.runner_server_abc import RunnerServerABC


class CloudRunnerServer(RunnerServerABC):

    async def poll_for_message_from_client(self) -> dict: ...

    async def push_message_to_client(self, payload: dict) -> None: ...
