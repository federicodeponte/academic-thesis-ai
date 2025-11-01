#!/usr/bin/env python3
"""
ENHANCEMENT TEST: Test Agent #15 on existing opensource thesis

This script tests ONLY the enhancement phase (Agent #15) on the
already-generated opensource thesis to validate the enhancement works.

Faster than full regeneration (~3-5 min vs 30+ min)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_config
from tests.test_utils import setup_model, run_agent

def main():
    """Test Agent #15 enhancement on existing opensource thesis."""
    config = get_config()

    print("="*70)
    print("AGENT #15 (ENHANCER) TEST")
    print("="*70)
    print()
    print(f"Model: {config.model.model_name}")
    print("Testing enhancement on existing opensource thesis")
    print()
    print("="*70)

    # Initialize model
    model = setup_model()

    # Output directory
    output_dir = config.paths.output_dir / "opensource_thesis"

    # Read existing opensource thesis
    thesis_path = output_dir / "FINAL_THESIS_OPENSOURCE.md"
    if not thesis_path.exists():
        print(f"❌ Opensource thesis not found at: {thesis_path}")
        print("   Run test_opensource_thesis.py first to generate the base thesis")
        return 1

    with open(thesis_path, 'r', encoding='utf-8') as f:
        draft_paper = f.read()

    draft_word_count = len(draft_paper.split())
    print(f"📄 Loaded draft thesis: {draft_word_count:,} words")
    print()

    # ====================================================================
    # TEST: AGENT #15 (ENHANCER)
    # ====================================================================
    print("="*70)
    print("🔧 Running Agent #15 (Enhancer)")
    print("="*70)
    print()
    print("This will add:")
    print("  • YAML metadata frontmatter")
    print("  • Enhanced 4-paragraph abstract")
    print("  • 5 comprehensive appendices")
    print("  • Limitations and Future Research sections")
    print("  • 3-5 tables and 1-2 figures")
    print("  • Expanded case studies")
    print()
    print("⏳ Enhancement may take 3-5 minutes...")
    print()

    enhanced_paper = run_agent(
        model=model,
        name="Agent #15 - Enhancer",
        prompt_path="prompts/06_enhance/enhancer.md",
        user_input=f"Enhance this thesis to publication-ready standard:\n\n{draft_paper}",
        save_to=output_dir / "FINAL_THESIS_OPENSOURCE_ENHANCED.md"
    )

    if not enhanced_paper:
        print("❌ Enhancement failed")
        return 1

    # Post-process: Remove markdown code block wrapper if present
    if enhanced_paper.startswith('```markdown\n'):
        enhanced_paper = enhanced_paper[12:]  # Remove ```markdown\n
    if enhanced_paper.endswith('\n```'):
        enhanced_paper = enhanced_paper[:-4]  # Remove \n```
    # Save cleaned version
    with open(output_dir / "FINAL_THESIS_OPENSOURCE_ENHANCED.md", 'w', encoding='utf-8') as f:
        f.write(enhanced_paper)

    enhanced_word_count = len(enhanced_paper.split())
    word_increase = enhanced_word_count - draft_word_count
    percent_increase = (word_increase / draft_word_count) * 100

    # ====================================================================
    # RESULTS
    # ====================================================================
    print()
    print("="*70)
    print("✅ ENHANCEMENT COMPLETE")
    print("="*70)
    print()
    print(f"Draft word count:    {draft_word_count:,} words")
    print(f"Enhanced word count: {enhanced_word_count:,} words")
    print(f"Word increase:       +{word_increase:,} words ({percent_increase:.1f}% increase)")
    print()
    print(f"Enhanced thesis saved to:")
    print(f"  {output_dir / 'FINAL_THESIS_OPENSOURCE_ENHANCED.md'}")
    print()

    # Basic validation
    print("="*70)
    print("🔍 VALIDATION")
    print("="*70)
    print()

    has_yaml = enhanced_paper.startswith('---')
    has_appendix = 'Appendix' in enhanced_paper
    has_table = '|' in enhanced_paper and '---' in enhanced_paper.split('\n', 20)[10:]
    has_limitations = 'Limitations' in enhanced_paper
    has_future_research = 'Future Research' in enhanced_paper

    print(f"✓ YAML frontmatter:     {'✅ YES' if has_yaml else '❌ NO'}")
    print(f"✓ Appendices:           {'✅ YES' if has_appendix else '❌ NO'}")
    print(f"✓ Tables:               {'✅ YES' if has_table else '❌ NO'}")
    print(f"✓ Limitations section:  {'✅ YES' if has_limitations else '❌ NO'}")
    print(f"✓ Future Research:      {'✅ YES' if has_future_research else '❌ NO'}")
    print()

    # Expected targets
    target_word_count = 14000
    target_increase = 6900

    meets_target = enhanced_word_count >= target_word_count
    meets_increase = word_increase >= target_increase

    print("="*70)
    print("📊 TARGET COMPARISON")
    print("="*70)
    print()
    print(f"Target word count:  {target_word_count:,} words")
    print(f"Actual word count:  {enhanced_word_count:,} words {'✅' if meets_target else '⚠️'}")
    print()
    print(f"Target increase:    +{target_increase:,} words")
    print(f"Actual increase:    +{word_increase:,} words {'✅' if meets_increase else '⚠️'}")
    print()

    if meets_target and meets_increase:
        print("✅ AGENT #15 WORKING AS EXPECTED")
    elif enhanced_word_count > draft_word_count:
        print("⚠️  AGENT #15 WORKING BUT BELOW TARGET")
    else:
        print("❌ AGENT #15 NOT ADDING CONTENT")

    print()
    print("="*70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
