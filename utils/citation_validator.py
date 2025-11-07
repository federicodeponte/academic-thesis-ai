#!/usr/bin/env python3
"""
ABOUTME: Citation validation utility to detect hallucinated/invalid citations
ABOUTME: Uses CrossRef API to verify DOIs and sanity checks for author names
"""

import json
import re
import requests
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationIssue:
    """Represents a citation validation issue."""
    citation_id: str
    severity: str  # 'critical', 'warning', 'info'
    issue_type: str
    message: str
    citation_text: str


class CitationValidator:
    """Validates citations for academic integrity."""

    def __init__(self, timeout: int = 10):
        """
        Initialize validator.

        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout
        self.crossref_api_base = "https://api.crossref.org/works/"

    def validate_doi(self, doi: str) -> Optional[bool]:
        """
        Verify if a DOI exists via CrossRef API.

        Args:
            doi: DOI to verify (can include https://doi.org/ prefix)

        Returns:
            True if DOI exists, False if DOI not found (404), None if network error
        """
        # Clean DOI (remove prefix if present)
        doi_clean = doi.replace('https://doi.org/', '').replace('http://doi.org/', '')

        try:
            response = requests.get(
                f"{self.crossref_api_base}{doi_clean}",
                timeout=self.timeout,
                headers={'User-Agent': 'AcademicThesisAI/1.0 (mailto:example@example.com)'}
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            # Network error - assume DOI might be valid
            return None  # Unknown

    def check_author_sanity(self, authors: List[str]) -> List[str]:
        """
        Check for suspicious author name patterns.

        Returns:
            List of issues found (empty if no issues)
        """
        issues = []

        for author in authors:
            # Pattern 1: Repetitive initials (e.g., "N. C. A. C. B. S. C. A.")
            if re.match(r'^([A-Z]\.\s*){6,}$', author):
                issues.append(f"Repetitive initials pattern: '{author}'")

            # Pattern 2: Same first and last name (e.g., "Smith, Smith")
            parts = author.split(',')
            if len(parts) == 2:
                last, first = parts[0].strip(), parts[1].strip()
                if last and first and last.lower() == first.lower():
                    issues.append(f"Same first/last name: '{author}'")

            # Pattern 3: Initials only, no full name (e.g., "E. A. W.")
            if re.match(r'^([A-Z]\.\s*){1,3}$', author):
                issues.append(f"Initials only (incomplete): '{author}'")

            # Pattern 4: Too many consecutive same letters
            if re.search(r'([A-Z])\.\s*\1\.\s*\1\.', author):
                issues.append(f"Repetitive letters: '{author}'")

        return issues

    def validate_citation(self, citation: Dict) -> List[ValidationIssue]:
        """
        Validate a single citation from citation database.

        Args:
            citation: Citation dict with keys: id, authors, year, title, doi, etc.

        Returns:
            List of validation issues found
        """
        issues = []
        cite_id = citation.get('id', 'unknown')
        title = citation.get('title', '')
        authors = citation.get('authors', [])
        doi = citation.get('doi', '')

        # Format citation text for display
        author_str = ', '.join(authors[:2])
        if len(authors) > 2:
            author_str += ' et al.'
        cite_text = f"{author_str} ({citation.get('year')}) - {title[:60]}..."

        # Check 1: Author name sanity
        author_issues = self.check_author_sanity(authors)
        for issue in author_issues:
            issues.append(ValidationIssue(
                citation_id=cite_id,
                severity='critical',
                issue_type='invalid_author',
                message=issue,
                citation_text=cite_text
            ))

        # Check 2: DOI validation (if DOI provided)
        if doi:
            doi_valid = self.validate_doi(doi)
            if doi_valid is False:
                issues.append(ValidationIssue(
                    citation_id=cite_id,
                    severity='critical',
                    issue_type='invalid_doi',
                    message=f"DOI not found: {doi}",
                    citation_text=cite_text
                ))
            elif doi_valid is None:
                issues.append(ValidationIssue(
                    citation_id=cite_id,
                    severity='warning',
                    issue_type='doi_check_failed',
                    message=f"Could not verify DOI (network error): {doi}",
                    citation_text=cite_text
                ))

        # Check 3: Generic AI-generated titles
        generic_patterns = [
            r'A Systematic Review$',
            r'A Comprehensive Study$',
            r'An Overview$',
            r'A Survey$',
        ]
        for pattern in generic_patterns:
            if re.search(pattern, title):
                issues.append(ValidationIssue(
                    citation_id=cite_id,
                    severity='warning',
                    issue_type='generic_title',
                    message=f"Generic title pattern: '{pattern.strip('$')}'",
                    citation_text=cite_text
                ))

        return issues

    def validate_database(self, database_path: Path) -> Tuple[List[ValidationIssue], Dict]:
        """
        Validate all citations in a citation database JSON file.

        Args:
            database_path: Path to citation_database.json

        Returns:
            Tuple of (issues_list, stats_dict)
        """
        with open(database_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        citations = data.get('citations', [])
        all_issues = []

        print(f"🔍 Validating {len(citations)} citations from {database_path.name}...")

        for citation in citations:
            issues = self.validate_citation(citation)
            all_issues.extend(issues)

        # Compute statistics
        stats = {
            'total_citations': len(citations),
            'total_issues': len(all_issues),
            'critical_issues': sum(1 for i in all_issues if i.severity == 'critical'),
            'warnings': sum(1 for i in all_issues if i.severity == 'warning'),
            'invalid_dois': sum(1 for i in all_issues if i.issue_type == 'invalid_doi'),
            'invalid_authors': sum(1 for i in all_issues if i.issue_type == 'invalid_author'),
        }

        return all_issues, stats

    def generate_report(self, issues: List[ValidationIssue], thesis_name: str) -> str:
        """
        Generate a human-readable validation report.

        Args:
            issues: List of validation issues
            thesis_name: Name of thesis for report header

        Returns:
            Formatted report string
        """
        if not issues:
            return f"✅ {thesis_name}: All citations passed validation!\n"

        report = [f"\n{'='*80}"]
        report.append(f"CITATION VALIDATION REPORT: {thesis_name}")
        report.append(f"{'='*80}\n")

        # Group by severity
        critical = [i for i in issues if i.severity == 'critical']
        warnings = [i for i in issues if i.severity == 'warning']

        if critical:
            report.append(f"❌ CRITICAL ISSUES ({len(critical)}):")
            report.append("-" * 80)
            for issue in critical:
                report.append(f"\n[{issue.citation_id}] {issue.message}")
                report.append(f"  {issue.citation_text}")

        if warnings:
            report.append(f"\n\n⚠️  WARNINGS ({len(warnings)}):")
            report.append("-" * 80)
            for issue in warnings:
                report.append(f"\n[{issue.citation_id}] {issue.message}")
                report.append(f"  {issue.citation_text}")

        report.append(f"\n{'='*80}")
        report.append(f"TOTAL ISSUES: {len(issues)} ({len(critical)} critical, {len(warnings)} warnings)")
        report.append(f"{'='*80}\n")

        return '\n'.join(report)


def main():
    """Main entry point for CLI validation."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate citations for academic integrity')
    parser.add_argument('database', nargs='?', help='Path to citation_database.json (or validate all)')
    parser.add_argument('--all', action='store_true', help='Validate all 3 thesis databases')

    args = parser.parse_args()

    validator = CitationValidator()

    # Determine which databases to validate
    if args.all or not args.database:
        base_dir = Path(__file__).parent.parent
        databases = [
            (base_dir / "tests/outputs/opensource_thesis/citation_database.json", "Open Source Thesis"),
            (base_dir / "tests/outputs/ai_pricing_thesis/citation_database.json", "AI Pricing Thesis"),
            (base_dir / "tests/outputs/co2_thesis_german/citation_database.json", "CO2 German Thesis"),
        ]
    else:
        databases = [(Path(args.database), Path(args.database).parent.name)]

    # Validate each database
    total_critical = 0
    total_warnings = 0

    for db_path, thesis_name in databases:
        if not db_path.exists():
            print(f"⚠️  Skipping {thesis_name}: Database not found at {db_path}")
            continue

        issues, stats = validator.validate_database(db_path)
        report = validator.generate_report(issues, thesis_name)
        print(report)

        total_critical += stats['critical_issues']
        total_warnings += stats['warnings']

    # Final summary
    print(f"\n{'='*80}")
    print("VALIDATION SUMMARY")
    print(f"{'='*80}")
    print(f"Total Critical Issues: {total_critical}")
    print(f"Total Warnings: {total_warnings}")

    if total_critical > 0:
        print(f"\n❌ VALIDATION FAILED - {total_critical} critical issues found")
        print("   These citations are likely hallucinated/invalid and must be fixed.")
        return 1
    elif total_warnings > 0:
        print(f"\n⚠️  VALIDATION PASSED WITH WARNINGS - {total_warnings} warnings")
        print("   Review these citations for potential issues.")
        return 0
    else:
        print("\n✅ ALL CITATIONS VALID")
        return 0


if __name__ == '__main__':
    exit(main())
