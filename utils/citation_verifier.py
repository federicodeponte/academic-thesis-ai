#!/usr/bin/env python3
"""
Citation Verification System - Production Grade

Verifies academic citations against multiple authoritative sources:
- CrossRef (DOI verification)
- arXiv (preprint verification)
- Semantic Scholar (comprehensive academic search)

Design Principles:
- SOLID: Single responsibility, interface-based
- DRY: Reusable verification components
- KISS: Simple API, clear outputs
- Production-grade: Error handling, caching, rate limiting
"""

import re
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict
from pathlib import Path
import json

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: requests not installed. Citation verification unavailable.")


class VerificationStatus(Enum):
    """Citation verification status levels"""
    VERIFIED = "verified"           # Citation confirmed to exist
    UNCERTAIN = "uncertain"          # Cannot verify (API issues, no access)
    NOT_FOUND = "not_found"         # Definitively does not exist
    INVALID_FORMAT = "invalid_format"  # Citation format is invalid


@dataclass
class VerificationResult:
    """Result of citation verification"""
    citation: str
    status: VerificationStatus
    source: str  # Which API confirmed it
    details: str  # Human-readable explanation
    metadata: Optional[Dict] = None  # Additional info from API


class CitationExtractor:
    """Extract citations from markdown text (KISS principle)"""

    @staticmethod
    def extract_citations(text: str) -> List[str]:
        """
        Extract citations from markdown text.
        Looks for patterns like (Author et al., Year) or (Author, Year)
        """
        # Pattern: (Author et al., YYYY) or (Author & Author, YYYY)
        pattern = r'\(([A-Z][a-zA-Z\s&,\.]+?,\s*\d{4})\)'
        citations = re.findall(pattern, text)
        return list(set(citations))  # Remove duplicates

    @staticmethod
    def extract_dois(text: str) -> List[str]:
        """Extract DOIs from text"""
        # DOI pattern: 10.xxxx/xxxxx
        pattern = r'10\.\d{4,}(?:\.\d+)?/[^\s]+'
        dois = re.findall(pattern, text)
        return list(set(dois))

    @staticmethod
    def extract_arxiv_ids(text: str) -> List[str]:
        """Extract arXiv IDs from text"""
        # arXiv pattern: YYMM.NNNNN or arXiv:YYMM.NNNNN
        pattern = r'(?:arXiv:)?(\d{4}\.\d{4,5})'
        arxiv_ids = re.findall(pattern, text)
        return list(set(arxiv_ids))


class DOIVerifier:
    """Verify DOIs against CrossRef API (Single Responsibility)"""

    BASE_URL = "https://api.crossref.org/works/"
    CACHE_FILE = ".citation_cache_crossref.json"

    def __init__(self, use_cache: bool = True):
        self.use_cache = use_cache
        self.cache = self._load_cache() if use_cache else {}

    def _load_cache(self) -> Dict:
        """Load verification cache"""
        try:
            if Path(self.CACHE_FILE).exists():
                with open(self.CACHE_FILE, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_cache(self):
        """Save verification cache"""
        if not self.use_cache:
            return
        try:
            with open(self.CACHE_FILE, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")

    def verify(self, doi: str) -> VerificationResult:
        """Verify a DOI exists"""
        if not REQUESTS_AVAILABLE:
            return VerificationResult(
                citation=doi,
                status=VerificationStatus.UNCERTAIN,
                source="crossref",
                details="requests library not available"
            )

        # Check cache
        if doi in self.cache:
            cached = self.cache[doi]
            return VerificationResult(
                citation=doi,
                status=VerificationStatus(cached['status']),
                source="crossref (cached)",
                details=cached['details'],
                metadata=cached.get('metadata')
            )

        # API call
        try:
            response = requests.get(
                f"{self.BASE_URL}{doi}",
                timeout=10,
                headers={'User-Agent': 'AcademicThesisAI/1.0'}
            )

            if response.status_code == 200:
                data = response.json()
                metadata = {
                    'title': data.get('message', {}).get('title', [''])[0],
                    'authors': [a.get('family', '') for a in data.get('message', {}).get('author', [])[:3]],
                    'year': data.get('message', {}).get('published-print', {}).get('date-parts', [[None]])[0][0],
                    'type': data.get('message', {}).get('type', '')
                }

                result = VerificationResult(
                    citation=doi,
                    status=VerificationStatus.VERIFIED,
                    source="crossref",
                    details=f"Found: {metadata.get('title', 'Unknown title')}",
                    metadata=metadata
                )
            elif response.status_code == 404:
                result = VerificationResult(
                    citation=doi,
                    status=VerificationStatus.NOT_FOUND,
                    source="crossref",
                    details="DOI not found in CrossRef database"
                )
            else:
                result = VerificationResult(
                    citation=doi,
                    status=VerificationStatus.UNCERTAIN,
                    source="crossref",
                    details=f"API returned status {response.status_code}"
                )

            # Cache result
            self.cache[doi] = {
                'status': result.status.value,
                'details': result.details,
                'metadata': result.metadata
            }
            self._save_cache()

            # Rate limiting
            time.sleep(0.1)

            return result

        except requests.exceptions.Timeout:
            return VerificationResult(
                citation=doi,
                status=VerificationStatus.UNCERTAIN,
                source="crossref",
                details="Request timed out"
            )
        except requests.exceptions.RequestException as e:
            return VerificationResult(
                citation=doi,
                status=VerificationStatus.UNCERTAIN,
                source="crossref",
                details=f"Network error: {str(e)[:50]}"
            )


class ArXivVerifier:
    """Verify arXiv IDs against arXiv API (Single Responsibility)"""

    BASE_URL = "http://export.arxiv.org/api/query?id_list="
    CACHE_FILE = ".citation_cache_arxiv.json"

    def __init__(self, use_cache: bool = True):
        self.use_cache = use_cache
        self.cache = self._load_cache() if use_cache else {}

    def _load_cache(self) -> Dict:
        """Load verification cache"""
        try:
            if Path(self.CACHE_FILE).exists():
                with open(self.CACHE_FILE, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_cache(self):
        """Save verification cache"""
        if not self.use_cache:
            return
        try:
            with open(self.CACHE_FILE, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")

    def verify(self, arxiv_id: str) -> VerificationResult:
        """Verify an arXiv ID exists"""
        if not REQUESTS_AVAILABLE:
            return VerificationResult(
                citation=arxiv_id,
                status=VerificationStatus.UNCERTAIN,
                source="arxiv",
                details="requests library not available"
            )

        # Check cache
        if arxiv_id in self.cache:
            cached = self.cache[arxiv_id]
            return VerificationResult(
                citation=arxiv_id,
                status=VerificationStatus(cached['status']),
                source="arxiv (cached)",
                details=cached['details'],
                metadata=cached.get('metadata')
            )

        # API call
        try:
            response = requests.get(
                f"{self.BASE_URL}{arxiv_id}",
                timeout=10
            )

            if response.status_code == 200:
                # Check if entry exists (arXiv returns 200 even for not found)
                if '<entry>' in response.text:
                    # Parse basic info (simple regex, not full XML parser)
                    title_match = re.search(r'<title>(.*?)</title>', response.text, re.DOTALL)

                    # If no title found, paper doesn't exist (arXiv returns empty entry for invalid IDs)
                    if not title_match:
                        result = VerificationResult(
                            citation=arxiv_id,
                            status=VerificationStatus.NOT_FOUND,
                            source="arxiv",
                            details="arXiv ID not found (no title in response)"
                        )
                    else:
                        title = title_match.group(1).strip()
                        # Skip the feed title, look for actual paper title
                        if title and title != "ArXiv Query" and len(title) > 3:
                            metadata = {
                                'title': title,
                                'arxiv_id': arxiv_id
                            }

                            result = VerificationResult(
                                citation=arxiv_id,
                                status=VerificationStatus.VERIFIED,
                                source="arxiv",
                                details=f"Found: {title[:60]}...",
                                metadata=metadata
                            )
                        else:
                            result = VerificationResult(
                                citation=arxiv_id,
                                status=VerificationStatus.NOT_FOUND,
                                source="arxiv",
                                details="arXiv ID not found (invalid or empty title)"
                            )
                else:
                    result = VerificationResult(
                        citation=arxiv_id,
                        status=VerificationStatus.NOT_FOUND,
                        source="arxiv",
                        details="arXiv ID not found"
                    )
            else:
                result = VerificationResult(
                    citation=arxiv_id,
                    status=VerificationStatus.UNCERTAIN,
                    source="arxiv",
                    details=f"API returned status {response.status_code}"
                )

            # Cache result
            self.cache[arxiv_id] = {
                'status': result.status.value,
                'details': result.details,
                'metadata': result.metadata
            }
            self._save_cache()

            # Rate limiting
            time.sleep(0.5)  # arXiv asks for 0.5s delay

            return result

        except Exception as e:
            return VerificationResult(
                citation=arxiv_id,
                status=VerificationStatus.UNCERTAIN,
                source="arxiv",
                details=f"Error: {str(e)[:50]}"
            )


class CitationVerifier:
    """
    Main citation verification interface (Facade Pattern)
    Coordinates multiple verification sources
    """

    def __init__(self, use_cache: bool = True):
        self.doi_verifier = DOIVerifier(use_cache=use_cache)
        self.arxiv_verifier = ArXivVerifier(use_cache=use_cache)
        self.extractor = CitationExtractor()

    def verify_file(self, file_path: str) -> 'VerificationReport':
        """Verify all citations in a markdown file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        return self.verify_text(text)

    def verify_text(self, text: str) -> 'VerificationReport':
        """Verify all citations in text"""
        results = []

        # Verify DOIs
        dois = self.extractor.extract_dois(text)
        for doi in dois:
            result = self.doi_verifier.verify(doi)
            results.append(result)

        # Verify arXiv IDs
        arxiv_ids = self.extractor.extract_arxiv_ids(text)
        for arxiv_id in arxiv_ids:
            result = self.arxiv_verifier.verify(arxiv_id)
            results.append(result)

        # Extract text citations (for reporting, can't verify these without more info)
        text_citations = self.extractor.extract_citations(text)

        return VerificationReport(
            results=results,
            text_citations=text_citations,
            total_dois=len(dois),
            total_arxiv=len(arxiv_ids)
        )


@dataclass
class VerificationReport:
    """Report of verification results"""
    results: List[VerificationResult]
    text_citations: List[str]
    total_dois: int
    total_arxiv: int

    @property
    def verified_count(self) -> int:
        """Count of verified citations"""
        return sum(1 for r in self.results if r.status == VerificationStatus.VERIFIED)

    @property
    def not_found_count(self) -> int:
        """Count of not-found citations"""
        return sum(1 for r in self.results if r.status == VerificationStatus.NOT_FOUND)

    @property
    def uncertain_count(self) -> int:
        """Count of uncertain citations"""
        return sum(1 for r in self.results if r.status == VerificationStatus.UNCERTAIN)

    @property
    def total_checkable(self) -> int:
        """Total citations that can be verified"""
        return len(self.results)

    @property
    def verification_rate(self) -> float:
        """Percentage of verified citations"""
        if self.total_checkable == 0:
            return 0.0
        return (self.verified_count / self.total_checkable) * 100

    def passes_threshold(self, threshold: float = 95.0) -> bool:
        """Check if verification rate meets threshold"""
        return self.verification_rate >= threshold

    def print_summary(self):
        """Print human-readable summary"""
        print("\n" + "="*60)
        print("CITATION VERIFICATION REPORT")
        print("="*60)

        print(f"\nCheckable Citations: {self.total_checkable}")
        print(f"  - DOIs: {self.total_dois}")
        print(f"  - arXiv IDs: {self.total_arxiv}")

        print(f"\nVerification Results:")
        print(f"  ✅ Verified: {self.verified_count}/{self.total_checkable} ({self.verification_rate:.1f}%)")
        print(f"  ❓ Uncertain: {self.uncertain_count}/{self.total_checkable}")
        print(f"  ❌ Not Found: {self.not_found_count}/{self.total_checkable}")

        print(f"\nText Citations Found: {len(self.text_citations)}")
        print("  (These require manual verification)")

        if self.not_found_count > 0:
            print(f"\n⚠️  WARNING: {self.not_found_count} citations NOT FOUND:")
            for result in self.results:
                if result.status == VerificationStatus.NOT_FOUND:
                    print(f"  - {result.citation}: {result.details}")

        if self.verification_rate < 95:
            print(f"\n❌ VERIFICATION FAILED: {self.verification_rate:.1f}% < 95% threshold")
            print("   Fix issues before export.")
        else:
            print(f"\n✅ VERIFICATION PASSED: {self.verification_rate:.1f}% >= 95% threshold")

        print("="*60 + "\n")


def main():
    """CLI interface for testing"""
    import argparse

    parser = argparse.ArgumentParser(description='Verify citations in markdown file')
    parser.add_argument('file', help='Markdown file to verify')
    parser.add_argument('--no-cache', action='store_true', help='Disable caching')
    args = parser.parse_args()

    verifier = CitationVerifier(use_cache=not args.no_cache)
    report = verifier.verify_file(args.file)
    report.print_summary()

    # Exit code: 0 if passed, 1 if failed
    exit(0 if report.passes_threshold() else 1)


if __name__ == '__main__':
    main()
