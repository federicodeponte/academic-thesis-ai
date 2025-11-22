#!/usr/bin/env python3
"""
Test basic Gemini SDK without Google Search grounding
To verify if SDK works for basic use
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("❌ google-generativeai not installed")
    sys.exit(1)

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ GOOGLE_API_KEY not set")
    sys.exit(1)

print("=" * 80)
print("TESTING BASIC GEMINI SDK (NO GOOGLE SEARCH)")
print("=" * 80)
print()

# Configure
genai.configure(api_key=api_key)

# Try different models
models_to_try = [
    'gemini-2.5-flash',
    'gemini-2.5-pro',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
]

print("Testing models without any tools...")
print()

for model_name in models_to_try:
    print(f"🔧 Trying {model_name}...")

    try:
        # Create model WITHOUT tools
        model = genai.GenerativeModel(model_name=model_name)

        # Generate simple content
        response = model.generate_content("What is 2+2? Answer with just the number.")

        print(f"✅ SUCCESS: {model_name} works!")
        print(f"   Response: {response.text}")
        print()
        break

    except Exception as e:
        error_str = str(e)
        if "API key not valid" in error_str:
            print(f"❌ FAILED: API key not valid for {model_name}")
        elif "not found" in error_str or "does not exist" in error_str:
            print(f"⚠️  SKIPPED: {model_name} does not exist")
        else:
            print(f"❌ FAILED: {error_str[:100]}")
        print()

else:
    print("=" * 80)
    print("❌ NO MODELS WORKED")
    print("=" * 80)
    print()
    print("This suggests the GOOGLE_API_KEY is completely invalid")
    print("or needs to be regenerated/replaced.")
    sys.exit(1)
