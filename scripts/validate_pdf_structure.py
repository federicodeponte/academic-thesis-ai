#!/usr/bin/env python3
"""
ABOUTME: Automated PDF structure validation - prevents regressions in PDF exports
ABOUTME: Validates cover pages, TOC, page counts, PDF engine, and detects duplicates

CRITICAL: Run this after EVERY PDF generation to catch regressions before publishing

Usage:
    python3 scripts/validate_pdf_structure.py examples/opensource_thesis.pdf
    python3 scripts/validate_pdf_structure.py --all  # Validate all showcase PDFs
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

try:
    import PyPDF2
except ImportError:
    print("❌ PyPDF2 not installed. Install with: pip install PyPDF2")
    sys.exit(1)


@dataclass
class PDFValidationResult:
    """Validation result for a single PDF."""
    pdf_path: Path
    passed: bool
    page_count: int
    engine_used: Optional[str]
    issues: List[str]
    warnings: List[str]


class PDFStructureValidator:
    """
    Validates PDF structure to prevent regressions.

    Checks for:
    1. Correct PDF engine (Pandoc/LaTeX, not LibreOffice)
    2. Single cover page (no duplicates)
    3. Table of Contents placement
    4. Expected page count ranges
    5. Duplicate content detection
    """

    # Expected page count ranges by thesis type
    EXPECTED_PAGE_COUNTS = {
        'opensource_thesis': (105, 115),     # ~108 pages
        'co2_thesis_german': (80, 90),       # ~84 pages
        'academic_ai_thesis': (105, 115),    # ~107 pages
        'ai_pricing_thesis': (110, 120),     # ~111 pages
    }

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def validate_pdf(self, pdf_path: Path) -> PDFValidationResult:
        """
        Validate PDF structure.

        Args:
            pdf_path: Path to PDF file

        Returns:
            PDFValidationResult with pass/fail and detected issues
        """
        issues = []
        warnings = []

        if not pdf_path.exists():
            return PDFValidationResult(
                pdf_path=pdf_path,
                passed=False,
                page_count=0,
                engine_used=None,
                issues=[f"PDF file not found: {pdf_path}"],
                warnings=[]
            )

        try:
            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                page_count = len(pdf_reader.pages)

                # Check 1: Verify PDF engine (should be Pandoc/LaTeX)
                engine = self._detect_pdf_engine(pdf_reader)
                if engine and 'LibreOffice' in engine:
                    issues.append(
                        f"❌ CRITICAL: Using LibreOffice engine instead of Pandoc/LaTeX "
                        f"(check for Korean Unicode or LaTeX compilation errors)"
                    )
                elif not engine:
                    warnings.append("⚠️  Could not detect PDF engine from metadata")

                # Check 2: Validate page count
                thesis_name = pdf_path.stem
                if thesis_name in self.EXPECTED_PAGE_COUNTS:
                    min_pages, max_pages = self.EXPECTED_PAGE_COUNTS[thesis_name]
                    if not (min_pages <= page_count <= max_pages):
                        issues.append(
                            f"❌ Unexpected page count: {page_count} "
                            f"(expected {min_pages}-{max_pages})"
                        )
                else:
                    warnings.append(f"⚠️  No expected page count for {thesis_name}")

                # Check 3: Detect duplicate cover pages (heuristic)
                duplicate_cover = self._detect_duplicate_covers(pdf_reader)
                if duplicate_cover:
                    issues.append(
                        f"❌ CRITICAL: Detected duplicate cover pages "
                        f"(check for extra \\maketitle call in pandoc_engine.py)"
                    )

                # Check 4: Verify TOC exists (heuristic)
                has_toc = self._detect_toc(pdf_reader)
                if not has_toc:
                    warnings.append("⚠️  Table of Contents not detected")

                # Check 5: Check metadata
                metadata_issues = self._validate_metadata(pdf_reader)
                issues.extend(metadata_issues)

                passed = len(issues) == 0

                return PDFValidationResult(
                    pdf_path=pdf_path,
                    passed=passed,
                    page_count=page_count,
                    engine_used=engine,
                    issues=issues,
                    warnings=warnings
                )

        except Exception as e:
            return PDFValidationResult(
                pdf_path=pdf_path,
                passed=False,
                page_count=0,
                engine_used=None,
                issues=[f"❌ Failed to validate PDF: {str(e)}"],
                warnings=[]
            )

    def _detect_pdf_engine(self, pdf_reader: PyPDF2.PdfReader) -> Optional[str]:
        """Detect which engine generated the PDF (Pandoc/LaTeX vs LibreOffice)."""
        metadata = pdf_reader.metadata
        if not metadata:
            return None

        # Check Creator and Producer fields
        creator = metadata.get('/Creator', '')
        producer = metadata.get('/Producer', '')

        # LibreOffice detection
        if 'LibreOffice' in creator or 'LibreOffice' in producer:
            return 'LibreOffice'

        # Pandoc/LaTeX detection
        if 'LaTeX' in producer or 'pdfTeX' in producer:
            return 'Pandoc/LaTeX'

        return f"{creator} / {producer}" if creator or producer else None

    def _detect_duplicate_covers(self, pdf_reader: PyPDF2.PdfReader) -> bool:
        """
        Detect duplicate cover pages (heuristic).

        Checks if first two pages have identical or very similar text content.
        This catches the duplicate \\maketitle bug.
        """
        if len(pdf_reader.pages) < 2:
            return False

        try:
            page1_text = pdf_reader.pages[0].extract_text()
            page2_text = pdf_reader.pages[1].extract_text()

            # Normalize whitespace
            page1_normalized = ' '.join(page1_text.split())
            page2_normalized = ' '.join(page2_text.split())

            # If first two pages are very similar (>80% overlap), likely duplicates
            if page1_normalized and page2_normalized:
                overlap = self._text_overlap(page1_normalized, page2_normalized)
                if overlap > 0.8:
                    return True

            return False

        except Exception:
            # Extraction failed, can't determine
            return False

    def _text_overlap(self, text1: str, text2: str) -> float:
        """Calculate text overlap percentage (simple heuristic)."""
        if not text1 or not text2:
            return 0.0

        # Exact match
        if text1 == text2:
            return 1.0

        # Check if one is substring of other
        shorter = min(text1, text2, key=len)
        longer = max(text1, text2, key=len)

        if shorter in longer:
            return len(shorter) / len(longer)

        # Word-level overlap
        words1 = set(text1.split())
        words2 = set(text2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.0

    def _detect_toc(self, pdf_reader: PyPDF2.PdfReader) -> bool:
        """Detect if PDF has Table of Contents (heuristic)."""
        # Check for bookmark/outline structure
        if hasattr(pdf_reader, 'outline') and pdf_reader.outline:
            return True

        # Check for "Table of Contents" or "Contents" text in first 5 pages
        try:
            for i in range(min(5, len(pdf_reader.pages))):
                text = pdf_reader.pages[i].extract_text()
                if re.search(r'\b(Table of Contents|Contents|Inhaltsverzeichnis)\b', text, re.IGNORECASE):
                    return True
        except Exception:
            pass

        return False

    def _validate_metadata(self, pdf_reader: PyPDF2.PdfReader) -> List[str]:
        """Validate PDF metadata."""
        issues = []
        metadata = pdf_reader.metadata

        if not metadata:
            issues.append("⚠️  PDF has no metadata")
            return issues

        # Check for title
        title = metadata.get('/Title', '')
        if not title or title.strip() == '':
            issues.append("⚠️  PDF missing title metadata")

        return issues

    def print_result(self, result: PDFValidationResult):
        """Print validation result."""
        print(f"\n{'='*70}")
        print(f"📄 PDF VALIDATION: {result.pdf_path.name}")
        print(f"{'='*70}\n")

        print(f"Page Count: {result.page_count}")
        print(f"PDF Engine: {result.engine_used or 'Unknown'}")
        print()

        if result.issues:
            print(f"❌ ISSUES FOUND ({len(result.issues)}):")
            for issue in result.issues:
                print(f"   {issue}")
            print()

        if result.warnings:
            print(f"⚠️  WARNINGS ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"   {warning}")
            print()

        if result.passed:
            print("✅ VALIDATION PASSED - PDF structure is correct\n")
        else:
            print("❌ VALIDATION FAILED - Fix issues above before publishing\n")

        print(f"{'='*70}\n")


def validate_all_showcase_pdfs() -> int:
    """
    Validate all showcase PDFs in examples/ directory.

    Returns:
        Exit code (0 = all passed, 1 = failures)
    """
    examples_dir = Path(__file__).parent.parent / 'examples'
    pdf_files = list(examples_dir.glob('*.pdf'))

    if not pdf_files:
        print(f"❌ No PDF files found in {examples_dir}")
        return 1

    validator = PDFStructureValidator(verbose=True)
    results = []

    print(f"\n{'='*70}")
    print(f"🔍 VALIDATING ALL SHOWCASE PDFs ({len(pdf_files)} files)")
    print(f"{'='*70}\n")

    for pdf_file in sorted(pdf_files):
        result = validator.validate_pdf(pdf_file)
        results.append(result)
        validator.print_result(result)

    # Summary
    passed_count = sum(1 for r in results if r.passed)
    failed_count = len(results) - passed_count

    print(f"\n{'='*70}")
    print(f"📊 VALIDATION SUMMARY")
    print(f"{'='*70}\n")
    print(f"Total PDFs: {len(results)}")
    print(f"✅ Passed: {passed_count}")
    print(f"❌ Failed: {failed_count}\n")

    if failed_count > 0:
        print("❌ VALIDATION FAILED - Fix issues before publishing to GitHub Pages\n")
        return 1
    else:
        print("✅ ALL PDFs VALIDATED - Ready for GitHub Pages publication\n")
        return 0


def main():
    """Validate PDF files from command line."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate PDF structure to prevent regressions'
    )
    parser.add_argument(
        'pdf_file',
        type=Path,
        nargs='?',
        help='PDF file to validate (omit to use --all)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate all PDFs in examples/ directory'
    )

    args = parser.parse_args()

    if args.all:
        sys.exit(validate_all_showcase_pdfs())
    elif args.pdf_file:
        validator = PDFStructureValidator(verbose=True)
        result = validator.validate_pdf(args.pdf_file)
        validator.print_result(result)
        sys.exit(0 if result.passed else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
