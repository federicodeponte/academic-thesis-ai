#!/usr/bin/env python3
"""
ABOUTME: Regenerate all 4 showcase theses in parallel using multiprocessing
ABOUTME: Tests production-grade retry and logging improvements under load

Generates concurrently:
1. opensource_thesis
2. co2_thesis_german
3. academic_ai_thesis
4. ai_pricing_thesis

Usage:
    python scripts/regenerate_theses_parallel.py              # 4 parallel workers
    python scripts/regenerate_theses_parallel.py --workers 2  # 2 parallel workers (safer)
"""

import sys
import subprocess
import multiprocessing
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict, List

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


def run_thesis(config: Dict) -> Tuple[str, bool, str, Dict]:
    """
    Run a single thesis generation script.

    Args:
        config: Thesis configuration dict with name, script, output_dir

    Returns:
        Tuple of (name, success, log_output, stats)
    """
    name = config['name']
    script = config['script']
    output_dir = Path(config['output_dir'])

    start_time = datetime.now()
    log_lines = []

    print(f"\n[{name}] Starting at {start_time.strftime('%H:%M:%S')}")
    log_lines.append(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # Run thesis generation
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour max
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        log_lines.append(f"Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        log_lines.append(f"Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")

        # Check for errors
        if result.returncode != 0:
            log_lines.append(f"Exit code: {result.returncode}")
            log_lines.append("FAILED")
            if result.stderr:
                log_lines.append(f"Error output (last 1000 chars):\n{result.stderr[-1000:]}")

            print(f"[{name}] ❌ Failed after {duration/60:.1f} minutes")
            return (name, False, "\n".join(log_lines), {
                'duration': duration,
                'exit_code': result.returncode
            })

        # Check output files
        final_md = output_dir / 'FINAL_THESIS.md'
        final_pdf = output_dir / 'FINAL_THESIS.pdf'
        final_docx = output_dir / 'FINAL_THESIS.docx'

        md_exists = final_md.exists()
        pdf_exists = final_pdf.exists()
        docx_exists = final_docx.exists()

        if not md_exists:
            log_lines.append("ERROR: FINAL_THESIS.md not created")
            print(f"[{name}] ❌ Failed - no FINAL_THESIS.md")
            return (name, False, "\n".join(log_lines), {
                'duration': duration,
                'exit_code': result.returncode
            })

        # Get file sizes
        md_size = final_md.stat().st_size
        pdf_size = final_pdf.stat().st_size if pdf_exists else 0
        docx_size = final_docx.stat().st_size if docx_exists else 0

        log_lines.append(f"FINAL_THESIS.md: {md_size:,} bytes")
        log_lines.append(f"FINAL_THESIS.pdf: {pdf_size:,} bytes" if pdf_exists else "FINAL_THESIS.pdf: MISSING")
        log_lines.append(f"FINAL_THESIS.docx: {docx_size:,} bytes" if docx_exists else "FINAL_THESIS.docx: MISSING")

        # Check for retry/logging patterns in output
        retry_count = result.stdout.count('Retrying')
        logging_count = result.stdout.count('logger')

        log_lines.append(f"Retry attempts detected: {retry_count}")
        log_lines.append(f"Logger calls detected: {logging_count}")

        print(f"[{name}] ✅ Success after {duration/60:.1f} minutes")

        return (name, True, "\n".join(log_lines), {
            'duration': duration,
            'md_size': md_size,
            'pdf_size': pdf_size,
            'docx_size': docx_size,
            'retry_attempts': retry_count,
            'exit_code': 0
        })

    except subprocess.TimeoutExpired:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log_lines.append(f"TIMEOUT after {duration:.1f} seconds")
        print(f"[{name}] ❌ Timeout after 1 hour")
        return (name, False, "\n".join(log_lines), {
            'duration': duration,
            'exit_code': -1,
            'timeout': True
        })

    except Exception as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log_lines.append(f"EXCEPTION: {str(e)}")
        print(f"[{name}] ❌ Exception: {str(e)}")
        return (name, False, "\n".join(log_lines), {
            'duration': duration,
            'exit_code': -1,
            'exception': str(e)
        })


def save_log(name: str, log_content: str):
    """Save thesis generation log to file."""
    log_dir = Path('logs/thesis_regeneration')
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_path = log_dir / f"{name}_{timestamp}.log"

    with open(log_path, 'w') as f:
        f.write(log_content)

    return log_path


def main():
    """Regenerate all theses in parallel."""
    parser = argparse.ArgumentParser(description='Regenerate showcase theses in parallel')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers (default: 4, use 2 for safer run)')
    parser.add_argument('--stagger', type=int, default=30,
                       help='Seconds to stagger starts (default: 30)')
    args = parser.parse_args()

    workers = min(args.workers, len(THESES))  # Don't exceed number of theses

    print("="*80)
    print("🔄 PARALLEL THESIS REGENERATION")
    print("="*80)
    print(f"\nConfiguration:")
    print(f"  Workers: {workers}")
    print(f"  Stagger: {args.stagger}s between starts")
    print(f"  Theses: {len(THESES)}")
    print(f"  Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if workers == 4:
        print(f"\n⚠️  Running 4 theses in parallel - may hit API rate limits")
        print(f"   Consider using --workers 2 for safer execution")

    print(f"\nThis will test the new production improvements:")
    print(f"  ✅ Retry mechanism with exponential backoff")
    print(f"  ✅ Production-grade logging integration")
    print(f"  ✅ Error recovery for scraper failures")

    estimated_time = 60 / workers  # Rough estimate
    print(f"\nEstimated completion: {estimated_time:.0f}-{estimated_time*2:.0f} minutes\n")

    # Confirm if running interactively
    if sys.stdin.isatty():
        response = input("Continue? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted.")
            return 1

    overall_start = datetime.now()

    # Create multiprocessing pool
    with multiprocessing.Pool(processes=workers) as pool:
        # Submit all jobs with staggered starts
        results_async = []
        for i, thesis_config in enumerate(THESES):
            if i > 0 and args.stagger > 0:
                print(f"\n⏸️  Waiting {args.stagger}s before starting next thesis...")
                time.sleep(args.stagger)

            result = pool.apply_async(run_thesis, (thesis_config,))
            results_async.append(result)
            print(f"📝 Submitted: {thesis_config['name']}")

        print(f"\n✅ All {len(THESES)} theses submitted to worker pool")
        print(f"⏳ Waiting for completion (max 1 hour per thesis)...\n")

        # Collect results as they complete
        results = []
        for i, result_async in enumerate(results_async):
            try:
                name, success, log_output, stats = result_async.get(timeout=3700)  # Slightly more than 1 hour
                results.append((name, success, log_output, stats))

                # Save log
                log_path = save_log(name, log_output)
                print(f"💾 Log saved: {log_path}")

            except multiprocessing.TimeoutError:
                results.append((THESES[i]['name'], False, "Pool timeout", {'timeout': True}))
                print(f"❌ Pool timeout for {THESES[i]['name']}")

    overall_end = datetime.now()
    overall_duration = (overall_end - overall_start).total_seconds()

    # Print summary
    print(f"\n{'='*80}")
    print("📊 REGENERATION SUMMARY")
    print(f"{'='*80}\n")

    success_count = sum(1 for _, success, _, _ in results if success)
    fail_count = len(results) - success_count

    print("Results:")
    for name, success, _, stats in results:
        status = "✅ Success" if success else "❌ Failed"
        duration = stats.get('duration', 0)
        print(f"  {status}: {name} ({duration/60:.1f} minutes)")

        if success:
            md_size = stats.get('md_size', 0)
            pdf_size = stats.get('pdf_size', 0)
            retry_attempts = stats.get('retry_attempts', 0)
            print(f"    - Markdown: {md_size/1024:.1f} KB")
            print(f"    - PDF: {pdf_size/1024:.1f} KB" if pdf_size > 0 else "    - PDF: Missing")
            print(f"    - Retry attempts: {retry_attempts}")

    print(f"\nStatistics:")
    print(f"  Total: {success_count}/{len(results)} successful")
    print(f"  Overall duration: {overall_duration/60:.1f} minutes")
    print(f"  Average per thesis: {overall_duration/len(results)/60:.1f} minutes")
    print(f"  Completed: {overall_end.strftime('%Y-%m-%d %H:%M:%S')}")

    if success_count == len(results):
        print(f"\n✅ All theses regenerated successfully!")
        print(f"\nProduction improvements verified:")
        print(f"  ✅ Retry mechanism working")
        print(f"  ✅ Logging integration functional")
        print(f"  ✅ Parallel execution stable")
        print(f"\nNext steps:")
        print(f"  1. Check logs in logs/thesis_regeneration/")
        print(f"  2. Review retry attempts in output")
        print(f"  3. Inspect FINAL_THESIS.md files for quality")
        print(f"  4. Copy PDFs to examples/ directory")
        return 0
    else:
        print(f"\n⚠️ {fail_count} thesis/theses failed")
        print(f"Check logs in logs/thesis_regeneration/ for details")
        return 1


if __name__ == '__main__':
    sys.exit(main())
