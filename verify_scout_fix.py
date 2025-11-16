#!/usr/bin/env python3
"""
Quick verification script for Bug #21 fixes.
Reads citation_database.json and regenerates Scout markdown to verify source breakdown.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.citation_database import load_citation_database


def verify_scout_output(thesis_dir: str) -> None:
    """Verify Scout output shows correct source breakdown."""
    output_dir = Path(f"tests/outputs/{thesis_dir}")
    citation_db_path = output_dir / "citation_database.json"

    if not citation_db_path.exists():
        print(f"❌ Citation database not found: {citation_db_path}")
        return

    # Load citation database
    citation_db = load_citation_database(citation_db_path)

    print(f"\n{'='*70}")
    print(f"🔍 Verifying: {thesis_dir}")
    print(f"{'='*70}")

    # Count by api_source
    sources_breakdown = {
        "Crossref": 0,
        "Semantic Scholar": 0,
        "Gemini Grounded": 0,
        "Gemini LLM": 0
    }

    for citation in citation_db.citations:
        api_source = citation.api_source
        if api_source in sources_breakdown:
            sources_breakdown[api_source] += 1
        elif api_source:
            print(f"⚠️  Unknown api_source: {api_source}")

    total = len(citation_db.citations)

    print(f"\n✅ Total Citations: {total}")
    print(f"\n📚 Source Breakdown:")
    for source, count in sources_breakdown.items():
        percentage = (count / total * 100) if total > 0 else 0
        if count > 0:
            print(f"   ✓ {source}: {count} ({percentage:.1f}%)")
        else:
            print(f"   - {source}: {count} ({percentage:.1f}%)")

    # Check if Scout markdown matches
    scout_path = output_dir / "01_scout.md"
    if scout_path.exists():
        with open(scout_path, 'r', encoding='utf-8') as f:
            scout_content = f.read()

        print(f"\n📝 Scout Markdown Check:")

        # Check for source breakdown section
        if "### Sources Breakdown" in scout_content:
            print("   ✓ Contains 'Sources Breakdown' section")
        else:
            print("   ❌ Missing 'Sources Breakdown' section")

        # Check for each source
        for source in sources_breakdown:
            if source in scout_content:
                print(f"   ✓ Mentions '{source}'")
            else:
                print(f"   - No mention of '{source}'")

    print()


def main():
    """Verify all 4 theses."""
    theses = [
        "ai_pricing_thesis",
        "opensource_thesis",
        "academic_ai_thesis",
        "co2_thesis_german"
    ]

    print("\n🔬 BUG #21 FIX VERIFICATION")
    print("="*70)
    print("Testing source breakdown calculation and reporting...")

    for thesis_dir in theses:
        verify_scout_output(thesis_dir)

    print(f"\n{'='*70}")
    print("✅ Verification complete!")
    print("="*70)


if __name__ == '__main__':
    main()
