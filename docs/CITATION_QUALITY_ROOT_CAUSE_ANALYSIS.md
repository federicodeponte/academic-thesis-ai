# Citation Quality: Root Cause Analysis

**Date**: 2025-11-19
**Issue**: ~50% of generated citations are low-quality/junk
**Current State**: Using post-generation filtering as band-aid

---

## Executive Summary

**Problem**: We're generating 55+ citations per thesis, but ~50% are junk (domain names as authors, broken URLs, hallucinations). Filtering reduces us to 28-30 citations - too few for a full thesis.

**Root Cause**: Citation generation uses Gemini Grounded Search which returns low-quality web results, not academic papers. We're asking for citations but getting website scrapes.

**Band-aid Solution** (Current): Filter junk after generation
- ❌ Wasteful (generate 55, throw away 25)
- ❌ Ends with too few citations (28-30)
- ❌ Doesn't address root cause

**Proper Solution** (Needed): Generate high-quality citations from the start
- ✅ Use academic APIs (Semantic Scholar, CrossRef, arXiv)
- ✅ Validate during generation, not after
- ✅ Generate 50+ REAL academic citations per thesis

---

## Current Citation Pipeline

### How Citations Are Generated Today

```
1. Signal Agent (03_signal.py)
   └─> Gemini API with Grounding enabled
       └─> Google Search grounding
           └─> Returns web pages (NOT academic papers)

2. Gemini returns citations with:
   - "api_source": "Gemini Grounded"
   - Often domain names as authors ("bcg.com", "mckinsey.com")
   - Often broken/paywalled URLs
   - Mix of real papers + junk websites

3. Metadata Scraping (scrape_citation_metadata.py)
   └─> Tries to fix bad citations by:
       - Scraping titles from URLs
       - Querying Crossref/Semantic Scholar
       - But can't fix fundamentally fake citations

4. Post-Generation Filtering (citation_quality_filter.py)
   └─> Removes obvious junk
       - Result: 28-30 citations (too few!)
```

### Why This Fails

**Gemini Grounded Search is NOT an academic database**:
- Returns general web results
- Prioritizes websites over academic papers
- No citation validation
- Hallucin ates authors and URLs

**Example Bad Citations** (from actual data):
```json
{
  "authors": ["dataconomy.com"],
  "title": "McKinsey: Open-source AI Tools...",
  "source_type": "website",
  "api_source": "Gemini Grounded"
}

{
  "authors": ["channelweb.co.uk"],
  "title": "channelweb.co.uk",
  "source_type": "website",
  "api_source": "Gemini Grounded"
}
```

These aren't academic citations - they're website scrapes.

---

## What We Should Do Instead

### Production-Grade Citation Generation

```
1. Query REAL Academic APIs First
   ├─> Semantic Scholar API (free, excellent)
   ├─> CrossRef API (DOI registry)
   ├─> arXiv API (preprints)
   └─> Google Scholar (via serpapi if needed)

2. Validate DURING Generation
   ├─> Check: Has DOI or arXiv ID?
   ├─> Check: Author is not a domain name?
   ├─> Check: Published in academic venue?
   └─> Reject: Anything that fails validation

3. Quality Thresholds
   ├─> Minimum citation count (40-50)
   ├─> Maximum retries (avoid infinite loops)
   └─> Fallback strategies if academic APIs fail

4. No Post-Filtering Needed
   └─> All citations are academic-grade from the start
```

### Academic API Integration

**Semantic Scholar** (RECOMMENDED):
```python
# Free, no API key required for basic use
# Returns: title, authors, year, venue, DOI, PDF URL, citation count

url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {
    "query": "open source software development",
    "fields": "title,authors,year,venue,externalIds,citationCount",
    "limit": 10
}
```

**CrossRef** (DOI Validation):
```python
# Validate that DOIs are real
url = f"https://api.crossref.org/works/{doi}"
# Returns: Full metadata if DOI exists, 404 if fake
```

**arXiv** (Preprints):
```python
# For computer science papers
url = "http://export.arxiv.org/api/query"
params = {"search_query": query, "max_results": 10}
```

---

## Implementation Plan

### Phase 1: Academic API Integration (Day 11)

**Goal**: Replace Gemini Grounded with real academic APIs

1. **Create `utils/academic_citation_search.py`**
   - `search_semantic_scholar(query, limit=10)` → List[Citation]
   - `search_crossref(query, limit=10)` → List[Citation]
   - `search_arxiv(query, limit=10)` → List[Citation]
   - `validate_doi(doi)` → bool
   - `validate_citation(citation)` → ValidationResult

2. **Add validation at generation time**
   - DOI must resolve (CrossRef check)
   - Author must not be domain name
   - Must have publication venue
   - Must have year

3. **Modify Signal Agent**
   - Remove Gemini Grounding for citations
   - Use academic APIs instead
   - Generate 50+ validated citations

4. **Testing**
   - Generate 1 thesis with new approach
   - Verify: 50+ citations, all academic-grade
   - Compare quality vs old approach

### Phase 2: Hybrid Approach (Day 12)

**Goal**: Combine academic APIs + carefully validated web sources

1. **Primary**: Academic APIs (80% of citations)
2. **Secondary**: Validated web sources (20%, only if needed)
   - Industry reports (McKinsey, BCG) - but validate properly
   - Government publications (.gov domains)
   - Technical documentation (official docs only)

3. **Strict validation rules** for web sources:
   - Whitelist of trusted domains
   - Must have real author (not domain name)
   - Must have publication date
   - URL must be accessible (not 403/404)

### Phase 3: Citation Quality Metrics (Day 13)

**Goal**: Measure and monitor citation quality

1. **Quality Score** per citation:
   - Has DOI: +2 points
   - Has arXiv ID: +1 point
   - Published in known venue: +2 points
   - Has citation count >10: +1 point
   - Author is verified: +1 point

2. **Thesis Quality Score**:
   - Average citation score
   - Minimum threshold: 4.0/7.0
   - Alert if below threshold

3. **Monitoring**:
   - Track API success rates
   - Track validation failure reasons
   - Alert on quality degradation

---

## Success Criteria

### Before (Current State):
- Generate 55 citations
- ~50% are junk
- Filter down to 28-30 citations
- ❌ Too few for thesis
- ❌ Wasteful process

### After (Target State):
- Generate 50-60 citations
- ~95% academic quality
- NO filtering needed
- ✅ 50+ real citations per thesis
- ✅ All from academic sources
- ✅ All validated

---

## Why This Matters

**Academic Integrity**:
- Theses should cite real research, not websites
- Domain names as authors destroy credibility
- Broken URLs frustrate readers

**User Trust**:
- Users expect academic-grade work
- Poor citations reflect badly on the entire system
- Quality > quantity

**Efficiency**:
- Stop generating junk just to filter it
- Direct path to quality citations
- Less wasted API calls

---

## Next Actions

1. **STOP current regeneration attempt #4**
   - It's using the same broken pipeline
   - Will produce 28-30 citations again

2. **Implement academic API integration** (Day 11)
   - Create `utils/academic_citation_search.py`
   - Add Semantic Scholar integration
   - Add validation functions

3. **Modify Signal Agent** to use academic APIs
   - Replace Gemini Grounding
   - Add validation loop
   - Generate 50+ quality citations

4. **Test with 1 thesis** before full regeneration
   - Verify quality improvement
   - Measure citation count
   - Compare to old approach

5. **Full regeneration** once proven
   - All 4 theses with new approach
   - Expect: 50+ citations each
   - Expect: >95% academic quality

---

## Conclusion

**Filtering is a band-aid**. We need to fix the generation pipeline to produce quality citations from the start.

The solution is clear:
1. Use academic APIs (Semantic Scholar, CrossRef, arXiv)
2. Validate during generation
3. Generate 50+ real academic citations per thesis

This is the production-grade solution. No more shortcuts.

---

**Status**: ⚠️ PENDING IMPLEMENTATION
**Priority**: 🔴 CRITICAL
**Timeline**: Days 11-13 (3 days)
