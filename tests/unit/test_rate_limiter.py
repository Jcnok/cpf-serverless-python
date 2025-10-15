import time
import unittest.mock

from src.core.utils.rate_limiter import (
    is_rate_limited,
    RATE_LIMIT_COUNT,
    RATE_LIMIT_WINDOW,
)


def test_first_request_not_limited():
    ip = "10.0.0.1"
    assert is_rate_limited(ip) is False


def test_multiple_requests_within_limit():
    ip = "10.0.0.2"
    for _ in range(RATE_LIMIT_COUNT - 1):
        assert is_rate_limited(ip) is False


def test_exceeding_rate_limit():
    ip = "10.0.0.3"
    for _ in range(RATE_LIMIT_COUNT):
        is_rate_limited(ip)
    assert is_rate_limited(ip) is True


def test_rate_limit_resets_after_window():
    ip = "10.0.0.4"
    for _ in range(RATE_LIMIT_COUNT + 1):
        is_rate_limited(ip)
    future_time = time.time() + RATE_LIMIT_WINDOW + 1
    with unittest.mock.patch("time.time", return_value=future_time):
        assert is_rate_limited(ip) is False
