from game_contracts.runner_server_abc import RunnerServerABC

from runners.utils.retries import safe_get, safe_post


class CloudRunnerServer(RunnerServerABC):

    def poll_for_message_from_client(self, game_id: str) -> dict: ...

    def push_message_to_client(self, game_id: str, payload: dict) -> None: ...

    def get_game_state(self, game_id: str) -> dict: ...
