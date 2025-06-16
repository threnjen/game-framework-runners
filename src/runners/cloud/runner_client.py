from game_contracts.runner_client_abc import RunnerClientABC


class CloudRunnerClient(RunnerClientABC):

    def poll_for_input(self) -> None: ...

    def request_user_action(self, actions) -> str: ...

    def post_message_to_server(self, choice) -> None: ...
