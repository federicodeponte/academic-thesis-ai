#!/usr/bin/env python3
import os
import google.generativeai as genai

# Configure API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Test simple prompt
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content("Say 'API key works!' if you can read this.")

print("✅ Gemini API Response:")
print(response.text)
