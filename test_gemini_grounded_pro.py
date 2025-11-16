#!/usr/bin/env python3
"""
Isolated test for Gemini Grounded with Gemini 2.5 Pro.
Tests Google Search grounding functionality.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from utils.api_citations.gemini_grounded import GeminiGroundedClient

def test_gemini_grounded_pro():
    """Test Gemini Grounded with industry query using Gemini 2.5 Pro."""

    print("=" * 80)
    print("GEMINI GROUNDED (2.5 PRO) ISOLATED TEST")
    print("=" * 80)

    # Industry query
    query = "McKinsey report AI pricing models"

    print(f"\n📝 Query: {query}")
    print(f"🤖 Model: gemini-2.5-pro")
    print(f"🔧 validate_urls: False (to prevent timeouts)")
    print(f"⏱️  timeout: 300s (5 minutes for Pro model)\n")

    client = GeminiGroundedClient(
        validate_urls=False,
        timeout=300  # Longer timeout for Gemini 2.5 Pro
    )

    print("🔍 Calling search_paper()...\n")
    result = client.search_paper(query)

    print("\n" + "=" * 80)
    print("RESULT")
    print("=" * 80)

    if result:
        print("✅ SUCCESS - Citation found!")
        print(f"\nTitle: {result.get('title')}")
        print(f"URL: {result.get('url')}")
        print(f"Source Type: {result.get('source_type')}")
        if result.get('snippet'):
            print(f"Snippet: {result.get('snippet')[:150]}...")
    else:
        print("❌ FAILED - No citation returned")

    print("\n" + "=" * 80)

    client.close()
    return result is not None

if __name__ == '__main__':
    success = test_gemini_grounded_pro()
    sys.exit(0 if success else 1)
