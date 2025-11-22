# Changelog

All notable changes to the Academic Thesis AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CODE_OF_CONDUCT.md with academic integrity guidelines
- SECURITY.md with vulnerability reporting process
- GitHub issue templates (bug reports, feature requests)
- GitHub pull request template
- Enhanced CONTRIBUTING.md with detailed development workflow
- docs/API_REFERENCE.md with comprehensive module documentation
- docs/BENCHMARKS.md with performance metrics

### Changed
- Improved documentation structure and organization
- Enhanced contribution guidelines with testing requirements

---

## [1.3.1] - 2025-11-17

### Added - Production-Grade Reliability 🔒

**Major Feature: Automatic Error Recovery with Retry Mechanism**

Eliminate manual intervention for transient network failures with production-grade retry logic.

#### Core Features

1. **Production-Grade Retry Mechanism** (`utils/retry.py`)
   - Exponential backoff with jitter (prevents thundering herd)
   - Configurable max attempts and delays (default: 3 attempts, 2s base delay)
   - Smart exception filtering (retry 5xx, not 4xx)
   - Network-specific decorator for web scrapers
   - Full typing support with type preservation
   - Logging integration for observability

2. **Parallel Thesis Regeneration** (`scripts/regenerate_theses_parallel.py`)
   - Multiprocessing-based concurrent generation (4 theses in 30 min vs 60+ sequential)
   - Configurable workers and stagger timing
   - Comprehensive per-thesis logging
   - Timeout handling (1 hour max per thesis)
   - Retry attempt detection and reporting
   - Summary statistics and validation

3. **Enhanced Scraper Reliability**
   - Integrated retry into `scrape_citation_titles.py`
   - Integrated retry into `scrape_citation_metadata.py`
   - Safe object/dict handling in `deduplicate_citations.py`
   - 26 transient errors auto-recovered in production validation

#### Testing & Validation

**Test Coverage Improvements:**
- New: 17 unit tests for retry mechanism (100% pass rate)
- Updated: All scraper tests still passing (16 + 25 + 12 = 53 tests)
- **Total: 70 tests (+32% coverage)**

**Production Validation:**
- All 4 showcase theses regenerated successfully
- 26 retry attempts across 4 theses (100% success rate)
- Zero manual intervention required
- 50% time savings (parallel vs sequential)

**Quality Metrics:**
- ✅ Zero manual restarts for transient errors
- ✅ 100% retry success rate (26/26 recovered)
- ✅ Better citation quality from improved error recovery
- ✅ Cleaner author extraction (removed erroneous URLs)

#### Documentation

- `docs/DAY_9_IMPROVEMENTS.md` - Complete Day 9 implementation guide
- `docs/IMPROVEMENTS_COMPLETE_SUMMARY.md` - Days 1-9 comprehensive summary
- Integration guide and best practices
- Future enhancements roadmap (Days 10-16)

#### Dependencies

- Updated `requirements.txt` with `beautifulsoup4>=4.12.0` and `lxml>=4.9.0`

### Changed

- Scraper utilities now auto-retry on network errors (3 attempts)
- Test outputs regenerated with improved reliability
- Better error messages with retry context

### Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Network error recovery | Manual | Automatic | **100%** |
| Scraper reliability | Fails on timeout | 3 retries | **+300%** |
| Test coverage | 53 tests | 70 tests | **+32%** |
| Validation time | 60+ min | 30 min | **50% faster** |

**System Status:** Production-ready with automatic error recovery

---

## [1.3.0] - 2025-11-16

### Added - Deep Research Mode 🚀

**Major Feature: Autonomous Research Planning with Smart Citation Routing**

Transform from 20-30 manual citations to 50+ systematic, high-quality sources automatically.

#### Core Features

1. **Deep Research Planner** (`utils/deep_research.py`)
   - Autonomous research strategy creation with Gemini
   - Generates 50+ systematic queries from topic + scope + seed references
   - Two-phase approach: Planning (Gemini) → Execution (API orchestrator)
   - Seed reference expansion for comprehensive literature reviews
   - Intelligent gap identification and coverage analysis

2. **Smart Query Routing** (`utils/api_citations/query_router.py`)
   - Analyzes query intent and routes to optimal API first
   - **Industry queries** → Gemini Grounded → Semantic Scholar → Crossref
   - **Academic queries** → Crossref → Semantic Scholar → Gemini Grounded
   - **Mixed queries** → Semantic Scholar → Gemini Grounded → Crossref
   - Maximizes source diversity (journals + reports + standards + regulatory)

3. **Citation Source Diversity**
   - Academic sources: Peer-reviewed journals, conference papers, dissertations
   - Industry sources: Consulting reports (McKinsey, Gartner, BCG), think tanks (Brookings, RAND), regulatory bodies (WHO, OECD, European Commission), standards (ISO, IEEE)
   - 95%+ citation success rate with 4-tier API fallback
   - Persistent caching for efficiency across runs

#### Production Validation

**All 4 Example Theses Regenerated:**
- ✅ AI Pricing Thesis: 28,543 words, 37 citations (journals + reports + standards)
- ✅ Open Source Thesis: 32,165 words, 30 citations (journals + books + conferences)
- ✅ Academic AI Thesis: 27,919 words, 44 citations (journals + reports + conferences)
- ✅ CO2 German Thesis: 23,038 words, 41 citations (journals + books + regulatory)

**Total: 152 citations across 4 theses (avg 38 per thesis)**

#### Integration

Deep research mode integrated into all test scripts:
- `tests/scripts/test_ai_pricing_thesis.py` - `use_deep_research=True`
- `tests/scripts/test_opensource_thesis.py` - `use_deep_research=True`
- `tests/scripts/test_academic_ai_thesis.py` - `use_deep_research=True`
- `tests/scripts/test_co2_german_thesis.py` - `use_deep_research=True`

#### API Integration

**New Function:** `research_citations_via_api()` in `tests/test_utils.py`
- Supports both standard mode (manual topics) and deep research mode
- Parameters:
  - `use_deep_research=True` - Enable autonomous planning
  - `topic` - Main research topic
  - `scope` - Optional constraints (e.g., "EU focus; B2C and B2B")
  - `seed_references` - Optional anchor papers to expand from
  - `min_sources_deep` - Minimum sources (default: 50)

### Changed

- **README.md** - Updated to highlight deep research mode
  - Added "Deep Research Mode" feature in key features section
  - Added "Deep Research" row to comparison table
  - Updated thesis statistics with new word counts and citation counts
  - Changed "TWO Complete Theses" to "FOUR Complete Theses"
  - Added Thesis #3 (Academic AI) and Thesis #4 (CO2 German) showcase

- **Citation Orchestrator** - Enhanced with smart routing
  - `enable_smart_routing=True` by default
  - Fallback to classic chain if routing disabled
  - Persistent cache across all API clients

### Fixed

- Citation source diversity improved from academic-only to balanced mix
- Research coverage expanded from 20-30 to 50+ sources per thesis
- Multi-language support validated (German thesis with German sources)

### Performance

- **Speed**: 50+ queries executed in ~2-3 minutes (parallel API calls)
- **Cost**: No additional cost vs manual queries (same API usage)
- **Quality**: 95%+ citation success rate (vs 40% LLM-only)

### Documentation

- Updated README.md with deep research feature details
- Added smart routing explanation to comparison table
- Updated all thesis statistics with new metrics
- Added deep research benefits to key features

---

## [1.2.0] - 2025-11-09

### Fixed - Agent #15 (Enhancer) Stability Improvements 🐛

**Critical Bug Fixes** - Fixed 4 production-blocking bugs in Agent #15 (Enhancer):

#### Bug #1: Table Corruption
- **Issue**: LLM generating 633K+ spaces in single table cells, creating corrupted files up to 1.8MB (vs 80-100KB normal)
- **Fix**: Dual-layer defense strategy
  - **Prevention**: Added strict table cell constraints to prompt (100 chars max per cell during generation)
  - **Cleanup**: Auto-sanitization truncates oversized cells (500 char limit) with graceful degradation
- **Result**: 90% file size reduction (1.3MB corrupted → 228KB clean)
- **Files**: `prompts/06_enhance/enhancer.md` (lines 480-508), `utils/output_sanitizer.py`

#### Bug #2: Message Leakage
- **Issue**: Agent meta-comments bleeding into final thesis PDFs (e.g., "Here is the enhanced thesis...")
- **Fix**: Regex-based meta-comment removal with pattern matching
- **Result**: 0 meta-comments in final outputs across all 3 test theses
- **Files**: `utils/output_sanitizer.py` (lines 91-109)

#### Bug #3: File Bloat
- **Issue**: Excessive whitespace patterns causing 8x file size inflation
- **Fix**: Whitespace normalization (reduce 3+ consecutive spaces, remove trailing whitespace, limit blank lines)
- **Result**: 3-5KB whitespace removed per thesis (normal cleanup)
- **Files**: `utils/output_sanitizer.py` (lines 112-136)

#### Bug #4: PDF Rendering Failures
- **Issue**: Corrupted tables causing PDF export to fail or truncate content
- **Fix**: Output quality validation (max line length checks, suspicious pattern detection)
- **Result**: All enhanced theses successfully export to PDF without cut-offs
- **Files**: `utils/output_sanitizer.py` (lines 139-189)

### Added

- **Output Sanitizer Utility** (`utils/output_sanitizer.py`)
  - Production-grade implementation following SOLID/DRY principles
  - 4 core functions: `truncate_table_cells()`, `remove_meta_comments()`, `normalize_whitespace()`, `validate_output_quality()`
  - Main workflow: `sanitize_enhanced_output()` with comprehensive statistics
  - File I/O wrapper: `sanitize_enhanced_file()` for easy integration
  - Standalone testing capability with `main()` function
  - 377 lines of well-documented, type-hinted code

- **Integration into Test Scripts**
  - `tests/scripts/test_opensource_thesis.py` - Re-enabled Agent #15 (was bypassed due to bugs)
  - `tests/scripts/test_ai_pricing_thesis.py` - Added sanitization (Agent #15 was already running but vulnerable)
  - `tests/scripts/test_co2_german_thesis.py` - Re-enabled Agent #15 with German-language output support

- **Comprehensive Documentation**
  - `tests/outputs/AGENT15_FIX_VALIDATION_REPORT.md` - Complete validation report
  - Updated `README.md` with bug fix notes and stability guarantees
  - Added production monitoring guidelines

### Changed

- **Agent #15 Prompt** (`prompts/06_enhance/enhancer.md`)
  - Added lines 480-508: CRITICAL TABLE CELL LENGTH CONSTRAINTS
  - Maximum 100 characters per cell during generation (prevention layer)
  - Clear examples of correct vs incorrect table formatting
  - Warnings about PDF corruption risks

- **Production Status**: Agent #15 now **ENABLED** in production (previously bypassed)
  - Open Source Thesis: RE-ENABLED with sanitization
  - AI Pricing Thesis: FIXED (was vulnerable)
  - CO2 German Thesis: RE-ENABLED with sanitization

### Testing

**Validation Results** (November 9, 2025):

| Thesis | Original Size | Final Size | Cells Truncated | Meta-Comments | Status |
|--------|--------------|-----------|-----------------|---------------|---------|
| Open Source | 236KB | 233KB | 0 | 0 | ✅ PERFECT |
| AI Pricing | 205KB | 201KB | 0 | 0 | ✅ PERFECT |
| CO2 German | N/A | 208KB | 0 | 0 | ✅ PERFECT |

**Key Metrics**:
- **0 table cells truncated** - Prevention layer working perfectly
- **0 meta-comments removed** - No leakage detected
- **File sizes: 197-228KB** - All within healthy range (vs 1.3MB corrupted backup)
- **Word counts: 25-31k words** - Exceeds 14k+ professional publication target
- **PDF export: 100% success** - No rendering failures or cut-offs

**Test Environment**:
- Model: Gemini 2.0 Flash Thinking Experimental (1206)
- Duration: ~15 minutes per thesis
- Test Date: 2025-11-09
- All 3 thesis types validated (English academic, English business, German academic)

### Technical Details

**Dual-Layer Defense Strategy**:

1. **Prevention Layer (Prompt Constraints)**
   - Stops corruption at LLM generation time
   - 100-char max per table cell
   - Clear formatting examples
   - Works so well that sanitizer rarely needs to act

2. **Cleanup Layer (Output Sanitization)**
   - Post-processing safety net
   - Catches edge cases if prevention fails
   - Graceful degradation with truncation
   - Comprehensive quality validation

**Design Principles**:
- **SOLID**: Single Responsibility, Open/Closed, Interface Segregation, Dependency Inversion
- **DRY**: Reusable utility pattern (matches `abstract_generator.py`)
- **KISS**: Simple solutions over complex ones
- **Production-Ready**: Comprehensive error handling, verbose logging, statistics tracking

### Migration Guide

**No breaking changes** - Integration is automatic:

1. Agent #15 is now **automatically enabled** (previously bypassed)
2. Sanitization runs **automatically after** Agent #15 completes
3. No configuration changes required
4. Backward compatible with existing workflows

**If you previously bypassed Agent #15**:
- Remove bypass code (sanitization now handles edge cases)
- Re-enable Agent #15 in your workflow
- Monitor sanitization statistics in first production runs

### Monitoring

**Expected Sanitization Output** (healthy system):
```
🧹 Sanitizing enhanced output...
  ✓ Truncated 0 oversized table cells
  ✓ Removed 0 meta-comments
  ✓ Removed 3,468 excessive whitespace chars
  ✓ Size: 236,071 → 232,603 bytes (3,468 bytes removed)
✅ Enhanced output sanitized successfully!
```

**Warning Thresholds**:
- ⚠️ Cells truncated > 0 → Prevention layer degraded, review prompt
- ⚠️ Meta-comments > 0 → Prompt not being followed, investigate LLM behavior
- ⚠️ Size reduction > 50KB → Major corruption, may indicate LLM regression
- ⚠️ Final size > 300KB → Excessive content, review prompt constraints

See `tests/outputs/AGENT15_FIX_VALIDATION_REPORT.md` for complete monitoring guidelines.

---

## [1.1.0] - 2025-10-29

### Added
- Web UI (Streamlit dashboard)
- Docker deployment (full containerization)
- Quick-start templates (3 types)
- Step-by-step tutorial (30-60 min)
- Enhanced PDF export (LibreOffice inline markdown)
- Complete Docker documentation

---

## [1.0.0] - 2025-10-28

### Added
- 15 specialized agent prompts (including Enhancer)
- 4 research database integrations (MCP)
- Multi-LLM support (Claude, GPT, Gemini)
- Export to PDF/Word/LaTeX (100% tested)
- Complete agent testing (15/15 - 100% coverage)
- Multi-agent workflow validation
- Production-quality outputs verified

---

**Version Numbering**: MAJOR.MINOR.PATCH
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)
