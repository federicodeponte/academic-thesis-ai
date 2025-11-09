#!/usr/bin/env python3
"""
Generate full academic abstracts for theses with placeholder abstracts.

This script:
1. Detects placeholder abstracts in thesis markdown files
2. Extracts key sections (Introduction, Conclusion) for context
3. Calls Gemini API to generate a 4-paragraph abstract
4. Replaces placeholder with generated content
5. Creates backups before modification

Usage: python scripts/generate_missing_abstracts.py
"""

import sys
import re
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from google import genai
from google.genai import types
from config import get_config

# Initialize Gemini client
config = get_config()
client = genai.Client(api_key=config.google_api_key)

def has_placeholder_abstract(md_content: str) -> bool:
    """Check if thesis has a placeholder abstract."""
    return "[Abstract will be automatically generated" in md_content or \
           "[Zusammenfassung wird während der PDF-Generierung" in md_content

def extract_thesis_sections(md_content: str, language: str = 'english') -> dict:
    """Extract beginning and ending content for abstract generation."""
    sections = {}

    # Extract title for context
    title_match = re.search(r'^title:\s*"([^"]+)"', md_content, re.MULTILINE)
    if title_match:
        sections['title'] = title_match.group(1)

    # Find where actual content starts (after frontmatter, TOC, and abstract placeholder)
    # Look for the first major chapter heading (# followed by text)
    content_start = 0

    # Skip YAML frontmatter
    if md_content.startswith('---'):
        end_frontmatter = md_content.find('---', 3)
        if end_frontmatter != -1:
            content_start = end_frontmatter + 3

    # Skip title page and TOC
    toc_match = re.search(r'## (Table of Contents|Inhaltsverzeichnis)', md_content[content_start:])
    if toc_match:
        content_start += toc_match.end()

    # Skip abstract placeholder
    abstract_match = re.search(r'## (Abstract|Zusammenfassung)', md_content[content_start:])
    if abstract_match:
        # Find where abstract section ends
        abstract_start = content_start + abstract_match.start()
        newpage_match = re.search(r'\\newpage', md_content[abstract_start:])
        if newpage_match:
            content_start = abstract_start + newpage_match.end()

    # Extract first major content section (introduction equivalent)
    main_content = md_content[content_start:].strip()

    # Get first 3000 chars of actual content as "introduction"
    sections['introduction'] = main_content[:3000]

    # Try to find Conclusion section
    if language == 'german':
        conc_pattern = r'# (Conclusion|Fazit|Schlussfolgerung)\n+(.*?)(?=\n---|$)'
    else:
        conc_pattern = r'# (Conclusion|Fazit)\n+(.*?)(?=\n---|$)'

    conc_match = re.search(conc_pattern, md_content, re.DOTALL)
    if conc_match:
        sections['conclusion'] = conc_match.group(2).strip()[:3000]
    else:
        # If no conclusion section found, use last 3000 chars before references
        refs_pattern = r'\n---\n+\d+\.'
        refs_match = re.search(refs_pattern, md_content)
        if refs_match:
            sections['conclusion'] = md_content[max(0, refs_match.start() - 3000):refs_match.start()].strip()
        else:
            # Just use last 3000 chars
            sections['conclusion'] = md_content[-3000:].strip()

    return sections

def generate_abstract_gemini(thesis_content: dict, language: str = 'english') -> str:
    """Generate 4-paragraph academic abstract using Gemini."""

    title = thesis_content.get('title', 'Academic Thesis')
    introduction = thesis_content.get('introduction', '')
    conclusion = thesis_content.get('conclusion', '')

    if language == 'german':
        prompt = f"""Du bist ein akademischer Schreiber für wissenschaftliche Zusammenfassungen.

TITEL DER THESIS: {title}

EINLEITUNG (AUSZUG):
{introduction[:1500]}

FAZIT (AUSZUG):
{conclusion[:1500]}

AUFGABE: Schreibe eine professionelle akademische Zusammenfassung mit GENAU 4 Absätzen (250-300 Wörter):

**Forschungsproblem und Ansatz:** [2-3 Sätze - Was ist das Problem? Warum ist es wichtig?]

**Methodik und Ergebnisse:** [2-3 Sätze - Wie wurde geforscht? Was wurde gefunden?]

**Wichtigste Beiträge:** [2-3 Sätze mit nummerierten Punkten (1), (2), (3)]

**Implikationen:** [2-3 Sätze - Was bedeutet das für Theorie und Praxis?]

**Schlüsselwörter:** [12-15 relevante Schlüsselwörter, kommagetrennt]

REGELN:
- Akademischer, professioneller Ton
- Keine Meta-Kommentare wie "Hier ist die Zusammenfassung"
- Beginne direkt mit dem ersten Absatz
- Genau diese 4-Absatz-Struktur verwenden
- 250-300 Wörter insgesamt
"""
    else:
        prompt = f"""You are an academic abstract writer for scholarly publications.

THESIS TITLE: {title}

INTRODUCTION (EXCERPT):
{introduction[:1500]}

CONCLUSION (EXCERPT):
{conclusion[:1500]}

TASK: Write a professional academic abstract with EXACTLY 4 paragraphs (250-300 words):

**Research Problem and Approach:** [2-3 sentences - What problem is addressed? Why is it important?]

**Methodology and Findings:** [2-3 sentences - How was the research conducted? What was discovered?]

**Key Contributions:** [2-3 sentences with numbered points (1), (2), (3)]

**Implications:** [2-3 sentences - What does this mean for theory and practice?]

**Keywords:** [12-15 relevant keywords, comma-separated]

RULES:
- Academic, professional tone
- No meta-comments like "Here is the abstract"
- Start directly with the first paragraph
- Use exactly this 4-paragraph structure
- 250-300 words total
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,  # Low temperature for consistent academic writing
                max_output_tokens=800,
            )
        )

        abstract = response.text.strip()

        # Clean up any meta-text that might have been added
        abstract = re.sub(r'^(Here is the abstract|Hier ist die Zusammenfassung).*?\n+', '', abstract, flags=re.IGNORECASE)

        return abstract

    except Exception as e:
        print(f"❌ ERROR generating abstract with Gemini: {e}")
        return None

def replace_placeholder_abstract(md_content: str, new_abstract: str, language: str = 'english') -> str:
    """Replace placeholder abstract with generated content."""

    if language == 'german':
        placeholder_pattern = r'## Zusammenfassung\n+\[Zusammenfassung wird während der PDF-Generierung.*?\]\n+\\newpage'
        replacement = f"## Zusammenfassung\n\n{new_abstract}\n\n\\newpage"
    else:
        placeholder_pattern = r'## Abstract\n+\[Abstract will be automatically generated.*?\]\n+\\newpage'
        replacement = f"## Abstract\n\n{new_abstract}\n\n\\newpage"

    updated_content = re.sub(placeholder_pattern, replacement, md_content, flags=re.DOTALL)

    return updated_content

def count_words(text: str) -> int:
    """Count words in text."""
    return len(re.findall(r'\b\w+\b', text))

def process_thesis(thesis_path: Path, language: str = 'english') -> bool:
    """Process a single thesis to generate abstract."""

    print(f"\n{'='*80}")
    print(f"Processing: {thesis_path.name}")
    print(f"{'='*80}")

    # Read thesis content
    with open(thesis_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Check if placeholder exists
    if not has_placeholder_abstract(original_content):
        print("✅ SKIPPED - Already has a full abstract")
        return True

    print("📝 Placeholder abstract detected - generating full abstract...")

    # Extract sections
    sections = extract_thesis_sections(original_content, language)

    if not sections.get('introduction') or not sections.get('conclusion'):
        print("❌ ERROR: Could not extract Introduction or Conclusion sections")
        return False

    print(f"  • Title: {sections.get('title', 'Unknown')}")
    print(f"  • Introduction: {len(sections['introduction'])} chars")
    print(f"  • Conclusion: {len(sections['conclusion'])} chars")

    # Generate abstract
    print("\n🤖 Calling Gemini to generate abstract...")
    new_abstract = generate_abstract_gemini(sections, language)

    if not new_abstract:
        print("❌ ERROR: Failed to generate abstract")
        return False

    word_count = count_words(new_abstract)
    print(f"✅ Abstract generated: {word_count} words")

    if word_count < 200 or word_count > 350:
        print(f"⚠️  WARNING: Word count outside target range (250-300)")

    # Replace placeholder
    updated_content = replace_placeholder_abstract(original_content, new_abstract, language)

    if updated_content == original_content:
        print("❌ ERROR: Failed to replace placeholder abstract")
        return False

    # Create backup
    backup_path = thesis_path.parent / f"{thesis_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"💾 Backup created: {backup_path.name}")

    # Write updated content
    with open(thesis_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"✅ Abstract written to: {thesis_path.name}")

    # Show preview
    print(f"\n📄 ABSTRACT PREVIEW:")
    print("-" * 80)
    preview = new_abstract[:300] + "..." if len(new_abstract) > 300 else new_abstract
    print(preview)
    print("-" * 80)

    return True

# Configuration for theses
theses_to_process = [
    {
        'path': project_root / 'tests/outputs/opensource_thesis/FINAL_THESIS.md',
        'language': 'english',
        'name': 'Open Source Thesis'
    },
    {
        'path': project_root / 'tests/outputs/co2_thesis_german/FINAL_THESIS.md',
        'language': 'german',
        'name': 'CO2 German Thesis'
    }
]

if __name__ == '__main__':
    print("="*80)
    print("ABSTRACT GENERATION FOR INCOMPLETE THESES")
    print("="*80)
    print("\nTarget: Generate full abstracts for theses with placeholders")
    print("Expected: 250-300 words, 4-paragraph academic format")
    print()

    success_count = 0
    total_count = len(theses_to_process)

    for thesis_config in theses_to_process:
        thesis_path = thesis_config['path']

        if not thesis_path.exists():
            print(f"\n❌ ERROR: File not found: {thesis_path}")
            continue

        success = process_thesis(
            thesis_path=thesis_path,
            language=thesis_config['language']
        )

        if success:
            success_count += 1

    print("\n" + "="*80)
    print("ABSTRACT GENERATION COMPLETE")
    print("="*80)
    print(f"\nResults: {success_count}/{total_count} theses processed successfully")

    if success_count == total_count:
        print("\n✅ ALL THESES NOW HAVE FULL ABSTRACTS")
        print("\nNext step: Regenerate PDFs to verify 100% completion")
    else:
        print(f"\n⚠️  WARNING: {total_count - success_count} thesis/theses failed to process")

    print("="*80)
