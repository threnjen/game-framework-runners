from game_contracts.runner_client_abc import RunnerClientABC


class LocalRunnerClient(RunnerClientABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        # Implement the logic to connect to the local runner client
        pass

    def disconnect(self):
        # Implement the logic to disconnect from the local runner client
        pass

    def send_command(self, command):
        # Implement the logic to send a command to the local runner client
        pass
