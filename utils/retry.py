#!/usr/bin/env python3
"""
ABOUTME: Production-grade retry decorator with exponential backoff and jitter
ABOUTME: Provides resilient error recovery for network operations and transient failures

This module implements a robust retry mechanism following industry best practices:
- Exponential backoff to avoid overwhelming failing services
- Jitter to prevent thundering herd problem
- Configurable max attempts and delays
- Type-safe with full typing support
- Logging integration for observability

Design Principles:
- SOLID: Single Responsibility (retry logic only)
- DRY: Reusable across all scrapers and API calls
- Production-grade: Handles transient failures gracefully
"""

import time
import random
import functools
from typing import TypeVar, Callable, Optional, Type, Tuple, Any
from utils.logging_config import get_logger

logger = get_logger(__name__)

# Type variable for preserving function signature
T = TypeVar('T')


def exponential_backoff_with_jitter(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True
) -> float:
    """
    Calculate delay with exponential backoff and optional jitter.

    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay in seconds (default: 1.0)
        max_delay: Maximum delay in seconds (default: 60.0)
        jitter: Add randomization to prevent thundering herd (default: True)

    Returns:
        Delay in seconds before next retry

    Example:
        >>> exponential_backoff_with_jitter(0)  # ~1s
        >>> exponential_backoff_with_jitter(1)  # ~2s
        >>> exponential_backoff_with_jitter(2)  # ~4s
        >>> exponential_backoff_with_jitter(3)  # ~8s
    """
    # Calculate exponential delay: base_delay * 2^attempt
    delay = min(base_delay * (2 ** attempt), max_delay)

    # Add jitter (randomize ±25% to prevent thundering herd)
    if jitter:
        jitter_range = delay * 0.25
        delay = delay + random.uniform(-jitter_range, jitter_range)

    # Ensure non-negative
    return max(0.0, delay)


def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to retry a function with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts (default: 3)
        base_delay: Initial delay in seconds (default: 1.0)
        max_delay: Maximum delay in seconds (default: 60.0)
        exceptions: Tuple of exception types to catch (default: all)
        on_retry: Optional callback on retry (exception, attempt) -> None

    Returns:
        Decorated function with retry logic

    Example:
        @retry(max_attempts=3, base_delay=2.0, exceptions=(requests.Timeout,))
        def fetch_url(url: str) -> str:
            response = requests.get(url, timeout=10)
            return response.text

    Raises:
        The last exception if all retries are exhausted
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Optional[Exception] = None

            for attempt in range(max_attempts):
                try:
                    # Attempt the function call
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    # If this was the last attempt, re-raise
                    if attempt == max_attempts - 1:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {str(e)}",
                            exc_info=True
                        )
                        raise

                    # Calculate backoff delay
                    delay = exponential_backoff_with_jitter(
                        attempt, base_delay, max_delay
                    )

                    # Log retry
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {str(e)}"
                        f" - Retrying in {delay:.2f}s..."
                    )

                    # Call custom retry callback if provided
                    if on_retry:
                        on_retry(e, attempt + 1)

                    # Wait before retrying
                    time.sleep(delay)

            # Should never reach here, but type checker needs it
            if last_exception:
                raise last_exception

            raise RuntimeError(f"{func.__name__}: Unreachable code reached")

        return wrapper
    return decorator


def retry_on_network_error(
    max_attempts: int = 3,
    base_delay: float = 2.0,
    max_delay: float = 30.0
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Specialized retry decorator for network operations.

    Catches common network exceptions:
    - requests.Timeout
    - requests.ConnectionError
    - requests.HTTPError (5xx only)

    Args:
        max_attempts: Maximum number of attempts (default: 3)
        base_delay: Initial delay in seconds (default: 2.0)
        max_delay: Maximum delay in seconds (default: 30.0)

    Returns:
        Decorated function with retry logic

    Example:
        @retry_on_network_error(max_attempts=5)
        def scrape_website(url: str) -> str:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
    """
    import requests

    def should_retry_http_error(exc: requests.HTTPError) -> bool:
        """Check if HTTP error is retriable (5xx only)."""
        if exc.response is None:
            return True
        # Retry 5xx server errors, not 4xx client errors
        return 500 <= exc.response.status_code < 600

    def custom_exception_filter(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)

                except (requests.Timeout, requests.ConnectionError) as e:
                    # Always retry timeouts and connection errors
                    if attempt == max_attempts - 1:
                        logger.error(f"Network error after {max_attempts} attempts: {e}")
                        raise

                    delay = exponential_backoff_with_jitter(attempt, base_delay, max_delay)
                    logger.warning(
                        f"Network error (attempt {attempt + 1}/{max_attempts}): {e} "
                        f"- Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)

                except requests.HTTPError as e:
                    # Only retry 5xx errors
                    if not should_retry_http_error(e) or attempt == max_attempts - 1:
                        raise

                    delay = exponential_backoff_with_jitter(attempt, base_delay, max_delay)
                    logger.warning(
                        f"HTTP {e.response.status_code if e.response else 'N/A'} error "
                        f"(attempt {attempt + 1}/{max_attempts}) - Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)

            raise RuntimeError(f"{func.__name__}: Unreachable code reached")

        return wrapper
    return custom_exception_filter


# Example usage and testing
if __name__ == '__main__':
    import requests

    # Test basic retry
    @retry(max_attempts=3, base_delay=0.1)
    def unreliable_function(fail_count: int) -> str:
        """Simulates a function that fails N times before succeeding."""
        if not hasattr(unreliable_function, 'attempts'):
            unreliable_function.attempts = 0

        unreliable_function.attempts += 1
        if unreliable_function.attempts <= fail_count:
            raise ValueError(f"Simulated failure {unreliable_function.attempts}")

        return "Success!"

    # Test network retry
    @retry_on_network_error(max_attempts=3, base_delay=0.1)
    def fetch_url(url: str) -> str:
        """Fetch URL with retry logic."""
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text[:100]

    # Run tests
    print("Testing retry decorator...")

    try:
        result = unreliable_function(2)
        print(f"✅ Result after retries: {result}")
    except Exception as e:
        print(f"❌ Failed: {e}")

    try:
        html = fetch_url("https://example.com")
        print(f"✅ Fetched: {html[:50]}...")
    except Exception as e:
        print(f"❌ Failed: {e}")

    print("\nDelay calculations:")
    for i in range(5):
        delay = exponential_backoff_with_jitter(i, base_delay=1.0, jitter=False)
        print(f"  Attempt {i}: {delay:.2f}s")
