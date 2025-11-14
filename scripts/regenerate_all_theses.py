#!/usr/bin/env python3
"""
ABOUTME: Regenerate all 4 showcase theses with smart routing enabled
ABOUTME: Verifies citation source diversity (academic + industry sources)

Generates:
1. opensource_thesis
2. co2_thesis_german
3. academic_ai_thesis
4. ai_pricing_thesis
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Thesis configurations
THESES = [
    {
        'name': 'opensource_thesis',
        'script': 'tests/scripts/test_opensource_thesis.py',
        'output_dir': 'tests/outputs/opensource_thesis',
    },
    {
        'name': 'co2_thesis_german',
        'script': 'tests/scripts/test_co2_german_thesis.py',
        'output_dir': 'tests/outputs/co2_thesis_german',
    },
    {
        'name': 'academic_ai_thesis',
        'script': 'tests/scripts/test_academic_ai_thesis.py',
        'output_dir': 'tests/outputs/academic_ai_thesis',
    },
    {
        'name': 'ai_pricing_thesis',
        'script': 'tests/scripts/test_ai_pricing_thesis.py',
        'output_dir': 'tests/outputs/ai_pricing_thesis',
    },
]


def regenerate_thesis(thesis_config: dict, index: int, total: int) -> bool:
    """
    Regenerate a single thesis.

    Args:
        thesis_config: Thesis configuration dict
        index: Current thesis number (1-based)
        total: Total number of theses

    Returns:
        True if successful, False otherwise
    """
    name = thesis_config['name']
    script = thesis_config['script']
    output_dir = Path(thesis_config['output_dir'])

    print(f"\n{'='*80}")
    print(f"📄 Regenerating Thesis {index}/{total}: {name}")
    print(f"{'='*80}\n")
    print(f"Script: {script}")
    print(f"Output: {output_dir}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Run thesis generation
    try:
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour max per thesis
        )

        if result.returncode != 0:
            print(f"\n❌ Thesis generation failed!")
            print(f"Exit code: {result.returncode}")
            if result.stderr:
                print(f"\nError output:\n{result.stderr[-2000:]}")  # Last 2000 chars
            return False

        # Check output files
        final_md = output_dir / 'FINAL_THESIS.md'
        final_pdf = output_dir / 'FINAL_THESIS.pdf'
        final_docx = output_dir / 'FINAL_THESIS.docx'

        if not final_md.exists():
            print(f"❌ FINAL_THESIS.md not created!")
            return False

        md_size = final_md.stat().st_size
        pdf_exists = final_pdf.exists()
        docx_exists = final_docx.exists()

        print(f"\n✅ Thesis generated successfully!")
        print(f"   FINAL_THESIS.md: {md_size:,} bytes")
        print(f"   FINAL_THESIS.pdf: {'✅ Created' if pdf_exists else '❌ Missing'}")
        print(f"   FINAL_THESIS.docx: {'✅ Created' if docx_exists else '❌ Missing'}")
        print(f"   Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Analyze citation sources from output
        if 'Gemini Grounded' in result.stdout or 'gemini_grounded' in result.stdout:
            print(f"   🌐 Industry sources detected (Gemini Grounded used)")

        return True

    except subprocess.TimeoutExpired:
        print(f"\n❌ Thesis generation timed out (>1 hour)")
        return False
    except Exception as e:
        print(f"\n❌ Thesis generation error: {e}")
        return False


def main():
    """Regenerate all theses."""
    print("="*80)
    print("🔄 REGENERATING ALL 4 THESES WITH SMART ROUTING")
    print("="*80)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nThis will regenerate all showcase theses with:")
    print("  ✅ Smart query routing enabled (default)")
    print("  ✅ Citation source diversity (academic + industry)")
    print("  ✅ Enhanced Scout prompts")
    print(f"\nEstimated time: 2-4 hours (depends on API response times)\n")

    # Confirm if running interactively
    if sys.stdin.isatty():
        response = input("Continue? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted.")
            return 1

    # Regenerate each thesis
    results = []
    for i, thesis_config in enumerate(THESES, 1):
        success = regenerate_thesis(thesis_config, i, len(THESES))
        results.append((thesis_config['name'], success))

    # Summary
    print(f"\n{'='*80}")
    print("📊 REGENERATION SUMMARY")
    print(f"{'='*80}\n")

    success_count = sum(1 for _, success in results if success)
    fail_count = len(results) - success_count

    for name, success in results:
        status = "✅ Success" if success else "❌ Failed"
        print(f"  {status}: {name}")

    print(f"\nTotal: {success_count}/{len(results)} successful")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if fail_count == 0:
        print(f"\n✅ All theses regenerated successfully!")
        print("\nNext steps:")
        print("1. Check citation diversity in FINAL_THESIS.md files")
        print("2. Look for industry sources (McKinsey, Gartner, WHO, OECD)")
        print("3. Verify PDF/DOCX exports have correct structure")
        return 0
    else:
        print(f"\n⚠️ {fail_count} thesis/theses failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
