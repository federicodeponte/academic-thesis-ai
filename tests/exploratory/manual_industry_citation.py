#!/usr/bin/env python3
"""
Test script to verify industry sources appear with URLs in References section
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()  # Load .env file

import google.generativeai as genai
from utils.api_citations.orchestrator import CitationResearcher
from utils.citation_compiler import CitationCompiler
from utils.citation_database import CitationDatabase

def test_industry_citation():
    """Test that industry sources get URLs in formatted references."""

    print("=" * 80)
    print("TESTING INDUSTRY CITATION FORMATTING")
    print("=" * 80)
    print()

    # Setup
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        return False

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    # Test query (should route to Gemini Grounded)
    query = "World Bank climate finance report"
    print(f"📍 Test Query: {query}")
    print(f"   Expected: Routes to Gemini Grounded, finds URL")
    print()

    # Research citation
    print("🔍 Researching citation...")
    researcher = CitationResearcher(
        gemini_model=model,
        enable_smart_routing=True,
        enable_crossref=True,
        enable_semantic_scholar=True,
        enable_gemini_grounded=True,
        enable_llm_fallback=True,
        verbose=True
    )

    citation = researcher.research_citation(query)

    if not citation:
        print("❌ No citation found")
        return False

    print()
    print("✅ Citation found!")
    print(f"   Title: {citation.title}")
    print(f"   Authors: {citation.authors}")
    print(f"   Year: {citation.year}")
    print(f"   Source Type: {citation.source_type}")
    print(f"   DOI: {citation.doi or '(none)'}")
    print(f"   URL: {citation.url or '(none)'}")
    print()

    # Check source_type
    if citation.source_type != "website":
        print(f"⚠️  Expected source_type='website', got '{citation.source_type}'")
        print(f"   (This is OK if URL exists - fallback will work)")
        print()

    # Check URL exists
    if not citation.url:
        print("❌ FAIL: No URL found in citation")
        print("   Industry sources MUST have URLs")
        return False

    print("✅ URL exists in citation metadata")
    print()

    # Format as reference
    print("📝 Formatting as APA reference...")
    db = CitationDatabase(citation_style="APA 7th")
    db.citations = [citation]
    citation.id = "cite_001"

    compiler = CitationCompiler(db)
    formatted_ref = compiler._format_apa_reference(citation)

    print()
    print("Formatted Reference:")
    print("-" * 80)
    print(formatted_ref)
    print("-" * 80)
    print()

    # Check URL appears in formatted reference
    if citation.url in formatted_ref:
        print("✅ SUCCESS: URL appears in formatted reference!")
        print(f"   URL: {citation.url}")
        return True
    else:
        print("❌ FAIL: URL does NOT appear in formatted reference")
        print(f"   Expected to find: {citation.url}")
        print(f"   In formatted text: {formatted_ref}")
        return False


if __name__ == '__main__':
    try:
        success = test_industry_citation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
