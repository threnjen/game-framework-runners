from game_contracts.runner_server_abc import RunnerServerABC


class LocalRunnerServer(RunnerServerABC):

    def poll_for_input(self) -> None: ...

    def push_response(self) -> None: ...
