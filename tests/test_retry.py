#!/usr/bin/env python3
"""
Unit tests for retry mechanism (utils/retry.py)

Tests cover:
- Basic retry logic
- Exponential backoff calculation
- Network error handling
- Custom exception filtering
- Jitter randomization
- Max attempts enforcement
"""

import pytest
import time
from unittest.mock import Mock, patch
import requests
from utils.retry import (
    exponential_backoff_with_jitter,
    retry,
    retry_on_network_error
)


# ============================================================
# Test: exponential_backoff_with_jitter
# ============================================================

def test_exponential_backoff_without_jitter():
    """Test exponential backoff calculation without jitter."""
    assert exponential_backoff_with_jitter(0, base_delay=1.0, jitter=False) == 1.0
    assert exponential_backoff_with_jitter(1, base_delay=1.0, jitter=False) == 2.0
    assert exponential_backoff_with_jitter(2, base_delay=1.0, jitter=False) == 4.0
    assert exponential_backoff_with_jitter(3, base_delay=1.0, jitter=False) == 8.0
    assert exponential_backoff_with_jitter(4, base_delay=1.0, jitter=False) == 16.0


def test_exponential_backoff_with_max_delay():
    """Test that max_delay is enforced."""
    # 2^10 = 1024, but max_delay should cap it at 60
    delay = exponential_backoff_with_jitter(10, base_delay=1.0, max_delay=60.0, jitter=False)
    assert delay == 60.0


def test_exponential_backoff_with_jitter_randomization():
    """Test that jitter adds randomization."""
    delays = [
        exponential_backoff_with_jitter(2, base_delay=1.0, jitter=True)
        for _ in range(10)
    ]

    # All delays should be near 4.0 but vary due to jitter
    assert all(3.0 <= d <= 5.0 for d in delays)

    # Should have variation (not all identical)
    assert len(set(delays)) > 1


def test_exponential_backoff_non_negative():
    """Test that delays are always non-negative."""
    for attempt in range(10):
        delay = exponential_backoff_with_jitter(attempt, base_delay=1.0)
        assert delay >= 0.0


# ============================================================
# Test: @retry decorator
# ============================================================

def test_retry_succeeds_first_attempt():
    """Test that retry decorator doesn't interfere with successful calls."""
    call_count = 0

    @retry(max_attempts=3)
    def successful_function():
        nonlocal call_count
        call_count += 1
        return "success"

    result = successful_function()
    assert result == "success"
    assert call_count == 1  # Should only call once


def test_retry_succeeds_after_failures():
    """Test that retry decorator retries until success."""
    call_count = 0

    @retry(max_attempts=3, base_delay=0.01)  # Fast retry for testing
    def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Simulated failure")
        return "success"

    result = flaky_function()
    assert result == "success"
    assert call_count == 3  # Should call 3 times total


def test_retry_exhausts_attempts():
    """Test that retry decorator raises after max_attempts."""
    call_count = 0

    @retry(max_attempts=3, base_delay=0.01)
    def always_fails():
        nonlocal call_count
        call_count += 1
        raise ValueError("Always fails")

    with pytest.raises(ValueError, match="Always fails"):
        always_fails()

    assert call_count == 3  # Should attempt 3 times


def test_retry_only_catches_specified_exceptions():
    """Test that retry only catches specified exception types."""
    call_count = 0

    @retry(max_attempts=3, base_delay=0.01, exceptions=(ValueError,))
    def raises_type_error():
        nonlocal call_count
        call_count += 1
        raise TypeError("Not caught")

    # Should raise immediately (not retried)
    with pytest.raises(TypeError, match="Not caught"):
        raises_type_error()

    assert call_count == 1  # Should not retry


def test_retry_with_custom_callback():
    """Test that on_retry callback is called."""
    call_count = 0
    callback_calls = []

    def custom_callback(exception, attempt):
        callback_calls.append((str(exception), attempt))

    @retry(max_attempts=3, base_delay=0.01, on_retry=custom_callback)
    def fails_twice():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError(f"Failure {call_count}")
        return "success"

    result = fails_twice()
    assert result == "success"
    assert len(callback_calls) == 2  # Called twice before success
    assert callback_calls[0] == ("Failure 1", 1)
    assert callback_calls[1] == ("Failure 2", 2)


def test_retry_backoff_timing():
    """Test that retry decorator actually waits between attempts."""
    start_time = time.time()
    call_count = 0

    @retry(max_attempts=3, base_delay=0.1, max_delay=1.0)
    def fails_twice():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Retry me")
        return "success"

    result = fails_twice()
    elapsed = time.time() - start_time

    # Should wait ~0.1s + ~0.2s = ~0.3s total (with jitter)
    assert elapsed >= 0.2  # At least some delay
    assert elapsed < 1.0   # But not too long


# ============================================================
# Test: @retry_on_network_error decorator
# ============================================================

def test_retry_on_network_error_timeout():
    """Test that retry_on_network_error retries timeouts."""
    call_count = 0

    @retry_on_network_error(max_attempts=3, base_delay=0.01)
    def timeout_once():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise requests.Timeout("Simulated timeout")
        return "success"

    result = timeout_once()
    assert result == "success"
    assert call_count == 2


def test_retry_on_network_error_connection_error():
    """Test that retry_on_network_error retries connection errors."""
    call_count = 0

    @retry_on_network_error(max_attempts=3, base_delay=0.01)
    def connection_error_once():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise requests.ConnectionError("Simulated connection error")
        return "success"

    result = connection_error_once()
    assert result == "success"
    assert call_count == 2


def test_retry_on_network_error_5xx_retry():
    """Test that retry_on_network_error retries 5xx errors."""
    call_count = 0

    @retry_on_network_error(max_attempts=3, base_delay=0.01)
    def server_error_once():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            response = Mock()
            response.status_code = 503
            raise requests.HTTPError("Service unavailable", response=response)
        return "success"

    result = server_error_once()
    assert result == "success"
    assert call_count == 2


def test_retry_on_network_error_4xx_no_retry():
    """Test that retry_on_network_error does NOT retry 4xx errors."""
    call_count = 0

    @retry_on_network_error(max_attempts=3, base_delay=0.01)
    def client_error():
        nonlocal call_count
        call_count += 1
        response = Mock()
        response.status_code = 404
        raise requests.HTTPError("Not found", response=response)

    # Should raise immediately (not retried)
    with pytest.raises(requests.HTTPError, match="Not found"):
        client_error()

    assert call_count == 1  # Should not retry


def test_retry_on_network_error_exhausts_attempts():
    """Test that retry_on_network_error raises after max_attempts."""
    call_count = 0

    @retry_on_network_error(max_attempts=3, base_delay=0.01)
    def always_timeout():
        nonlocal call_count
        call_count += 1
        raise requests.Timeout("Always times out")

    with pytest.raises(requests.Timeout, match="Always times out"):
        always_timeout()

    assert call_count == 3


# ============================================================
# Integration Tests
# ============================================================

def test_retry_integration_with_real_function():
    """Test retry decorator with a more realistic scenario."""
    attempts = []

    @retry(max_attempts=5, base_delay=0.01, exceptions=(ValueError, RuntimeError))
    def unstable_api_call(should_succeed_on_attempt: int):
        attempt_num = len(attempts) + 1
        attempts.append(attempt_num)

        if attempt_num < should_succeed_on_attempt:
            if attempt_num % 2 == 0:
                raise ValueError(f"Attempt {attempt_num}: Validation error")
            else:
                raise RuntimeError(f"Attempt {attempt_num}: Runtime error")

        return {"status": "success", "attempts": attempt_num}

    # Should succeed on 4th attempt
    result = unstable_api_call(4)
    assert result["status"] == "success"
    assert result["attempts"] == 4
    assert len(attempts) == 4


def test_retry_preserves_return_type():
    """Test that retry decorator preserves return types."""
    @retry(max_attempts=3)
    def returns_dict() -> dict:
        return {"key": "value"}

    @retry(max_attempts=3)
    def returns_list() -> list:
        return [1, 2, 3]

    @retry(max_attempts=3)
    def returns_int() -> int:
        return 42

    assert isinstance(returns_dict(), dict)
    assert isinstance(returns_list(), list)
    assert isinstance(returns_int(), int)


# ============================================================
# Run tests
# ============================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
