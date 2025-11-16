#!/usr/bin/env python3
"""
Test basic Gemini REST API without Google Search grounding
To verify if API key is valid for basic use
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
print("TESTING BASIC GEMINI REST API (NO GOOGLE SEARCH)")
print("=" * 80)
print()

# Build request body WITHOUT googleSearch tool
model_name = "gemini-2.5-pro-latest"
prompt = "What is 2+2? Just answer with the number."

body = {
    "contents": [
        {
            "role": "user",
            "parts": [{"text": prompt}]
        }
    ],
    "generationConfig": {
        "temperature": 0.2,
        "maxOutputTokens": 100,
    },
    # NO tools array - testing basic API access
}

print(f"🔧 Model: {model_name}")
print(f"🔍 Query: {prompt}")
print(f"📦 Tools: None (basic test)")
print()

# Make REST API call
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

print(f"🌐 Endpoint: /v1beta/models/{model_name}:generateContent")
print()

try:
    response = requests.post(
        url,
        json=body,
        headers={"Content-Type": "application/json"},
        timeout=30
    )

    print(f"📊 Status Code: {response.status_code}")
    print()

    if not response.ok:
        print(f"❌ API Error:")
        print("-" * 80)
        error_text = response.text
        print(error_text)
        print("-" * 80)
        print()
        print("Trying gemini-2.5-flash instead...")
        print()

        # Try flash model
        model_name2 = "gemini-2.5-flash"
        url2 = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name2}:generateContent?key={api_key}"

        response2 = requests.post(
            url2,
            json=body,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        print(f"📊 Flash model status: {response2.status_code}")

        if not response2.ok:
            print(f"❌ Flash model also failed:")
            print(response2.text)
            sys.exit(1)
        else:
            response = response2
            model_name = model_name2

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
            print(text)
        print("-" * 80)
        print()
        print(f"✅ {model_name} API is working!")
        print()
        print("This confirms the API key is valid for basic Gemini use.")
        print("The Google Search grounding feature may require:")
        print("  - Special API access/permissions")
        print("  - Different API tier (paid/enterprise)")
        print("  - May not be available with current key")
    else:
        print("❌ No candidates in response")
        print(json.dumps(data, indent=2))

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
