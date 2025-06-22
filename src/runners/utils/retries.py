import functools
import logging
import time

import requests


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
