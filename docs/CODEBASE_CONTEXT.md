# Codebase Context: game-framework-runners

## Purpose
Transport layer between game UI and game logic core. Implements `RunnerClientABC`, `RunnerServerABC`, and `GameMetadataHandlerABC` from `game-framework-contracts`.

## Package
- Package name: `game-runners`
- Install root: `src/`; importable as `runners.*`
- Python >= 3.12

## Folder Structure
```
src/runners/
├── local/
│   ├── client_runner.py     # LocalRunnerClient — full HTTP implementation
│   ├── server_runner.py     # LocalRunnerServer — full HTTP implementation
│   └── metadata_runner.py   # GameMetadataHandler — in-memory, placeholder persistence
├── cloud/
│   ├── client_runner.py     # CloudRunnerClient — stub only
│   ├── server_runner.py     # CloudRunnerServer — stub only
│   └── metadata_runner.py   # GameMetadataHandler — stub only
└── utils/
    ├── hmacsigner.py        # HMACSigner: sign(envelope) → str, verify(envelope, sig) → bool
    └── retries.py           # retry_on_exception decorator; safe_get(url, params); safe_post(url, payload)
```

## Key Symbols

| Symbol | File | Notes |
|---|---|---|
| `LocalRunnerClient` | `local/client_runner.py` | Implements `RunnerClientABC`; connects to FastAPI at `http://localhost:8000` |
| `LocalRunnerServer` | `local/server_runner.py` | Implements `RunnerServerABC`; validates HMAC + seq + player on inbound messages |
| `GameMetadataHandler` (local) | `local/metadata_runner.py` | Implements `GameMetadataHandlerABC`; uses `@lru_cache` for `get_valid_players` |
| `GameMetadataHandler` (cloud) | `cloud/metadata_runner.py` | All methods return empty / pass — not implemented |
| `HMACSigner` | `utils/hmacsigner.py` | HMAC-SHA256; signs `client_id + game_id + seq + payload` |
| `safe_get` / `safe_post` | `utils/retries.py` | 3 retries, exponential backoff (1s, 2s, 4s) |
| `retry_on_exception` | `utils/retries.py` | Decorator; configurable `max_attempts`, `backoff_strategy`, `allowed_exceptions` |

## Contracts Implemented
From `game-framework-contracts`:
- `RunnerClientABC`: `poll_for_server_response()`, `post_to_server(game_id, client_id, payload)`, `get_games_for_player(game_configs)`, `setup_new_game(game_configs)`, `initialize_server(params)`
- `RunnerServerABC`: `poll_for_message_from_client(game_id)`, `push_message_to_client(game_id, payload)`, `get_game_state(game_id)`
- `GameMetadataHandlerABC`: `get_valid_players(game_id)`, `get_game_state(game_id)`, `get_games_by_player(player_id)`, `setup_new_game_id(game_configs)`, `update_game_state(game_id, game_state)`, `preprocess_action(action, player_id)`, `filter_state_for_player(state, player_id)`

## Message Model
`MessageEnvelope` (Pydantic, from `game-contracts`):
- `game_id: str`, `client_id: str`, `source: MessageSource`, `seq: int`, `signature: str | None`, `payload: dict`
- `LocalRunnerServer` validates: player in valid list → HMAC signature → seq > last seen

## Patterns
- Runners import `HMACSigner` and `safe_get`/`safe_post` from `runners.utils`
- `LocalRunnerClient.post_to_server` builds the envelope locally and signs it before posting
- `LocalRunnerClient.poll_for_server_response` is `async`; all others are synchronous
- Local runners default to `http://localhost:8000` and `player_id="player1"`; override via constructor

## Do Not
- Do not treat `cloud/` runners as functional — they are all stubs (`...` bodies)
- Do not expect `GameMetadataHandler.get_valid_players` to hit a database; it returns a hardcoded list in the local implementation
- Do not use `LocalRunnerClient.post_to_server`'s `payload` parameter — the current implementation ignores it and hardcodes `{"move": "play_card", "card": "Surge"}` (known placeholder)
- Do not call `safe_get`/`safe_post` directly with a non-200 expected status without passing `expected_status`
- Do not rely on `update_game_state` in the local metadata handler for persistence in production — it writes to a flat JSON file in the working directory
