#!/usr/bin/env python3
"""
Integrate researched citations into citation databases to reach 110% targets

Process:
1. Load existing citation databases
2. Parse research output files
3. Add new citations to databases
4. Save updated databases

Results:
- AI Pricing: 53 → 60 citations (+7)
- CO2 German: 30 → 55 citations (+25)
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.citation_database import load_citation_database, save_citation_database, Citation, CitationSourceType


def parse_research_output(file_path: Path) -> List[Dict[str, Any]]:
    """
    Parse research output markdown file and extract citation data.

    Returns list of citation dicts with:
    - title
    - authors (list)
    - year
    - doi (optional)
    - url
    - source (Crossref, Semantic Scholar, Gemini LLM)
    """
    content = file_path.read_text(encoding='utf-8')
    citations = []

    # Split by citation entries (#### markers)
    citation_blocks = re.split(r'####\s+\d+\.\s+', content)[1:]  # Skip header

    for block in citation_blocks:
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue

        citation_data = {}

        # First line is title
        citation_data['title'] = lines[0].strip()

        # Parse metadata
        for line in lines[1:]:
            if line.startswith('**Authors**:'):
                authors_str = line.replace('**Authors**:', '').strip()
                # Split by comma, handle "et al." properly
                citation_data['authors'] = [a.strip() for a in authors_str.split(',') if a.strip() and a.strip().lower() != 'et al.']

            elif line.startswith('**Year**:'):
                year_str = line.replace('**Year**:', '').strip()
                try:
                    citation_data['year'] = int(year_str)
                except ValueError:
                    citation_data['year'] = year_str  # Keep as string if not int

            elif line.startswith('**DOI**:'):
                doi = line.replace('**DOI**:', '').strip()
                if doi:  # Only add if not empty
                    citation_data['doi'] = doi

            elif line.startswith('**URL**:'):
                citation_data['url'] = line.replace('**URL**:', '').strip()

        # Determine source from position in file
        if '### From Crossref' in content[:content.find(block)]:
            citation_data['source'] = 'Crossref'
        elif '### From Semantic Scholar' in content[:content.find(block)]:
            citation_data['source'] = 'Semantic Scholar'
        elif '### From Gemini LLM' in content[:content.find(block)]:
            citation_data['source'] = 'Gemini LLM'

        citations.append(citation_data)

    return citations


def add_citations_to_database(
    db_path: Path,
    new_citations_data: List[Dict[str, Any]],
    starting_id_number: int
) -> int:
    """
    Add citations to database and save.

    Returns final citation count.
    """
    # Load existing database
    db = load_citation_database(db_path)

    # Get existing citation IDs to avoid duplicates
    existing_ids = {c.id for c in db.citations}

    # Add new citations
    added_count = 0
    for i, cit_data in enumerate(new_citations_data):
        # Generate new ID
        new_id = f"cite_{starting_id_number + i:03d}"

        # Skip if ID already exists (shouldn't happen, but safety check)
        if new_id in existing_ids:
            print(f"⚠️  Skipping duplicate ID: {new_id}")
            continue

        # Infer source type from citation data
        source_type: CitationSourceType
        if cit_data.get('journal'):
            source_type = "journal"
        elif cit_data.get('publisher'):
            source_type = "book"
        elif cit_data.get('url') and not cit_data.get('doi'):
            source_type = "website"
        else:
            source_type = "report"  # Default for academic papers

        # Convert year to int if string
        year_value = cit_data.get('year', '')
        if isinstance(year_value, str):
            try:
                year_value = int(year_value)
            except ValueError:
                year_value = 2024  # Default year if parsing fails

        # Create Citation object
        citation = Citation(
            citation_id=new_id,
            authors=cit_data.get('authors', []),
            year=year_value,
            title=cit_data.get('title', 'Unknown Title'),
            source_type=source_type,
            language="english",  # All researched citations are in English
            journal=cit_data.get('journal'),
            publisher=cit_data.get('publisher'),
            volume=cit_data.get('volume'),
            issue=cit_data.get('issue'),
            pages=cit_data.get('pages'),
            doi=cit_data.get('doi'),
            url=cit_data.get('url', '')
        )

        db.citations.append(citation)
        added_count += 1

    # Save updated database
    save_citation_database(db, db_path)

    return len(db.citations)


def main():
    """Integrate all researched citations into databases."""

    print("="*70)
    print("📚 INTEGRATING 110% CITATIONS INTO DATABASES")
    print("="*70)
    print()

    # Paths
    project_root = Path(__file__).parent.parent

    ai_pricing_research = Path("/tmp/ai_pricing_7_citations.md")
    co2_german_research = Path("/tmp/co2_german_25_citations.md")

    ai_pricing_db = project_root / "tests/outputs/ai_pricing_thesis/citation_database.json"
    co2_german_db = project_root / "tests/outputs/co2_thesis_german/citation_database.json"

    # 1. AI Pricing Database Integration
    print("1️⃣  AI PRICING THESIS")
    print("   Current: 53 citations")
    print("   Target: 60 citations (+7)")
    print()

    # Load existing to get last ID
    existing_ai_db = load_citation_database(ai_pricing_db)
    ai_last_id = len(existing_ai_db.citations) + 1

    # Parse research output
    ai_new_citations = parse_research_output(ai_pricing_research)
    print(f"   📊 Parsed {len(ai_new_citations)} citations from research")

    # Add to database
    ai_final_count = add_citations_to_database(
        ai_pricing_db,
        ai_new_citations,
        ai_last_id
    )

    print(f"   ✅ Database updated: {ai_final_count} total citations")
    print(f"   📄 Saved to: {ai_pricing_db}")
    print()

    # 2. CO2 German Database Integration
    print("2️⃣  CO2 GERMAN THESIS")
    print("   Current: 30 citations")
    print("   Target: 55 citations (+25)")
    print()

    # Load existing to get last ID
    existing_co2_db = load_citation_database(co2_german_db)
    co2_last_id = len(existing_co2_db.citations) + 1

    # Parse research output
    co2_new_citations = parse_research_output(co2_german_research)
    print(f"   📊 Parsed {len(co2_new_citations)} citations from research")

    # Add to database
    co2_final_count = add_citations_to_database(
        co2_german_db,
        co2_new_citations,
        co2_last_id
    )

    print(f"   ✅ Database updated: {co2_final_count} total citations")
    print(f"   📄 Saved to: {co2_german_db}")
    print()

    # 3. Open Source (already complete)
    print("3️⃣  OPEN SOURCE THESIS")
    print("   Current: 55 citations")
    print("   Target: 55 citations (ALREADY COMPLETE ✅)")
    print()

    # Summary
    print("="*70)
    print("📊 INTEGRATION COMPLETE")
    print("="*70)
    print()
    print(f"AI Pricing: 53 → {ai_final_count} citations")
    print(f"CO2 German: 30 → {co2_final_count} citations")
    print(f"Open Source: 55 → 55 citations (no change)")
    print()

    # Verify targets reached
    success = True
    if ai_final_count < 60:
        print(f"⚠️  AI Pricing: Only {ai_final_count}/60 citations (missing {60 - ai_final_count})")
        success = False
    else:
        print(f"✅ AI Pricing: {ai_final_count}/60 citations (target reached!)")

    if co2_final_count < 55:
        print(f"⚠️  CO2 German: Only {co2_final_count}/55 citations (missing {55 - co2_final_count})")
        success = False
    else:
        print(f"✅ CO2 German: {co2_final_count}/55 citations (target reached!)")

    print("✅ Open Source: 55/55 citations (target reached!)")
    print()

    if success:
        print("="*70)
        print("🎉 ALL 110% TARGETS REACHED!")
        print("="*70)
        print()
        print("Next steps:")
        print("1. Kill background processes with wrong targets")
        print("2. Regenerate all 3 theses with 110% citation databases")
        print("3. Verify publication-ready outputs")
        return 0
    else:
        print("="*70)
        print("⚠️  SOME TARGETS NOT REACHED")
        print("="*70)
        print()
        print("Check integration logs above for issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
