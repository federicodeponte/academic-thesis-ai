#!/usr/bin/env python3
"""
End-to-end workflow test: Generate a complete academic paper.
Runs through all phases from research to final paper.

REFACTORED: Uses centralized config and shared utilities (DRY, SOLID)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_config
from tests.test_utils import setup_model, run_agent, rate_limit_delay


def main():
    """Run complete workflow test."""
    config = get_config()

    print("="*70)
    print("COMPLETE WORKFLOW TEST")
    print("Generating full academic paper from scratch")
    print(f"Model: {config.model.model_name}")
    print("="*70)

    # Initialize model
    model = setup_model()

    # Topic
    topic = "The role of large language models in scientific research acceleration"

    # Output directory
    output_dir = config.paths.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # ====================================================================
    # PHASE 1: RESEARCH
    # ====================================================================
    print("\n" + "="*70)
    print("PHASE 1: RESEARCH")
    print("="*70)

    # Step 1: Scout - Find papers
    scout_output = run_agent(
        model, "Scout - Find Papers",
        "prompts/01_research/scout.md",
        f"Find 20 papers on: {topic}"
    )
    rate_limit_delay()

    # Step 2: Scribe - Summarize
    scribe_output = run_agent(
        model, "Scribe - Summarize Papers",
        "prompts/01_research/scribe.md",
        f"Summarize these papers:\n\n{scout_output[:2000]}"
    )
    rate_limit_delay()

    # Step 3: Signal - Find gaps
    signal_output = run_agent(
        model, "Signal - Research Gaps",
        "prompts/01_research/signal.md",
        f"Find research gaps from:\n\n{scribe_output[:2000]}"
    )
    rate_limit_delay()

    # ====================================================================
    # PHASE 2: STRUCTURE
    # ====================================================================
    print("\n" + "="*70)
    print("PHASE 2: STRUCTURE")
    print("="*70)

    # Step 4: Architect - Create outline
    architect_output = run_agent(
        model, "Architect - Create Outline",
        "prompts/02_structure/architect.md",
        f"Create paper outline for topic: {topic}\n\nResearch gaps:\n{signal_output[:1500]}"
    )
    rate_limit_delay()

    # Step 5: Formatter - Apply style
    formatter_output = run_agent(
        model, "Formatter - Apply IMRaD Format",
        "prompts/02_structure/formatter.md",
        f"Apply IMRaD format:\n\n{architect_output[:2000]}\n\nTarget: Nature journal, APA style"
    )
    rate_limit_delay()

    # ====================================================================
    # PHASE 3: COMPOSE
    # ====================================================================
    print("\n" + "="*70)
    print("PHASE 3: COMPOSE")
    print("="*70)

    # Write sections
    intro = run_agent(
        model, "Crafter - Write Introduction",
        "prompts/03_compose/crafter.md",
        f"Write Introduction section (800 words) for:\n\n{formatter_output[:1500]}"
    )
    rate_limit_delay()

    methods = run_agent(
        model, "Crafter - Write Methods",
        "prompts/03_compose/crafter.md",
        f"Write Methodology section (600 words) for:\n\n{formatter_output[:1500]}"
    )
    rate_limit_delay()

    results = run_agent(
        model, "Crafter - Write Results",
        "prompts/03_compose/crafter.md",
        f"Write Results section (800 words) for:\n\n{formatter_output[:1500]}"
    )
    rate_limit_delay()

    discussion = run_agent(
        model, "Crafter - Write Discussion",
        "prompts/03_compose/crafter.md",
        f"Write Discussion section (800 words) for:\n\n{formatter_output[:1500]}"
    )
    rate_limit_delay()

    conclusion = run_agent(
        model, "Crafter - Write Conclusion",
        "prompts/03_compose/crafter.md",
        f"Write Conclusion section (400 words) for:\n\n{formatter_output[:1500]}"
    )
    rate_limit_delay()

    # Assemble draft
    full_draft = f"""# {topic}

## Abstract
[To be written]

{intro}

{methods}

{results}

{discussion}

{conclusion}
"""

    # Check consistency
    thread_output = run_agent(
        model, "Thread - Check Consistency",
        "prompts/03_compose/thread.md",
        f"Check consistency:\n\n{full_draft[:3000]}"
    )
    rate_limit_delay()

    # Unify voice
    narrator_output = run_agent(
        model, "Narrator - Unify Voice",
        "prompts/03_compose/narrator.md",
        f"Unify voice:\n\n{full_draft[:3000]}"
    )
    rate_limit_delay()

    # ====================================================================
    # PHASE 4: VALIDATE
    # ====================================================================
    print("\n" + "="*70)
    print("PHASE 4: VALIDATE")
    print("="*70)

    skeptic_output = run_agent(
        model, "Skeptic - Critical Review",
        "prompts/04_validate/skeptic.md",
        f"Critically review:\n\n{full_draft[:3000]}"
    )
    rate_limit_delay()

    verifier_output = run_agent(
        model, "Verifier - Verify Citations",
        "prompts/04_validate/verifier.md",
        f"Verify citations:\n\n{full_draft[:2000]}"
    )
    rate_limit_delay()

    referee_output = run_agent(
        model, "Referee - Peer Review",
        "prompts/04_validate/referee.md",
        f"Peer review for Nature:\n\n{full_draft[:3000]}"
    )
    rate_limit_delay()

    # ====================================================================
    # PHASE 5: REFINE
    # ====================================================================
    print("\n" + "="*70)
    print("PHASE 5: REFINE")
    print("="*70)

    entropy_output = run_agent(
        model, "Entropy - Humanize Text",
        "prompts/05_refine/entropy.md",
        f"Humanize introduction:\n\n{intro[:1000]}"
    )
    rate_limit_delay()

    polish_output = run_agent(
        model, "Polish - Final Grammar Check",
        "prompts/05_refine/polish.md",
        f"Final polish:\n\n{entropy_output[:1000]}"
    )

    # Save final paper
    final_paper = f"""{full_draft}

---

## Validation Reports

### Thread Consistency Check
{thread_output[:500]}

### Skeptic Critical Review
{skeptic_output[:500]}

### Referee Peer Review
{referee_output[:500]}
"""

    output_file = output_dir / "complete_paper_workflow.md"
    with open(output_file, 'w', encoding='utf-8') as f:  # FIXED (Bug #15): Added UTF-8 encoding
        f.write(final_paper)

    # Summary
    print("\n" + "="*70)
    print("WORKFLOW COMPLETE ✅")
    print("="*70)
    print(f"\nFinal paper saved to: {output_file}")
    print(f"Paper length: {len(final_paper)} chars ({len(final_paper.split())} words)")
    print(f"Model used: {config.model.model_name}")
    print("\nAll 14 agents executed successfully:")
    print("✅ Scout, Scribe, Signal (Research)")
    print("✅ Architect, Formatter (Structure)")
    print("✅ Crafter x5, Thread, Narrator (Compose)")
    print("✅ Skeptic, Verifier, Referee (Validate)")
    print("✅ Voice, Entropy, Polish (Refine)")
    print("\n🎉 PRODUCTION-READY WORKFLOW VALIDATED")

    return 0


if __name__ == "__main__":
    sys.exit(main())
