#!/usr/bin/env python3
"""
Test the Scout Agent with a simple research query
"""
import os
import google.generativeai as genai

# Configure
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Read Scout Agent prompt
with open('prompts/01_research/scout.md', 'r', encoding='utf-8') as f:  # FIXED (Bug #15): Added UTF-8 encoding
    scout_prompt = f.read()

# Simple test query
user_query = """
Topic: "Transformers in natural language processing"

Requirements:
- Focus on papers from 2020-2024
- Include foundational papers
- Prioritize highly-cited work
"""

# Combine prompt with query
full_prompt = f"{scout_prompt}\n\n{user_query}"

print("🔍 Testing Scout Agent...")
print("=" * 50)

# Call Gemini
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content(full_prompt)

print("\n📊 Scout Agent Response:\n")
print(response.text[:2000])  # First 2000 chars
print("\n..." if len(response.text) > 2000 else "")
print("\n" + "=" * 50)
print(f"✅ Total response length: {len(response.text)} characters")
