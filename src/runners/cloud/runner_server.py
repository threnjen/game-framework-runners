from game_contracts.runner_server_abc import RunnerServerABC


class CloudRunnerServer(RunnerServerABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        # Implement the logic to start the cloud runner server
        pass

    def stop(self):
        # Implement the logic to stop the cloud runner server
        pass

    def run(self):
        # Implement the logic to run the cloud runner server
        pass
