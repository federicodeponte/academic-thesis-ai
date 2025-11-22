# QUALITY CHECKLIST - Academic Thesis AI System

**Version:** 1.0
**Last Updated:** 2025-01-06
**Purpose:** Comprehensive validation checklist for thesis generation and publication

---

## ⚠️ CRITICAL: Use This Checklist Before EVERY Delivery

This checklist ensures production-ready, publication-quality theses. **DO NOT skip any section.**

---

## Phase 1: Pre-Generation Configuration Checks

**Run BEFORE starting thesis generation**

### 1.1 Word Count Configuration

- [ ] **Test script word count targets match requirements:**
  - Introduction: 2,500 words
  - Literature Review: 6,000 words
  - Methodology: 2,500 words
  - Analysis/Results: 6,000 words
  - Discussion: 3,000 words
  - Conclusion: 1,000 words
  - **Total:** 21,000 words minimum

- [ ] **Formatter prompt defaults verified:**
  - `prompts/02_structure/formatter.md` lines 343-354 show 21,000 total

- [ ] **Crafter prompt word count enforcement present:**
  - `prompts/03_compose/crafter.md` includes word count requirements section
  - Minimum compliance expectations clearly stated
  - Rejection criteria for undersized content defined

### 1.2 Citation Database

- [ ] **Citation database prepared:**
  - `citations_database.json` exists with adequate sources
  - All citations have complete metadata (author, year, title, DOI/URL)
  - Citation IDs formatted as `cite_001`, `cite_002`, etc.

- [ ] **No placeholder citations in research phase:**
  - All `[MISSING:...]` placeholders researched and replaced
  - `[VERIFY]` tags minimized (only for truly uncertain sources)

- [ ] **DOI validation (CRITICAL - no 404s allowed):**
  ```bash
  # Validate all DOIs return 200 OK (no 404 errors)
  python3 -m utils.citation_validator --all
  # Or validate single thesis:
  # python3 -m utils.citation_validator tests/outputs/[thesis_name]/citation_database.json
  # Should report: "✅ All citations passed validation!"
  ```
  - **Requirement**: All DOI links must resolve (no 404 errors)
  - **If DOI is broken**: Remove DOI field, keep citation with other metadata
  - **Why**: User requirement: "sources that throw 404 are not allowed"

### 1.3 Language Consistency

- [ ] **Language determined for thesis:**
  - English: Use standard metadata labels
  - German: All metadata translated (Abschnitt, Wortzahl, Entwurf v1, etc.)
  - Spanish/French: Appropriate translations applied

- [ ] **Agent prompts configured for target language:**
  - Crafter agent aware of thesis language
  - Formatter agent using correct metadata labels
  - Citation Compiler configured for correct citation style

---

## Phase 2: Post-Generation Markdown Validation

**Run AFTER thesis generation, BEFORE PDF export**

### 2.1 File Completeness

- [ ] **All agent outputs present:**
  ```bash
  ls -lh tests/outputs/[thesis_name]/*.md
  # Should see: 01_research.md through 16_enhanced_final.md
  ```

- [ ] **FINAL_THESIS.md exists and is reasonable size:**
  ```bash
  ls -lh tests/outputs/[thesis_name]/FINAL_THESIS.md
  # Should be ~80-150KB, NOT 1.6MB+
  ```

### 2.2 Word Count Verification

- [ ] **Total word count meets minimum (20,000+ words):**
  ```bash
  wc -w tests/outputs/[thesis_name]/FINAL_THESIS.md
  # Should show 20,000-40,000 words
  ```

- [ ] **Section-level word counts meet targets:**
  - Check each section header in markdown
  - Verify Introduction ≥ 2,500 words
  - Verify Literature Review ≥ 6,000 words
  - Verify Methodology ≥ 2,500 words
  - Verify Analysis ≥ 6,000 words
  - Verify Discussion ≥ 3,000 words
  - Verify Conclusion ≥ 1,000 words

### 2.3 Content Quality Checks

- [ ] **No table corruption:**
  ```bash
  grep "^|" FINAL_THESIS.md | awk '{print NR, length($0)}' | sort -k2 -n | tail -5
  # No lines should exceed ~300 characters
  ```

- [ ] **No Agent #15 enhancement notes in content:**
  ```bash
  grep -i "thesis enhancer" FINAL_THESIS.md
  # Should return NO results
  ```

  ```bash
  grep -i "Wichtiger Hinweis zur Wortzahl" FINAL_THESIS.md  # German
  # Should return NO results
  ```

- [ ] **Citation format validation:**
  ```bash
  # Check for orphaned cite IDs (should be replaced by Citation Compiler)
  grep -o "{cite_[0-9]\{3\}}" FINAL_THESIS.md | wc -l
  # Should be 0 (all replaced with formatted citations)
  ```

- [ ] **No excessive [VERIFY] or [MISSING] placeholders:**
  ```bash
  grep -c "\[VERIFY\]" FINAL_THESIS.md
  # Should be 0-2 (minimal, justified)

  grep -c "\[MISSING:" FINAL_THESIS.md
  # Should be 0 (all researched and replaced)
  ```

- [ ] **Metadata headers removed from content sections:**
  ```bash
  grep -E "^\*\*Section:\*\*|\*\*Word Count:\*\*|\*\*Status:\*\*" FINAL_THESIS.md
  # Should return NO results in main content (only in YAML frontmatter if present)
  ```

### 2.4 Language-Specific Checks

#### For German Theses:

- [ ] **German metadata labels used:**
  ```bash
  grep "Abschnitt:" FINAL_THESIS.md
  grep "Wortzahl:" FINAL_THESIS.md
  grep "Entwurf v1" FINAL_THESIS.md
  # Should find German labels, NOT English
  ```

- [ ] **German characters present in content:**
  ```bash
  grep -o "[äöüßÄÖÜ]" FINAL_THESIS.md | wc -l
  # Should be >100 for authentic German content
  ```

#### For English Theses:

- [ ] **English metadata labels used:**
  ```bash
  grep "Section:" FINAL_THESIS.md
  grep "Word Count:" FINAL_THESIS.md
  grep "Draft v1" FINAL_THESIS.md
  ```

### 2.5 Structure Validation

- [ ] **All required sections present:**
  - [ ] Abstract
  - [ ] Introduction
  - [ ] Literature Review
  - [ ] Methodology
  - [ ] Analysis/Results
  - [ ] Discussion
  - [ ] Conclusion
  - [ ] References
  - [ ] Appendices (if applicable)

- [ ] **Section numbering consistent:**
  ```bash
  grep "^#" FINAL_THESIS.md | head -20
  # Check numbering scheme (1., 2., 3. or Chapter 1, etc.)
  ```

---

## Phase 3: PDF Export Quality Checks

**Run AFTER cleanup script, DURING/AFTER PDF generation**

### 3.1 Cleanup Script Execution

- [ ] **Run cleanup script:**
  ```bash
  python3 scripts/clean_thesis_for_publication.py
  # Generates FINAL_THESIS_CLEAN.md
  ```

- [ ] **Verify cleanup removed metadata:**
  ```bash
  grep -E "Section:|Word Count:|Status:|Draft v1" tests/outputs/[thesis_name]/FINAL_THESIS_CLEAN.md
  # Should return NO results
  ```

- [ ] **Verify cleanup removed Style Variance Report:**
  ```bash
  head -50 tests/outputs/[thesis_name]/FINAL_THESIS_CLEAN.md | grep -i "Style Variance"
  # Should return NO results
  ```

- [ ] **Verify cleanup removed metadata sections:**
  ```bash
  grep -E "## Content|## Citations Used|## Notes for Revision" FINAL_THESIS_CLEAN.md
  # Should return NO results
  ```

- [ ] **Verify cleanup removed Appendix B checklists:**
  ```bash
  grep "Appendix B:" FINAL_THESIS_CLEAN.md
  # Should return NO results (implementation checklists removed)
  ```

### 3.2 PDF Generation

- [ ] **Export PDF using Pandoc:**
  ```bash
  # Convert to ASCII to avoid Unicode errors
  iconv -f UTF-8 -t ASCII//TRANSLIT FINAL_THESIS_CLEAN.md | \
    pandoc -o examples/thesis_[name].pdf \
      --pdf-engine=pdflatex \
      -V geometry:margin=1in \
      -V fontsize=12pt
  ```

- [ ] **PDF generated successfully:**
  ```bash
  ls -lh examples/thesis_[name].pdf
  # Should be 200-500KB for 20-40K word thesis
  ```

- [ ] **PDF page count reasonable:**
  ```bash
  pdfinfo examples/thesis_[name].pdf | grep Pages
  # Should be 30-50 pages for full thesis
  ```

### 3.3 PDF Content Inspection

**CRITICAL: Visual and content validation**

#### 3.3.1 First Pages (Title, Abstract, Introduction)

- [ ] **Extract and review first 2 pages:**
  ```bash
  pdftotext -f 1 -l 2 examples/thesis_[name].pdf - | head -120
  ```

- [ ] **Verify title page formatting:**
  - [ ] Thesis title visible and clear
  - [ ] Author information (if applicable)
  - [ ] Date/institution (if applicable)
  - [ ] No metadata artifacts ("Section:", "Word Count:", etc.)
  - [ ] No Agent #15 enhancement messages

- [ ] **Verify abstract formatting:**
  - [ ] Abstract heading present
  - [ ] Abstract content readable
  - [ ] Keywords present (if applicable)
  - [ ] No placeholder text

#### 3.3.2 Last Pages (References Section)

- [ ] **Extract and review last 2 pages:**
  ```bash
  pdftotext -f [last-1] -l [last] examples/thesis_[name].pdf - | tail -150
  ```

- [ ] **Verify references formatting:**
  - [ ] References section header visible
  - [ ] Citations properly formatted (APA 7th, IEEE, etc.)
  - [ ] DOI/URLs present where applicable
  - [ ] Alphabetical order maintained
  - [ ] No orphaned `{cite_XXX}` IDs
  - [ ] No `[MISSING:...]` placeholders

#### 3.3.3 Middle Section (Body Content Sampling)

- [ ] **Extract middle pages for quality check:**
  ```bash
  # Sample pages 20-22 from a 40-page thesis
  pdftotext -f 20 -l 22 examples/thesis_[name].pdf - | head -80
  ```

- [ ] **Verify body content quality:**
  - [ ] Academic prose flows naturally
  - [ ] Citations appear inline correctly
  - [ ] No metadata artifacts
  - [ ] No broken formatting
  - [ ] Figures/tables referenced properly (if applicable)

#### 3.3.4 Issue Detection (Automated Scans)

- [ ] **Scan for LaTeX artifacts:**
  ```bash
  pdftotext examples/thesis_[name].pdf - | grep -E "\\\\cite|\\\\ref|\\\\begin|\\\\end"
  # Should return NO results (LaTeX commands should be rendered)
  ```

- [ ] **Scan for metadata leakage:**
  ```bash
  pdftotext examples/thesis_[name].pdf - | grep -E "Section:|Word Count:|Draft v1|Status:|Entwurf v1|Wortzahl:"
  # Should return NO results
  ```

- [ ] **Scan for placeholder citations:**
  ```bash
  pdftotext examples/thesis_[name].pdf - | grep -E "\{cite_[0-9]{3}\}"
  # Should return NO results (all cite IDs should be replaced)
  ```

- [ ] **Scan for TODO/VERIFY tags:**
  ```bash
  pdftotext examples/thesis_[name].pdf - | grep -E "TODO|VERIFY|\[MISSING:"
  # Should return NO results
  ```

- [ ] **Scan for Agent #15 enhancement artifacts:**
  ```bash
  pdftotext examples/thesis_[name].pdf - | grep -i "Thesis Enhancer"
  pdftotext examples/thesis_[name].pdf - | grep -i "Wichtiger Hinweis"  # German
  # Should return NO results
  ```

#### 3.3.5 Language-Specific PDF Validation

**For German Theses:**

- [ ] **Verify German character rendering:**
  ```bash
  pdftotext examples/thesis_co2_bepreisung_german.pdf - | grep -o "[äöüßÄÖÜ]" | sort | uniq -c
  # Should show counts for each umlaut/ß (e.g., 500+ instances)
  ```

- [ ] **Sample German content readability:**
  ```bash
  pdftotext -f 5 -l 6 examples/thesis_co2_bepreisung_german.pdf - | head -50
  # Manually verify German text flows naturally with proper umlauts
  ```

**For English Theses:**

- [ ] **Verify no Unicode character errors:**
  ```bash
  pdftotext examples/thesis_[name].pdf - | grep -E "\?\?\?|�"
  # Should return NO results (indicates encoding issues)
  ```

---

## Phase 4: Final Delivery Production-Ready Checks

**Run BEFORE copying PDFs to `examples/` directory or sharing**

### 4.1 File Organization

- [ ] **PDF in correct location:**
  ```bash
  ls -lh examples/thesis_*.pdf
  # All 3 showcase theses should be present
  ```

- [ ] **Clean markdown preserved (for version control):**
  ```bash
  ls -lh tests/outputs/*/FINAL_THESIS_CLEAN.md
  # Clean versions saved for future reference
  ```

- [ ] **Original markdown preserved (for debugging):**
  ```bash
  ls -lh tests/outputs/*/FINAL_THESIS.md
  # Original with metadata preserved
  ```

### 4.2 Metadata Validation

- [ ] **PDF properties check:**
  ```bash
  pdfinfo examples/thesis_[name].pdf
  ```
  - [ ] Title field set (if applicable)
  - [ ] Author field set (if applicable)
  - [ ] Creation date reasonable
  - [ ] File size appropriate (200-500KB for 30-50 pages)
  - [ ] Page count correct

### 4.3 Accessibility and Usability

- [ ] **PDF opens correctly:**
  - [ ] Opens in browser/PDF viewer without errors
  - [ ] Text is selectable (not scanned image)
  - [ ] Navigation works (if table of contents present)

- [ ] **Manual visual inspection (CRITICAL):**
  - [ ] Open PDF in viewer (Evince, Adobe, Preview)
  - [ ] Scroll through ENTIRE document page-by-page
  - [ ] Check for:
    - [ ] Proper page breaks
    - [ ] No cut-off sections
    - [ ] Consistent formatting throughout
    - [ ] Figures/tables render correctly (if present)
    - [ ] Headers/footers appropriate
    - [ ] No orphaned headings (heading at bottom of page with content on next)

### 4.4 Cross-Thesis Consistency

**For multi-thesis deliveries:**

- [ ] **All theses use consistent formatting:**
  - [ ] Same PDF generation method (Pandoc + pdflatex)
  - [ ] Same page margins (1 inch)
  - [ ] Same font size (12pt)
  - [ ] Similar page counts relative to word count

- [ ] **All theses pass same quality checks:**
  - [ ] Each thesis validated individually
  - [ ] No thesis skipped due to time pressure
  - [ ] Issues documented for each thesis

### 4.5 Documentation

- [ ] **README/documentation updated:**
  - [ ] PDF showcase examples listed
  - [ ] Word counts documented
  - [ ] Generation date noted
  - [ ] Known limitations disclosed (if any)

- [ ] **Quality audit trail created:**
  - [ ] This checklist completed for each thesis
  - [ ] Issues found and resolved documented
  - [ ] Sign-off by generator/reviewer

---

## Automated Validation Script

**Use this script to automate Phase 3.3.4 checks:**

```bash
#!/bin/bash
# validate_pdf_quality.sh

THESIS_NAME=$1
PDF_PATH="examples/thesis_${THESIS_NAME}.pdf"

echo "=== PDF QUALITY VALIDATION: $THESIS_NAME ==="
echo ""

# Check PDF exists
if [ ! -f "$PDF_PATH" ]; then
  echo "❌ PDF not found: $PDF_PATH"
  exit 1
fi

echo "✅ PDF found: $PDF_PATH"
echo "   Size: $(ls -lh $PDF_PATH | awk '{print $5}')"
echo "   Pages: $(pdfinfo $PDF_PATH | grep Pages | awk '{print $2}')"
echo ""

# LaTeX artifacts
echo "🔍 Checking for LaTeX artifacts..."
LATEX_COUNT=$(pdftotext $PDF_PATH - | grep -c -E "\\\\cite|\\\\ref|\\\\begin" || true)
if [ $LATEX_COUNT -gt 0 ]; then
  echo "❌ Found $LATEX_COUNT LaTeX artifacts"
  pdftotext $PDF_PATH - | grep -E "\\\\cite|\\\\ref|\\\\begin" | head -5
else
  echo "✅ No LaTeX artifacts"
fi
echo ""

# Metadata leakage
echo "🔍 Checking for metadata leakage..."
METADATA_COUNT=$(pdftotext $PDF_PATH - | grep -c -E "Section:|Word Count:|Draft v1|Status:" || true)
if [ $METADATA_COUNT -gt 0 ]; then
  echo "❌ Found $METADATA_COUNT metadata artifacts"
  pdftotext $PDF_PATH - | grep -E "Section:|Word Count:|Draft v1|Status:" | head -5
else
  echo "✅ No metadata leakage"
fi
echo ""

# Orphaned cite IDs
echo "🔍 Checking for orphaned cite IDs..."
CITE_COUNT=$(pdftotext $PDF_PATH - | grep -c "{cite_" || true)
if [ $CITE_COUNT -gt 0 ]; then
  echo "❌ Found $CITE_COUNT orphaned cite IDs"
  pdftotext $PDF_PATH - | grep -o "{cite_[0-9]\{3\}}" | head -10
else
  echo "✅ No orphaned cite IDs"
fi
echo ""

# TODO/VERIFY tags
echo "🔍 Checking for TODO/VERIFY tags..."
TODO_COUNT=$(pdftotext $PDF_PATH - | grep -c -E "TODO|VERIFY|\[MISSING:" || true)
if [ $TODO_COUNT -gt 0 ]; then
  echo "❌ Found $TODO_COUNT placeholder tags"
  pdftotext $PDF_PATH - | grep -E "TODO|VERIFY|\[MISSING:" | head -5
else
  echo "✅ No placeholder tags"
fi
echo ""

# Agent #15 artifacts
echo "🔍 Checking for Agent #15 enhancement artifacts..."
ENHANCER_COUNT=$(pdftotext $PDF_PATH - | grep -c -i "Thesis Enhancer\|Wichtiger Hinweis" || true)
if [ $ENHANCER_COUNT -gt 0 ]; then
  echo "❌ Found $ENHANCER_COUNT enhancer artifacts"
  pdftotext $PDF_PATH - | grep -i "Thesis Enhancer\|Wichtiger Hinweis" | head -3
else
  echo "✅ No enhancer artifacts"
fi
echo ""

echo "=== VALIDATION COMPLETE ==="
```

**Usage:**
```bash
chmod +x scripts/validate_pdf_quality.sh
./scripts/validate_pdf_quality.sh opensource_project_adoption
./scripts/validate_pdf_quality.sh ai_pricing_strategies
./scripts/validate_pdf_quality.sh co2_bepreisung_german
```

---

## Issue Resolution Guide

### Common Issues and Fixes

| Issue | Symptom | Root Cause | Solution |
|-------|---------|------------|----------|
| **[VERIFY] in PDF** | Placeholder citations visible | Agent couldn't determine year from context | Re-run Citation Research (Agent #14) with more context |
| **{cite_XXX} in PDF** | Orphaned citation IDs | Citation Compiler failed | Check citations_database.json, re-run Agent #14 |
| **DOI returns 404** | Citation link broken, user req: "no 404s" | DOI invalid, hallucinated, or gray literature | Remove DOI field from citation_database.json, keep citation with other metadata (author/title/year) |
| **Metadata visible in PDF** | "Section:", "Word Count:" in PDF | Cleanup script not run or incomplete | Run `clean_thesis_for_publication.py` before PDF export |
| **Agent #15 note in PDF** | Enhancement message at start | Cleanup script didn't remove it | Update `remove_style_variance_report()` function |
| **[MISSING:...] in PDF** | Missing citation placeholders | Research phase incomplete | Run citation research script, update database |
| **Thesis too short** | <15,000 words actual output | Word count targets too low | Update test script targets to 21,000 words |
| **Table corruption** | PDF cuts off at table | Agent #15 whitespace padding bug | Skip Agent #15, use 15_compiled_citations.md instead |
| **Unicode errors in PDF** | "! LaTeX Error: Unicode character..." | pdflatex doesn't support Unicode | Use `iconv -t ASCII//TRANSLIT` before pandoc |
| **German characters broken** | Umlauts render as "?" | Encoding issue in PDF export | Verify UTF-8 encoding, use `iconv` if needed |
| **Wrong metadata language** | "Draft v1" in German thesis | Language not set in prompts | Update Crafter/Formatter prompts for German |

---

## Sign-Off

**Thesis Name:** ___________________________
**Generation Date:** ___________________________
**Generated By:** ___________________________
**Reviewed By:** ___________________________
**Quality Score:** _____ / 100

**All Phase 4 Checks Passed:** ☐ Yes ☐ No (Document exceptions below)

**Production-Ready for Delivery:** ☐ Yes ☐ No

**Exceptions/Notes:**
_______________________________________________________________________________
_______________________________________________________________________________
_______________________________________________________________________________

**Signature:** _____________________________ **Date:** _____________

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-01-06 | Initial comprehensive quality checklist | Claude (Academic Thesis AI) |
| 1.1 | 2025-01-07 | Added DOI validation check (no 404s allowed), added DOI 404 error to issue resolution guide | Claude (Academic Thesis AI) |

---

**END OF QUALITY CHECKLIST**
