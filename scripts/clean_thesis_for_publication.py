#!/usr/bin/env python3
"""
ABOUTME: Strip metadata from thesis markdown files for clean PDF publication
ABOUTME: Removes YAML frontmatter and section metadata headers
"""

import re
import sys
from pathlib import Path
from typing import List


def remove_yaml_frontmatter(content: str) -> str:
    """
    Remove YAML frontmatter from markdown content.

    Removes everything from first --- to second --- (inclusive).

    Args:
        content: Markdown content with YAML frontmatter

    Returns:
        Content without frontmatter
    """
    # Pattern: starts with ---, followed by anything, ending with ---
    pattern = r'^---\s*\n.*?\n---\s*\n'
    cleaned = re.sub(pattern, '', content, count=1, flags=re.DOTALL | re.MULTILINE)
    return cleaned


def remove_metadata_headers(content: str) -> str:
    """
    Remove metadata headers from thesis content.

    Removes lines like:
    - **Section:** Introduction
    - **Word Count:** 1200
    - **Status:** Draft v1 (Humanized)
    - **Abschnitt:** Einleitung (German)
    - **Wortzahl:** 1200 (German)

    Args:
        content: Markdown content

    Returns:
        Content without metadata headers
    """
    lines = content.split('\n')
    cleaned_lines = []

    # Metadata patterns to remove (English and German)
    metadata_patterns = [
        r'^\*\*Section:\*\*',
        r'^\*\*Word Count:\*\*',
        r'^\*\*Status:\*\*',
        r'^\*\*Abschnitt:\*\*',
        r'^\*\*Wortzahl:\*\*',
        r'^\*\*Citations Used:\*\*',
        r'^\*\*Research Problem',
        r'^\*\*Key Findings',
        r'^\*\*Significance',
    ]

    for line in lines:
        # Check if line matches any metadata pattern
        is_metadata = False
        for pattern in metadata_patterns:
            if re.match(pattern, line.strip()):
                is_metadata = True
                break

        # Keep line if it's not metadata
        if not is_metadata:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def remove_metadata_sections(content: str) -> str:
    """
    Remove entire metadata sections from thesis content.

    Removes sections like:
    - ## Content / ## Inhalt (section markers)
    - ## Citations Used (with all numbered lists)
    - ## Notes for Revision (with all checklists)
    - ## Word Count Breakdown (with all breakdowns)

    Args:
        content: Markdown content

    Returns:
        Content without metadata sections
    """
    lines = content.split('\n')
    cleaned_lines = []
    skip_until_next_heading = False

    # Metadata section headings to remove (including their content)
    metadata_section_patterns = [
        r'^##\s+Content\s*$',
        r'^##\s+Inhalt\s*$',  # German
        r'^##\s+Citations Used\s*$',
        r'^##\s+Notes for Revision\s*$',
        r'^##\s+Word Count Breakdown\s*$',
    ]

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if this is a metadata section heading
        is_metadata_section = False
        for pattern in metadata_section_patterns:
            if re.match(pattern, stripped):
                is_metadata_section = True
                skip_until_next_heading = True
                break

        if is_metadata_section:
            continue  # Skip this heading

        # If we're skipping, check if we've hit the next real heading
        if skip_until_next_heading:
            # Check if this is a new heading (## or # but NOT the metadata ones)
            if re.match(r'^#{1,6}\s+\w', stripped):
                # This is a new heading - stop skipping
                skip_until_next_heading = False
                cleaned_lines.append(line)
            # Otherwise keep skipping (this is content of the metadata section)
        else:
            # Not skipping - keep this line
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def remove_style_variance_report(content: str) -> str:
    """
    Remove Style Variance Report and all metadata from thesis content.

    Removes:
    - Style Variance Report section
    - Entropy scores and AI detection metrics
    - Example transformations
    - Anti-AI detection technique documentation
    - AI Detection Testing sections
    - Cautions sections
    - Humanized Introduction metadata

    Keeps only real academic content starting from first academic section heading.

    Args:
        content: Markdown content

    Returns:
        Content without metadata
    """
    lines = content.split('\n')

    # Find thesis title (first level-1 heading with capital letter)
    title_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^#\s+[A-ZÄÖÜßÉÈÊÀÂÙÛÔÇ]', stripped):  # Support German/French characters
            title_idx = i
            break

    if title_idx is None:
        # No title found, return as-is
        return content

    # Academic section keywords (English and German)
    academic_keywords = [
        r'Introduction',
        r'Einleitung',
        r'Abstract',
        r'Zusammenfassung',
        r'Background',
        r'Hintergrund',
        r'Literature Review',
        r'Literaturübersicht',
        r'Literaturüberblick',
        r'Methodology',
        r'Methodik',
        r'Methods',
        r'Methoden',
        r'Results',
        r'Ergebnisse',
        r'Analysis',
        r'Analyse',
        r'Discussion',
        r'Diskussion',
        r'Conclusion',
        r'Fazit',
        r'Schlussfolgerung',
        r'References',
        r'Literaturverzeichnis',
        r'Appendix',
        r'Anhang',
        r'Acknowledgments',
        r'Danksagung',
        r'The Genesis',  # Special case for "The Genesis and Evolution"
        r'Die Entstehung',  # German equivalent
    ]

    # Find first academic section (level-2 or level-3 heading with academic keyword)
    first_academic_section_idx = None
    for i in range(title_idx + 1, len(lines)):
        stripped = lines[i].strip()
        # Check if this is a heading (level 2 or 3)
        if re.match(r'^#{2,3}\s+', stripped):
            # Check if it contains academic keywords
            for keyword in academic_keywords:
                if re.search(keyword, stripped, re.IGNORECASE):
                    first_academic_section_idx = i
                    break
            if first_academic_section_idx:
                break

    if first_academic_section_idx is None:
        # No academic section found, keep from title onwards (safe fallback)
        return '\n'.join(lines[title_idx:])

    # Keep title + first academic section onwards
    # Skip everything between title and first academic section (metadata)
    cleaned_lines = [lines[title_idx]] + lines[first_academic_section_idx:]
    return '\n'.join(cleaned_lines)


def remove_excessive_dividers(content: str) -> str:
    """
    Remove excessive horizontal rule dividers (---).

    Keeps dividers that appear to be legitimate section breaks,
    but removes those that are only separating metadata sections.

    Strategy: Remove dividers that have empty lines or other dividers nearby.

    Args:
        content: Markdown content

    Returns:
        Content with reduced dividers
    """
    lines = content.split('\n')
    cleaned_lines = []

    for i, line in enumerate(lines):
        # Check if this is a horizontal rule
        if re.match(r'^---\s*$', line.strip()):
            # Check context: is this divider surrounded by empty lines?
            prev_empty = (i == 0 or not lines[i-1].strip())
            next_empty = (i == len(lines)-1 or not lines[i+1].strip())

            # If divider is surrounded by empty lines, it's likely metadata separation
            if prev_empty and next_empty:
                continue  # Skip this divider

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def remove_placeholder_text(content: str) -> str:
    """
    Remove placeholder text patterns from thesis content.

    Removes patterns like:
    - [To be completed with proper citations]
    - [To be completed...]
    - [VERIFY]
    - [TODO: ...]

    Args:
        content: Markdown content

    Returns:
        Content without placeholder text
    """
    # Remove common placeholder patterns
    patterns = [
        r'\[To be completed with proper citations\]',
        r'\[To be completed.*?\]',
        r'\[VERIFY\]',
        r'\[TODO:.*?\]',
        r'\[PLACEHOLDER.*?\]',
        r'\[INSERT.*?\]',
    ]

    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)

    return content


def deduplicate_references_headers(content: str) -> str:
    """
    Remove duplicate "## References" headers.

    If there are multiple consecutive References sections, keep only the first one
    and merge the content.

    Args:
        content: Markdown content

    Returns:
        Content with deduplicated References headers
    """
    lines = content.split('\n')
    cleaned_lines = []
    last_was_references = False

    for line in lines:
        stripped = line.strip()

        # Check if this is a References header
        is_references_header = (
            re.match(r'^##\s+References\s*$', stripped) or
            re.match(r'^##\s+Literaturverzeichnis\s*$', stripped)  # German
        )

        if is_references_header:
            # Only add if we haven't just seen a References header
            if not last_was_references:
                cleaned_lines.append(line)
                last_was_references = True
            # Otherwise skip this duplicate header
        else:
            cleaned_lines.append(line)
            # Reset flag if we see non-empty content
            if stripped:
                last_was_references = False

    return '\n'.join(cleaned_lines)


def remove_appendix_b_checklists(content: str) -> str:
    """
    Remove Appendix B implementation checklists from thesis content.

    Removes entire Appendix B sections that contain implementation checklists
    with checkbox items, which are development metadata rather than academic content.

    Removes sections like:
    - ## Appendix B: AI Agent Pricing Strategy Checklist for Providers
    - ## Anhang B: Implementierungs-Checkliste für CO2-Bepreisungsprojekte
    - ## Appendix B: Open Source Project Adoption and Implementation Checklist

    Args:
        content: Markdown content

    Returns:
        Content without Appendix B checklists
    """
    lines = content.split('\n')
    cleaned_lines = []
    skip_appendix_b = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if this is Appendix B heading (English or German)
        if re.match(r'^##\s+Appendix B:', stripped) or re.match(r'^##\s+Anhang B:', stripped):
            skip_appendix_b = True
            continue  # Skip Appendix B heading

        # If we're skipping Appendix B, check if we've hit Appendix C or another major section
        if skip_appendix_b:
            # Check if this is Appendix C (or Anhang C) or another major heading
            if (re.match(r'^##\s+Appendix [C-Z]:', stripped) or
                re.match(r'^##\s+Anhang [C-Z]:', stripped) or
                re.match(r'^#\s+', stripped)):  # Also stop at top-level headings
                # This is a new section - stop skipping
                skip_appendix_b = False
                cleaned_lines.append(line)
            # Otherwise keep skipping (this is content of Appendix B)
        else:
            # Not skipping - keep this line
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def clean_thesis_markdown(input_file: Path, output_file: Path = None) -> None:
    """
    Clean thesis markdown file for publication.

    Args:
        input_file: Path to FINAL_THESIS.md
        output_file: Output path (defaults to input_file with _CLEAN suffix)
    """
    # Default output file
    if output_file is None:
        output_file = input_file.parent / f"{input_file.stem}_CLEAN{input_file.suffix}"

    print(f"📄 Reading: {input_file}")

    # Read original content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_lines = len(content.split('\n'))
    print(f"   Original: {original_lines} lines")

    # Remove YAML frontmatter
    print(f"   Removing YAML frontmatter...")
    content = remove_yaml_frontmatter(content)

    # Remove Style Variance Report from beginning
    print(f"   Removing Style Variance Report...")
    content = remove_style_variance_report(content)

    # Remove metadata section headings (## Content, ## Citations Used, etc.)
    print(f"   Removing metadata sections...")
    content = remove_metadata_sections(content)

    # Remove Appendix B implementation checklists
    print(f"   Removing Appendix B implementation checklists...")
    content = remove_appendix_b_checklists(content)

    # Remove inline metadata headers (**Section:**, **Word Count:**, etc.)
    print(f"   Removing metadata headers...")
    content = remove_metadata_headers(content)

    # Remove placeholder text patterns
    print(f"   Removing placeholder text...")
    content = remove_placeholder_text(content)

    # Deduplicate References headers
    print(f"   Deduplicating References headers...")
    content = deduplicate_references_headers(content)

    # Remove excessive horizontal dividers
    print(f"   Removing excessive dividers...")
    content = remove_excessive_dividers(content)

    # Clean up excessive blank lines (more than 2 consecutive)
    print(f"   Cleaning up blank lines...")
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # Remove leading/trailing whitespace
    content = content.strip() + '\n'

    cleaned_lines = len(content.split('\n'))
    print(f"   Cleaned: {cleaned_lines} lines")
    print(f"   Removed: {original_lines - cleaned_lines} lines")

    # Write cleaned content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Saved: {output_file}")
    print()


def main():
    """Main entry point."""
    print("="*80)
    print("THESIS CLEANER - Remove Metadata for Publication")
    print("="*80)
    print()

    # Get input file from command line or use defaults
    if len(sys.argv) > 1:
        input_files = [Path(sys.argv[1])]
    else:
        # Default: clean all 3 thesis files
        base_dir = Path(__file__).parent.parent
        input_files = [
            base_dir / "tests/outputs/opensource_thesis/FINAL_THESIS.md",
            base_dir / "tests/outputs/ai_pricing_thesis/FINAL_THESIS.md",
            base_dir / "tests/outputs/co2_thesis_german/FINAL_THESIS.md",
        ]

    # Clean each file
    cleaned_count = 0
    for input_file in input_files:
        if not input_file.exists():
            print(f"❌ File not found: {input_file}")
            continue

        clean_thesis_markdown(input_file)
        cleaned_count += 1

    print("="*80)
    print(f"✅ Cleaned {cleaned_count} thesis file(s)")
    print("="*80)
    print()
    print("Next steps:")
    print("1. Review cleaned files (*_CLEAN.md)")
    print("2. Export to PDF using your PDF generation tool")
    print("3. Replace PDFs in examples/ directory")
    print("4. Push to GitHub")


if __name__ == "__main__":
    main()
