from game_contracts.metadata_handler_abc import GameMetadataHandlerABC


class GameMetadataHandler(GameMetadataHandlerABC):
    def __init__(self) -> None:
        pass

    def get_game_state(self, game_id: str) -> dict:
        return {}

    def get_games_by_player(self, player_id: str) -> dict:
        return {}

    def setup_new_game_id(self, game_configs: dict) -> dict:
        return {}

    def update_game_state(self, game_id: str, game_state: dict) -> None:
        pass
