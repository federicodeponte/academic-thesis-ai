"""
ABOUTME: Configuration package for academic thesis AI system
ABOUTME: Provides concurrency settings and rate limiting configuration
"""

from config.concurrency_config import get_concurrency_config

__all__ = ['get_concurrency_config']
