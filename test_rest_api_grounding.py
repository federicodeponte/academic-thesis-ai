#!/usr/bin/env python3
"""
Test Gemini REST API with Google Search grounding
Uses the same pattern as gtm-os-v2
"""

import os
import sys
import json
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ GOOGLE_API_KEY not set")
    sys.exit(1)

print("=" * 80)
print("TESTING GEMINI REST API WITH GOOGLE SEARCH GROUNDING")
print("=" * 80)
print()

# Build request body (matching gtm-os-v2 pattern)
model_name = "gemini-2.5-flash"
prompt = "Find a credible web source about: World Bank climate finance report. Include the URL."

body = {
    "contents": [
        {
            "role": "user",
            "parts": [{"text": prompt}]
        }
    ],
    "generationConfig": {
        "temperature": 0.2,
        "maxOutputTokens": 8192,
    },
    "tools": [
        {"googleSearch": {}},  # Enable Google Search grounding
    ]
}

print(f"🔧 Model: {model_name}")
print(f"🔍 Query: World Bank climate finance report")
print(f"📦 Tools: {body['tools']}")
print()

# Make REST API call
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

print(f"🌐 URL: {url[:100]}...")
print()

try:
    response = requests.post(
        url,
        json=body,
        headers={"Content-Type": "application/json"},
        timeout=120
    )

    print(f"📊 Status Code: {response.status_code}")
    print()

    if not response.ok:
        print(f"❌ API Error:")
        print("-" * 80)
        error_text = response.text
        print(error_text)
        print("-" * 80)
        sys.exit(1)

    data = response.json()

    print("✅ API call successful!")
    print()

    # Check for candidates
    if 'candidates' in data and data['candidates']:
        candidate = data['candidates'][0]

        print("📝 Response Content:")
        print("-" * 80)
        content = candidate.get('content', {})
        parts = content.get('parts', [])
        if parts:
            text = parts[0].get('text', '')
            print(text[:500])
            if len(text) > 500:
                print(f"\n... ({len(text)} total characters)")
        print("-" * 80)
        print()

        # Check for grounding metadata
        grounding_metadata = candidate.get('groundingMetadata')
        if grounding_metadata:
            print("🌐 Grounding Metadata Found:")
            print("-" * 80)

            # Extract grounding chunks
            grounding_chunks = grounding_metadata.get('groundingChunks', [])
            print(f"Grounding chunks: {len(grounding_chunks)}")

            for i, chunk in enumerate(grounding_chunks):
                web = chunk.get('web', {})
                if web:
                    uri = web.get('uri')
                    title = web.get('title')
                    print(f"\nChunk {i+1}:")
                    print(f"  Title: {title}")
                    print(f"  URL: {uri}")

            # Check web search queries
            web_search_queries = grounding_metadata.get('webSearchQueries', [])
            if web_search_queries:
                print(f"\nWeb search queries: {web_search_queries}")

            print("-" * 80)
            print()
            print("✅ Google Search grounding is WORKING!")
        else:
            print("⚠️  No grounding metadata in response")
            print("This may mean Google Search grounding is not enabled or available")
    else:
        print("❌ No candidates in response")
        print(json.dumps(data, indent=2))

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
