#!/usr/bin/env python3
"""
ABOUTME: Parallel thesis generation runner with tier-adaptive execution
ABOUTME: Runs multiple thesis scripts concurrently using multiprocessing
"""

import sys
import argparse
import multiprocessing
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.concurrency_config import get_concurrency_config


def run_thesis_script(script_path: Path, log_path: Path) -> Tuple[str, int, float]:
    """
    Run a single thesis generation script.

    Args:
        script_path: Path to thesis test script
        log_path: Path to save output log

    Returns:
        tuple: (script_name, return_code, duration_seconds)
    """
    script_name = script_path.stem
    start_time = time.time()

    try:
        # Run thesis script, redirecting output to log file
        with open(log_path, 'w') as log_file:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True
            )

        duration = time.time() - start_time
        return (script_name, result.returncode, duration)

    except Exception as e:
        duration = time.time() - start_time
        # Log error
        with open(log_path, 'a') as log_file:
            log_file.write(f"\n\n❌ SCRIPT EXECUTION ERROR:\n{str(e)}\n")

        return (script_name, 1, duration)  # Return code 1 = error


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def main():
    """Run all thesis generation scripts in parallel."""
    parser = argparse.ArgumentParser(
        description='Run multiple thesis generation scripts in parallel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Run all 4 default theses in parallel
  python3 tests/scripts/run_all_theses_parallel.py

  # Run specific theses only
  python3 tests/scripts/run_all_theses_parallel.py --scripts opensource pricing

  # Force tier detection before running
  python3 tests/scripts/run_all_theses_parallel.py --detect-tier

Available thesis scripts:
  - opensource: test_opensource_thesis.py (Open Source Software Impact)
  - pricing: test_ai_pricing_thesis.py (AI Pricing Strategies)
  - co2: test_co2_german_thesis.py (CO2 Management German)
  - academic_ai: test_academic_ai_thesis.py (Academic Thesis AI Meta-thesis)

Tier-Adaptive Execution:
  - FREE TIER (10 RPM):  Recommend running 1 thesis per Google Cloud account
  - PAID TIER (2,000 RPM): Can run all 4 theses on single account
        '''
    )

    parser.add_argument(
        '--scripts',
        nargs='+',
        choices=['opensource', 'pricing', 'co2', 'academic_ai'],
        help='Specific thesis scripts to run (default: all)'
    )
    parser.add_argument(
        '--detect-tier',
        action='store_true',
        help='Force fresh API tier detection before running'
    )
    parser.add_argument(
        '--max-workers',
        type=int,
        help='Max parallel processes (default: auto-detect based on tier)'
    )
    parser.add_argument(
        '--logs-dir',
        type=Path,
        default=Path('/tmp'),
        help='Directory for log files (default: /tmp)'
    )

    args = parser.parse_args()

    # Detect API tier and get concurrency config
    print("\n" + "="*80)
    print("PARALLEL THESIS GENERATION RUNNER")
    print("="*80 + "\n")

    config = get_concurrency_config(verbose=True, force_detect=args.detect_tier)
    config.print_summary()

    # Determine max workers
    if args.max_workers:
        max_workers = args.max_workers
        print(f"ℹ️  Manual override: max_workers = {max_workers}\n")
    else:
        max_workers = config.max_parallel_theses

    # Check tier safety
    if config.tier == "free" and max_workers > 1:
        print("⚠️  WARNING: Running multiple theses on FREE TIER (10 RPM)")
        print("   This may cause rate limit errors.")
        print("   Recommended: Use 1 thesis per Google Cloud account")
        print("   Or: Reduce --max-workers=1")
        print()

        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("\n❌ Aborted by user\n")
            return 1

    # Define all available thesis scripts
    scripts_root = Path(__file__).parent
    all_scripts = {
        'opensource': scripts_root / 'test_opensource_thesis.py',
        'pricing': scripts_root / 'test_ai_pricing_thesis.py',
        'co2': scripts_root / 'test_co2_german_thesis.py',
        'academic_ai': scripts_root / 'test_academic_ai_thesis.py',
    }

    # Select scripts to run
    if args.scripts:
        selected_scripts = {name: all_scripts[name] for name in args.scripts}
    else:
        selected_scripts = all_scripts

    # Verify scripts exist
    missing = [name for name, path in selected_scripts.items() if not path.exists()]
    if missing:
        print(f"❌ ERROR: Missing thesis scripts: {', '.join(missing)}\n")
        return 1

    # Create log paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = args.logs_dir / f"thesis_parallel_{timestamp}"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_paths = {
        name: log_dir / f"{name}.log"
        for name in selected_scripts.keys()
    }

    # Display execution plan
    print(f"📋 Execution Plan:")
    print(f"   Theses to generate: {len(selected_scripts)}")
    print(f"   Parallel workers: {max_workers}")
    print(f"   Log directory: {log_dir}")
    print()

    for name in selected_scripts.keys():
        print(f"   • {name}: {log_paths[name]}")
    print()

    # Start timer
    overall_start = time.time()
    print(f"🚀 Starting parallel thesis generation at {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*80}\n")

    # Create task list
    tasks = [
        (script_path, log_paths[name])
        for name, script_path in selected_scripts.items()
    ]

    # Run tasks in parallel using multiprocessing
    with multiprocessing.Pool(processes=max_workers) as pool:
        # Map tasks to worker processes
        results = pool.starmap(run_thesis_script, tasks)

    # Calculate total duration
    overall_duration = time.time() - overall_start

    # Display results
    print(f"\n{'='*80}")
    print(f"EXECUTION COMPLETE")
    print(f"{'='*80}\n")

    print(f"⏱️  Total Duration: {format_duration(overall_duration)}\n")
    print(f"📊 Results:\n")

    success_count = 0
    failure_count = 0

    for name, return_code, duration in results:
        status = "✅ SUCCESS" if return_code == 0 else "❌ FAILED"
        status_color = status

        if return_code == 0:
            success_count += 1
        else:
            failure_count += 1

        print(f"   {status_color} {name:20s} ({format_duration(duration)})")
        print(f"      Log: {log_paths[name]}")
        print()

    # Summary
    print(f"{'='*80}")
    print(f"Summary: {success_count}/{len(results)} succeeded, {failure_count}/{len(results)} failed")
    print(f"{'='*80}\n")

    if failure_count > 0:
        print("⚠️  Some theses failed. Check log files for details.\n")
        return 1
    else:
        print("✅ All theses generated successfully!\n")

        # Show output locations
        print("📁 Generated Theses:")
        output_base = Path(__file__).parent.parent.parent / "tests" / "outputs"

        for name in selected_scripts.keys():
            thesis_dir_map = {
                'opensource': 'opensource_thesis',
                'pricing': 'ai_pricing_thesis',
                'co2': 'co2_thesis_german',
                'academic_ai': 'academic_ai_thesis',
            }

            thesis_dir = output_base / thesis_dir_map[name]
            final_pdf = thesis_dir / "FINAL_THESIS.pdf"

            if final_pdf.exists():
                print(f"   • {name}: {final_pdf}")
            else:
                print(f"   • {name}: {thesis_dir} (PDF not found)")

        print()
        return 0


if __name__ == "__main__":
    sys.exit(main())
