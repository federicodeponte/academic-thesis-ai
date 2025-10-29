#!/usr/bin/env python3
"""
Test: Generate content with AI → Export to PDF
"""
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

print("📝 Generating mini-paper with AI...")

# Generate a short academic paper
prompt = """
Write a 500-word academic paper (in Markdown format) about:
"The Impact of Transformers on Natural Language Processing"

Include:
# Title
## Abstract
## Introduction  
## Main Contribution
## Conclusion

Use proper academic tone. Include 3 example citations (you can make them up for this test).
"""

response = model.generate_content(prompt)
paper_content = response.text

# Save to markdown
with open('ai_generated_paper.md', 'w') as f:
    f.write(paper_content)

print("✅ AI-generated paper saved to: ai_generated_paper.md")
print(f"📊 Length: {len(paper_content)} characters\n")
print("Preview:")
print("-" * 60)
print(paper_content[:800])
print("...")
print("-" * 60)

# Now export to PDF using our utility
print("\n📄 Exporting to PDF...")
import subprocess
result = subprocess.run(
    ['python3', 'utils/export.py', '--format', 'pdf', '--output', 'ai_paper.pdf', 'ai_generated_paper.md'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ PDF export successful!")
    subprocess.run(['ls', '-lh', 'ai_paper.pdf'])
else:
    print("❌ Export failed:")
    print(result.stderr)
