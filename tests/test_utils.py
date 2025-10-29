#!/usr/bin/env python3
"""
ABOUTME: Shared test utilities for all test scripts (DRY principle)
ABOUTME: Provides reusable functions for model setup, prompt loading, and agent execution
"""

import sys
import time
from pathlib import Path
from typing import Optional, Callable, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from config import get_config


def setup_model(model_override: Optional[str] = None) -> genai.GenerativeModel:
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

    genai.configure(api_key=config.google_api_key)

    model_name = model_override or config.model.model_name

    return genai.GenerativeModel(
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
    model: genai.GenerativeModel,
    name: str,
    prompt_path: str,
    user_input: str,
    save_to: Optional[Path] = None,
    verbose: bool = True
) -> str:
    """
    Run an AI agent with given prompt and input.

    Args:
        model: Configured Gemini model instance
        name: Human-readable name for the agent (for logging)
        prompt_path: Path to agent prompt file
        user_input: User's request/input for the agent
        save_to: Optional path to save output
        verbose: Whether to print progress messages

    Returns:
        str: Agent's output text

    Raises:
        Exception: If agent execution fails
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"🤖 {name}")
        print(f"{'='*70}")

    # Load agent prompt
    agent_prompt = load_prompt(prompt_path)

    # Combine agent prompt with user input
    full_prompt = f"{agent_prompt}\n\n---\n\nUser Request:\n{user_input}"

    # Generate response
    if verbose:
        print("Generating...", end=' ', flush=True)

    start_time = time.time()

    try:
        response = model.generate_content(full_prompt)
        output = response.text
    except Exception as e:
        if verbose:
            print(f"❌ Error")
        raise Exception(f"Agent execution failed: {str(e)}") from e

    elapsed = time.time() - start_time

    # Save output if path provided
    if save_to:
        save_to.parent.mkdir(parents=True, exist_ok=True)
        with open(save_to, 'w', encoding='utf-8') as f:
            f.write(output)

    if verbose:
        print(f"✅ Done ({elapsed:.1f}s, {len(output):,} chars)")
        if save_to:
            print(f"Saved to: {save_to}")

    return output


def test_agent(
    model: genai.GenerativeModel,
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
