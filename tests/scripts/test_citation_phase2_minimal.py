#!/usr/bin/env python3
"""
Minimal Phase 2 Test: Citation Database Architecture Integration
Tests that Crafters use citation IDs and Citation Compiler works
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.test_utils import setup_model, run_agent
from utils.citation_manager import extract_citations_from_text
from utils.citation_database import save_citation_database, load_citation_database
from utils.citation_compiler import CitationCompiler

def main():
    print("\n" + "="*70)
    print("📋 Phase 2 Minimal Integration Test")
    print("="*70)

    # Sample research notes with citations and references
    research_notes = """
# Research on Open Source Software

Recent studies show that open source development follows a bazaar model (Raymond, 1999).
The Linux kernel development demonstrates massive collaboration (Torvalds & Diamond, 2001).
Economic analysis reveals incentives for open source contribution (Lerner & Tirole, 2002).

## References

Raymond, E. S. (1999). The cathedral and the bazaar: Musings on Linux and open source by an accidental revolutionary. O'Reilly Media.

Torvalds, L., & Diamond, D. (2001). Just for fun: The story of an accidental revolutionary. HarperBusiness.

Lerner, J., & Tirole, J. (2002). Some simple economics of open source. The Journal of Industrial Economics, 50(2), 197-234. https://doi.org/10.1111/1467-6451.00174
"""

    # Step 1: Extract citations
    print("\n1. Testing Citation Manager...")
    model = setup_model()

    citation_database = extract_citations_from_text(
        text=research_notes,
        model=model,
        language="english",
        citation_style="APA 7th",
        verbose=True
    )

    print(f"\n✅ Extracted {len(citation_database.citations)} citations")

    # Prepare citation summary for Crafter
    citation_summary = f"\n\n## CITATION DATABASE\n\nYou have access to {len(citation_database.citations)} citations. Use citation IDs (cite_001, cite_002, etc.) instead of inline citations.\n\n"
    citation_summary += "Available citations:\n"
    for citation in citation_database.citations:
        authors_str = ", ".join(citation.authors[:2])
        if len(citation.authors) > 2:
            authors_str += " et al."
        citation_summary += f"- {citation.id}: {authors_str} ({citation.year}) - {citation.title[:60]}...\n"

    # Step 2: Test Crafter with citation database
    print("\n2. Testing Crafter with citation IDs...")

    crafter_output = run_agent(
        model=model,
        name="Crafter - Test Citation IDs",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"Write a brief paragraph (100 words) about open source development models.\n\n"
            f"Include:\n"
            f"- Reference to bazaar model\n"
            f"- Example of Linux kernel\n"
            f"- Economic incentives\n"
            f"{citation_summary}"
        ),
        save_to=None  # Don't save
    )

    if not crafter_output:
        print("❌ Crafter failed")
        return False

    print(f"\n📝 Crafter output preview:")
    print(crafter_output[:500])

    # Step 3: Check if Crafter used citation IDs
    print("\n3. Validating citation format...")

    has_citation_ids = "{cite_" in crafter_output
    has_inline_citations = "(" in crafter_output and ")" in crafter_output and any(
        str(year) in crafter_output for year in range(1990, 2025)
    )
    has_verify_tags = "[VERIFY]" in crafter_output

    if has_citation_ids:
        print("✅ Crafter used citation IDs (e.g., {cite_001})")
    else:
        print("❌ Crafter did NOT use citation IDs")

    if has_verify_tags:
        print("❌ Found [VERIFY] tags - FAILURE")
    else:
        print("✅ No [VERIFY] tags found")

    # Step 4: Test Citation Compiler
    print("\n4. Testing Citation Compiler...")

    compiler = CitationCompiler(citation_database)
    compiled_output, missing_ids = compiler.compile_citations(crafter_output)

    print(f"\n📝 Compiled output preview:")
    print(compiled_output[:500])

    # Validate compilation
    validation_result = compiler.validate_compilation(crafter_output, compiled_output)

    print(f"\n✅ Total citations: {validation_result['total_citations']}")
    print(f"✅ Successfully compiled: {validation_result['successfully_compiled']}")
    print(f"✅ Missing: {validation_result['missing_citations']}")

    # Step 5: Generate reference list
    print("\n5. Testing reference generation...")

    reference_list = compiler.generate_reference_list(crafter_output)
    print(reference_list)

    # Summary
    print("\n" + "="*70)
    print("📊 Phase 2 Integration Test Summary")
    print("="*70)

    success = (
        has_citation_ids and
        not has_verify_tags and
        validation_result['missing_citations'] == 0
    )

    if success:
        print("✅ Phase 2 Integration: SUCCESS")
        print("✅ Crafter uses citation IDs correctly")
        print("✅ No [VERIFY] tags created")
        print("✅ Citation Compiler achieves 100% success")
        print("\n🎯 Phase 2 proof of concept validated!")
    else:
        print("❌ Phase 2 Integration: FAILURE")
        if not has_citation_ids:
            print("   - Crafter not using citation IDs")
        if has_verify_tags:
            print("   - [VERIFY] tags still being created")
        if validation_result['missing_citations'] > 0:
            print(f"   - {validation_result['missing_citations']} missing citations")

    print("="*70)

    return success

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
