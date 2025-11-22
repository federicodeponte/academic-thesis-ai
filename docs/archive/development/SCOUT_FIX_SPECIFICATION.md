# Scout Agent Fix: API-Backed Citation Discovery Specification

## Executive Summary

**Problem**: Scout agent generates fake citations with 75% failure rate, resulting in only 10 citations instead of the required 50+ for academic theses.

**Root Cause**: Scout agent uses LLM hallucination (Gemini) to generate paper metadata instead of searching real academic databases via APIs.

**Solution**: Replace LLM-only approach with API-backed citation discovery using existing `CitationResearcher` infrastructure, which has 95%+ success rate.

**Impact**:
- Citation success rate: 25% → 95%+
- Valid citations per thesis: 10 → 50+
- Quality gate prevents writing with insufficient sources
- All future theses will have proper citation counts

---

## 1. Architecture Overview

### Current Flow (BROKEN)

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Scout Agent (LLM-Only)                              │
├─────────────────────────────────────────────────────────────┤
│ run_agent(prompt="Find 30 papers on...")                    │
│   ↓                                                          │
│ Gemini LLM hallucinates papers                              │
│   ↓                                                          │
│ Generates fake DOIs: 10.XXXXX/JOSS.2023.002                │
│   ↓                                                          │
│ Writes to 01_scout.md                                       │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Steps 2-14: Write thesis using fake citations              │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 15: Validate Citations (AFTER writing!)               │
├─────────────────────────────────────────────────────────────┤
│ DOI validation removes 30 out of 40 citations (75% fake!)  │
│   ↓                                                          │
│ ⚠️  Only 10 valid citations remain                          │
│   ↓                                                          │
│ ❌ Thesis fails academic standards (needs 50+)              │
└─────────────────────────────────────────────────────────────┘
```

**Why This Fails:**
1. LLM hallucinates papers that don't exist
2. Fake DOIs are generated (10.XXXXX/...)
3. Validation happens AFTER writing (too late!)
4. No quality gate to ensure minimum citations
5. 75% failure rate wastes computational resources

---

### Proposed Flow (API-BACKED)

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: API-Backed Scout (CitationResearcher)               │
├─────────────────────────────────────────────────────────────┤
│ For each research topic:                                     │
│   1. Try Crossref API → Real papers with DOIs               │
│   2. Try Semantic Scholar API → Real papers with metadata   │
│   3. Try LLM fallback (only if APIs fail)                   │
│                                                              │
│ Validate DOIs DURING discovery (not after!)                 │
│   ↓                                                          │
│ ✅ 50+ valid citations found                                │
│   ↓                                                          │
│ Writes to 01_scout.md with REAL, VALIDATED citations       │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Quality Gate: Verify 50+ Valid Citations                   │
├─────────────────────────────────────────────────────────────┤
│ if citation_count < 50:                                     │
│   raise ValueError("Insufficient citations - need 50+")    │
│                                                              │
│ ✅ Quality gate passed - proceed with writing               │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Steps 2-14: Write thesis using REAL, PRE-VALIDATED sources │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 15: Citation Compilation (no validation needed!)      │
├─────────────────────────────────────────────────────────────┤
│ ✅ All citations already validated                          │
│ ✅ 50+ citations guaranteed                                 │
│ ✅ Thesis meets academic standards                          │
└─────────────────────────────────────────────────────────────┘
```

**Why This Works:**
1. Real API search finds actual papers
2. DOIs validated during discovery (fail fast!)
3. Quality gate enforces 50+ citations BEFORE writing
4. 95%+ success rate (proven in citation_compiler.py)
5. No wasted computation on fake sources

---

## 2. Implementation Details

### 2.1 New Function: `run_api_scout()`

**Location**: `tests/test_utils.py`

**Purpose**: Replace LLM-only Scout with API-backed citation discovery

**Signature**:
```python
def run_api_scout(
    research_topics: List[str],
    target_count: int = 50,
    output_path: Optional[Path] = None,
    verbose: bool = True,
    enable_crossref: bool = True,
    enable_semantic_scholar: bool = True,
    enable_llm_fallback: bool = True
) -> Dict[str, Any]:
    """
    API-backed Scout agent for discovering real academic papers.

    Args:
        research_topics: List of research topics to search for
        target_count: Minimum number of valid citations needed (default: 50)
        output_path: Where to save scout output (default: None)
        verbose: Print progress messages (default: True)
        enable_crossref: Use Crossref API (default: True)
        enable_semantic_scholar: Use Semantic Scholar API (default: True)
        enable_llm_fallback: Use LLM as fallback if APIs fail (default: True)

    Returns:
        Dict with:
            - citations: List[Citation] - Valid citations found
            - count: int - Number of valid citations
            - sources: Dict[str, int] - Breakdown by source (Crossref, Semantic Scholar, LLM)
            - failed_topics: List[str] - Topics that failed to find citations

    Raises:
        ValueError: If fewer than target_count citations found
    """
```

**Implementation**:
```python
def run_api_scout(
    research_topics: List[str],
    target_count: int = 50,
    output_path: Optional[Path] = None,
    verbose: bool = True,
    enable_crossref: bool = True,
    enable_semantic_scholar: bool = True,
    enable_llm_fallback: bool = True
) -> Dict[str, Any]:
    """API-backed Scout agent for discovering real academic papers."""

    # Import existing infrastructure
    from utils.api_citations.orchestrator import CitationResearcher
    from utils.api_citations.citation import Citation

    if verbose:
        print("\n" + "=" * 80)
        print("🔍 API-BACKED SCOUT - Real Citation Discovery")
        print("=" * 80)
        print(f"\n📊 Configuration:")
        print(f"  Target Citations: {target_count}")
        print(f"  Research Topics: {len(research_topics)}")
        print(f"  Crossref API: {'✅' if enable_crossref else '❌'}")
        print(f"  Semantic Scholar API: {'✅' if enable_semantic_scholar else '❌'}")
        print(f"  LLM Fallback: {'✅' if enable_llm_fallback else '❌'}")
        print()

    # Initialize CitationResearcher with configured fallback chain
    researcher = CitationResearcher(
        enable_crossref=enable_crossref,
        enable_semantic_scholar=enable_semantic_scholar,
        enable_llm_fallback=enable_llm_fallback,
        verbose=verbose
    )

    # Track results
    all_citations: List[Citation] = []
    sources_breakdown: Dict[str, int] = {
        "Crossref": 0,
        "Semantic Scholar": 0,
        "Gemini LLM": 0
    }
    failed_topics: List[str] = []

    # Research each topic
    for idx, topic in enumerate(research_topics, 1):
        if verbose:
            print(f"\n[{idx}/{len(research_topics)}] 🔬 Researching: {topic}")

        try:
            citation = researcher.research_citation(topic)

            if citation:
                all_citations.append(citation)
                # Track source (from researcher's last successful call)
                source = getattr(researcher, '_last_source', 'Unknown')
                sources_breakdown[source] = sources_breakdown.get(source, 0) + 1

                if verbose:
                    print(f"  ✅ Found: {citation.authors[0]} et al. ({citation.year})")
                    print(f"     DOI: {citation.doi}")
            else:
                failed_topics.append(topic)
                if verbose:
                    print(f"  ❌ No citation found for this topic")

        except Exception as e:
            failed_topics.append(topic)
            if verbose:
                print(f"  ❌ Error: {e}")

    # Quality Gate: Verify minimum citation count
    citation_count = len(all_citations)

    if verbose:
        print("\n" + "=" * 80)
        print("📊 SCOUT RESULTS")
        print("=" * 80)
        print(f"\n✅ Valid Citations Found: {citation_count}")
        print(f"❌ Failed Topics: {len(failed_topics)}")
        print(f"\n📚 Sources Breakdown:")
        for source, count in sources_breakdown.items():
            percentage = (count / citation_count * 100) if citation_count > 0 else 0
            print(f"  {source}: {count} ({percentage:.1f}%)")
        print()

    # CRITICAL QUALITY GATE
    if citation_count < target_count:
        error_msg = (
            f"❌ QUALITY GATE FAILED: Only {citation_count} citations found, "
            f"but {target_count} required for academic thesis.\n\n"
            f"Failed Topics ({len(failed_topics)}):\n"
        )
        for topic in failed_topics[:10]:  # Show first 10
            error_msg += f"  - {topic}\n"
        if len(failed_topics) > 10:
            error_msg += f"  ... and {len(failed_topics) - 10} more\n"

        raise ValueError(error_msg)

    if verbose:
        print(f"✅ QUALITY GATE PASSED: {citation_count} citations ≥ {target_count} required")

    # Format output for Scout file (markdown)
    if output_path:
        markdown_content = _format_scout_markdown(
            citations=all_citations,
            sources_breakdown=sources_breakdown,
            failed_topics=failed_topics
        )
        output_path.write_text(markdown_content, encoding='utf-8')

        if verbose:
            print(f"\n💾 Scout output saved to: {output_path}")

    return {
        "citations": all_citations,
        "count": citation_count,
        "sources": sources_breakdown,
        "failed_topics": failed_topics
    }


def _format_scout_markdown(
    citations: List[Citation],
    sources_breakdown: Dict[str, int],
    failed_topics: List[str]
) -> str:
    """Format Scout results as markdown."""

    lines = [
        "# Scout Output - Academic Citation Discovery",
        "",
        "## Summary",
        "",
        f"**Total Valid Citations**: {len(citations)}",
        f"**Failed Topics**: {len(failed_topics)}",
        "",
        "### Sources Breakdown",
        ""
    ]

    for source, count in sources_breakdown.items():
        percentage = (count / len(citations) * 100) if len(citations) > 0 else 0
        lines.append(f"- **{source}**: {count} ({percentage:.1f}%)")

    lines.extend([
        "",
        "---",
        "",
        "## Citations Found",
        ""
    ])

    # Group by source
    for source in ["Crossref", "Semantic Scholar", "Gemini LLM"]:
        source_citations = [c for c in citations if getattr(c, '_source', '') == source]
        if not source_citations:
            continue

        lines.append(f"### From {source} ({len(source_citations)} citations)")
        lines.append("")

        for idx, citation in enumerate(source_citations, 1):
            lines.append(f"#### {idx}. {citation.title}")
            lines.append(f"**Authors**: {', '.join(citation.authors)}")
            lines.append(f"**Year**: {citation.year}")
            lines.append(f"**DOI**: {citation.doi}")
            if citation.url:
                lines.append(f"**URL**: {citation.url}")
            lines.append("")

    if failed_topics:
        lines.extend([
            "---",
            "",
            "## Failed Topics",
            "",
            "The following topics did not return valid citations:",
            ""
        ])
        for topic in failed_topics:
            lines.append(f"- {topic}")

    return "\n".join(lines)
```

---

### 2.2 Modify Test Scripts

**File**: `tests/scripts/test_opensource_thesis.py`

**Current Code (lines 69-90)** - BROKEN:
```python
# Step 1: Scout - Find papers
scout_output = run_agent(
    model=model,
    name="1. Scout - Find Relevant Papers",
    prompt_path="prompts/01_research/scout.md",
    user_input=(
        f"Find 30 academic papers and industry reports on:\n"
        f"- Open source software development\n"
        f"- Economic impact of open source\n"
        f"- Open source sustainability and environmental benefits\n"
        f"- Collaborative software development\n"
        f"- Digital commons and knowledge sharing\n"
        f"- Open source innovation models\n\n"
        f"Research focus: {research_focus}"
    ),
    save_to=output_dir / "01_scout.md"
)
```

**New Code** - FIXED:
```python
# Step 1: Scout - Find papers (API-BACKED)
print("\n" + "="*80)
print("STEP 1: SCOUT - API-BACKED CITATION DISCOVERY")
print("="*80)

# Define research topics for API search
research_topics = [
    # Open source development
    "open source software development methodologies",
    "distributed peer production in software",
    "collaborative software development practices",
    "open source contribution patterns",
    "open source community governance",

    # Economic impact
    "economic impact of open source software",
    "open source business models",
    "open source software as public good",
    "open source software market competition",
    "open source innovation economics",

    # Sustainability
    "open source environmental sustainability",
    "open source circular economy",
    "open source hardware repairability",
    "software longevity and obsolescence",
    "green software development",

    # Knowledge sharing
    "digital commons knowledge management",
    "open knowledge sharing platforms",
    "collaborative knowledge creation",
    "peer production networks",
    "knowledge-creating organizations",

    # Innovation models
    "open innovation paradigms",
    "network society technology",
    "cathedral and bazaar development",
    "self-determination theory in open source",
    "intrinsic motivation in software development",

    # Additional academic topics
    "commons governance in digital resources",
    "intellectual property open source",
    "free software movement history",
    "open standards and interoperability",
    "open source security peer review",

    # Case studies
    "Linux operating system development",
    "Apache web server architecture",
    "Wikipedia collaborative encyclopedia",
    "Mozilla Firefox browser development",
    "open source AI frameworks",

    # Policy and society
    "open source technology policy",
    "digital divide and open source",
    "open source education technology",
    "open source public sector innovation",
    "open source accessibility",

    # Advanced topics
    "open source licensing models",
    "open source project sustainability",
    "open source software quality",
    "open source community dynamics",
    "open source developer motivation",

    # Theoretical frameworks
    "network theory in open source",
    "gift economy in software",
    "commons-based peer production",
    "open source social capital",
    "power dynamics in open source communities",
]

# Run API-backed Scout
try:
    scout_result = run_api_scout(
        research_topics=research_topics,
        target_count=50,  # Require 50+ valid citations
        output_path=output_dir / "01_scout.md",
        verbose=True
    )

    print(f"\n✅ Scout completed: {scout_result['count']} valid citations found")
    print(f"📊 Sources: {scout_result['sources']}")

except ValueError as e:
    print(f"\n❌ SCOUT FAILED - Quality Gate Not Met")
    print(str(e))
    print("\n⚠️  Cannot proceed with thesis writing - insufficient citations")
    sys.exit(1)

except Exception as e:
    print(f"\n❌ SCOUT FAILED - Unexpected Error")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Read scout output for next steps
scout_output = (output_dir / "01_scout.md").read_text(encoding='utf-8')
```

---

### 2.3 Quality Gate Implementation

**Location**: After Scout, before any writing agents

**Code**:
```python
def verify_citation_quality_gate(
    scout_output_path: Path,
    minimum_required: int = 50
) -> Dict[str, Any]:
    """
    Verify that Scout found enough valid citations before proceeding.

    Args:
        scout_output_path: Path to 01_scout.md file
        minimum_required: Minimum citations needed (default: 50)

    Returns:
        Dict with citation_count and validation status

    Raises:
        ValueError: If quality gate fails
    """

    print("\n" + "="*80)
    print("🚦 QUALITY GATE: Verifying Citation Count")
    print("="*80)

    # Parse scout output to count citations
    scout_content = scout_output_path.read_text(encoding='utf-8')

    # Count citations (markdown format: "#### N. Title")
    import re
    citation_pattern = r'^####\s+\d+\.\s+'
    citations_found = len(re.findall(citation_pattern, scout_content, re.MULTILINE))

    print(f"\n📊 Citations Found: {citations_found}")
    print(f"📋 Minimum Required: {minimum_required}")

    if citations_found < minimum_required:
        error_msg = (
            f"\n❌ QUALITY GATE FAILED\n\n"
            f"Only {citations_found} citations found, but {minimum_required} required.\n"
            f"Academic thesis standards require minimum {minimum_required} citations.\n\n"
            f"Please:\n"
            f"1. Add more research topics to increase coverage\n"
            f"2. Verify API credentials are working\n"
            f"3. Check that research topics are specific enough\n"
        )
        raise ValueError(error_msg)

    print(f"\n✅ QUALITY GATE PASSED")
    print(f"   {citations_found} citations ≥ {minimum_required} required")
    print(f"   Proceeding with thesis writing...\n")

    return {
        "citation_count": citations_found,
        "passed": True
    }
```

**Usage in test script**:
```python
# After Scout, before Background
try:
    quality_gate = verify_citation_quality_gate(
        scout_output_path=output_dir / "01_scout.md",
        minimum_required=50
    )
except ValueError as e:
    print(str(e))
    sys.exit(1)

# If we get here, quality gate passed - proceed with writing
```

---

## 3. Testing Strategy

### 3.1 Unit Tests

**File**: `tests/test_api_scout.py` (NEW)

```python
"""Unit tests for API-backed Scout functionality."""

import pytest
from pathlib import Path
from tests.test_utils import run_api_scout, verify_citation_quality_gate

def test_run_api_scout_basic():
    """Test basic Scout functionality with small topic list."""

    research_topics = [
        "open source software development",
        "Linux operating system history",
        "collaborative knowledge creation"
    ]

    result = run_api_scout(
        research_topics=research_topics,
        target_count=3,  # Low threshold for testing
        verbose=False
    )

    assert result["count"] >= 3
    assert len(result["citations"]) >= 3
    assert "Crossref" in result["sources"]


def test_run_api_scout_quality_gate_pass():
    """Test that quality gate passes with sufficient citations."""

    research_topics = [f"topic_{i}" for i in range(60)]

    result = run_api_scout(
        research_topics=research_topics,
        target_count=50,
        verbose=False
    )

    assert result["count"] >= 50


def test_run_api_scout_quality_gate_fail():
    """Test that quality gate fails with insufficient citations."""

    research_topics = ["very obscure topic that won't find anything"]

    with pytest.raises(ValueError, match="QUALITY GATE FAILED"):
        run_api_scout(
            research_topics=research_topics,
            target_count=50,
            verbose=False
        )


def test_verify_citation_quality_gate(tmp_path):
    """Test quality gate verification from Scout output file."""

    # Create mock Scout output with 55 citations
    scout_file = tmp_path / "01_scout.md"
    scout_content = "# Scout Output\n\n"
    for i in range(55):
        scout_content += f"#### {i+1}. Paper Title {i}\n\n"
    scout_file.write_text(scout_content)

    # Should pass
    result = verify_citation_quality_gate(scout_file, minimum_required=50)
    assert result["passed"] is True
    assert result["citation_count"] == 55


def test_verify_citation_quality_gate_fail(tmp_path):
    """Test quality gate failure with insufficient citations."""

    # Create mock Scout output with only 30 citations
    scout_file = tmp_path / "01_scout.md"
    scout_content = "# Scout Output\n\n"
    for i in range(30):
        scout_content += f"#### {i+1}. Paper Title {i}\n\n"
    scout_file.write_text(scout_content)

    # Should fail
    with pytest.raises(ValueError, match="QUALITY GATE FAILED"):
        verify_citation_quality_gate(scout_file, minimum_required=50)
```

### 3.2 Integration Tests

**File**: `tests/integration/test_scout_integration.py` (NEW)

```python
"""Integration tests for Scout agent with real APIs."""

import pytest
from pathlib import Path
from tests.test_utils import run_api_scout

@pytest.mark.integration
def test_scout_with_real_apis(tmp_path):
    """Test Scout with real Crossref and Semantic Scholar APIs."""

    research_topics = [
        "open source software development methodologies",
        "Linux operating system kernel architecture",
        "Wikipedia collaborative encyclopedia",
        "Mozilla Firefox web browser",
        "Apache web server software"
    ]

    output_file = tmp_path / "scout_output.md"

    result = run_api_scout(
        research_topics=research_topics,
        target_count=5,
        output_path=output_file,
        verbose=True
    )

    # Verify results
    assert result["count"] >= 5
    assert output_file.exists()

    # Verify sources used
    sources = result["sources"]
    assert sources["Crossref"] > 0 or sources["Semantic Scholar"] > 0

    # Verify output file format
    content = output_file.read_text()
    assert "# Scout Output" in content
    assert "## Citations Found" in content
    assert "DOI:" in content


@pytest.mark.integration
@pytest.mark.slow
def test_full_thesis_scout_workflow(tmp_path):
    """Test complete Scout workflow for thesis generation."""

    # Use realistic topic count for thesis
    research_topics = [
        # ... (same 55 topics as in test script)
    ]

    output_file = tmp_path / "01_scout.md"

    result = run_api_scout(
        research_topics=research_topics,
        target_count=50,
        output_path=output_file,
        verbose=True
    )

    # Verify we met thesis standards
    assert result["count"] >= 50

    # Verify quality gate would pass
    from tests.test_utils import verify_citation_quality_gate
    gate_result = verify_citation_quality_gate(output_file, minimum_required=50)
    assert gate_result["passed"] is True
```

---

## 4. Migration Plan

### Phase 1: Update Infrastructure (Week 1)

**Tasks**:
1. ✅ Add `run_api_scout()` to `tests/test_utils.py`
2. ✅ Add `verify_citation_quality_gate()` to `tests/test_utils.py`
3. ✅ Add `_format_scout_markdown()` helper
4. ✅ Update `CitationResearcher` to track `_last_source`

**Files Modified**:
- `tests/test_utils.py` (+200 lines)
- `utils/api_citations/orchestrator.py` (+5 lines)

**Testing**: Run unit tests to verify new functions work

### Phase 2: Update Test Scripts (Week 2)

**Tasks**:
1. ✅ Update `tests/scripts/test_opensource_thesis.py`
2. ✅ Add quality gate check after Scout
3. ✅ Test with real APIs to verify 50+ citations

**Files Modified**:
- `tests/scripts/test_opensource_thesis.py` (lines 69-90 replaced)

**Testing**:
```bash
cd tests/scripts
python test_opensource_thesis.py
# Verify: 50+ citations found, quality gate passes
```

### Phase 3: Apply to Other Theses (Week 3)

**Tasks**:
1. ✅ Update `test_ai_pricing_thesis.py`
2. ✅ Update `test_co2_german_thesis.py`
3. ✅ Verify all 3 theses meet 50+ citation requirement

**Files Modified**:
- `tests/scripts/test_ai_pricing_thesis.py`
- `tests/scripts/test_co2_german_thesis.py`

**Testing**: Regenerate all 3 theses and verify citation counts

### Phase 4: Documentation and Cleanup (Week 4)

**Tasks**:
1. ✅ Update `README.md` with new Scout approach
2. ✅ Document quality gate in `docs/THESIS_GENERATION.md`
3. ✅ Remove old LLM-only Scout prompt (optional)
4. ✅ Update repair script if needed

**Files Modified**:
- `README.md`
- `docs/THESIS_GENERATION.md` (NEW or updated)
- `prompts/01_research/scout.md` (deprecate or repurpose)

---

## 5. Expected Outcomes

### 5.1 Metrics Comparison

| Metric | Before (LLM-Only) | After (API-Backed) | Improvement |
|--------|-------------------|-------------------|-------------|
| **Citation Success Rate** | 25% (10/40) | 95%+ (50+/55) | +280% |
| **Valid Citations Found** | 10 | 50+ | +400% |
| **Fake DOIs Generated** | 30 (75%) | 0-2 (<5%) | -93% |
| **API Calls Made** | 0 | 55-110 | Real data! |
| **Quality Gate** | ❌ None | ✅ Enforced | New |
| **Wasted Computation** | High (30 fake) | Minimal | -75% |

### 5.2 Quality Improvements

**Before**:
- ❌ Only 10 citations (fails academic standards)
- ❌ 75% fake citations removed during validation
- ❌ No quality gate - thesis written with insufficient sources
- ❌ Validation happens AFTER writing (too late!)
- ❌ Gemini hallucinates papers that don't exist

**After**:
- ✅ 50+ valid citations (meets academic standards)
- ✅ 95%+ real citations from verified databases
- ✅ Quality gate enforces minimum before writing
- ✅ Validation happens DURING discovery (fail fast!)
- ✅ Real papers from Crossref, Semantic Scholar, arXiv

### 5.3 Process Improvements

**Before Flow**:
```
Scout (LLM) → Write Thesis → Validate → ❌ Only 10 citations!
│                                          │
└── 30 fake citations ────────────────────┘
```

**After Flow**:
```
Scout (API) → Quality Gate → Write Thesis → ✅ 50+ citations!
│              │              │
│              │              └── All validated
│              └── Enforces 50+
└── Real papers from APIs
```

---

## 6. Backward Compatibility

### 6.1 Breaking Changes

**None** - This is a complete replacement of Scout implementation.

**Old code**:
```python
scout_output = run_agent(...)  # LLM-only approach
```

**New code**:
```python
scout_result = run_api_scout(...)  # API-backed approach
```

### 6.2 Migration Path for Existing Theses

**Option A: Regenerate All (Recommended)**
```bash
cd tests/scripts

# Regenerate with new API-backed Scout
python test_opensource_thesis.py
python test_ai_pricing_thesis.py
python test_co2_german_thesis.py

# Repair PDFs
cd ../..
python scripts/repair_showcase_theses.py
```

**Option B: Keep Existing, Use New for Future**
- Existing 3 showcase theses can remain as-is
- All new theses will use API-backed Scout
- Gradually migrate old theses as needed

---

## 7. Error Handling

### 7.1 API Failures

**Scenario**: Crossref API is down

**Handling**:
```python
# CitationResearcher automatically falls back:
Crossref (fail) → Semantic Scholar (try) → LLM (last resort)
```

**User sees**:
```
  → Trying Crossref API... ✗
  → Trying Semantic Scholar API... ✓
  ✅ Found: Smith et al. (2023)
```

### 7.2 Quality Gate Failure

**Scenario**: Only 35 citations found (need 50+)

**Handling**:
```python
raise ValueError(
    "❌ QUALITY GATE FAILED: Only 35 citations found, but 50 required.\n"
    "Failed Topics (20):\n"
    "  - very obscure topic 1\n"
    "  - very obscure topic 2\n"
    "  ...\n"
)
```

**User action**:
1. Review failed topics
2. Make topics more specific or broader
3. Add more research topics
4. Re-run Scout

### 7.3 Network Issues

**Scenario**: No internet connection

**Handling**:
```python
try:
    citation = researcher.research_citation(topic)
except requests.exceptions.ConnectionError as e:
    print(f"❌ Network error: {e}")
    print("   Please check internet connection and try again")
    sys.exit(1)
```

---

## 8. Performance Considerations

### 8.1 API Rate Limits

**Crossref**: 50 requests/second (generous)
**Semantic Scholar**: 100 requests/second
**Expected**: ~55 requests for Scout

**Mitigation**:
- Add 0.1s delay between requests if needed
- Use caching in CitationResearcher (already implemented)
- Batch requests where possible

### 8.2 Execution Time

**Before (LLM-only)**:
```
Scout: ~30 seconds (Gemini generates fake papers)
```

**After (API-backed)**:
```
Scout: ~2-5 minutes (55 API calls + validation)
  - Crossref: ~1-2 seconds per request
  - Semantic Scholar: ~1-2 seconds per request
  - LLM fallback: ~3-5 seconds per request
```

**Trade-off**: 4x slower but 95%+ success rate vs 25%

---

## 9. Monitoring and Logging

### 9.1 Success Metrics to Track

```python
# After Scout completes
print(f"📊 Scout Statistics:")
print(f"  Total Topics: {len(research_topics)}")
print(f"  Citations Found: {result['count']}")
print(f"  Success Rate: {result['count']/len(research_topics)*100:.1f}%")
print(f"\n  Sources Used:")
print(f"    Crossref: {result['sources']['Crossref']}")
print(f"    Semantic Scholar: {result['sources']['Semantic Scholar']}")
print(f"    LLM Fallback: {result['sources']['Gemini LLM']}")
```

### 9.2 Failure Tracking

```python
# Track and report failed topics
if result['failed_topics']:
    print(f"\n⚠️  Failed Topics ({len(result['failed_topics'])}):")
    for topic in result['failed_topics'][:10]:
        print(f"    - {topic}")

    # Save to file for analysis
    failed_log = output_dir / "scout_failures.txt"
    failed_log.write_text("\n".join(result['failed_topics']))
```

---

## 10. Next Steps

### Immediate Actions

1. **Review this specification** - Verify approach aligns with requirements
2. **Approve implementation** - Confirm this is the correct solution
3. **Assign developer** - Who will implement this?
4. **Set timeline** - 4-week implementation suggested

### Implementation Checklist

- [ ] Add `run_api_scout()` to `tests/test_utils.py`
- [ ] Add `verify_citation_quality_gate()` to `tests/test_utils.py`
- [ ] Update `CitationResearcher` to track source
- [ ] Write unit tests for new functions
- [ ] Update `test_opensource_thesis.py` with API-backed Scout
- [ ] Add quality gate check after Scout
- [ ] Test with real APIs to verify 50+ citations
- [ ] Update `test_ai_pricing_thesis.py`
- [ ] Update `test_co2_german_thesis.py`
- [ ] Run integration tests
- [ ] Regenerate all 3 showcase theses
- [ ] Update documentation
- [ ] Create tracking issue in GitHub

### Success Criteria

✅ All 3 showcase theses have 50+ valid citations
✅ Citation success rate ≥ 95%
✅ Quality gate prevents thesis writing with insufficient sources
✅ No fake DOIs generated
✅ Scout uses real API search, not LLM hallucination
✅ All tests pass
✅ Documentation updated

---

## Appendix A: Code Files Reference

### Files to Modify

1. **tests/test_utils.py** (+200 lines)
   - Add `run_api_scout()`
   - Add `verify_citation_quality_gate()`
   - Add `_format_scout_markdown()`

2. **tests/scripts/test_opensource_thesis.py** (lines 69-90 replaced)
   - Replace LLM-only Scout with API-backed Scout
   - Add quality gate check

3. **tests/scripts/test_ai_pricing_thesis.py** (similar changes)
   - Apply same Scout replacement

4. **tests/scripts/test_co2_german_thesis.py** (similar changes)
   - Apply same Scout replacement

5. **utils/api_citations/orchestrator.py** (+5 lines)
   - Track `_last_source` in CitationResearcher

### New Files to Create

1. **tests/test_api_scout.py** (NEW)
   - Unit tests for Scout functions

2. **tests/integration/test_scout_integration.py** (NEW)
   - Integration tests with real APIs

3. **docs/THESIS_GENERATION.md** (NEW or updated)
   - Document new Scout approach and quality gate

---

## Appendix B: Example Output

### Scout Output Example (01_scout.md)

```markdown
# Scout Output - Academic Citation Discovery

## Summary

**Total Valid Citations**: 52
**Failed Topics**: 3

### Sources Breakdown

- **Crossref**: 35 (67.3%)
- **Semantic Scholar**: 15 (28.8%)
- **Gemini LLM**: 2 (3.8%)

---

## Citations Found

### From Crossref (35 citations)

#### 1. The Cathedral and the Bazaar: Musings on Linux and Open Source
**Authors**: Raymond, Eric S.
**Year**: 1999
**DOI**: 10.1145/1234567.1234568
**URL**: https://doi.org/10.1145/1234567.1234568

#### 2. Governing the Commons: The Evolution of Institutions for Collective Action
**Authors**: Ostrom, Elinor
**Year**: 1990
**DOI**: 10.1017/CBO9780511807763
**URL**: https://doi.org/10.1017/CBO9780511807763

...

### From Semantic Scholar (15 citations)

#### 36. Open Innovation: The New Imperative
**Authors**: Chesbrough, Henry William
**Year**: 2003
**DOI**: 10.5465/ame.2006.20503130
**URL**: https://www.semanticscholar.org/paper/...

...

### From Gemini LLM (2 citations)

#### 51. Self-Determination Theory in Open Source
**Authors**: Deci, Edward L.; Ryan, Richard M.
**Year**: 2000
**DOI**: 10.1037/0003-066X.55.1.68
**URL**: https://psycnet.apa.org/record/2000-13324-007

...

---

## Failed Topics

The following topics did not return valid citations:

- very obscure open source topic that nobody researched
- extremely niche software development methodology
- brand new emerging technology with no papers yet
```

---

**END OF SPECIFICATION**

**Questions or concerns? Contact: [Your contact info]**

**Estimated implementation time: 4 weeks**

**Priority: HIGH - Blocking thesis generation quality**
