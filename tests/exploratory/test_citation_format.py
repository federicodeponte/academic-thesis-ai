#!/usr/bin/env python3
"""Quick test to verify citation formatter fix for missing publishers"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from utils.citation_database import Citation, CitationDatabase
from utils.citation_compiler import CitationCompiler

# Create test citations WITHOUT publishers
test_citations = [
    Citation(
        citation_id="cite_001",
        authors=["Benkler"],
        year=2006,
        title="The Wealth of Networks: How Social Production Transforms Markets and Freedom",
        source_type="book",
        language="english",
        publisher=None  # Missing publisher
    ),
    Citation(
        citation_id="cite_002",
        authors=["Chesbrough"],
        year=2003,
        title="Open Innovation: The New Imperative for Creating and Profiting from Technology",
        source_type="book",
        language="english",
        publisher=""  # Empty publisher
    ),
    Citation(
        citation_id="cite_003",
        authors=["O'Reilly"],
        year=1999,
        title="The Open Source Definition",
        source_type="book",
        language="english",
        publisher="O'Reilly Media"  # Has publisher
    )
]

# Create database
db = CitationDatabase(
    citations=test_citations,
    citation_style="APA 7th"
)

# Create compiler
compiler = CitationCompiler(database=db)

# Test formatting
print("=" * 70)
print("CITATION FORMATTER TEST - MISSING PUBLISHER FIX VERIFICATION")
print("=" * 70)
print()

for citation in test_citations:
    ref = compiler._format_apa_reference(citation)
    print(f"ID: {citation.id}")
    print(f"Publisher: {repr(citation.publisher)}")
    print(f"Reference: {ref}")

    # Check for buggy ". ." pattern
    if ". ." in ref:
        print("❌ BUG FOUND: Double period pattern detected!")
    else:
        print("✅ Correct formatting (no double period)")
    print()

print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
