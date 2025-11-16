#!/usr/bin/env python3
"""
Debug script to isolate Gemini Grounded 0% citation issue.
Tests a single industry query and shows exactly where it fails.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from utils.api_citations.gemini_grounded import GeminiGroundedClient


def test_gemini_grounded():
    """Test Gemini Grounded with a single industry query."""

    print("=" * 80)
    print("GEMINI GROUNDED DEBUG TEST")
    print("=" * 80)

    # Test query that should return industry sources
    query = "McKinsey report AI pricing models"

    print(f"\n📝 Query: {query}")
    print(f"🎯 Expected: Industry report URL from McKinsey or similar\n")

    # Initialize client with verbose output
    print("🔧 Initializing Gemini Grounded client...")
    print(f"   validate_urls: True")
    print(f"   timeout: 120s")
    print(f"   forbidden_domains: []")
    print()

    client = GeminiGroundedClient(
        validate_urls=True,  # Default setting
        timeout=120
    )

    print("🔍 Calling search_paper()...\n")

    # Call search
    result = client.search_paper(query)

    print("\n" + "=" * 80)
    print("RESULT")
    print("=" * 80)

    if result:
        print("✅ SUCCESS - Citation found!")
        print(f"\nTitle: {result.get('title')}")
        print(f"URL: {result.get('url')}")
        print(f"Snippet: {result.get('snippet', 'N/A')[:100]}...")
    else:
        print("❌ FAILED - No citation returned")
        print("\nPossible reasons:")
        print("  1. No grounding chunks in API response")
        print("  2. All URLs failed validation (HTTP != 200)")
        print("  3. All URLs failed redirect unwrapping")
        print("  4. URLs filtered by forbidden_domains")

    print("\n" + "=" * 80)

    # Clean up
    client.close()


if __name__ == '__main__':
    test_gemini_grounded()
