# Local Development: game-framework-runners

## Prerequisites

- Python 3.12+
- [Pipenv](https://pipenv.pypa.io/) (`pip install pipenv`)
- The `game-framework-contracts` repo cloned as a sibling directory (i.e., `../game-framework-contracts/`)
- The `game-framework-app-server` running locally if you need end-to-end testing

## Step 1 — Build the contracts package

`game-runners` depends on `game-contracts` from a local dist file. Build it first:

```bash
cd ../game-framework-contracts
make build
```

This produces `dist/game_contracts-0.1.0.tar.gz`, which is referenced by the Pipfile.

## Step 2 — Install dependencies

```bash
cd game-framework-runners
pipenv install
```

For development tools (formatter, build):

```bash
pipenv install --dev
```

## Step 3 — Activate the environment

```bash
pipenv shell
```

## Step 4 — Install the package in editable mode (optional)

If you need `runners.*` importable outside of `pipenv run`, install the package:

```bash
pip install -e .
```

## Running Tests

There are no tests in this repo yet. Once tests are added, run them with:

```bash
pipenv run pytest
```

## Code Formatting

```bash
pipenv run black src/
pipenv run isort src/
```

## Building the Package

```bash
pipenv run python -m build
```

Output goes to `dist/`.

## Environment Variables

No environment variables are required for local development. The default runner configuration uses:

| Setting | Default | Set in |
|---|---|---|
| App server URL | `http://localhost:8000` | Constructor parameter |
| Player ID | `player1` | Constructor parameter |
| HMAC secret | `"your_secret_key"` | Constructor (hardcoded placeholder — change before production use) |

## End-to-End Local Testing

To exercise the runners against a real app-server:

1. Start the app-server: see `game-framework-app-server` repo
2. Import and instantiate the local runner in a script or REPL:

```python
from runners.local.client_runner import LocalRunnerClient

client = LocalRunnerClient(fastapi_url="http://localhost:8000", player_id="player1")
games = client.get_games_for_player({"player_id": "player1"})
print(games)
```

## Notes

- The `cloud/` runners are stubs and will raise `NotImplementedError` if called — they are not usable for local testing.
- The local metadata handler writes game state to `{game_id}.json` in the current working directory.
