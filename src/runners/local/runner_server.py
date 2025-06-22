import requests
import time
import logging
import functools
from game_contracts.runner_server_abc import RunnerServerABC


def retry_on_exception(
    max_attempts=3,
    backoff_strategy=None,
    allowed_exceptions=(Exception,),
    log_prefix="",
):
    if backoff_strategy is None:
        backoff_strategy = lambda attempt: 2**attempt  # 1s, 2s, 4s

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    last_exception = e
                    delay = backoff_strategy(attempt)
                    logging.warning(
                        f"{log_prefix} Attempt {attempt+1} failed: {e}. Retrying in {delay}s..."
                    )
                    time.sleep(delay)
            logging.error(f"{log_prefix} All {max_attempts} attempts failed.")
            raise Exception(
                f"{log_prefix} Function {func.__name__} failed after {max_attempts} attempts. Last exception: {last_exception}"
            )

        return wrapper

    return decorator


@retry_on_exception(log_prefix="GET /poll")
def safe_get(url: str, params: dict, expected_status=200):
    response = requests.get(url, params=params)
    if response.status_code != expected_status:
        raise requests.HTTPError(f"Status {response.status_code}")
    return response


@retry_on_exception(log_prefix="POST /push")
def safe_post(url: str, payload: dict, expected_status=200):
    response = requests.post(url, json=payload)
    if response.status_code != expected_status:
        raise requests.HTTPError(f"Status {response.status_code}")
    return response


class LocalRunnerServer(RunnerServerABC):
    def __init__(self, fastapi_url="http://localhost:8000"):
        self.fastapi_url = fastapi_url

    def poll_for_message_from_client(self, game_id: str) -> dict:
        """Poll the FastAPI server for incoming messages from client"""
        while True:
            try:
                res = safe_get(
                    f"{self.fastapi_url}/poll_from_server", params={"game_id": game_id}
                )
                if res.status_code == 200:
                    return res.json()
            except Exception as e:
                print("Error polling for message:", e)
            time.sleep(0.5)

    def push_message_to_client(self, game_id: str, payload: dict) -> None:
        """Send a message to a specific client (they poll for it)"""
        res = safe_post(
            f"{self.fastapi_url}/push_to_client",
            payload=payload,
        )
        res.raise_for_status()

    def get_game_state(self, game_id: str) -> dict:
        """Fetch metadata for a specific game"""
        res = safe_get(f"{self.fastapi_url}/game_state", params={"game_id": game_id})
        if res.status_code == 200:
            return res.json()
        else:
            return {}
