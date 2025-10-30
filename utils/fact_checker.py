#!/usr/bin/env python3
"""
Fact-Checking System - Production Grade

Verifies quantitative claims in academic text:
- Extracts statistics, percentages, costs, time durations
- Traces claims to cited sources
- Detects unsupported claims
- Identifies self-contradictions

Design Principles:
- SOLID: Single responsibility, interface-based
- DRY: Reusable claim extraction and verification
- KISS: Simple API, clear outputs
- Production-grade: Error handling, pattern matching
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict
from pathlib import Path


class ClaimStatus(Enum):
    """Fact-check status levels"""
    VERIFIED = "verified"           # Claim verified against source
    CITED_UNVERIFIED = "cited_unverified"  # Has citation but not checked
    UNCITED = "uncited"             # No citation provided
    CONTRADICTED = "contradicted"   # Contradicts other claims in text


@dataclass
class Claim:
    """Represents a quantitative claim"""
    text: str           # Full sentence containing the claim
    value: str          # The specific number/statistic
    claim_type: str     # percentage, cost, duration, count, etc.
    citation: Optional[str] = None   # Associated citation if found
    location: str = ""  # Line number or context


@dataclass
class FactCheckResult:
    """Result of fact-checking a claim"""
    claim: Claim
    status: ClaimStatus
    details: str  # Human-readable explanation
    evidence: Optional[str] = None  # Supporting or contradicting evidence


class ClaimExtractor:
    """Extract quantitative claims from text (KISS principle)"""

    # Patterns for different types of claims
    PERCENTAGE_PATTERN = r'(\d+(?:\.\d+)?%)'
    COST_PATTERN = r'(\$[\d,]+(?:\.\d{2})?)'
    DURATION_PATTERN = r'(\d+(?:,\d+)?)\s*(?:person-)?(?:hours?|days?|weeks?|months?|years?)'
    COUNT_PATTERN = r'(\d+(?:,\d+)?)\s*(?:papers?|studies?|articles?|researchers?|participants?|samples?)'
    RATE_PATTERN = r'(\d+(?:\.\d+)?x)\s*(?:faster|slower|improvement|reduction)'

    # Citation patterns to associate with claims
    CITATION_PATTERN = r'\(([A-Z][a-zA-Z\s&,\.]+?,\s*\d{4})\)'

    @staticmethod
    def extract_claims(text: str) -> List[Claim]:
        """
        Extract all quantitative claims from text.
        Returns claims with their types and associated citations.
        """
        claims = []
        lines = text.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Extract percentages
            for match in re.finditer(ClaimExtractor.PERCENTAGE_PATTERN, line):
                claim = ClaimExtractor._create_claim(
                    line, match.group(1), 'percentage',
                    f"line {line_num}"
                )
                claims.append(claim)

            # Extract costs
            for match in re.finditer(ClaimExtractor.COST_PATTERN, line):
                claim = ClaimExtractor._create_claim(
                    line, match.group(1), 'cost',
                    f"line {line_num}"
                )
                claims.append(claim)

            # Extract durations
            for match in re.finditer(ClaimExtractor.DURATION_PATTERN, line, re.IGNORECASE):
                claim = ClaimExtractor._create_claim(
                    line, match.group(0), 'duration',
                    f"line {line_num}"
                )
                claims.append(claim)

            # Extract counts
            for match in re.finditer(ClaimExtractor.COUNT_PATTERN, line, re.IGNORECASE):
                claim = ClaimExtractor._create_claim(
                    line, match.group(0), 'count',
                    f"line {line_num}"
                )
                claims.append(claim)

            # Extract rates/multipliers
            for match in re.finditer(ClaimExtractor.RATE_PATTERN, line, re.IGNORECASE):
                claim = ClaimExtractor._create_claim(
                    line, match.group(0), 'rate',
                    f"line {line_num}"
                )
                claims.append(claim)

        return claims

    @staticmethod
    def _create_claim(line: str, value: str, claim_type: str, location: str) -> Claim:
        """Create a Claim object with citation if found"""
        # Look for citation near the claim (same sentence or nearby)
        citation_match = re.search(ClaimExtractor.CITATION_PATTERN, line)
        citation = citation_match.group(1) if citation_match else None

        return Claim(
            text=line.strip(),
            value=value,
            claim_type=claim_type,
            citation=citation,
            location=location
        )


class ContradictionDetector:
    """Detect self-contradicting claims (Single Responsibility)"""

    @staticmethod
    def find_contradictions(claims: List[Claim]) -> List[tuple]:
        """
        Find claims that contradict each other.
        Returns list of (claim1, claim2, reason) tuples.
        """
        contradictions = []

        # Group claims by type for comparison
        by_type = {}
        for claim in claims:
            if claim.claim_type not in by_type:
                by_type[claim.claim_type] = []
            by_type[claim.claim_type].append(claim)

        # Check for contradictions within same type
        for claim_type, type_claims in by_type.items():
            if claim_type == 'percentage':
                contradictions.extend(
                    ContradictionDetector._check_percentage_contradictions(type_claims)
                )

        return contradictions

    @staticmethod
    def _check_percentage_contradictions(claims: List[Claim]) -> List[tuple]:
        """Check for contradicting percentage claims"""
        contradictions = []

        # Look for claims about same topic with different values
        for i, claim1 in enumerate(claims):
            for claim2 in claims[i+1:]:
                # Simple heuristic: same words nearby but different percentages
                words1 = set(claim1.text.lower().split())
                words2 = set(claim2.text.lower().split())
                overlap = len(words1 & words2) / max(len(words1), len(words2))

                if overlap > 0.5 and claim1.value != claim2.value:
                    reason = f"Different percentages for similar claims: {claim1.value} vs {claim2.value}"
                    contradictions.append((claim1, claim2, reason))

        return contradictions


class FactChecker:
    """
    Main fact-checking interface (Facade Pattern)
    Coordinates claim extraction and verification
    """

    def __init__(self):
        self.extractor = ClaimExtractor()
        self.detector = ContradictionDetector()

    def check_file(self, file_path: str) -> 'FactCheckReport':
        """Check all claims in a markdown file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.check_text(text)

    def check_text(self, text: str) -> 'FactCheckReport':
        """Check all claims in text"""
        # Extract all claims
        claims = self.extractor.extract_claims(text)

        # Categorize claims
        results = []
        for claim in claims:
            result = self._verify_claim(claim)
            results.append(result)

        # Detect contradictions
        contradictions = self.detector.find_contradictions(claims)

        return FactCheckReport(
            results=results,
            contradictions=contradictions,
            total_claims=len(claims)
        )

    def _verify_claim(self, claim: Claim) -> FactCheckResult:
        """Verify a single claim"""
        if claim.citation:
            # Has citation, but we can't verify without citation verification
            return FactCheckResult(
                claim=claim,
                status=ClaimStatus.CITED_UNVERIFIED,
                details=f"Cited as {claim.citation} (verification pending)"
            )
        else:
            # No citation provided
            return FactCheckResult(
                claim=claim,
                status=ClaimStatus.UNCITED,
                details="No citation provided for this claim"
            )


@dataclass
class FactCheckReport:
    """Report of fact-checking results"""
    results: List[FactCheckResult]
    contradictions: List[tuple]
    total_claims: int

    @property
    def cited_count(self) -> int:
        """Count of claims with citations"""
        return sum(1 for r in self.results
                  if r.status == ClaimStatus.CITED_UNVERIFIED)

    @property
    def uncited_count(self) -> int:
        """Count of claims without citations"""
        return sum(1 for r in self.results
                  if r.status == ClaimStatus.UNCITED)

    @property
    def citation_rate(self) -> float:
        """Percentage of claims with citations"""
        if self.total_claims == 0:
            return 0.0
        return (self.cited_count / self.total_claims) * 100

    def passes_threshold(self, threshold: float = 95.0) -> bool:
        """Check if citation rate meets threshold"""
        return self.citation_rate >= threshold

    def print_summary(self):
        """Print human-readable summary"""
        print("\n" + "="*60)
        print("FACT-CHECK REPORT")
        print("="*60)

        print(f"\nQuantitative Claims Found: {self.total_claims}")

        # Breakdown by type
        by_type = {}
        for result in self.results:
            claim_type = result.claim.claim_type
            if claim_type not in by_type:
                by_type[claim_type] = 0
            by_type[claim_type] += 1

        print("\nBy Type:")
        for claim_type, count in sorted(by_type.items()):
            print(f"  - {claim_type}: {count}")

        print(f"\nCitation Status:")
        print(f"  ✅ Cited: {self.cited_count}/{self.total_claims} ({self.citation_rate:.1f}%)")
        print(f"  ❌ Uncited: {self.uncited_count}/{self.total_claims}")

        if self.uncited_count > 0:
            print(f"\n⚠️  WARNING: {self.uncited_count} claims WITHOUT citations:")
            for result in self.results:
                if result.status == ClaimStatus.UNCITED:
                    print(f"  - {result.claim.value}: \"{result.claim.text[:60]}...\" ({result.claim.location})")

        if self.contradictions:
            print(f"\n🔥 CONTRADICTIONS DETECTED: {len(self.contradictions)}")
            for claim1, claim2, reason in self.contradictions:
                print(f"\n  ⚠️  {reason}")
                print(f"     Claim 1: {claim1.value} at {claim1.location}")
                print(f"     Claim 2: {claim2.value} at {claim2.location}")

        if self.citation_rate < 95:
            print(f"\n❌ FACT-CHECK FAILED: {self.citation_rate:.1f}% < 95% threshold")
            print("   All claims must be cited.")
        else:
            print(f"\n✅ FACT-CHECK PASSED: {self.citation_rate:.1f}% >= 95% threshold")

        print("="*60 + "\n")


def main():
    """CLI interface for testing"""
    import argparse

    parser = argparse.ArgumentParser(description='Fact-check claims in markdown file')
    parser.add_argument('file', help='Markdown file to check')
    args = parser.parse_args()

    checker = FactChecker()
    report = checker.check_file(args.file)
    report.print_summary()

    # Exit code: 0 if passed, 1 if failed
    exit(0 if report.passes_threshold() else 1)


if __name__ == '__main__':
    main()
