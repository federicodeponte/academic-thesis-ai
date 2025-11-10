#!/usr/bin/env python3
"""
Test safety filter fix for Gemini LLM fallback.

Tests queries that previously failed with finish_reason=2 (safety filter).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.api_citations import CitationResearcher
from tests.test_utils import setup_model


def main():
    """Test safety filter fix on previously failing queries."""
    print("="*70)
    print("SAFETY FILTER FIX TEST")
    print("="*70)
    print("\nTesting queries that previously failed with finish_reason=2")
    print("(Gemini safety filter blocking academic research)")
    print()

    model = setup_model()

    # These queries previously failed with safety filter (finish_reason=2)
    test_queries = [
        "Report on technology's role in global challenges",
        "Benefits of community-driven development in open source",
        "Open source and digital sovereignty in developing nations",
        "Examples of government open-source adoption and savings",
        "Open source and vendor lock-in reduction",
    ]

    with CitationResearcher(gemini_model=model, verbose=True) as researcher:
        results = []

        for i, topic in enumerate(test_queries, 1):
            print(f"\n[{i}/{len(test_queries)}] Testing: {topic}")
            print("-" * 70)

            citation = researcher.research_citation(topic)

            if citation:
                results.append((topic, "SUCCESS", citation))
                print(f"✅ Found: {citation.authors[0]} et al. ({citation.year})")
                if citation.doi:
                    print(f"   DOI: {citation.doi}")
                elif citation.url:
                    print(f"   URL: {citation.url}")
            else:
                results.append((topic, "FAILED", None))
                print(f"❌ Not found (all sources failed)")

        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)

        success_count = sum(1 for _, status, _ in results if status == "SUCCESS")
        total_count = len(results)
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0

        print(f"\nSuccess Rate: {success_count}/{total_count} ({success_rate:.1f}%)")
        print(f"Previous (with safety filter): 0/{total_count} (0%)")
        print(f"Expected improvement: {success_rate:.1f}% increase\n")

        for topic, status, citation in results:
            if status == "SUCCESS":
                print(f"✅ {topic[:60]}...")
            else:
                print(f"❌ {topic[:60]}...")

        print("\n" + "="*70)
        if success_rate > 50:
            print("✅ SAFETY FILTER FIX WORKING")
            print(f"   {success_rate:.1f}% of previously blocked queries now succeed")
        else:
            print("⚠️  SAFETY FILTER FIX PARTIAL")
            print(f"   Only {success_rate:.1f}% success rate on blocked queries")
        print("="*70)

        return 0 if success_rate > 50 else 1


if __name__ == "__main__":
    sys.exit(main())
