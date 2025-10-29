#!/usr/bin/env python3
"""
ABOUTME: Centralized configuration management for Academic Thesis AI
ABOUTME: Single source of truth for all settings, models, and environment variables
"""

import os
from dataclasses import dataclass, field
from typing import Literal, Optional
from pathlib import Path


# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional - will use system environment variables
    pass


@dataclass
class ModelConfig:
    """
    Model configuration with sensible defaults.

    Supports Gemini models with configurable parameters.
    """
    provider: Literal['gemini', 'claude', 'openai'] = 'gemini'
    model_name: str = field(default_factory=lambda: os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'))
    temperature: float = 0.7
    max_output_tokens: Optional[int] = None

    def __post_init__(self):
        """Validate model configuration."""
        valid_models = [
            'gemini-2.5-flash',
            'gemini-2.5-pro',
            'gemini-2.0-flash-exp',  # Legacy support
            'gemini-1.5-flash',
            'gemini-1.5-pro'
        ]
        if self.provider == 'gemini' and self.model_name not in valid_models:
            raise ValueError(
                f"Invalid Gemini model: {self.model_name}. "
                f"Valid options: {', '.join(valid_models)}"
            )


@dataclass
class ValidationConfig:
    """Configuration for validation agents (Skeptic, Verifier, Referee)."""
    use_pro_model: bool = field(default_factory=lambda: os.getenv('USE_PRO_FOR_VALIDATION', 'false').lower() == 'true')
    pro_model_name: str = 'gemini-2.5-pro'
    validate_per_section: bool = True  # Always validate each section independently

    def get_validation_model(self, base_model: str) -> str:
        """Return appropriate model for validation tasks."""
        return self.pro_model_name if self.use_pro_model else base_model


@dataclass
class PathConfig:
    """Path configuration for outputs and prompts."""
    project_root: Path = field(default_factory=lambda: Path(__file__).parent)
    output_dir: Path = field(default_factory=lambda: Path('tests/outputs'))
    prompts_dir: Path = field(default_factory=lambda: Path('prompts'))

    def __post_init__(self):
        """Ensure paths are absolute."""
        self.output_dir = self.project_root / self.output_dir
        self.prompts_dir = self.project_root / self.prompts_dir


@dataclass
class AppConfig:
    """
    Application-wide configuration.

    Single source of truth for all settings across the application.
    Follows SOLID principles and provides type-safe access to configuration.
    """
    # API Keys
    google_api_key: str = field(default_factory=lambda: os.getenv('GOOGLE_API_KEY', ''))
    anthropic_api_key: str = field(default_factory=lambda: os.getenv('ANTHROPIC_API_KEY', ''))
    openai_api_key: str = field(default_factory=lambda: os.getenv('OPENAI_API_KEY', ''))

    # Sub-configurations
    model: ModelConfig = field(default_factory=ModelConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    paths: PathConfig = field(default_factory=PathConfig)

    # Citation and paper settings
    citation_style: str = field(default_factory=lambda: os.getenv('CITATION_STYLE', 'apa'))
    ai_detection_threshold: float = field(default_factory=lambda: float(os.getenv('AI_DETECTION_THRESHOLD', '0.20')))

    def __post_init__(self):
        """Validate configuration on initialization."""
        if self.model.provider == 'gemini' and not self.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is required for Gemini models. "
                "Set it in .env file or environment."
            )

        if self.model.provider == 'claude' and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY required for Claude models")

        if self.model.provider == 'openai' and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY required for OpenAI models")


# Global configuration instance - single source of truth
config = AppConfig()


def get_config() -> AppConfig:
    """
    Get the global configuration instance.

    Returns:
        AppConfig: The application configuration
    """
    return config


def update_model(model_name: str) -> None:
    """
    Update the model name at runtime.

    Args:
        model_name: New model name to use
    """
    global config
    config.model.model_name = model_name
    config.model.__post_init__()  # Re-validate


if __name__ == '__main__':
    # Configuration validation on import
    print(f"✅ Configuration loaded successfully")
    print(f"Model: {config.model.model_name}")
    print(f"Provider: {config.model.provider}")
    print(f"Validation per section: {config.validation.validate_per_section}")
    print(f"Output directory: {config.paths.output_dir}")
