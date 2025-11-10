#!/usr/bin/env python3
"""
Comprehensive Thesis Repair Script

Fixes all metadata pollution and content preservation issues in showcase theses:
1. Removes H2 metadata sections (## Citations Used, ## Notes for Revision, etc.)
2. Removes inline metadata (**Section:**, **Word Count:**, **Status:**)
3. Restores proper section names (not generic "## Content")
4. Verifies References sections are intact
5. Regenerates clean PDFs

Usage:
    python3 scripts/repair_showcase_theses.py
    python3 scripts/repair_showcase_theses.py --thesis opensource  # Repair specific thesis
"""

import sys
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.output_sanitizer import sanitize_enhanced_file
from utils.section_restorer import restore_sections_in_file


def sanitize_all_variants(output_dir: Path, verbose: bool = True) -> int:
    """
    Sanitize ALL .md files in thesis directory to remove placeholders.

    This catches variant files like FINAL_THESIS_CLEAN.md that users might view.

    Args:
        output_dir: Path to thesis output directory
        verbose: Print detailed progress

    Returns:
        Number of files sanitized
    """
    if verbose:
        print("\n🧹 Sanitizing ALL markdown variants in directory...")

    files_cleaned = 0

    # Get all .md files, excluding backups
    for md_file in sorted(output_dir.glob("*.md")):
        # Skip backup directories
        if "backup" in str(md_file):
            continue

        # Skip section files (06_introduction.md, etc.) - they're pristine
        if md_file.name[0].isdigit() and md_file.name[1].isdigit() and md_file.name[2] == '_':
            # But DO clean numbered compilation files (14_, 15_, 16_)
            if not md_file.name.startswith(('14_', '15_', '16_')):
                continue

        try:
            if verbose:
                print(f"  Sanitizing {md_file.name}...", end=" ")

            success = sanitize_enhanced_file(
                input_path=md_file,
                output_path=None,  # In-place
                verbose=False  # Don't print detailed stats for each file
            )

            if success:
                files_cleaned += 1
                if verbose:
                    print("✅")
            else:
                if verbose:
                    print("⚠️ No changes needed")
        except Exception as e:
            if verbose:
                print(f"❌ Error: {e}")

    if verbose:
        print(f"\n✅ Sanitized {files_cleaned} variant files")

    return files_cleaned


def repair_thesis(thesis_name: str, language: str, output_dir: Path) -> bool:
    """
    Repair a single thesis with all fixes.

    Args:
        thesis_name: Name of thesis (for display)
        language: Language of thesis (english, german, spanish)
        output_dir: Path to thesis output directory

    Returns:
        True if repair succeeded, False otherwise
    """
    print("=" * 80)
    print(f"REPAIRING: {thesis_name}")
    print("=" * 80)

    # Paths
    final_thesis = output_dir / "FINAL_THESIS.md"
    enhanced_file = output_dir / "16_enhanced_final.md"
    pre_enhancement = output_dir / "15_compiled_citations.md"

    if not final_thesis.exists():
        print(f"❌ {final_thesis} not found - skipping")
        return False

    # Step 0: Sanitize ALL markdown variants in directory (catches FINAL_THESIS_CLEAN.md, etc.)
    print("\n🧹 Step 0: Sanitizing ALL markdown variants...")
    variants_cleaned = sanitize_all_variants(output_dir, verbose=True)
    if variants_cleaned > 0:
        print(f"✅ Cleaned {variants_cleaned} variant files")
    else:
        print("✅ No variants needed cleaning")

    # Step 1: Sanitize enhanced output (remove H2 metadata sections, inline metadata)
    print("\n🧹 Step 1: Sanitizing enhanced output...")
    if enhanced_file.exists():
        sanitize_success = sanitize_enhanced_file(
            input_path=enhanced_file,
            output_path=None,  # In-place
            verbose=True
        )

        if sanitize_success:
            print("✅ Sanitization complete")

            # Copy sanitized version to FINAL_THESIS.md
            with open(enhanced_file, 'r', encoding='utf-8') as f:
                sanitized_content = f.read()
            with open(final_thesis, 'w', encoding='utf-8') as f:
                f.write(sanitized_content)
            print(f"✅ Updated {final_thesis} with sanitized content")
        else:
            print("⚠️  Sanitization failed - continuing with existing content")
    else:
        print(f"⚠️  {enhanced_file} not found - skipping sanitization")

    # Step 2: Restore proper section names (if they were replaced with "## Content")
    print("\n🔧 Step 2: Restoring proper section names...")
    if pre_enhancement.exists() and enhanced_file.exists():
        sections_restored = restore_sections_in_file(
            enhanced_path=enhanced_file,
            pre_enhancement_path=pre_enhancement,
            language=language,
            verbose=True
        )

        if sections_restored:
            # Copy restored version to FINAL_THESIS.md
            with open(enhanced_file, 'r', encoding='utf-8') as f:
                restored_content = f.read()
            with open(final_thesis, 'w', encoding='utf-8') as f:
                f.write(restored_content)
            print(f"✅ Updated {final_thesis} with restored sections")
        else:
            print("✅ No section restoration needed - all sections intact")
    else:
        print(f"⚠️  Backup files not found - skipping section restoration")

    # Step 3: Verify References section exists
    print("\n📚 Step 3: Verifying References section...")
    with open(final_thesis, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for References section based on language
    references_headers = {
        'english': ['## References', '## Bibliography'],
        'german': ['## Literaturverzeichnis', '## Quellenverzeichnis', '## References'],
        'spanish': ['## Referencias', '## Bibliografía', '## References'],
    }

    headers = references_headers.get(language, references_headers['english'])
    references_found = any(header in content for header in headers)

    if not references_found:
        print(f"❌ References section not found!")
        print(f"   Checked for: {', '.join(headers)}")
        print(f"   You may need to manually restore from {pre_enhancement}")
        return False

    # Check if References section is empty (just header, no citations)
    references_empty = True
    for header in headers:
        if header in content:
            # Extract content after References header
            refs_start = content.find(header)
            refs_section = content[refs_start:]

            # Check if there's any content after header (more than just blank lines)
            refs_lines = [line.strip() for line in refs_section.split('\n')[1:] if line.strip()]
            if len(refs_lines) > 0:
                references_empty = False
                print(f"✅ References section found with {len(refs_lines)} lines of content")
                break

    if references_empty:
        print(f"⚠️  References section exists but appears empty")
        print(f"   You may need to manually restore from {pre_enhancement}")
        # Don't fail - sanitization still succeeded

    # Step 4: Regenerate PDF with pandoc directly
    print("\n📤 Step 4: Regenerating PDF...")
    try:
        pdf_path = output_dir / "FINAL_THESIS.pdf"

        # Use pandoc directly with academic formatting
        result = subprocess.run([
            'pandoc',
            str(final_thesis),
            '-o', str(pdf_path),
            '--pdf-engine=xelatex',
            '-V', 'fontsize=12pt',           # Standard academic font size
            '-V', 'linestretch=1.5',          # 1.5 line spacing (academic standard)
            '-V', 'geometry:margin=1in',
            '-V', 'documentclass=article',
            '--toc',                          # Table of contents
            '--toc-depth=3',
            '--number-sections',              # Number sections
            '--quiet'
        ], capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            pdf_size = pdf_path.stat().st_size
            print(f"✅ PDF regenerated: {pdf_size:,} bytes")
        else:
            print(f"⚠️  PDF export failed: {result.stderr}")
            # Don't fail the whole repair if PDF generation fails
            print(f"⚠️  Continuing without PDF regeneration")
    except FileNotFoundError:
        print(f"⚠️  pandoc not found - skipping PDF regeneration")
        print(f"   Install with: sudo apt-get install texlive-xetex")
    except Exception as e:
        print(f"⚠️  PDF export error: {e}")
        print(f"⚠️  Continuing without PDF regeneration")

    # Step 5: Copy PDF to examples/ for GitHub Pages
    print("\n📤 Step 5: Copying PDF to examples/ for GitHub Pages...")
    try:
        import shutil
        project_root = Path(__file__).parent.parent
        examples_dir = project_root / "examples"
        examples_dir.mkdir(exist_ok=True)

        # Determine destination filename based on thesis
        if 'opensource' in str(output_dir).lower():
            dest_name = 'opensource_thesis.pdf'
        elif 'ai_pricing' in str(output_dir).lower():
            dest_name = 'ai_pricing_thesis.pdf'
        elif 'co2' in str(output_dir).lower():
            dest_name = 'co2_thesis_german.pdf'
        else:
            dest_name = 'FINAL_THESIS.pdf'

        source_pdf = output_dir / "FINAL_THESIS.pdf"
        dest_pdf = examples_dir / dest_name

        if source_pdf.exists():
            shutil.copy2(source_pdf, dest_pdf)
            dest_size = dest_pdf.stat().st_size
            print(f"✅ Copied to {dest_pdf} ({dest_size:,} bytes)")
        else:
            print(f"⚠️  Source PDF not found: {source_pdf}")
    except Exception as e:
        print(f"⚠️  Failed to copy to examples/: {e}")
        print(f"⚠️  Continuing anyway")

    print("\n" + "=" * 80)
    print(f"✅ {thesis_name} REPAIR COMPLETE")
    print("=" * 80)
    return True


def main():
    """Repair all showcase theses."""
    import argparse

    parser = argparse.ArgumentParser(description='Repair showcase theses')
    parser.add_argument('--thesis', choices=['opensource', 'ai_pricing', 'co2_thesis_german', 'all'],
                       default='all', help='Which thesis to repair (default: all)')
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    tests_output = project_root / "tests" / "outputs"

    # Define theses to repair
    theses = {
        'opensource': {
            'name': 'Open Source Software Thesis',
            'language': 'english',
            'dir': tests_output / 'opensource_thesis'
        },
        'ai_pricing': {
            'name': 'AI Pricing Strategy Thesis',
            'language': 'english',
            'dir': tests_output / 'ai_pricing_thesis'
        },
        'co2_thesis_german': {
            'name': 'CO2 Zertifikate Thesis (German)',
            'language': 'german',
            'dir': tests_output / 'co2_thesis_german'
        }
    }

    # Filter based on argument
    if args.thesis != 'all':
        theses = {args.thesis: theses[args.thesis]}

    print("=" * 80)
    print("COMPREHENSIVE THESIS REPAIR SCRIPT")
    print("=" * 80)
    print()
    print(f"Repairing {len(theses)} thesis/theses:")
    for key, info in theses.items():
        print(f"  • {info['name']} ({info['language']})")
    print()
    print("Fixes applied:")
    print("  0. Sanitize ALL .md variants (FINAL_THESIS_CLEAN.md, COMPLETE_DRAFT.md, etc.)")
    print("  1. Remove H2 metadata sections (## Citations Used, etc.)")
    print("  2. Remove inline metadata (**Section:**, **Word Count:**, etc.)")
    print("  3. Restore proper section names (not generic '## Content')")
    print("  4. Verify References sections intact")
    print("  5. Regenerate clean PDFs")
    print("  6. Copy PDFs to examples/ for GitHub Pages")
    print()
    print("=" * 80)

    # Repair each thesis
    results = {}
    for key, info in theses.items():
        success = repair_thesis(
            thesis_name=info['name'],
            language=info['language'],
            output_dir=info['dir']
        )
        results[key] = success
        print()

    # Summary
    print("=" * 80)
    print("REPAIR SUMMARY")
    print("=" * 80)

    successful = sum(1 for v in results.values() if v)
    total = len(results)

    for key, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {status}: {theses[key]['name']}")

    print()
    print(f"Total: {successful}/{total} theses repaired successfully")

    if successful == total:
        print()
        print("🎉 ALL THESES REPAIRED SUCCESSFULLY!")
        print()
        print("Next steps:")
        print("  1. Review FINAL_THESIS.md files for quality")
        print("  2. Check PDFs render correctly")
        print("  3. Verify References sections have citations")
        return 0
    else:
        print()
        print("⚠️  Some theses failed repair - review errors above")
        return 1


if __name__ == '__main__':
    sys.exit(main())
