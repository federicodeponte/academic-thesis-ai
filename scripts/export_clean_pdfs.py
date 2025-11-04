#!/usr/bin/env python3
"""
ABOUTME: Export clean thesis PDFs for public publication
ABOUTME: Uses cleaned markdown files (without metadata) and professional PDF export
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.export_professional import export_pdf


def main():
    """Export all 3 clean thesis PDFs to examples/ directory."""
    print("="*80)
    print("CLEAN PDF EXPORTER - Generate Publication-Ready PDFs")
    print("="*80)
    print()

    base_dir = Path(__file__).parent.parent

    # Define thesis files (clean versions)
    theses = [
        {
            "name": "Open Source Thesis",
            "md_file": base_dir / "tests/outputs/opensource_thesis/FINAL_THESIS_CLEAN.md",
            "pdf_file": base_dir / "examples/opensource_thesis.pdf"
        },
        {
            "name": "AI Pricing Thesis",
            "md_file": base_dir / "tests/outputs/ai_pricing_thesis/FINAL_THESIS_CLEAN.md",
            "pdf_file": base_dir / "examples/ai_pricing_thesis.pdf"
        },
        {
            "name": "CO2 German Thesis",
            "md_file": base_dir / "tests/outputs/co2_thesis_german/FINAL_THESIS_CLEAN.md",
            "pdf_file": base_dir / "examples/co2_german_thesis.pdf"
        }
    ]

    # Create examples directory if needed
    examples_dir = base_dir / "examples"
    examples_dir.mkdir(exist_ok=True)

    # Export each thesis
    success_count = 0
    failed_count = 0

    for thesis in theses:
        print(f"\n{'='*80}")
        print(f"Exporting: {thesis['name']}")
        print(f"{'='*80}")

        if not thesis['md_file'].exists():
            print(f"❌ Markdown file not found: {thesis['md_file']}")
            failed_count += 1
            continue

        # Export to PDF
        if export_pdf(thesis['md_file'], thesis['pdf_file'], engine='auto'):
            success_count += 1
            print(f"✅ Successfully exported: {thesis['pdf_file']}")
        else:
            failed_count += 1
            print(f"❌ Failed to export: {thesis['pdf_file']}")

    # Summary
    print(f"\n{'='*80}")
    print(f"EXPORT SUMMARY")
    print(f"{'='*80}")
    print(f"Total theses: {len(theses)}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"{'='*80}")

    if failed_count > 0:
        print("\n⚠️  Some PDFs failed to export. Check error messages above.")
        sys.exit(1)
    else:
        print("\n✅ All PDFs exported successfully!")
        print()
        print("Next steps:")
        print("1. Verify PDFs look clean (no metadata)")
        print("2. Push to GitHub: git add examples/*.pdf && git commit -m 'Replace PDFs with clean versions' && git push")


if __name__ == "__main__":
    main()
