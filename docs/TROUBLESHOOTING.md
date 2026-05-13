# Troubleshooting: game-framework-runners

## Local Setup

### `ModuleNotFoundError: No module named 'game_contracts'`

**Symptom:** Import error when running any runner or test.

**Cause:** The `game-contracts` package has not been built, or the dist file is missing/stale.

**Fix:**
```bash
cd ../game-framework-contracts
make build
cd ../game-framework-runners
pipenv install
```

---

### `pipenv install` fails with "Could not find a version that satisfies the requirement game-contracts"

**Symptom:** Pipenv cannot resolve the local file dependency.

**Cause:** The path `../game-framework-contracts/dist/game_contracts-0.1.0.tar.gz` does not exist.

**Fix:** Build the contracts package first (see above). Ensure both repos are sibling directories.

---

### `ModuleNotFoundError: No module named 'runners'`

**Symptom:** `from runners.local.client_runner import LocalRunnerClient` fails.

**Cause:** The package is not installed or the virtual environment is not active.

**Fix:**
```bash
pipenv shell
pip install -e .
```

---

## Runtime Errors

### `requests.exceptions.ConnectionError` or `httpx.ConnectError`

**Symptom:** Any runner method raises a connection error.

**Cause:** The app-server is not running, or the `fastapi_url` points to the wrong address/port.

**Fix:** Start the app-server (see `game-framework-app-server` repo) and verify the URL passed to the runner constructor.

---

### `ValueError: Signature verification failed — rejecting message.`

**Symptom:** `LocalRunnerServer.poll_for_message_from_client` raises this error.

**Cause:** The HMAC secret in `LocalRunnerClient` does not match the one in `LocalRunnerServer`.

**Fix:** Ensure both client and server are instantiated with the same `secret` value in `HMACSigner`. Both currently default to `"your_secret_key"` — confirm neither has been changed independently.

---

### `ValueError: Replay detected: sequence number is stale.`

**Symptom:** Server rejects a message with a stale sequence number.

**Cause:** A message with an equal or lower `seq` value than the last accepted message was received. This can happen if the client is reset without resetting the server's sequence tracker.

**Fix:** Restart both client and server instances together, or reset `sequence_number` on both sides to the same value.

---

### `ValueError: Invalid client ID <id> for game <id>`

**Symptom:** Server rejects a message with an invalid client ID.

**Cause:** The `client_id` in the envelope is not in the list returned by `GameMetadataHandler.get_valid_players`.

**Fix (local dev):** The local metadata handler returns `["player_1", "player_2"]`. Ensure the client is using one of these IDs, or update the handler for your test scenario.

---

### All `safe_get` / `safe_post` calls fail after 3 attempts

**Symptom:** `Exception: Function <name> failed after 3 attempts.` logged.

**Cause:** The app-server is returning a non-200 status code, or is unreachable.

**Fix:** Check the app-server logs for errors. If the server is returning a non-200 status intentionally, pass `expected_status` to `safe_get`/`safe_post` or handle the response before using the wrappers.

---

## Integration

### Cloud runners do nothing / return `None`

**Symptom:** `CloudRunnerClient` or `CloudRunnerServer` methods return nothing or raise `TypeError`.

**Cause:** Cloud runners are stubs — all method bodies are `...` (ellipsis).

**Fix:** Use `local/` runners for all current development. Cloud implementations are not yet complete.
