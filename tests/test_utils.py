#!/usr/bin/env python3
"""
ABOUTME: Shared test utilities for all test scripts (DRY principle)
ABOUTME: Provides reusable functions for model setup, prompt loading, and agent execution
"""

import sys
import time
import logging
from pathlib import Path
from typing import Optional, Callable, Tuple, List, TYPE_CHECKING, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from config import get_config
from utils.output_validators import ValidationResult

# Configure logging
logger = logging.getLogger(__name__)


def setup_model(model_override: Optional[str] = None) -> Any:
    """
    Initialize and return configured Gemini model.

    Args:
        model_override: Optional model name to override config default

    Returns:
        genai.GenerativeModel: Configured Gemini model instance

    Raises:
        ValueError: If API key is missing or model name is invalid
    """
    config = get_config()

    if not config.google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Set it in .env file or environment variables."
        )

    genai.configure(api_key=config.google_api_key)  # type: ignore[attr-defined]

    model_name = model_override or config.model.model_name

    return genai.GenerativeModel(  # type: ignore[attr-defined]
        model_name,
        generation_config={
            'temperature': config.model.temperature,
        }
    )


def load_prompt(prompt_path: str) -> str:
    """
    Load agent prompt from markdown file.

    Args:
        prompt_path: Path to prompt file (relative to project root or absolute)

    Returns:
        str: Content of the prompt file

    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    config = get_config()
    path = Path(prompt_path)

    # If relative path, try relative to project root
    if not path.is_absolute():
        path = config.paths.project_root / path

    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def run_agent(
    model: Any,
    name: str,
    prompt_path: str,
    user_input: str,
    save_to: Optional[Path] = None,
    verbose: bool = True,
    validators: Optional[List[Callable[[str], ValidationResult]]] = None,
    max_retries: int = 3
) -> str:
    """
    Run an AI agent with given prompt and input, with optional validation.

    This function is the core execution layer for all agents in the thesis pipeline.
    It handles LLM interaction, output validation, retries, and file I/O.

    Args:
        model: Configured Gemini model instance
        name: Human-readable name for the agent (for logging)
        prompt_path: Path to agent prompt file
        user_input: User's request/input for the agent
        save_to: Optional path to save output
        verbose: Whether to print progress messages
        validators: Optional list of validation functions to apply to output
        max_retries: Maximum retry attempts if validation fails (default: 3)

    Returns:
        str: Validated agent output text

    Raises:
        Exception: If agent execution fails or validation fails after all retries

    Example:
        >>> from utils.output_validators import ScoutOutputValidator
        >>> output = run_agent(
        ...     model=model,
        ...     name="Scout",
        ...     prompt_path="prompts/01_research/scout.md",
        ...     user_input="Find papers on AI",
        ...     validators=[ScoutOutputValidator.validate]
        ... )
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"🤖 {name}")
        print(f"{'='*70}")

    # Load agent prompt
    agent_prompt = load_prompt(prompt_path)

    # Combine agent prompt with user input
    full_prompt = f"{agent_prompt}\n\n---\n\nUser Request:\n{user_input}"

    logger.debug(f"Agent '{name}': Starting execution")
    logger.debug(f"Prompt length: {len(full_prompt)} chars")
    logger.debug(f"Validators: {len(validators) if validators else 0}")

    # Initialize output variable with explicit type
    output: str = ""

    # Retry loop with exponential backoff
    for attempt in range(max_retries):
        if verbose and attempt > 0:
            print(f"Retry attempt {attempt}/{max_retries}...", end=' ', flush=True)
        elif verbose:
            print("Generating...", end=' ', flush=True)

        start_time = time.time()

        try:
            # Generate LLM response
            response = model.generate_content(full_prompt)
            output = str(response.text)  # Explicit cast for type safety

            logger.debug(f"Agent '{name}': Generated {len(output)} chars in {time.time() - start_time:.1f}s")

            # Validate output if validators provided
            if validators:
                validation_passed = True
                for i, validator in enumerate(validators):
                    logger.debug(f"Agent '{name}': Running validator {i+1}/{len(validators)}")
                    result = validator(output)

                    if not result.is_valid:
                        validation_passed = False
                        logger.warning(
                            f"Agent '{name}': Validation failed on attempt {attempt+1}/{max_retries}: "
                            f"{result.error_message}"
                        )

                        if verbose:
                            print(f"⚠️ Validation failed: {result.error_message}")

                        # If not last attempt, retry with backoff
                        if attempt < max_retries - 1:
                            backoff_seconds = 2 ** attempt  # Exponential: 1s, 2s, 4s
                            logger.debug(f"Agent '{name}': Backing off for {backoff_seconds}s")
                            time.sleep(backoff_seconds)
                            break  # Break validator loop to retry LLM call
                        else:
                            # Last attempt failed - raise error
                            error_msg = (
                                f"Agent '{name}' validation failed after {max_retries} attempts: "
                                f"{result.error_message}"
                            )
                            logger.error(error_msg)
                            raise ValueError(error_msg)
                    else:
                        logger.debug(f"Agent '{name}': Validator {i+1} passed")

                # If all validators passed, break retry loop
                if validation_passed:
                    logger.info(f"Agent '{name}': All {len(validators)} validators passed")
                    break
            else:
                # No validators - success on first attempt
                logger.debug(f"Agent '{name}': No validators, accepting output")
                break

        except Exception as e:
            if verbose:
                print(f"❌ Error")

            logger.error(f"Agent '{name}': Exception on attempt {attempt+1}: {str(e)}")

            # If not last attempt and it's a transient error, retry
            if attempt < max_retries - 1 and _is_transient_error(e):
                backoff_seconds = 2 ** attempt
                logger.debug(f"Agent '{name}': Transient error, retrying after {backoff_seconds}s")
                time.sleep(backoff_seconds)
                continue
            else:
                raise Exception(f"Agent '{name}' execution failed: {str(e)}") from e

    elapsed = time.time() - start_time

    # Save output if path provided
    if save_to:
        try:
            save_to.parent.mkdir(parents=True, exist_ok=True)
            with open(save_to, 'w', encoding='utf-8') as f:
                f.write(output)

            # Verify file was created successfully
            if not save_to.exists():
                raise IOError(f"Output file not created: {save_to}")

            file_size = save_to.stat().st_size
            if file_size == 0:
                raise IOError(f"Output file is empty: {save_to}")

            logger.info(f"Agent '{name}': Saved output to {save_to} ({file_size} bytes)")

        except Exception as e:
            logger.error(f"Agent '{name}': Failed to save output to {save_to}: {str(e)}")
            raise

    if verbose:
        print(f"✅ Done ({elapsed:.1f}s, {len(output):,} chars)")
        if save_to:
            print(f"Saved to: {save_to}")

    return output


def _is_transient_error(error: Exception) -> bool:
    """
    Check if error is transient and worth retrying.

    Args:
        error: Exception to check

    Returns:
        bool: True if error is transient (network, rate limit, etc.)
    """
    error_str = str(error).lower()
    transient_patterns = [
        'timeout',
        'rate limit',
        'quota',
        'service unavailable',
        'temporarily unavailable',
        '429',  # Too Many Requests
        '503',  # Service Unavailable
        '504',  # Gateway Timeout
    ]

    return any(pattern in error_str for pattern in transient_patterns)


def test_agent(
    model: Any,
    name: str,
    prompt_path: str,
    user_input: str,
    validation_fn: Callable[[str], Tuple[bool, str]],
    output_file: Optional[Path] = None
) -> Tuple[bool, str]:
    """
    Test a single agent with validation.

    Args:
        model: Configured Gemini model
        name: Agent name
        prompt_path: Path to agent prompt
        user_input: Test input
        validation_fn: Function to validate output (returns is_valid, message)
        output_file: Optional path to save output

    Returns:
        Tuple[bool, str]: (is_valid, output_text)
    """
    print(f"\n{'='*70}")
    print(f"Testing {name}")
    print(f"{'='*70}")

    try:
        output = run_agent(
            model=model,
            name=name,
            prompt_path=prompt_path,
            user_input=user_input,
            save_to=output_file,
            verbose=False
        )

        # Validate output
        is_valid, message = validation_fn(output)

        print(f"{'✅ PASS' if is_valid else '❌ FAIL'}")
        print(f"Result: {message}")
        print(f"Output length: {len(output)} chars")
        if output_file:
            print(f"Saved to: {output_file}")

        return is_valid, output

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False, str(e)


def count_words(text: str) -> int:
    """
    Count words in text.

    Args:
        text: Input text

    Returns:
        int: Word count
    """
    return len(text.split())


def rate_limit_delay(seconds: int = 2) -> None:
    """
    Sleep for rate limiting (Gemini free tier: 10 requests/minute).

    Args:
        seconds: Seconds to wait (default: 2 seconds = safe for 10/min limit)
    """
    time.sleep(seconds)


if __name__ == '__main__':
    # Test configuration
    print("Testing configuration...")
    config = get_config()
    print(f"✅ Model: {config.model.model_name}")
    print(f"✅ Output dir: {config.paths.output_dir}")

    # Test model setup
    print("\nTesting model setup...")
    try:
        model = setup_model()
        print(f"✅ Model initialized: {config.model.model_name}")
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # Test prompt loading
    print("\nTesting prompt loading...")
    try:
        prompt = load_prompt("prompts/01_research/scout.md")
        print(f"✅ Prompt loaded ({len(prompt)} chars)")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    print("\n✅ All utilities working correctly")
