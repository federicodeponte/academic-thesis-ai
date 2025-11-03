#!/usr/bin/env python3
"""
ABOUTME: Citation compiler for deterministic citation ID replacement
ABOUTME: Replaces {cite_001} with formatted citations, generates reference lists
"""

import re
from typing import Any, Dict, List, Tuple, Set
from pathlib import Path

from utils.citation_database import Citation, CitationDatabase, CitationStyle


class CitationCompiler:
    """Deterministic citation compiler using dictionary lookup."""

    def __init__(self, database: CitationDatabase):
        """
        Initialize compiler with citation database.

        Args:
            database: CitationDatabase with all available citations
        """
        self.database = database
        self.citation_lookup = {c.id: c for c in database.citations}
        self.style = database.citation_style

    def compile_citations(self, text: str) -> Tuple[str, List[str]]:
        """
        Replace citation IDs with formatted citations.

        Args:
            text: Text containing citation IDs like {cite_001}

        Returns:
            tuple: (formatted_text, list_of_missing_ids)
        """
        missing_ids: List[str] = []

        def replace_citation(match: re.Match) -> str:
            """Replace single citation ID with formatted citation."""
            cite_id = match.group(0).strip('{}')  # Extract cite_001 from {cite_001}

            if cite_id not in self.citation_lookup:
                missing_ids.append(cite_id)
                return f"[MISSING: {cite_id}]"

            citation = self.citation_lookup[cite_id]
            return self.format_in_text_citation(citation)

        # Replace all {cite_XXX} patterns
        citation_pattern = r'\{cite_\d{3}\}'
        formatted_text = re.sub(citation_pattern, replace_citation, text)

        return formatted_text, missing_ids

    def format_in_text_citation(self, citation: Citation) -> str:
        """
        Format in-text citation based on style.

        Args:
            citation: Citation to format

        Returns:
            str: Formatted in-text citation (e.g., "(Smith et al., 2023)")
        """
        if self.style == "APA 7th":
            return self._format_apa_in_text(citation)
        elif self.style == "IEEE":
            return self._format_ieee_in_text(citation)
        else:
            # Default to APA
            return self._format_apa_in_text(citation)

    def _format_apa_in_text(self, citation: Citation) -> str:
        """Format in-text citation in APA 7th style."""
        authors = citation.authors
        year = citation.year

        if len(authors) == 1:
            return f"({authors[0]}, {year})"
        elif len(authors) == 2:
            return f"({authors[0]} & {authors[1]}, {year})"
        else:
            # 3+ authors use et al.
            return f"({authors[0]} et al., {year})"

    def _format_ieee_in_text(self, citation: Citation) -> str:
        """Format in-text citation in IEEE style (numbered)."""
        # For Phase 1, we'll use citation number from ID
        # cite_001 -> [1], cite_002 -> [2]
        number = citation.id.replace("cite_", "")
        return f"[{int(number)}]"

    def generate_reference_list(self, text: str) -> str:
        """
        Generate reference list from citations used in text.

        Args:
            text: Text with formatted citations (to determine which were used)

        Returns:
            str: Formatted reference list
        """
        # Find all cited IDs in original format
        cited_ids = self._extract_cited_ids(text)

        # Get citations for cited IDs only
        cited_citations = [
            self.citation_lookup[cid]
            for cid in sorted(cited_ids)
            if cid in self.citation_lookup
        ]

        if not cited_citations:
            return "## References\n\n(No citations found)\n"

        # Sort alphabetically by first author (APA style)
        if self.style == "APA 7th":
            cited_citations.sort(key=lambda c: c.authors[0].lower())

        # Format references
        references = ["## References\n"]

        for citation in cited_citations:
            if self.style == "APA 7th":
                ref = self._format_apa_reference(citation)
            elif self.style == "IEEE":
                ref = self._format_ieee_reference(citation)
            else:
                ref = self._format_apa_reference(citation)

            references.append(ref)

        return "\n\n".join(references)

    def _extract_cited_ids(self, text: str) -> Set[str]:
        """Extract all citation IDs mentioned in text."""
        # Find both {cite_XXX} and formatted citations
        # For now, look for {cite_XXX} patterns
        pattern = r'\{cite_\d{3}\}'
        matches = re.findall(pattern, text)
        return {match.strip('{}') for match in matches}

    def _format_apa_reference(self, citation: Citation) -> str:
        """Format full reference in APA 7th style."""
        authors = citation.authors
        year = citation.year
        title = citation.title

        # Format authors
        if len(authors) == 1:
            author_str = f"{authors[0]}."
        elif len(authors) == 2:
            author_str = f"{authors[0]}, & {authors[1]}."
        else:
            author_str = ", ".join(authors[:-1]) + f", & {authors[-1]}."

        # Format based on source type
        source_type = citation.source_type

        if source_type == 'journal':
            journal = citation.journal or ""
            volume = citation.volume
            issue = citation.issue
            pages = citation.pages or ""
            doi = citation.doi or ""

            ref = f"{author_str} ({year}). {title}. *{journal}*"
            if volume:
                ref += f", *{volume}*"
            if issue:
                ref += f"({issue})"
            if pages:
                ref += f", {pages}"
            if doi:
                ref += f". https://doi.org/{doi}"
            ref += "."

        elif source_type == 'book':
            publisher = citation.publisher or ""
            ref = f"{author_str} ({year}). *{title}*. {publisher}."

        elif source_type in ['report', 'website']:
            url = citation.url or ""
            publisher = citation.publisher or ""

            ref = f"{author_str} ({year}). *{title}*."
            if publisher:
                ref = f"{author_str} ({year}). *{title}*. {publisher}."
            if url:
                ref += f" {url}"

        elif source_type == 'conference':
            publisher = citation.publisher or ""
            pages = citation.pages or ""

            ref = f"{author_str} ({year}). {title}."
            if publisher:
                ref += f" {publisher}."
            if pages:
                ref += f" (pp. {pages})."

        else:
            # Fallback
            ref = f"{author_str} ({year}). {title}."

        return ref

    def _format_ieee_reference(self, citation: Citation) -> str:
        """Format full reference in IEEE style."""
        authors = citation.authors
        year = citation.year
        title = citation.title

        # Format authors (initials first in IEEE)
        if len(authors) <= 3:
            author_str = ", ".join([f"{a}." for a in authors])
        else:
            author_str = f"{authors[0]}. et al."

        # Format based on source type
        source_type = citation.source_type

        if source_type == 'journal':
            journal = citation.journal or ""
            volume = citation.volume or ""
            pages = citation.pages or ""

            ref = f"[{citation.id.replace('cite_', '')}] {author_str}, \"{title},\" *{journal}*"
            if volume:
                ref += f", vol. {volume}"
            if pages:
                ref += f", pp. {pages}"
            ref += f", {year}."

        else:
            ref = f"[{citation.id.replace('cite_', '')}] {author_str}, \"{title},\" {year}."

        return ref

    def validate_compilation(self, original: str, compiled: str) -> Dict[str, Any]:
        """
        Validate that compilation completed successfully.

        Args:
            original: Original text with citation IDs
            compiled: Compiled text with formatted citations

        Returns:
            dict: Validation results with success status and issues
        """
        issues = []

        # Check for remaining citation IDs (should be none)
        remaining_ids = re.findall(r'\{cite_\d{3}\}', compiled)
        if remaining_ids:
            issues.append(f"Found {len(remaining_ids)} un-replaced citation IDs: {remaining_ids[:5]}")

        # Check for MISSING markers
        missing_markers = re.findall(r'\[MISSING: cite_\d{3}\]', compiled)
        if missing_markers:
            issues.append(f"Found {len(missing_markers)} missing citations: {missing_markers}")

        # Extract citation IDs from original
        original_ids = set(re.findall(r'cite_\d{3}', original))

        # Check all IDs were processed
        unprocessed = original_ids - {m.replace('[MISSING: ', '').replace(']', '') for m in missing_markers}

        return {
            'success': len(issues) == 0,
            'issues': issues,
            'total_citations': len(original_ids),
            'successfully_compiled': len(original_ids) - len(missing_markers),
            'missing_citations': len(missing_markers),
        }

    def generate_coverage_report(self, draft: str) -> Dict[str, Any]:
        """
        Analyze citation coverage in draft.

        Args:
            draft: Text with citation IDs

        Returns:
            dict with coverage statistics and unused citations
        """
        # Find all citation IDs used in draft
        cited_ids = self._extract_cited_ids(draft)

        # Get all available citations
        all_citation_ids = set(self.citation_lookup.keys())

        # Calculate unused
        unused_ids = all_citation_ids - cited_ids
        unused_citations = [
            self.citation_lookup[cid]
            for cid in sorted(unused_ids)
        ]

        # Calculate statistics
        total = len(all_citation_ids)
        used = len(cited_ids)
        coverage = (used / total * 100) if total > 0 else 0

        return {
            'total_citations_available': total,
            'citations_used': used,
            'citations_unused': len(unused_ids),
            'coverage_percentage': coverage,
            'unused_citations': unused_citations,
            'cited_ids': cited_ids,
        }


def format_coverage_report(report: Dict[str, Any]) -> str:
    """
    Format coverage report as markdown.

    Args:
        report: Coverage report from generate_coverage_report()

    Returns:
        str: Formatted markdown report
    """
    output = f"""# Citation Coverage Report

## Summary Statistics

- **Total citations available**: {report['total_citations_available']}
- **Citations used in draft**: {report['citations_used']}
- **Citations unused**: {report['citations_unused']}
- **Coverage percentage**: {report['coverage_percentage']:.1f}%

## Analysis

"""

    # Add analysis based on coverage percentage
    if report['coverage_percentage'] < 50:
        output += "⚠️  **Low citation coverage** - Consider using more sources from the database.\n\n"
    elif report['coverage_percentage'] > 90:
        output += "✅ **Excellent citation coverage** - Most available sources are utilized.\n\n"
    else:
        output += "✅ **Good citation coverage** - Reasonable use of available sources.\n\n"

    # List unused citations
    if report['unused_citations']:
        output += "## Unused Citations\n\n"
        output += "The following citations are in the database but not used in the draft:\n\n"

        for citation in report['unused_citations']:
            authors_str = ", ".join(citation.authors[:2])
            if len(citation.authors) > 2:
                authors_str += " et al."

            # Truncate title if too long
            title = citation.title
            if len(title) > 80:
                title = title[:77] + "..."

            output += f"- **{citation.id}**: {authors_str} ({citation.year}) - {title}\n"

    else:
        output += "## All Citations Used\n\n"
        output += "✅ All citations in the database have been used in the draft.\n"

    return output


def compile_citations_in_file(
    input_path: Path,
    output_path: Path,
    database: CitationDatabase
) -> Tuple[bool, List[str]]:
    """
    Compile citations in file using database.

    Args:
        input_path: Input file with citation IDs
        output_path: Output file for compiled text
        database: Citation database

    Returns:
        tuple: (success, list_of_missing_ids)
    """
    # Read input
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Compile citations
    compiler = CitationCompiler(database)
    compiled_text, missing_ids = compiler.compile_citations(text)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(compiled_text)

    return len(missing_ids) == 0, missing_ids
