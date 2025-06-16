from game_contracts.runner_client_abc import RunnerClientABC


class CloudRunnerClient(RunnerClientABC):

    def poll_for_input(self) -> None: ...

    def poll_for_server_response(self) -> str: ...

    def send_action_to_server(self, action) -> None: ...
