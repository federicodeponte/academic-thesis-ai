#!/usr/bin/env python3
"""
ABOUTME: Quality gate - validate thesis is publication-ready before marking as FINAL
ABOUTME: Checks for [VERIFY], [MISSING], {cite_MISSING} markers, and required sections
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict


def check_verify_markers(content: str) -> Tuple[int, List[str]]:
    """
    Find all [VERIFY] placeholders in content.

    Returns:
        (count, list of examples)
    """
    pattern = r'\[VERIFY[^\]]*\]'
    matches = re.findall(pattern, content, re.IGNORECASE)

    # Get unique examples (max 10)
    unique_examples = list(set(matches))[:10]

    return len(matches), unique_examples


def check_missing_citations(content: str) -> Tuple[int, List[str]]:
    """
    Find {cite_MISSING:...} placeholders.

    Returns:
        (count, list of topics)
    """
    pattern = r'\{cite_MISSING:([^}]+)\}'
    matches = re.findall(pattern, content)

    return len(matches), matches[:10]


def check_missing_bracket_markers(content: str) -> Tuple[int, List[str]]:
    """
    Find [MISSING: ...] placeholders.

    These are created when Scout agent fails to research citations.
    They're just as critical as [VERIFY] markers.

    Returns:
        (count, list of examples)
    """
    pattern = r'\[MISSING:([^\]]+)\]'
    matches = re.findall(pattern, content)

    # Get unique examples (max 10)
    unique_examples = list(set(matches))[:10]

    return len(matches), unique_examples


def check_required_sections(content: str) -> Dict[str, bool]:
    """
    Check if thesis has all required sections (multilingual support).

    Supports English, German, Spanish, French section names.
    Handles both numbered (e.g., "# 3. Methodology") and non-numbered (e.g., "## Methodology") sections.

    Returns:
        Dict of section_name: present (bool)
    """
    # FIXED (Bug #13): Added (\d+\.?\s*)? to match optional numbered sections
    # FIXED (Bug #18): Extended regex to handle Roman numerals, Chapter prefixes, and various numbering formats
    # Examples:
    #   - Plain: "# Methodology"
    #   - Numbered: "# 3. Methodology", "## 3.1 Methodology"
    #   - Roman numerals: "# I. Introduction", "# IV. Methodology"
    #   - Chapter prefix: "# Chapter 1: Methodology", "# Kapitel 3: Methodik"
    #   - Mixed: "# Chapter I: Introduction"

    # Comprehensive number prefix pattern (handles Arabic, Roman, Chapter prefix)
    # (?:...) = non-capturing group
    # (Chapter|Kapitel|Capítulo|Chapitre)?\s* = optional chapter prefix
    # ([IVXLCDM]+|\d+)\.?\s* = Roman numerals OR Arabic numbers, optional dot
    # [:\-]?\s* = optional colon or dash separator
    number_prefix = r'((?:Chapter|Kapitel|Cap[íi]tulo|Chapitre)?\s*([IVXLCDM]+|\d+)[\.:;\-]?\s*)?'

    sections = {
        'Abstract': rf'#+\s*{number_prefix}(Abstract|Zusammenfassung|Resumen|Résumé)',
        'Introduction': rf'#+\s*{number_prefix}(Introduction|Einleitung|Introducción)',
        'Literature Review': rf'#+\s*{number_prefix}(Literature Review|Literaturübersicht|Literaturüberblick|Revisión de Literatura|Revue de Littérature)',
        'Methodology': rf'#+\s*{number_prefix}(Methodology|Method|Methodik|Metodología|Méthodologie)',
        'References': rf'#+\s*{number_prefix}(References|Literaturverzeichnis|Bibliografie|Bibliografia|Références)',
    }

    results = {}
    for section_name, pattern in sections.items():
        results[section_name] = bool(re.search(pattern, content, re.IGNORECASE))

    return results


def validate_thesis(file_path: Path, verbose: bool = True) -> bool:
    """
    Validate thesis is publication-ready.

    Returns:
        True if publication-ready, False otherwise
    """
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if verbose:
        print(f"\n{'='*70}")
        print(f"📋 THESIS QUALITY VALIDATION: {file_path.name}")
        print(f"{'='*70}\n")

    # Track overall status
    is_valid = True

    # Check 1: [VERIFY] markers
    verify_count, verify_examples = check_verify_markers(content)
    if verify_count > 0:
        is_valid = False
        if verbose:
            print(f"❌ Found {verify_count} [VERIFY] placeholders")
            print(f"   Examples:")
            for example in verify_examples[:5]:
                print(f"   - {example}")
            print()
    elif verbose:
        print(f"✅ No [VERIFY] markers found")

    # Check 2: Missing citations
    missing_count, missing_topics = check_missing_citations(content)
    if missing_count > 0:
        is_valid = False
        if verbose:
            print(f"❌ Found {missing_count} missing citations {{cite_MISSING:...}}")
            print(f"   Topics:")
            for topic in missing_topics[:5]:
                print(f"   - {topic}")
            print()
    elif verbose:
        print(f"✅ No missing citation placeholders")

    # Check 3: [MISSING: ...] markers (Scout agent failures)
    missing_bracket_count, missing_bracket_examples = check_missing_bracket_markers(content)
    if missing_bracket_count > 0:
        is_valid = False
        if verbose:
            print(f"❌ Found {missing_bracket_count} [MISSING: ...] markers (Scout agent failures)")
            print(f"   Examples:")
            for example in missing_bracket_examples[:5]:
                print(f"   - [MISSING: {example}]")
            print()
    elif verbose:
        print(f"✅ No [MISSING] bracket markers")

    # Check 4: Required sections
    sections = check_required_sections(content)
    missing_sections = [name for name, present in sections.items() if not present]

    if missing_sections:
        is_valid = False
        if verbose:
            print(f"❌ Missing required sections: {', '.join(missing_sections)}")
    elif verbose:
        print(f"✅ All required sections present")

    # Check 4: Word count
    word_count = len(content.split())
    if verbose:
        print(f"\n📊 Statistics:")
        print(f"   - Word count: {word_count:,}")
        print(f"   - Character count: {len(content):,}")

    if word_count < 8000:
        if verbose:
            print(f"⚠️  Warning: Word count below 8,000 (academic minimum)")

    # Final verdict
    if verbose:
        print(f"\n{'='*70}")
        if is_valid:
            print("✅ THESIS IS PUBLICATION-READY")
        else:
            print("❌ THESIS NOT PUBLICATION-READY")
            print("\nAction required:")
            action_num = 1
            if verify_count > 0:
                print(f"  {action_num}. Fill {verify_count} [VERIFY] placeholders with proper citations")
                action_num += 1
            if missing_count > 0:
                print(f"  {action_num}. Research and add {missing_count} {{cite_MISSING:...}} citations")
                action_num += 1
            if missing_bracket_count > 0:
                print(f"  {action_num}. Research and add {missing_bracket_count} [MISSING: ...] citations (Scout failures)")
                action_num += 1
            if missing_sections:
                print(f"  {action_num}. Add missing sections: {', '.join(missing_sections)}")
        print(f"{'='*70}\n")

    return is_valid


def main():
    """Validate thesis files from command line."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate thesis quality')
    parser.add_argument('file', type=Path, help='Thesis file to validate')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')

    args = parser.parse_args()

    is_valid = validate_thesis(args.file, verbose=not args.quiet)

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
