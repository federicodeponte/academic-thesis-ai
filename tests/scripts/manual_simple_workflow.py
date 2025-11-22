#!/usr/bin/env python3
"""
Test a simplified version of the paper writing workflow
"""
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

print("🧪 Testing Multi-Agent Workflow (Simplified)")
print("=" * 60)

# Test 1: Scout Agent (simplified)
print("\n1️⃣ SCOUT AGENT - Find papers")
print("-" * 60)
scout_prompt = """
You are a research scout. Find 5 highly-cited papers on "BERT for text classification".
Return as JSON with: title, authors, year, why_relevant.
"""
response1 = model.generate_content(scout_prompt)
print(response1.text[:500])

# Test 2: Architect Agent (simplified)
print("\n\n2️⃣ ARCHITECT AGENT - Create outline")
print("-" * 60)
architect_prompt = """
You are a paper architect. Create a simple outline for a paper about "BERT for text classification".
Include: Introduction, Related Work, Methods, Results, Conclusion.
Keep it brief (200 words max).
"""
response2 = model.generate_content(architect_prompt)
print(response2.text)

# Test 3: Crafter Agent (simplified)
print("\n\n3️⃣ CRAFTER AGENT - Write introduction")
print("-" * 60)
crafter_prompt = """
You are an academic writer. Write a 150-word introduction for a paper on "BERT for text classification".
Include: hook, context, gap, your contribution. Use academic tone.
"""
response3 = model.generate_content(crafter_prompt)
print(response3.text)

# Test 4: Entropy Agent (simplified)
print("\n\n4️⃣ ENTROPY AGENT - Humanize text")
print("-" * 60)
text_to_humanize = response3.text
entropy_prompt = f"""
You are a style editor. Make this text more natural and less AI-like:
- Vary sentence length
- Add natural transitions
- Remove AI patterns like "it is important to note"

Text to improve:
{text_to_humanize}
"""
response4 = model.generate_content(entropy_prompt)
print(response4.text)

print("\n" + "=" * 60)
print("✅ All 4 agents tested successfully!")
