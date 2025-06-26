import json

from game_contracts.metadata_handler_abc import GameMetadataHandlerABC
from functools import lru_cache


class GameMetadataHandler(GameMetadataHandlerABC):
    def __init__(self) -> None:
        pass

    @lru_cache(maxsize=128)
    def get_valid_players(self, game_id: str) -> list:
        """Placeholder for retrieving valid players for a game."""
        return ["player_1", "player_2"]

    def get_game_state(self, game_id: str) -> dict:
        return {}

    def get_games_by_player(self, player_id: str) -> dict:
        """Placeholder for retrieving games by player ID."""
        test_games = {
            "player_1": {
                "12345": {"game_details": "stuff"},
                "67890": {"game_details": "stuff"},
            },
            "player_2": {"54321": {"game_details": "stuff"}},
        }
        return test_games.get(player_id, {})

    def setup_new_game_id(self, game_configs: dict) -> dict:
        """Placeholder for setting up a new game ID."""
        return {"game_id": "12345", "queue_id": "67890"}

    def update_game_state(self, game_id: str, game_state: dict) -> None:
        """Placeholder for updating the game state."""
        with open(f"{game_id}.json", "w") as f:
            json.dump(game_state, f)

    def preprocess_action(self, action: str, player_id: str):
        """Adjust or validate action before logic sees it."""
        return action

    def filter_state_for_player(self, state: str, player_id: str):
        """Hide private info, etc."""
        return state
