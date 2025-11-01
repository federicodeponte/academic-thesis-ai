#!/usr/bin/env python3
"""
QUICK TEST: Test Agent #14 (Citation Verifier) only

Tests citation verification on existing opensource thesis draft.
Fast test (~2-3 min) to validate [VERIFY] placeholder completion.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_config
from tests.test_utils import setup_model, run_agent


def main():
    """Test Agent #14 citation verification on existing draft."""
    config = get_config()

    print("="*70)
    print("AGENT #14 (CITATION VERIFIER) TEST")
    print("="*70)
    print()
    print(f"Model: {config.model.model_name}")
    print("Testing citation verification on existing opensource thesis draft")
    print()
    print("="*70)

    # Initialize model
    model = setup_model()

    # Output directory
    output_dir = config.paths.output_dir / "opensource_thesis"

    # Read existing draft thesis
    draft_path = output_dir / "FINAL_THESIS_OPENSOURCE.md"
    if not draft_path.exists():
        print(f"❌ Draft thesis not found at: {draft_path}")
        print("   Run test_opensource_thesis.py first to generate the draft")
        return 1

    with open(draft_path, 'r', encoding='utf-8') as f:
        draft_paper = f.read()

    draft_word_count = len(draft_paper.split())
    print(f"📄 Loaded draft thesis: {draft_word_count:,} words")

    # Count [VERIFY] placeholders
    verify_count = draft_paper.count('[VERIFY]')
    print(f"🔍 Found {verify_count} [VERIFY] placeholders to complete")
    print()

    # ====================================================================
    # TEST: AGENT #14 (CITATION VERIFIER)
    # ====================================================================
    print("="*70)
    print("🔍 Running Agent #14 (Citation Verifier)")
    print("="*70)
    print()
    print("This will:")
    print("  • Find all [VERIFY] citation placeholders")
    print("  • Complete missing metadata (year, publisher, DOI)")
    print("  • Validate APA 7th edition format")
    print("  • Output: 100% verified citations")
    print()
    print("⏳ Citation verification may take 2-3 minutes...")
    print()

    verified_paper = run_agent(
        model=model,
        name="Agent #14 - Citation Verifier",
        prompt_path="prompts/05_refine/citation_verifier.md",
        user_input=f"Complete all [VERIFY] citation placeholders in this thesis:\n\n{draft_paper}",
        save_to=output_dir / "TEST_verified_citations.md"
    )

    if not verified_paper:
        print("❌ Citation verification failed")
        return 1

    verified_word_count = len(verified_paper.split())

    # ====================================================================
    # RESULTS
    # ====================================================================
    print()
    print("="*70)
    print("✅ CITATION VERIFICATION COMPLETE")
    print("="*70)
    print()
    print(f"Draft word count:    {draft_word_count:,} words")
    print(f"Verified word count: {verified_word_count:,} words")
    print()
    print(f"Verified thesis saved to:")
    print(f"  {output_dir / 'TEST_verified_citations.md'}")
    print()

    # Validation
    print("="*70)
    print("🔍 VALIDATION")
    print("="*70)
    print()

    verify_count_after = verified_paper.count('[VERIFY]')

    print(f"[VERIFY] placeholders before: {verify_count}")
    print(f"[VERIFY] placeholders after:  {verify_count_after}")
    print()

    if verify_count_after == 0:
        print("✅ SUCCESS: All [VERIFY] placeholders completed!")
    elif verify_count_after < verify_count:
        print(f"⚠️  PARTIAL: {verify_count - verify_count_after} placeholders completed")
        print(f"   {verify_count_after} still remain")
    else:
        print("❌ FAILURE: No placeholders were completed")

    print()
    print("="*70)

    # Show sample citations
    if verify_count_after == 0:
        print("\n📚 Sample verified citations (first 5):")
        print("-" * 70)
        lines = verified_paper.split('\n')
        citation_count = 0
        for line in lines:
            if '(' in line and ')' in line and any(year in line for year in ['2019', '2020', '2021', '2022', '2023', '2024']):
                print(f"  {line[:100]}")
                citation_count += 1
                if citation_count >= 5:
                    break
        print()

    return 0 if verify_count_after == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
