#!/usr/bin/env python3
"""
Verbose test of GeminiGroundedClient to see exactly what's happening
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from utils.api_citations.gemini_grounded import GeminiGroundedClient

print("=" * 80)
print("VERBOSE GEMINI GROUNDED CLIENT TEST")
print("=" * 80)
print()

# Create client
print("Creating GeminiGroundedClient...")
try:
    client = GeminiGroundedClient()
    print(f"✅ Client created successfully")
    print(f"   Model: {client.model_name}")
    print(f"   Base URL: {client.base_url}")
    print(f"   Timeout: {client.timeout}s")
    print()
except Exception as e:
    print(f"❌ Failed to create client: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test search
query = "World Bank climate finance report"
print(f"Searching for: {query}")
print()

try:
    result = client.search_paper(query)

    if result:
        print("✅ CITATION FOUND!")
        print("-" * 80)
        print(f"Title: {result.get('title')}")
        print(f"URL: {result.get('url')}")
        print(f"Authors: {result.get('authors')}")
        print(f"Date: {result.get('date')}")
        print(f"Snippet: {result.get('snippet')}")
        print(f"Source Type: {result.get('source_type')}")
        print("-" * 80)
    else:
        print("❌ NO CITATION FOUND")
        print("This means one of these steps failed:")
        print("  1. API call failed")
        print("  2. Grounding metadata extraction failed")
        print("  3. URL validation/unwrapping failed")
        print()
        print("Check error messages above for details")

except Exception as e:
    print(f"❌ Search error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    client.close()
