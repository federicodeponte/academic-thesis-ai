#!/usr/bin/env python3
"""
Test API-backed citation research to verify Crossref and Semantic Scholar integration.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.api_citations import CrossrefClient, SemanticScholarClient, CitationResearcher
from tests.test_utils import setup_model


def test_crossref():
    """Test Crossref API client."""
    print("\n" + "="*70)
    print("TEST 1: Crossref API Client")
    print("="*70)

    with CrossrefClient() as client:
        # Test queries
        test_queries = [
            "Open source software economic impact",
            "CO2 emissions trading effectiveness",
            "AI pricing strategies LLM APIs",
        ]

        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            result = client.search_paper(query)

            if result:
                print(f"✅ Found: {result['title'][:70]}...")
                print(f"   Authors: {', '.join(result['authors'][:3])}")
                print(f"   Year: {result['year']}")
                print(f"   DOI: {result.get('doi', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 0):.2f}")
            else:
                print(f"❌ No results")


def test_semantic_scholar():
    """Test Semantic Scholar API client."""
    print("\n" + "="*70)
    print("TEST 2: Semantic Scholar API Client")
    print("="*70)

    with SemanticScholarClient() as client:
        # Test queries
        test_queries = [
            "Linux kernel development collaboration",
            "Carbon pricing mechanism climate change",
            "transformer architecture attention mechanism",
        ]

        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            result = client.search_paper(query)

            if result:
                print(f"✅ Found: {result['title'][:70]}...")
                print(f"   Authors: {', '.join(result['authors'][:3])}")
                print(f"   Year: {result['year']}")
                print(f"   URL: {result.get('url', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 0):.2f}")
            else:
                print(f"❌ No results")


def test_orchestrator():
    """Test full fallback chain orchestrator."""
    print("\n" + "="*70)
    print("TEST 3: Citation Researcher Orchestrator (Fallback Chain)")
    print("="*70)

    model = setup_model()

    with CitationResearcher(gemini_model=model, verbose=True) as researcher:
        # Test queries (mix of easy and hard)
        test_topics = [
            "Report on technology's role in global challenges",
            "Free Software Foundation (FSF) - The Free Software Definition",
            "Schmidt & Johnson (2023) - The Economic Impact of Open Source Software",
            "Energy efficiency of Linux in data centers",
            "Wikipedia's model of knowledge creation and quality control",
        ]

        results = []
        for topic in test_topics:
            citation = researcher.research_citation(topic)
            if citation:
                results.append((topic, citation, "SUCCESS"))
            else:
                results.append((topic, None, "FAILED"))

        # Print summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)

        success_count = sum(1 for _, _, status in results if status == "SUCCESS")
        total_count = len(results)
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0

        print(f"\nSuccess Rate: {success_count}/{total_count} ({success_rate:.1f}%)")
        print(f"Target: 95%+ (Current LLM-only: ~40%)\n")

        for topic, citation, status in results:
            if status == "SUCCESS":
                print(f"✅ {topic[:60]}...")
                print(f"   → {citation.authors[0]} et al. ({citation.year})")
                if citation.doi:
                    print(f"   → DOI: {citation.doi}")
            else:
                print(f"❌ {topic[:60]}...")


def main():
    """Run all API integration tests."""
    print("="*70)
    print("API-BACKED CITATION RESEARCH INTEGRATION TEST")
    print("="*70)
    print("\nTesting Crossref → Semantic Scholar → Gemini LLM fallback chain")
    print("Expected improvement: 40% → 95%+ success rate\n")

    try:
        # Test 1: Crossref
        test_crossref()

        # Test 2: Semantic Scholar
        test_semantic_scholar()

        # Test 3: Full orchestrator with fallback
        test_orchestrator()

        print("\n" + "="*70)
        print("✅ ALL API INTEGRATION TESTS COMPLETE")
        print("="*70)

        return 0

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
