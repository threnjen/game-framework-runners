from game_contracts.runner_client_abc import RunnerClientABC


class LocalRunnerClient(RunnerClientABC):

    def poll_for_input(self) -> None: ...

    def push_response(self) -> None: ...
