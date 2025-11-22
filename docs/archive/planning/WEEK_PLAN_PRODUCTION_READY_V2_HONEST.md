# Week Plan: Production-Ready OpenDraft (V2 - Honest Edition)

**Date**: 2025-11-19
**Status**: 🔴 CRITICAL - Current system generates 30 citations, needs 50+
**Philosophy**: Outcomes over activities. Ship working features, not infrastructure.

---

## Executive Summary: The Brutal Truth

**Current State**:
- ❌ Only 30 citations per thesis (need 50-60)
- ❌ Gemini Grounded still partially active despite "disable"
- ❌ Quality filter too aggressive (45% rejection rate)
- ⚠️ Built 803 lines of duplicate code (unnecessary)

**Target State** (End of Week):
- ✅ 50-60 quality citations per thesis, reproducibly
- ✅ Zero Gemini Grounded citations
- ✅ Zero domain names as authors
- ✅ 4 perfect showcase theses deployed to GitHub Pages
- ✅ System works for ANY topic, not just our 4

**Success Metric**: Can generate a thesis on any topic with 50+ quality citations in <30 minutes.

---

## Day 1 (Monday): FIX THE CITATION ENGINE - FOR REAL THIS TIME

**Objective**: Get to 50+ citations per thesis, actually disable Gemini Grounded

**Status from Previous Attempt**: ⚠️ INCOMPLETE
- Built infrastructure ✓
- Didn't achieve targets ✗
- 30/50 citations (60% of goal) ✗

### Morning (3 hours): Root Cause Fix

**Task 1: Investigate & Fix Orchestrator Bug** (1 hour)
- Read `utils/api_citations/orchestrator.py` lines 48-100
- Understand why `enable_gemini_grounded=False` doesn't work
- Fix: Wrap client initialization in `if self.enable_gemini_grounded:` block
- Verify: Zero Gemini Grounded citations in test

**Task 2: Remove Duplicate Code** (30 min)
- Delete OR repurpose `utils/academic_citation_search.py`
- Decision: Keep if it adds value, delete if it duplicates orchestrator
- Rationale: DRY principle - no duplication

**Task 3: Fix Quality Filter** (30 min)
- Current: 45% rejection rate (too aggressive)
- Options:
  - A) Lower threshold from 4.0/7.0 to 3.0/7.0
  - B) Remove DOI requirement for conference papers
  - C) Remove filter entirely, trust academic APIs
- **Choose based on data inspection**: Which citations were wrongly rejected?

**Task 4: Clear Citation Cache** (5 min)
```bash
rm -f .citation_cache_orchestrator.json
rm -rf tests/outputs/opensource_thesis/
```

**Success Criteria**:
- ✅ Gemini Grounded initialization bug fixed
- ✅ No code duplication
- ✅ Quality filter tuned or removed
- ✅ Cache cleared

### Afternoon (3 hours): Increase Citation Generation

**Task 5: Analyze Why Only 30 Citations** (30 min)
- Inspect test output: How many queries succeeded vs failed?
- Count rate limit failures
- Calculate: To get 50 citations with current success rate, how many queries needed?

**Math**:
```
Current: 62 queries → 55 successful → 30 after filtering
Success rate: 55/62 = 89%
Filter pass rate: 30/55 = 55%
Combined rate: 0.89 * 0.55 = 49%

To get 50 citations: 50 / 0.49 = 102 queries needed
With safety margin: 120 queries
```

**Task 6: Increase Deep Research Query Count** (15 min)
- Modify `DeepResearchPlanner` to generate 120+ queries (was 62)
- OR increase `target_minimum` parameter
- Verify: Test generates 120 queries

**Task 7: Re-test with Fixed System** (1.5 hours)
- Run opensource thesis test
- Monitor: API usage, rate limiting, citation count
- **Success Criteria**: 50+ citations, 0 Gemini Grounded

**Task 8: Manual Quality Inspection** (45 min)
- Review all 50+ citations manually
- Check: No domain names as authors
- Check: All have DOIs or arXiv IDs
- Check: Titles are real papers, not websites

**Success Criteria**:
- ✅ 50-60 citations generated
- ✅ Zero Gemini Grounded citations
- ✅ Zero domain-as-author
- ✅ Manual inspection confirms quality

### Evening: Document ACTUAL Success (30 min)

**Only if Day 1 objectives met**:
- Update `docs/DAY1_ACADEMIC_API_FOUNDATION.md` with real results
- Commit changes with message: "fix: achieve 50+ citation target"

**If objectives NOT met**:
- Document failure honestly
- Analyze root cause
- Plan Day 1.5 iteration

---

## Day 2 (Tuesday): Verify Reproducibility

**Objective**: Prove system works for ANY topic, not just opensource

**Prerequisite**: Day 1 MUST be complete (50+ citations achieved)

### Morning (3 hours): Test 3 New Topics

Generate theses for completely different topics:

**Test 1: Technical Topic** (1 hour)
- Topic: "Quantum Computing Applications in Drug Discovery"
- Target: 50+ citations
- Verify: Quality, diversity, no junk

**Test 2: Social Science Topic** (1 hour)
- Topic: "Impact of Remote Work on Mental Health"
- Target: 50+ citations
- Verify: Quality, diversity, no junk

**Test 3: Niche Topic** (1 hour)
- Topic: "Microplastics in Deep Sea Ecosystems"
- Target: 50+ citations
- Verify: Quality, diversity, no junk

**Success Criteria**:
- ✅ All 3 topics generate 50+ citations
- ✅ No manual intervention required
- ✅ Quality consistent across topics

### Afternoon (4 hours): Fix Edge Cases

**Based on morning tests**, fix any discovered issues:

**Common Edge Cases**:
1. Very niche topics with <50 papers available
   - Solution: Graceful degradation, clear error message
2. Non-English topics
   - Solution: Define scope (English-only for v1.0)
3. Very recent topics (2024-2025)
   - Solution: Verify recency bias in APIs
4. Interdisciplinary topics
   - Solution: Verify query diversity covers all aspects

**Task**: For EACH edge case found:
1. Document the failure
2. Implement fix
3. Re-test
4. Verify fix works

**Success Criteria**:
- ✅ Edge cases documented
- ✅ Fixes implemented and tested
- ✅ System handles edge cases gracefully

---

## Day 3 (Wednesday): Regenerate Showcase Theses

**Objective**: Generate 4 perfect showcase theses with new system

**Prerequisite**: Day 2 complete (reproducibility verified)

### Morning (2 hours): Pre-flight Checks

**Task 1: Backup Current State** (15 min)
```bash
mv tests/outputs tests/outputs_day2_backup
mkdir tests/outputs
```

**Task 2: Clear All Caches** (5 min)
```bash
rm -f .citation_cache_orchestrator.json
find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null
```

**Task 3: Verify System Health** (30 min)
- Run unit tests: `pytest tests/ -v`
- Verify: All 39 citation tests pass
- Verify: No import errors, no deprecated warnings

**Task 4: Plan Parallel Execution** (15 min)
- 4 theses: opensource, ai_pricing, co2_german, academic_ai
- Estimate: 30 min each = 2 hours total
- Strategy: Run 2 in parallel (avoid rate limits)

**Task 5: Monitor Setup** (15 min)
```bash
# Create real-time monitoring script
watch -n 60 'find tests/outputs -name "citation_database.json" -exec wc -l {} \;'
```

### Afternoon (4 hours): Execute Regeneration

**Batch 1: opensource + ai_pricing** (2 hours)
```bash
# Terminal 1
python3 tests/scripts/test_opensource_thesis.py

# Terminal 2
python3 tests/scripts/test_ai_pricing_thesis.py
```

**Monitor**: Citation counts, API errors, quality

**Batch 2: co2_german + academic_ai** (2 hours)
```bash
# Terminal 1
python3 tests/scripts/test_co2_thesis_german.py

# Terminal 2
python3 tests/scripts/test_academic_ai_thesis.py
```

**Monitor**: Same as Batch 1

### Evening (2 hours): Quality Assurance

**For EACH thesis**:

**QA Checklist**:
- [ ] Citation count: 50-60 ✓
- [ ] Zero Gemini Grounded citations ✓
- [ ] Zero domain-as-author ✓
- [ ] All citations have DOIs or arXiv IDs ✓
- [ ] Bibliography formatting correct ✓
- [ ] Thesis reads coherently ✓
- [ ] No broken markdown ✓

**If ANY thesis fails QA**:
1. Document failure
2. Re-run that thesis only
3. Investigate if systematic issue

**Success Criteria**:
- ✅ 4 theses, each with 50-60 quality citations
- ✅ All pass QA checklist
- ✅ No manual fixes needed

---

## Day 4 (Thursday): Deploy & Document

**Objective**: Deploy showcase theses, create professional documentation

### Morning (3 hours): GitHub Pages Deployment

**Task 1: Generate PDFs** (1 hour)
```bash
cd tests/outputs/opensource_thesis
pandoc FINAL_THESIS.md -o opensource_thesis.pdf --pdf-engine=xelatex
# Repeat for all 4
```

**Task 2: Deploy to GitHub Pages** (30 min)
```bash
mkdir -p docs/examples
cp tests/outputs/*/FINAL_THESIS.pdf docs/examples/
git add docs/examples/
git commit -m "feat: deploy 4 showcase theses"
git push
```

**Task 3: Verify Deployment** (15 min)
- Visit: `https://[user].github.io/opendraft/examples/opensource_thesis.pdf`
- Verify: All 4 PDFs accessible, render correctly

**Task 4: Create Showcase README** (45 min)
```markdown
# OpenDraft - Showcase Examples

## Live Examples

1. [How Open Source Software Can Save the World](examples/opensource_thesis.pdf) - 57 citations
2. [AI Pricing Strategies](examples/ai_pricing_thesis.pdf) - 54 citations
3. [CO2 Emissions Analysis](examples/co2_thesis_german.pdf) - 52 citations
4. [Academic AI Applications](examples/academic_ai_thesis.pdf) - 59 citations

## Quality Metrics

- **Average Citations**: 55.5 per thesis
- **Academic Source Rate**: 100% (Semantic Scholar + CrossRef only)
- **Zero junk citations**: Domain-as-author eliminated
- **Generation Time**: <30 minutes per thesis
```

### Afternoon (4 hours): Documentation Sprint

**Doc 1: ACADEMIC_CITATION_SYSTEM.md** (1.5 hours)
```markdown
# Academic Citation System

## Overview
- How it works: API fallback chain
- Academic APIs: Semantic Scholar, CrossRef, arXiv
- Quality validation: What makes a citation "quality"
- Success rate: 50+ citations, 100% academic

## Architecture
[Diagram of citation flow]

## API Integration Details
- Semantic Scholar: 200M+ papers, free tier
- CrossRef: 140M+ papers, DOI registry
- arXiv: Preprints (CS, Math, Physics)

## Quality Assurance
- Validation rules
- Filter criteria
- Manual inspection process
```

**Doc 2: REPRODUCIBILITY_GUIDE.md** (1 hour)
```markdown
# Reproducibility Guide

## Quick Start
```bash
python3 tests/scripts/test_opensource_thesis.py
```

## Generate Thesis for Any Topic

Step 1: Create test script
Step 2: Define topic and scope
Step 3: Run and monitor
Step 4: Verify quality

## Expected Outcomes
- 50-60 citations per thesis
- <30 minute generation time
- 100% academic sources

## Troubleshooting
- If < 50 citations: [solutions]
- If rate limited: [solutions]
- If quality issues: [solutions]
```

**Doc 3: Update Main README** (1 hour)
- Add showcase links
- Add citation quality stats
- Add "Try It Yourself" section
- Add production-ready badges

**Doc 4: API Setup Guide** (30 min)
```markdown
# API Setup

No API keys required! All academic APIs are free tier:
- Semantic Scholar: No key needed
- CrossRef: No key needed
- arXiv: No key needed

Optional: Configure for higher rate limits [...]
```

**Success Criteria**:
- ✅ All 4 PDFs deployed and accessible
- ✅ Documentation professional-grade
- ✅ Clear reproducibility instructions

---

## Day 5 (Friday): Testing & Hardening

**Objective**: Stress test, edge cases, production hardening

### Morning (4 hours): Comprehensive Testing

**Test Suite 1: Edge Case Topics** (2 hours)

Generate theses for challenging topics:
1. **Very Niche**: "Role of Gut Microbiome in Parkinson's Disease"
   - Expected: Might only get 35-40 citations (acceptable with warning)
2. **Very Broad**: "Climate Change"
   - Expected: Too many papers, need smart query refinement
3. **Recent**: "Large Language Models Safety" (2023-2025)
   - Expected: Good coverage, verify recency
4. **Interdisciplinary**: "AI Ethics in Healthcare"
   - Expected: Sources from CS + Medicine + Ethics

**For EACH test**:
- Document: Citation count, sources, quality
- Identify: System limitations
- Decide: Accept limitation OR fix

**Test Suite 2: Failure Mode Testing** (1 hour)

Deliberately break things:
1. **Disconnect internet mid-generation**
   - Verify: Graceful error message, retry logic works
2. **Rate limit simulation**
   - Verify: Exponential backoff works
3. **Malformed topic input**
   - Verify: Clear error message, doesn't crash

**Test Suite 3: Performance Testing** (1 hour)

Measure:
- Time to generate 1 thesis: <30 min target
- API calls per thesis: <200 target
- Memory usage: <2GB target
- CPU usage: Monitor during generation

### Afternoon (3 hours): Production Hardening

**Task 1: Error Handling Audit** (1 hour)
- Review ALL error messages
- Ensure: Clear, actionable, no stack traces to user
- Add: Logging for debugging without cluttering user output

**Task 2: Input Validation** (30 min)
- Validate: Topic not empty
- Validate: Scope reasonable length
- Validate: Target citation count in range (30-100)

**Task 3: Rate Limit Optimization** (1 hour)
- Measure: Actual API usage patterns
- Optimize: Batch requests where possible
- Implement: Smart backoff (respect Retry-After headers)

**Task 4: Monitoring & Metrics** (30 min)
```python
# Add metrics collection
metrics = {
    "total_queries": 0,
    "successful_citations": 0,
    "failed_queries": 0,
    "api_breakdown": {},
    "generation_time_seconds": 0,
    "quality_filter_removed": 0
}
# Log metrics at end of generation
```

**Success Criteria**:
- ✅ Handles all edge cases gracefully
- ✅ Clear error messages, no crashes
- ✅ Performance within targets
- ✅ Production-grade error handling

---

## Day 6 (Saturday): Performance & Scale

**Objective**: Optimize for production-scale usage

### Morning (3 hours): Performance Profiling

**Task 1: Profile Thesis Generation** (1 hour)
```bash
python3 -m cProfile -o profile.stats tests/scripts/test_opensource_thesis.py
python3 -c "import pstats; p=pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"
```

Identify bottlenecks:
- API calls (expected)
- LLM generation (expected)
- Unexpected slow operations?

**Task 2: Optimize Hot Paths** (2 hours)

**Common Optimizations**:
1. **Parallel API calls** where possible
   - Don't: Sequential API calls
   - Do: Batch 5-10 queries, execute in parallel
2. **Reduce redundant API calls**
   - Check cache before calling API
   - Deduplicate queries before sending
3. **Optimize LLM prompts**
   - Shorter prompts = faster generation
   - But: Don't sacrifice quality

**Task 3: Measure Improvement** (30 min)
- Before: Baseline time
- After: Optimized time
- Target: 20-30% improvement

### Afternoon (3 hours): Scalability Testing

**Test 1: Generate 5 Theses in Parallel** (1.5 hours)
```bash
# Launch 5 in parallel
for topic in "AI" "Climate" "Healthcare" "Education" "Economics"; do
  python3 generate_thesis.py "$topic" &
done
wait
```

**Monitor**:
- Do they all complete?
- Any rate limiting issues?
- Resource usage (CPU, memory, network)

**Test 2: Measure Resource Usage** (30 min)
- Peak memory: Should stay <5GB for 5 parallel
- CPU: Should utilize available cores
- Network: Respect API rate limits

**Test 3: Add Resource Guards** (1 hour)
```python
# Max parallel generations
MAX_CONCURRENT = 3

# Memory check before starting
if memory_usage() > 4GB:
    raise ResourceError("Insufficient memory")
```

**Success Criteria**:
- ✅ Can handle 5 parallel generations
- ✅ No resource exhaustion
- ✅ Clear limits documented

---

## Day 7 (Sunday): Polish & Release

**Objective**: Final polish, release prep, marketing

### Morning (3 hours): Final Quality Pass

**Task 1: Re-review All 4 Showcase Theses** (1 hour)
- Read each thesis end-to-end
- Check: Flow, coherence, citations integrated
- Fix: Any minor formatting issues

**Task 2: Create Demo Video/GIF** (1.5 hours)
- Screen recording: Generate thesis from start to finish
- Show: Command → Progress → Results (30 sec)
- Highlight: 50+ citations, quality validation, speed

**Task 3: Final Documentation Review** (30 min)
- Proofread all docs
- Fix typos, broken links
- Verify code examples work

### Afternoon (4 hours): Release Preparation

**Task 1: Create CHANGELOG.md** (30 min)
```markdown
# Changelog

## [2.0.0] - 2025-11-19

### Added
- Academic citation system (Semantic Scholar, CrossRef, arXiv)
- Quality validation (DOI verification, author validation)
- 4 showcase theses with 50+ citations each
- Reproducibility guide

### Changed
- Citation generation now 100% academic sources
- Zero domain-as-author citations
- Generation time <30 min

### Removed
- Gemini Grounded for citations (kept for other features)
- Post-generation filtering (quality ensured at generation time)
```

**Task 2: Git Tag & Release** (30 min)
```bash
git tag -a v2.0.0 -m "Production-ready academic citation system"
git push origin v2.0.0

gh release create v2.0.0 \
  --title "v2.0.0: Production-Ready Academic Citations" \
  --notes "50+ quality citations per thesis, reproducible for any topic"
```

**Task 3: Update README Badges** (15 min)
```markdown
![Citations](https://img.shields.io/badge/citations-50+-green)
![Quality](https://img.shields.io/badge/academic-100%25-blue)
![Generation](https://img.shields.io/badge/time-<30min-orange)
```

**Task 4: Community Prep** (45 min)
- Create issue templates
- Create pull request template
- Add CONTRIBUTING.md
- Add CODE_OF_CONDUCT.md

**Task 5: Marketing Materials** (2 hours)

**Tweet Thread** (30 min):
```
🧵 Thread: I built an AI that generates academic theses with 50+ quality citations

Old system: 28 citations (too few), 50% junk
New system: 50-60 citations, 100% academic

How we did it: [thread]
```

**LinkedIn Post** (30 min):
Professional version of tweet thread

**Dev.to Article** (1 hour):
```markdown
# How We Built a Production-Grade Academic Citation System

## The Problem
[Story of 28 citations → need 50+]

## The Solution
[Academic API integration]

## The Results
[Showcase theses, metrics]

## Try It Yourself
[Reproducibility guide]
```

**Success Criteria**:
- ✅ Everything polished and professional
- ✅ Release tagged v2.0.0
- ✅ Documentation complete
- ✅ Marketing materials ready

---

## Success Metrics (End of Week)

### Quantitative Targets

| Metric | Before | Target | Measured |
|--------|--------|--------|----------|
| **Citation Count** | 28-30 | 50-60 | __ |
| **Academic Source %** | ~50% | 100% | __ |
| **Domain-as-Author** | Yes | 0 | __ |
| **Generation Time** | Unknown | <30 min | __ |
| **Reproducibility** | No | Any topic | __ |

### Qualitative Targets

- [ ] **4 Perfect Showcase Theses**: Manually verified, deployed
- [ ] **Documentation**: Professional, clear, complete
- [ ] **Reproducibility**: Works for any topic without manual intervention
- [ ] **Production-Ready**: Error handling, monitoring, scalable

### Go/No-Go Criteria

**Ship to v2.0.0 if ALL of**:
- ✅ All 4 showcase theses have 50-60 citations
- ✅ Zero Gemini Grounded citations in showcases
- ✅ Zero domain-as-author in showcases
- ✅ System generates 50+ citations for 3/3 new test topics
- ✅ Documentation complete and professional

**Do NOT ship if ANY of**:
- ❌ <50 citations in any showcase thesis
- ❌ Gemini Grounded citations present
- ❌ Domain-as-author present
- ❌ Fails to reproduce on new topics
- ❌ Documentation incomplete

---

## Daily Standup Format

**Each morning (9 AM)**:

1. **Yesterday**: What was accomplished (with metrics)
2. **Today**: What will be done (specific, measurable)
3. **Blockers**: Issues preventing progress
4. **Metrics**: Current citation stats

**Example**:
```
Yesterday:
- ✅ Fixed orchestrator bug (Gemini Grounded now disabled)
- ❌ Only got 42 citations in test (need 50+)

Today:
- Increase query count from 62 to 120
- Re-test, target 50+ citations
- If successful, move to Day 2

Blockers:
- Rate limiting on Semantic Scholar (429 errors)
- Solution: Implement better backoff

Metrics:
- Citations: 42/50 (84% of target)
- Academic: 100% (target met)
```

---

## Risk Management

### Risk 1: Still Can't Reach 50+ Citations

**Likelihood**: Medium (30%)
**Impact**: High (blocks entire week)

**Mitigation**:
- Option A: Lower target to 40-45 (acceptable minimum)
- Option B: Relax quality filter (allow more sources)
- Option C: Add web sources with strict validation

**Decision Tree**:
```
If 40-45 citations with 100% academic:
  → ACCEPT (still better than 28)
  → Document as "acceptable quality"

If <40 citations:
  → REJECT
  → Investigate root cause
  → Delay v2.0.0 release
```

### Risk 2: Academic APIs Have Downtime

**Likelihood**: Low (10%)
**Impact**: High (can't generate theses)

**Mitigation**:
- Implement fallback chain (if Semantic Scholar down, use CrossRef only)
- Cache aggressively (previous results)
- Clear error messages ("Semantic Scholar unavailable, retrying...")

### Risk 3: Quality Still Issues (Domain-as-Author)

**Likelihood**: Medium (20%)
**Impact**: Medium (damages credibility)

**Mitigation**:
- Manual QA on ALL showcase theses
- Automated validation in CI/CD
- User reporting mechanism

---

## Post-Week Plan

**Week 2: Advanced Features**
- Multi-language support (Spanish, German, French)
- Custom citation styles (APA, MLA, Chicago, IEEE)
- Citation recommendation engine
- Topic expansion suggestions

**Week 3: User Interface**
- Web UI for thesis generation
- Real-time progress tracking
- Citation management interface
- One-click PDF export

**Week 4: Community & Scale**
- Open source release announcement
- Accept community contributions
- Scale testing (100+ concurrent generations)
- Production deployment guide

---

## Commitment: Outcome-Driven Development

### Principles for This Week

1. **Outcomes > Activities**
   - Don't report "wrote 800 lines" - report "achieved 50+ citations"
   - Don't report "added 20 tests" - report "zero bugs in production"

2. **Verify > Assume**
   - Don't assume Gemini Grounded disabled - verify zero citations from it
   - Don't assume quality - manually inspect every showcase thesis

3. **Honest Metrics**
   - Report failures immediately
   - No cherry-picking metrics
   - No declaring success before verification

4. **User Value > Code Elegance**
   - 50 working citations > 800 lines of "clean code" that delivers 30
   - DRY/SOLID/KISS are means, not ends

5. **Ship > Perfect**
   - v2.0.0 with 50 citations > v3.0.0 someday with 100
   - Done is better than perfect

---

## Final Checklist (End of Week)

**Before declaring "Week Complete"**:

### Technical Checklist
- [ ] All 4 showcase theses generated
- [ ] Each thesis has 50-60 citations
- [ ] Zero Gemini Grounded citations across all 4
- [ ] Zero domain-as-author across all 4
- [ ] Tested on 3+ new topics successfully
- [ ] All unit tests passing
- [ ] No errors in generation logs

### Documentation Checklist
- [ ] ACADEMIC_CITATION_SYSTEM.md complete
- [ ] REPRODUCIBILITY_GUIDE.md complete
- [ ] README updated with showcase links
- [ ] CHANGELOG.md for v2.0.0
- [ ] API setup guide clear

### Deployment Checklist
- [ ] 4 PDFs deployed to GitHub Pages
- [ ] All PDFs accessible via web
- [ ] Git tagged v2.0.0
- [ ] GitHub release created

### Quality Checklist
- [ ] Manual QA passed on all 4 theses
- [ ] Read all 4 theses end-to-end
- [ ] Verified bibliography formatting
- [ ] No broken markdown links
- [ ] Professional appearance

### Verification Checklist
- [ ] Generated new thesis from scratch to verify reproducibility
- [ ] No manual intervention needed
- [ ] Generation time <30 min
- [ ] 50+ citations achieved

**ONLY THEN**: Declare week complete and ship v2.0.0

---

**Status**: 📋 PLAN READY
**Philosophy**: No BS. Ship working features. Verify everything.
**Next**: Start Day 1 - Fix citation engine for real this time.
