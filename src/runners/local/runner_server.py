from game_contracts.runner_server_abc import RunnerServerABC


class LocalRunnerServer(RunnerServerABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        # Implement the logic to start the local runner server
        pass

    def stop(self):
        # Implement the logic to stop the local runner server
        pass

    def run(self):
        # Implement the logic to run the local runner server
        pass
