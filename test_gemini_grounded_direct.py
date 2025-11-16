#!/usr/bin/env python3
"""
Direct test of Gemini Grounded client to see actual errors
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ GOOGLE_API_KEY not set")
    sys.exit(1)

print("=" * 80)
print("DIRECT GEMINI GROUNDED TEST")
print("=" * 80)
print()

# Configure
genai.configure(api_key=api_key)

# Try the new API syntax
print("🔧 Creating model with Tool(google_search_retrieval={})...")
try:
    from google.generativeai.types import Tool
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash-exp',
        tools=[Tool(google_search_retrieval={})]
    )
    print("✅ Model created successfully")
    print(f"   Model: {model.model_name}")
    print(f"   Tools: {model._tools}")
except Exception as e:
    print(f"❌ Model creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test with a search query
print()
print("🔍 Testing with query: 'World Bank climate finance report'")
print()

try:
    response = model.generate_content(
        "Find a World Bank climate finance report and provide the URL"
    )

    print("✅ Generation successful!")
    print()
    print("Response text:")
    print("-" * 80)
    print(response.text)
    print("-" * 80)
    print()

    # Check for grounding metadata
    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        print("📊 Candidate info:")
        print(f"   Has grounding_metadata: {hasattr(candidate, 'grounding_metadata')}")

        if hasattr(candidate, 'grounding_metadata'):
            metadata = candidate.grounding_metadata
            print(f"   Grounding metadata: {metadata}")

            if hasattr(metadata, 'grounding_chunks'):
                print(f"   Grounding chunks: {len(metadata.grounding_chunks) if metadata.grounding_chunks else 0}")
                for i, chunk in enumerate(metadata.grounding_chunks or []):
                    print(f"     Chunk {i}: {chunk}")

except Exception as e:
    print(f"❌ Generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
