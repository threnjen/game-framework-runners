from game_contracts.runner_client_abc import RunnerClientABC
import requests
import time


class LocalRunnerClient(RunnerClientABC):

    def __init__(self, player_id) -> None:
        super().__init__()
        self.player_id = "player_1"

    def poll_for_input(self) -> None:

        while True:
            res = requests.get(
                "http://localhost:8000/get_available_actions",
                params={"player_id": self.player_id},
            )
            actions = res.json().get("available_actions", [])
            if actions:
                break
            time.sleep(1)
        return actions

    def request_user_action(self, actions) -> str:
        print(f"Available actions: {actions}")
        choice = input("Choose action: ")
        while choice not in actions:
            choice = input("Invalid. Choose again: ")

    def post_message_to_server(self, choice) -> None:
        requests.post(
            f"http://localhost:8000/post_action",
            params={"player_id": self.player_id},
            json=choice,
        )


if __name__ == "__main__":
    player_id = "player_1"

    runner_client = LocalRunnerClient(player_id)

    while True:
        actions = runner_client.poll_for_input()
        choice = runner_client.request_user_action(actions)
        response = runner_client.push_response(choice)
