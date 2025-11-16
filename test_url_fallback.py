#!/usr/bin/env python3
"""
Simple test to verify URL fallback works in citation formatting
Tests the fix without needing external APIs
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.citation_database import Citation, CitationDatabase
from utils.citation_compiler import CitationCompiler


def test_url_fallback():
    """Test that citations with URL but no DOI display URLs correctly."""

    print("=" * 80)
    print("TESTING URL FALLBACK IN CITATION FORMATTING")
    print("=" * 80)
    print()

    # Create test citations
    test_cases = [
        {
            'name': 'Website source (source_type=website)',
            'citation': Citation(
                citation_id='cite_001',
                authors=['World Bank'],
                year=2024,
                title='Climate Finance Report 2024',
                source_type='website',
                language='english',
                url='https://www.worldbank.org/climate-finance-2024',
                doi='',  # No DOI
            ),
            'expected_contains': 'https://www.worldbank.org/climate-finance-2024'
        },
        {
            'name': 'Journal source with URL fallback (source_type=journal)',
            'citation': Citation(
                citation_id='cite_002',
                authors=['Smith', 'Johnson'],
                year=2023,
                title='AI Governance Framework',
                source_type='journal',
                language='english',
                journal='Tech Policy Review',
                url='https://techpolicy.org/ai-governance',
                doi='',  # No DOI - should fall back to URL
            ),
            'expected_contains': 'https://techpolicy.org/ai-governance'
        },
        {
            'name': 'Report source with URL (source_type=report)',
            'citation': Citation(
                citation_id='cite_003',
                authors=['OECD'],
                year=2024,
                title='Digital Economy Outlook',
                source_type='report',
                language='english',
                publisher='OECD Publishing',
                url='https://www.oecd.org/digital-economy-2024',
                doi='',
            ),
            'expected_contains': 'https://www.oecd.org/digital-economy-2024'
        },
    ]

    # Test each case
    results = []
    for test_case in test_cases:
        print(f"📋 Test Case: {test_case['name']}")
        print(f"   Source Type: {test_case['citation'].source_type}")
        print(f"   Has DOI: {bool(test_case['citation'].doi)}")
        print(f"   Has URL: {bool(test_case['citation'].url)}")

        # Format citation
        db = CitationDatabase(
            citations=[test_case['citation']],
            citation_style="APA 7th"
        )
        compiler = CitationCompiler(db)

        formatted = compiler._format_apa_reference(test_case['citation'])

        print()
        print("Formatted Reference:")
        print("-" * 80)
        print(formatted)
        print("-" * 80)

        # Check if URL appears
        expected_url = test_case['expected_contains']
        if expected_url in formatted:
            print(f"✅ SUCCESS: URL appears in formatted reference")
            results.append(True)
        else:
            print(f"❌ FAIL: URL does NOT appear")
            print(f"   Expected to find: {expected_url}")
            results.append(False)

        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total} test cases")

    if passed == total:
        print("✅ ALL TESTS PASSED")
        print()
        print("URL fallback is working correctly:")
        print("  - Website sources show URLs ✓")
        print("  - Journal sources with no DOI show URLs ✓")
        print("  - Report sources show URLs ✓")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        return False


if __name__ == '__main__':
    try:
        success = test_url_fallback()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
