#!/usr/bin/env python3
"""
Auto-update script for examples/ directory.

This script copies the latest successful thesis PDFs from tests/outputs/
to examples/ for showcase on GitHub Pages.

Usage:
    python3 scripts/update_examples.py
    python3 scripts/update_examples.py --dry-run
"""

import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent

def get_thesis_output_dirs() -> dict[str, Path]:
    """
    Get all thesis output directories with FINAL_THESIS.md.

    Returns:
        Dict mapping thesis name to output directory path
    """
    project_root = get_project_root()
    outputs_dir = project_root / "tests" / "outputs"

    thesis_dirs = {}

    if not outputs_dir.exists():
        return thesis_dirs

    for thesis_dir in outputs_dir.iterdir():
        if not thesis_dir.is_dir():
            continue

        final_md = thesis_dir / "FINAL_THESIS.md"
        final_pdf = thesis_dir / "FINAL_THESIS.pdf"

        # Only include if both MD and PDF exist
        if final_md.exists() and final_pdf.exists():
            thesis_dirs[thesis_dir.name] = thesis_dir

    return thesis_dirs

def should_update_example(thesis_name: str, source_pdf: Path, dest_pdf: Path, verbose: bool = True) -> bool:
    """
    Check if example PDF should be updated.

    Args:
        thesis_name: Name of thesis
        source_pdf: Source PDF path from tests/outputs/
        dest_pdf: Destination PDF path in examples/
        verbose: Whether to print details

    Returns:
        True if PDF should be updated
    """
    if not dest_pdf.exists():
        if verbose:
            print(f"  ➕ {thesis_name}: No existing PDF - will create")
        return True

    # Compare modification times
    source_mtime = source_pdf.stat().st_mtime
    dest_mtime = dest_pdf.stat().st_mtime

    if source_mtime > dest_mtime:
        source_time = datetime.fromtimestamp(source_mtime).strftime("%b %d %H:%M")
        dest_time = datetime.fromtimestamp(dest_mtime).strftime("%b %d %H:%M")

        if verbose:
            print(f"  📝 {thesis_name}: Source newer ({source_time} > {dest_time})")
        return True
    else:
        if verbose:
            print(f"  ✅ {thesis_name}: Already up-to-date")
        return False

def update_examples(dry_run: bool = False, verbose: bool = True) -> int:
    """
    Update examples/ directory with latest thesis PDFs.

    Args:
        dry_run: If True, only show what would be updated
        verbose: Whether to print detailed output

    Returns:
        Number of files updated
    """
    project_root = get_project_root()
    examples_dir = project_root / "examples"

    # Create examples/ if it doesn't exist
    if not examples_dir.exists():
        if verbose:
            print(f"Creating examples/ directory: {examples_dir}")
        if not dry_run:
            examples_dir.mkdir(parents=True, exist_ok=True)

    # Find all thesis output directories
    thesis_dirs = get_thesis_output_dirs()

    if not thesis_dirs:
        if verbose:
            print("❌ No thesis outputs found in tests/outputs/")
            print("   Run thesis generation tests first:")
            print("   python3 tests/scripts/test_opensource_thesis.py")
        return 0

    if verbose:
        print(f"\n{'='*70}")
        print(f"🔄 AUTO-UPDATE EXAMPLES")
        print(f"{'='*70}\n")
        print(f"Found {len(thesis_dirs)} thesis output(s):\n")

    # Check each thesis
    updates_needed = []

    for thesis_name, thesis_dir in sorted(thesis_dirs.items()):
        source_pdf = thesis_dir / "FINAL_THESIS.pdf"
        dest_pdf = examples_dir / f"{thesis_name}.pdf"

        if should_update_example(thesis_name, source_pdf, dest_pdf, verbose):
            updates_needed.append((thesis_name, source_pdf, dest_pdf))

    # Perform updates
    if not updates_needed:
        if verbose:
            print(f"\n✅ All examples are up-to-date!")
        return 0

    if verbose:
        print(f"\n{'='*70}")

        if dry_run:
            print(f"📋 DRY RUN - Would update {len(updates_needed)} file(s):")
        else:
            print(f"🚀 Updating {len(updates_needed)} file(s):")
        print(f"{'='*70}\n")

    updated_count = 0

    for thesis_name, source_pdf, dest_pdf in updates_needed:
        source_size = source_pdf.stat().st_size

        if verbose:
            print(f"{'[DRY RUN] ' if dry_run else ''}Copying:")
            print(f"  From: {source_pdf}")
            print(f"  To:   {dest_pdf}")
            print(f"  Size: {source_size:,} bytes")

        if not dry_run:
            try:
                shutil.copy2(source_pdf, dest_pdf)

                # Verify copy
                if dest_pdf.exists() and dest_pdf.stat().st_size == source_size:
                    if verbose:
                        print(f"  ✅ Success\n")
                    updated_count += 1
                else:
                    if verbose:
                        print(f"  ❌ Failed - size mismatch\n")
            except Exception as e:
                if verbose:
                    print(f"  ❌ Failed: {e}\n")
        else:
            if verbose:
                print(f"  ✅ Would copy\n")
            updated_count += 1

    if verbose:
        print(f"{'='*70}")

        if dry_run:
            print(f"📋 DRY RUN COMPLETE - Would update {updated_count} file(s)")
        else:
            print(f"✅ UPDATE COMPLETE - Updated {updated_count} file(s)")

        print(f"{'='*70}\n")

        if not dry_run and updated_count > 0:
            print("📝 Next steps:")
            print("   1. Review changes: git status")
            print("   2. Commit: git add examples/ && git commit -m 'Update showcase PDFs'")
            print("   3. Push: git push origin master")
            print()

    return updated_count

def main():
    parser = argparse.ArgumentParser(
        description="Auto-update examples/ directory with latest thesis PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update examples/ with latest PDFs
  python3 scripts/update_examples.py

  # Dry run (show what would be updated)
  python3 scripts/update_examples.py --dry-run

  # Quiet mode (only show errors)
  python3 scripts/update_examples.py --quiet
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without making changes'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Only show errors (no verbose output)'
    )

    args = parser.parse_args()

    try:
        updated_count = update_examples(
            dry_run=args.dry_run,
            verbose=not args.quiet
        )

        # Exit with success if any files were updated or would be updated
        return 0 if updated_count >= 0 else 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
