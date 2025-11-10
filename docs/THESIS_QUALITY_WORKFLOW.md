# Thesis Generation Quality Workflow

## Overview

This document defines the **quality gates** and **proper workflow** for generating publication-ready academic theses. It ensures no thesis is marked as "FINAL" unless it meets publication standards.

## The Problem This Solves

**Before quality gates:**
- ❌ Theses marked as "FINAL" with 50+ [VERIFY] citation placeholders
- ❌ No automated validation of publication-readiness
- ❌ Manual PDF exports using incomplete source files
- ❌ Inconsistent file naming (FINAL_THESIS vs FINAL_THESIS_CLEAN confusion)

**After quality gates:**
- ✅ Automated validation before marking as FINAL
- ✅ Clear pass/fail criteria for publication-readiness
- ✅ Prevents incomplete theses from being exported
- ✅ Standardized workflow across all thesis generation scripts

---

## File Naming Convention

### Generation Pipeline Files

| File | Purpose | Status | Use For |
|------|---------|--------|---------|
| `01_scout.md` - `13_entropy.md` | Agent outputs | Intermediate | Debugging only |
| `14_draft_pre_citation_check.md` | Pre-citation draft | Intermediate | Debugging only |
| `15_compiled_citations.md` | Post-citation compilation | Intermediate | Debugging only |
| `16_enhanced_final.md` | Enhanced with tables/appendices | Intermediate | Debugging only |
| **`FINAL_THESIS.md`** | ✅ **Sanitized final version** | **FINAL** | **PDF/DOCX export** |
| `FINAL_THESIS.pdf` | Exported PDF | Final | Publication |
| `FINAL_THESIS.docx` | Exported Word | Final | Publication |

### ❌ Files to NEVER Use for Export

| File | Why Not | Issue |
|------|---------|-------|
| `FINAL_THESIS_CLEAN.md` | Polluted with agent diagnostic outputs | Contains Entropy reports, style variance analysis |
| `*_backup_*.md` | Old versions | May be outdated or corrupted |
| `14_draft_pre_citation_check.md` | Pre-citation processing | Has {cite_XXX} placeholders |

---

## Generation Workflow

### Phase 1: Research & Writing (Steps 1-13)

```
Scout → Scribe → Signal → Architect → Formatter
  → Intro → Lit Review → Methodology → Analysis → Discussion → Conclusion
  → Skeptic → Entropy
```

**Output:** `13_entropy.md` (draft with humanized intro)

### Phase 2: Citation Processing (Step 14)

```
Citation Manager → Citation Compiler
  • Extract all {cite_XXX} references
  • Compile into APA 7th format
  • Research missing citations (if enabled)
  • Generate reference list
```

**Output:** `15_compiled_citations.md` (citations formatted)

### Phase 3: Enhancement (Step 15)

```
Enhancer Agent → Output Sanitizer
  • Add YAML metadata
  • Generate 4-paragraph abstract
  • Add 3-5 tables and 1-2 figures
  • Add 4-5 comprehensive appendices
  • Add Limitations/Future Research sections
  • Sanitize output (remove agent meta-comments)
```

**Output:** `16_enhanced_final.md` → **`FINAL_THESIS.md`** (sanitized)

### Phase 4: Quality Gate (NEW)

```
Quality Validator
  ✅ Check for [VERIFY] placeholders
  ✅ Check for {cite_MISSING:...} placeholders
  ✅ Verify all required sections present
  ✅ Validate word count (8,000+ recommended)
```

**Outcome:** PASS ✅ or FAIL ❌

### Phase 5: Export

```
ONLY IF QUALITY GATE PASSES:
  FINAL_THESIS.md → PDF (Pandoc/LaTeX)
  FINAL_THESIS.md → DOCX (Pandoc)
```

---

## Quality Gate Criteria

### ✅ Publication-Ready Thesis Must Have:

1. **Zero [VERIFY] markers**
   ```
   ❌ [VERIFY: Source on Linux adoption]
   ❌ [VERIFY DOI/URL]
   ❌ A. Al-Emran et al., 2023 [VERIFY]
   ```

2. **Zero missing citation placeholders**
   ```
   ❌ {cite_MISSING:open source economics}
   ```

3. **All required sections**
   - ✅ Abstract
   - ✅ Introduction
   - ✅ Literature Review
   - ✅ Methodology (or equivalent)
   - ✅ References

4. **Adequate word count**
   - ⚠️  Warning if < 8,000 words
   - ✅ Typical: 14,000-35,000 words

---

## How to Validate Thesis Quality

### Manual Validation

```bash
python3 scripts/validate_thesis_quality.py tests/outputs/my_thesis/FINAL_THESIS.md
```

### Automated Validation (in generation scripts)

Quality gates are **automatically run** in all thesis generation scripts:
- `tests/scripts/test_ai_pricing_thesis.py`
- `tests/scripts/test_opensource_thesis.py`
- `tests/scripts/test_co2_german_thesis.py`

**Example output:**
```
======================================================================
🔍 QUALITY GATE: Validating Publication-Readiness
======================================================================

✅ No [VERIFY] markers found
✅ No missing citation placeholders
✅ All required sections present

📊 Statistics:
   - Word count: 34,748
   - Character count: 251,193

======================================================================
✅ THESIS IS PUBLICATION-READY
======================================================================
```

---

## Fixing Quality Issues

### Issue #1: [VERIFY] Placeholders

**Problem:** Citations marked as [VERIFY] instead of properly researched.

**Solutions:**

1. **Automated (Recommended):**
   ```bash
   python3 scripts/fill_missing_citations.py tests/outputs/my_thesis/FINAL_THESIS.md
   ```

2. **Manual:**
   - Search for each `[VERIFY]` marker
   - Research proper citation via DOI/CrossRef
   - Replace with APA 7th format citation

3. **Regenerate:**
   - Re-run thesis generation script
   - Ensure `research_missing=True` in Citation Compiler

### Issue #2: Missing Sections

**Problem:** Required academic sections not generated.

**Solution:**
- Check agent outputs (steps 6-11) for errors
- Regenerate thesis with proper prompts
- Verify outline (step 4) includes all sections

### Issue #3: Low Word Count

**Problem:** Thesis below 8,000 words.

**Solutions:**
- Check Enhancer agent (step 15) ran successfully
- Verify appendices were added
- Expand case studies and analysis sections

---

## Prevention: Best Practices

### ✅ DO

1. **Always run full pipeline** - Don't skip Step 14 (Citation Compiler) or Step 15 (Enhancer)
2. **Enable citation research** - Set `research_missing=True` in Citation Compiler
3. **Check quality gate output** - Review validation report before exporting
4. **Use FINAL_THESIS.md for exports** - Never use intermediate files
5. **Commit validation reports** - Track quality over time

### ❌ DON'T

1. **Don't export from `*_CLEAN.md` files** - They're polluted with agent outputs
2. **Don't skip quality gates** - They catch critical issues
3. **Don't manually edit FINAL_THESIS.md** - Regenerate instead
4. **Don't ignore [VERIFY] markers** - They indicate incomplete research
5. **Don't use backup files for export** - They may be corrupted/outdated

---

## Current Status (Nov 2025)

### ✅ AI Pricing Thesis - PUBLICATION-READY
- **File:** `tests/outputs/ai_pricing_thesis/FINAL_THESIS.md`
- **Status:** ✅ 0 [VERIFY] markers, all citations verified
- **Output:** `examples/ai_pricing_thesis.pdf` (128 pages, 534KB)

### ❌ Open Source Thesis - NOT READY
- **File:** `tests/outputs/opensource_thesis/FINAL_THESIS.md`
- **Status:** ❌ 54 [VERIFY] markers
- **Action Required:** Fill missing citations or regenerate

### ❌ CO2 German Thesis - NOT READY
- **File:** `tests/outputs/co2_thesis_german/FINAL_THESIS.md`
- **Status:** ❌ 10 [VERIFY] markers
- **Action Required:** Fill missing citations or regenerate

---

## Regeneration Plan

To fix the 2 incomplete theses:

### Option 1: Automated Citation Filling (Fast)
```bash
# Fill missing citations using AI research
python3 scripts/fill_missing_citations.py tests/outputs/opensource_thesis/FINAL_THESIS.md
python3 scripts/fill_missing_citations.py tests/outputs/co2_thesis_german/FINAL_THESIS.md

# Re-export PDFs
python3 scripts/export_clean_pdfs.py
```

**Time:** ~10 minutes
**Cost:** ~$2-3 (Gemini API for citation research)

### Option 2: Full Regeneration (Thorough)
```bash
# Regenerate complete theses
python3 tests/scripts/test_opensource_thesis.py
python3 tests/scripts/test_co2_german_thesis.py
```

**Time:** ~30 minutes
**Cost:** ~$10-15 (full thesis generation)
**Benefit:** Fresh generation with latest bug fixes

---

## Quality Gate Implementation

### Code Integration

**Location:** All thesis generation scripts
**Trigger:** After writing `FINAL_THESIS.md`, before PDF export
**Behavior:** Validates but doesn't block (warns instead)

**Example:**
```python
# Write final thesis
with open(final_md, 'w') as f:
    f.write(final_paper)

# QUALITY GATE: Validate publication-readiness
from scripts.validate_thesis_quality import validate_thesis
is_publication_ready = validate_thesis(final_md, verbose=True)

if not is_publication_ready:
    print("\n⚠️  WARNING: Thesis has quality issues but export will continue")
    print("   Fix issues before publishing to production")

# Continue with PDF/DOCX export...
```

---

## Monitoring & Metrics

Track these metrics per thesis generation:

- **[VERIFY] count:** 0 required for publication
- **Word count:** 8,000+ recommended
- **Citation count:** Varies by field (typically 30-50)
- **Table/figure count:** 3-7 typical
- **Appendix count:** 4-5 recommended
- **Generation time:** 20-30 minutes typical
- **API cost:** $15-25 per complete thesis

---

## Troubleshooting

### Q: Quality gate shows missing sections but they exist?

**A:** Check header format. Validator looks for `# Introduction` or `## Introduction`. If headers use numbering like `# 1. Introduction`, update the regex pattern in `validate_thesis_quality.py`.

### Q: How do I bypass the quality gate for testing?

**A:** Comment out the quality gate block in the generation script, but **never commit bypassed code** to production.

### Q: Citation Compiler shows "missing citations" - is this normal?

**A:** Yes, if `research_missing=True`. The compiler will automatically research and fill them. If disabled, you'll get [VERIFY] markers instead.

### Q: Can I manually fix [VERIFY] markers?

**A:** Yes, but regeneration is recommended for consistency. If manually fixing, ensure APA 7th format compliance.

---

## Future Improvements

- [ ] Make quality gate blocking (fail generation if not ready)
- [ ] Add citation quality scoring (DOI validation, author formatting)
- [ ] Integrate plagiarism detection
- [ ] Add readability metrics (Flesch-Kincaid, etc.)
- [ ] Generate quality report PDF
- [ ] Track quality trends across thesis versions

---

**Last Updated:** November 10, 2025
**Maintainer:** Federico De Ponte
**Version:** 1.0.0
