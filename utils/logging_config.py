#!/usr/bin/env python3
"""
ABOUTME: Centralized logging configuration for OpenDraft system
ABOUTME: Provides consistent logging format, levels, and handlers across all modules

Usage:
    from utils.logging_config import get_logger

    logger = get_logger(__name__)
    logger.info("Starting citation research...")
    logger.warning("API rate limit approaching")
    logger.error("Failed to scrape title", exc_info=True)

Features:
- Console and file logging
- Color-coded output for terminal
- Structured format with timestamps
- Automatic log rotation (10MB per file, 5 backups)
- Module-specific loggers with hierarchy
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
import sys


# Log directory (created if doesn't exist)
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Log file paths
MAIN_LOG_FILE = LOG_DIR / "opendraft.log"
ERROR_LOG_FILE = LOG_DIR / "errors.log"

# Log format
LOG_FORMAT = "%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ANSI color codes for terminal output
COLORS = {
    'DEBUG': '\033[36m',      # Cyan
    'INFO': '\033[32m',       # Green
    'WARNING': '\033[33m',    # Yellow
    'ERROR': '\033[31m',      # Red
    'CRITICAL': '\033[35m',   # Magenta
    'RESET': '\033[0m'        # Reset
}


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds color to console output.

    Colors:
    - DEBUG: Cyan
    - INFO: Green
    - WARNING: Yellow
    - ERROR: Red
    - CRITICAL: Magenta
    """

    def format(self, record):
        """Add color codes to log level in terminal output."""
        levelname = record.levelname
        if levelname in COLORS:
            record.levelname = f"{COLORS[levelname]}{levelname}{COLORS['RESET']}"
        return super().format(record)


def setup_logging(
    level: int = logging.INFO,
    console_output: bool = True,
    file_output: bool = True
) -> None:
    """
    Configure root logger with console and file handlers.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Enable console logging
        file_output: Enable file logging

    Example:
        # Development mode (verbose console, no files)
        setup_logging(level=logging.DEBUG, file_output=False)

        # Production mode (quiet console, detailed files)
        setup_logging(level=logging.WARNING, console_output=True, file_output=True)
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture all levels, filter in handlers

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Console handler (color-coded, INFO+)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = ColoredFormatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

    # File handler (all logs, rotating)
    if file_output:
        # Main log file (all levels)
        file_handler = logging.handlers.RotatingFileHandler(
            MAIN_LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

        # Error log file (ERROR+ only)
        error_handler = logging.handlers.RotatingFileHandler(
            ERROR_LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        root_logger.addHandler(error_handler)


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Module name (typically __name__)
        level: Optional logging level override

    Returns:
        Logger instance configured with module name

    Example:
        # In utils/deduplicate_citations.py
        logger = get_logger(__name__)
        logger.info("Starting deduplication...")

        # In tests/test_citations.py (debug mode)
        logger = get_logger(__name__, level=logging.DEBUG)
    """
    logger = logging.getLogger(name)

    # Set level if specified
    if level is not None:
        logger.setLevel(level)

    return logger


# Initialize logging on module import (can be reconfigured later)
setup_logging(
    level=logging.INFO,
    console_output=True,
    file_output=True
)


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == '__main__':
    """Test logging configuration with sample messages."""

    print("Testing logging configuration...\n")

    # Get logger for this module
    logger = get_logger(__name__)

    # Test all log levels
    logger.debug("Debug message - detailed execution info")
    logger.info("Info message - normal operation")
    logger.warning("Warning message - potential issue")
    logger.error("Error message - operation failed")
    logger.critical("Critical message - system failure")

    # Test structured logging
    logger.info(
        "Citation scraped successfully",
        extra={
            'citation_id': 'cite_042',
            'source': 'Crossref',
            'title': 'Example Paper'
        }
    )

    # Test exception logging
    try:
        raise ValueError("Simulated error for testing")
    except Exception as e:
        logger.error("Exception occurred during test", exc_info=True)

    print(f"\n✅ Logs written to:")
    print(f"   Main log: {MAIN_LOG_FILE}")
    print(f"   Error log: {ERROR_LOG_FILE}")
