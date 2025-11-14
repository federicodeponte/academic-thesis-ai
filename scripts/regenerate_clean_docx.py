#!/usr/bin/env python3
"""
ABOUTME: Regenerate clean DOCX files from FINAL_THESIS.md (strips Entropy diagnostics)
ABOUTME: Uses sanitized markdown and export_professional.py to create clean Word docs

Usage:
    python3 scripts/regenerate_clean_docx.py                    # All showcase theses
    python3 scripts/regenerate_clean_docx.py opensource_thesis  # Specific thesis
"""

import sys
import subprocess
import os
from pathlib import Path

# Add project root to Python path for export_professional.py imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Thesis output directories
THESIS_DIRS = {
    'opensource_thesis': 'tests/outputs/opensource_thesis',
    'co2_thesis_german': 'tests/outputs/co2_thesis_german',
    'academic_ai_thesis': 'tests/outputs/academic_ai_thesis',
    'ai_pricing_thesis': 'tests/outputs/ai_pricing_thesis',
}


def regenerate_docx(thesis_name: str, thesis_dir: Path) -> bool:
    """
    Regenerate DOCX for a single thesis.

    Args:
        thesis_name: Name of thesis (e.g., 'opensource_thesis')
        thesis_dir: Path to thesis output directory

    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*70}")
    print(f"📄 Regenerating DOCX: {thesis_name}")
    print(f"{'='*70}\n")

    final_md = thesis_dir / 'FINAL_THESIS.md'
    output_docx = thesis_dir / 'FINAL_THESIS.docx'
    examples_docx = Path('examples') / f'{thesis_name}.docx'

    if not final_md.exists():
        print(f"❌ FINAL_THESIS.md not found: {final_md}")
        return False

    # Regenerate DOCX from markdown
    print(f"🔧 Generating DOCX from {final_md.name}...")
    try:
        # Set PYTHONPATH to project root for imports
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path(__file__).parent.parent)

        result = subprocess.run([
            sys.executable, 'utils/export_professional.py',
            str(final_md),
            '--docx', str(output_docx)
        ], capture_output=True, text=True, timeout=60, env=env)

        if result.returncode != 0:
            print(f"❌ DOCX export failed: {result.stderr}")
            return False

        docx_size = output_docx.stat().st_size
        print(f"✅ DOCX generated: {docx_size:,} bytes")

        # Copy to examples/ directory
        print(f"📋 Copying to {examples_docx}...")
        import shutil
        examples_docx.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output_docx, examples_docx)

        print(f"✅ Copied to examples/")
        return True

    except subprocess.TimeoutExpired:
        print(f"❌ DOCX export timed out (>60s)")
        return False
    except Exception as e:
        print(f"❌ DOCX export error: {e}")
        return False


def main():
    """Regenerate clean DOCX files."""
    import argparse

    parser = argparse.ArgumentParser(description='Regenerate clean DOCX files')
    parser.add_argument(
        'thesis',
        nargs='?',
        choices=list(THESIS_DIRS.keys()) + ['all'],
        default='all',
        help='Thesis to regenerate (default: all)'
    )

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent

    if args.thesis == 'all':
        theses_to_process = THESIS_DIRS.items()
    else:
        theses_to_process = [(args.thesis, THESIS_DIRS[args.thesis])]

    print("="*70)
    print("🔄 CLEAN DOCX REGENERATION")
    print("="*70)
    print(f"\nProcessing {len(list(theses_to_process))} thesis/theses")

    success_count = 0
    fail_count = 0

    for thesis_name, thesis_dir_str in theses_to_process:
        thesis_dir = project_root / thesis_dir_str

        if regenerate_docx(thesis_name, thesis_dir):
            success_count += 1
        else:
            fail_count += 1

    # Summary
    print(f"\n{'='*70}")
    print(f"📊 REGENERATION SUMMARY")
    print(f"{'='*70}\n")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {fail_count}")

    if fail_count == 0:
        print(f"\n✅ All DOCX files regenerated successfully!")
        return 0
    else:
        print(f"\n⚠️  {fail_count} DOCX regeneration(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
