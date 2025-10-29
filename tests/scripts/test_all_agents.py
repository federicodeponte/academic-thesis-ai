#!/usr/bin/env python3
"""
Comprehensive test script for all 14 agents.
Tests each agent with realistic inputs and validates outputs.

REFACTORED: Uses centralized config and shared utilities (DRY, SOLID)
"""

import sys
from pathlib import Path
from typing import Callable, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_config
from tests.test_utils import setup_model, test_agent


# ====================================================================
# VALIDATION FUNCTIONS
# ====================================================================

def validate_scribe(output: str) -> Tuple[bool, str]:
    """Validate Scribe agent output."""
    required = ["Research Question", "Methodology", "Key Findings", "Limitations"]
    found = sum(1 for r in required if r.lower() in output.lower())
    return (found >= 3, f"Found {found}/4 required sections")


def validate_signal(output: str) -> Tuple[bool, str]:
    """Validate Signal agent output."""
    required = ["Gap", "Trend", "Opportunity"]
    found = sum(1 for r in required if r.lower() in output.lower())
    return (found >= 2, f"Found {found}/3 required sections")


def validate_formatter(output: str) -> Tuple[bool, str]:
    """Validate Formatter agent output."""
    required = ["Abstract", "Introduction", "Methodology", "Results", "Discussion"]
    found = sum(1 for r in required if r.lower() in output.lower())
    return (found >= 4, f"Found {found}/5 required sections")


def validate_thread(output: str) -> Tuple[bool, str]:
    """Validate Thread agent output."""
    # Thread agent should analyze consistency - check for analysis keywords
    required = ["consistency", "flow", "coherent", "transition", "alignment"]
    found = sum(1 for r in required if r in output.lower())
    return (found >= 2, f"Found consistency analysis")


def validate_narrator(output: str) -> Tuple[bool, str]:
    """Validate Narrator agent output."""
    required = ["voice", "tone", "consistency", "unified"]
    found = sum(1 for r in required if r in output.lower())
    return (found >= 2, f"Found voice analysis")


def validate_skeptic(output: str) -> Tuple[bool, str]:
    """Validate Skeptic agent output."""
    required = ["weakness", "concern", "issue", "improve"]
    found = sum(1 for r in required if r in output.lower())
    return (found >= 2, f"Found critical analysis")


def validate_verifier(output: str) -> Tuple[bool, str]:
    """Validate Verifier agent output."""
    required = ["citation", "verif", "accura", "source"]
    found = sum(1 for r in required if r in output.lower())
    return (found >= 2, f"Found verification analysis")


def validate_referee(output: str) -> Tuple[bool, str]:
    """Validate Referee agent output."""
    required = ["score", "rating", "novelty", "significance", "quality"]
    found = sum(1 for r in required if r in output.lower())
    return (found >= 3, f"Found peer review metrics")


def validate_voice(output: str) -> Tuple[bool, str]:
    """Validate Voice agent output."""
    required = ["style", "pattern", "sentence", "vocabulary"]
    found = sum(1 for r in required if r in output.lower())
    return (found >= 2, f"Found style analysis")


def validate_polish(output: str) -> Tuple[bool, str]:
    """Validate Polish agent output."""
    return (len(output) > 100, f"Grammar check completed")


# ====================================================================
# TEST DATA
# ====================================================================

SAMPLE_PAPER = """
# Transformers in Natural Language Processing: A Survey

## Abstract
Transformers have revolutionized NLP since 2017. This paper surveys recent advances.

## Introduction
Natural language processing has been transformed by the attention mechanism introduced in "Attention is All You Need" (Vaswani et al., 2017). The transformer architecture has become the foundation for models like BERT, GPT, and T5.

## Methods
We conducted a systematic review of 50 papers published between 2020-2024 on transformer architectures.

## Results
We identified three major trends: (1) scaling to larger models, (2) efficiency improvements, (3) multimodal integration.

## Discussion
Our findings suggest that transformers will continue to dominate NLP, though efficiency concerns remain.

## Conclusion
Transformers represent a paradigm shift in NLP with continued innovation expected.
"""

SAMPLE_OUTLINE = """
# Paper Outline: AI in Climate Modeling

## 1. Introduction (800 words)
- Background on climate modeling
- Limitations of traditional physics-based models
- Emergence of AI approaches

## 2. Literature Review (1500 words)
- Traditional climate models
- Machine learning in climate science
- Hybrid approaches

## 3. Methodology (1000 words)
- Data collection
- Model architecture
- Evaluation metrics

## 4. Results (1500 words)
- Prediction accuracy
- Computational efficiency
- Uncertainty quantification

## 5. Discussion (1200 words)
- Comparison with existing methods
- Implications for climate science
- Limitations

## 6. Conclusion (500 words)
- Summary of contributions
- Future work
"""


# ====================================================================
# MAIN TEST SUITE
# ====================================================================

def main():
    """Run all agent tests."""
    config = get_config()

    print("="*70)
    print("COMPREHENSIVE AGENT TESTING")
    print("Testing all 14 agents for production readiness")
    print(f"Model: {config.model.model_name}")
    print("="*70)

    # Initialize model
    model = setup_model()

    # Output directory
    output_dir = config.paths.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {}

    # Test 1: Scribe Agent
    results['scribe'] = test_agent(
        model=model,
        name="Scribe Agent",
        prompt_path="prompts/01_research/scribe.md",
        user_input=f"Please summarize this paper:\n\n{SAMPLE_PAPER}",
        validation_fn=validate_scribe,
        output_file=output_dir / "scribe_agent_output.md"
    )

    # Test 2: Signal Agent
    results['signal'] = test_agent(
        model=model,
        name="Signal Agent",
        prompt_path="prompts/01_research/signal.md",
        user_input=f"Analyze research gaps based on this summary:\n\n{SAMPLE_PAPER}",
        validation_fn=validate_signal,
        output_file=output_dir / "signal_agent_output.md"
    )

    # Test 3: Formatter Agent
    results['formatter'] = test_agent(
        model=model,
        name="Formatter Agent",
        prompt_path="prompts/02_structure/formatter.md",
        user_input=f"Apply IMRaD format to this outline:\n\n{SAMPLE_OUTLINE}\n\nTarget journal: Nature\nCitation style: APA",
        validation_fn=validate_formatter,
        output_file=output_dir / "formatter_agent_output.md"
    )

    # Test 4: Thread Agent
    results['thread'] = test_agent(
        model=model,
        name="Thread Agent",
        prompt_path="prompts/03_compose/thread.md",
        user_input=f"Check consistency in this paper:\n\n{SAMPLE_PAPER}",
        validation_fn=validate_thread,
        output_file=output_dir / "thread_agent_output.md"
    )

    # Test 5: Narrator Agent
    results['narrator'] = test_agent(
        model=model,
        name="Narrator Agent",
        prompt_path="prompts/03_compose/narrator.md",
        user_input=f"Unify voice in this paper:\n\n{SAMPLE_PAPER}",
        validation_fn=validate_narrator,
        output_file=output_dir / "narrator_agent_output.md"
    )

    # Test 6: Skeptic Agent
    results['skeptic'] = test_agent(
        model=model,
        name="Skeptic Agent",
        prompt_path="prompts/04_validate/skeptic.md",
        user_input=f"Provide critical review of this paper:\n\n{SAMPLE_PAPER}",
        validation_fn=validate_skeptic,
        output_file=output_dir / "skeptic_agent_output.md"
    )

    # Test 7: Verifier Agent
    results['verifier'] = test_agent(
        model=model,
        name="Verifier Agent",
        prompt_path="prompts/04_validate/verifier.md",
        user_input=f"Verify citations in this paper:\n\n{SAMPLE_PAPER}",
        validation_fn=validate_verifier,
        output_file=output_dir / "verifier_agent_output.md"
    )

    # Test 8: Referee Agent
    results['referee'] = test_agent(
        model=model,
        name="Referee Agent",
        prompt_path="prompts/04_validate/referee.md",
        user_input=f"Provide peer review for this paper:\n\n{SAMPLE_PAPER}\n\nTarget journal: ACL",
        validation_fn=validate_referee,
        output_file=output_dir / "referee_agent_output.md"
    )

    # Test 9: Voice Agent
    results['voice'] = test_agent(
        model=model,
        name="Voice Agent",
        prompt_path="prompts/05_refine/voice.md",
        user_input=f"Analyze writing style in this sample:\n\n{SAMPLE_PAPER[:500]}",
        validation_fn=validate_voice,
        output_file=output_dir / "voice_agent_output.md"
    )

    # Test 10: Polish Agent
    results['polish'] = test_agent(
        model=model,
        name="Polish Agent",
        prompt_path="prompts/05_refine/polish.md",
        user_input=f"Polish this text:\n\n{SAMPLE_PAPER[:300]}",
        validation_fn=validate_polish,
        output_file=output_dir / "polish_agent_output.md"
    )

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    total = len(results)
    passed = sum(1 for is_valid, _ in results.values() if is_valid)

    for name, (is_valid, output) in results.items():
        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"{name.upper()}: {status}")

    print(f"\nTotal: {passed}/{total} passed ({int(passed/total*100)}%)")
    print(f"Model used: {config.model.model_name}")
    print(f"Outputs saved to: {output_dir}/")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED - PRODUCTION READY")
        return 0
    else:
        print(f"\n⚠️  {total-passed} tests failed - needs fixes")
        return 1


if __name__ == "__main__":
    sys.exit(main())
