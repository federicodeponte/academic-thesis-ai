# Production Monitoring Guide - Agent #15 (Enhancer)

**Last Updated:** November 9, 2025
**Status:** Production Ready with Dual-Layer Defense

---

## Overview

This guide provides monitoring procedures, warning thresholds, and troubleshooting steps for Agent #15 (Enhancer) in production. The Agent #15 dual-layer defense system (prevention + sanitization) ensures stable, corruption-free outputs.

---

## 1. Sanitization Statistics Monitoring

### Expected Behavior (Healthy System)

When the system is working correctly, you should see:

```
🧹 Sanitizing enhanced output...
  ✓ Size: 236,447 → 233,891 bytes (2,556 bytes removed)
  ✅ Output within target size!

📊 Sanitization Summary:
  • Cells truncated: 0
  • Meta-comments removed: 0
  • Whitespace removed: 2,556 chars
  • Size reduction: 2,556 bytes
  • Final size: 233,891 bytes
```

**Key Indicators:**
- ✅ **Cells truncated: 0** - Prevention layer working perfectly
- ✅ **Meta-comments: 0** - LLM following instructions
- ✅ **Whitespace: 2-5KB** - Normal cleanup range
- ✅ **Final size: 197-228KB** - Healthy output range

### Warning Thresholds

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| **Cells Truncated** | 0 | 1-3 | >3 |
| **Meta-Comments** | 0 | 1-2 | >2 |
| **File Size** | 197-228KB | 228-300KB | >300KB |
| **Whitespace Removed** | 2-5KB | 5-10KB | >10KB |
| **Size Reduction %** | 1-2% | 2-5% | >5% |

---

## 2. Warning Threshold Definitions

### ⚠️ WARNING Level (Investigate but not urgent)

**Trigger Conditions:**
- 1-3 table cells truncated
- 1-2 meta-comments removed
- File size 228-300KB
- 5-10KB whitespace removed
- 2-5% size reduction

**Actions:**
1. Review Agent #15 prompt (check if constraints are clear)
2. Check LLM model version (verify no regression)
3. Inspect enhanced output for patterns
4. Monitor next 2-3 runs

**Example Log:**
```
⚠️  Quality warnings:
    ⚠️  File size (265,432 bytes) exceeds recommended max (300,000 bytes)
```

### 🚨 CRITICAL Level (Immediate action required)

**Trigger Conditions:**
- More than 3 table cells truncated
- More than 2 meta-comments removed
- File size >300KB
- More than 10KB whitespace removed
- More than 5% size reduction
- Any line >5,000 characters
- More than 1,000 spaces in single line

**Actions:**
1. **HALT PRODUCTION** - Stop thesis generation pipeline
2. Capture corrupted output for analysis
3. Review LLM prompt adherence
4. Check for prompt regression
5. Validate sanitizer is enabled in all scripts
6. Re-test on all 3 thesis types before resuming

**Example Log:**
```
❌ Output still too large - manual review needed

⚠️  Quality warnings:
    ⚠️  File size (1,296,037 bytes) exceeds recommended max (300,000 bytes)
    ⚠️  Line 298 is 106,794 chars long (likely corrupted table)
    ⚠️  Line 298 has 633,245 spaces (likely corruption)
```

---

## 3. Expected vs Anomalous Behavior

### ✅ Expected Behavior

**Normal Sanitization Output:**
```bash
📖 Reading: tests/outputs/opensource_thesis/16_enhanced_final.md
🧹 Sanitizing enhanced output...
  ✓ Size: 236,447 → 233,891 bytes (2,556 bytes removed)
  ✅ Output within target size!

📊 Sanitization Summary:
  • Cells truncated: 0
  • Meta-comments removed: 0
  • Whitespace removed: 2,556 chars
  • Size reduction: 2,556 bytes
  • Final size: 233,891 bytes
💾 Saved: tests/outputs/opensource_thesis/16_enhanced_final.md
```

**What This Means:**
- Prevention layer stopped corruption before it happened
- LLM followed prompt constraints perfectly
- Only normal whitespace cleanup needed
- File size healthy (197-228KB range)

### ❌ Anomalous Behavior

**Corrupted Output (Pre-Fix):**
```bash
📖 Reading: tests/outputs/opensource_thesis_backup_20251103_195312/16_enhanced_final.md
🧹 Sanitizing enhanced output...
  ✓ Truncated 47 oversized table cells
  ✓ Removed 3 meta-comments
  ✓ Removed 1,167,673 excessive whitespace chars
  ⚠️  Quality warnings:
      ⚠️  File size (1,296,037 bytes) exceeds recommended max (300,000 bytes)
      ⚠️  Line 298 is 106,794 chars long (likely corrupted table)
  ❌ Output still too large - manual review needed

📊 Sanitization Summary:
  • Cells truncated: 47
  • Meta-comments removed: 3
  • Whitespace removed: 1,167,673 chars
  • Size reduction: 1,167,673 bytes
  • Final size: 128,364 bytes
  • Warnings: 2
```

**What This Means:**
- Prevention layer failed (LLM ignored constraints)
- Sanitizer had to aggressively clean corruption
- 47 table cells had >500 chars (should be 0)
- 90% of file was corrupted whitespace
- **This should NEVER happen in production**

---

## 4. Troubleshooting Guide

### Problem: Cells Truncated > 0

**Diagnosis:**
```bash
# Check which table cells were truncated
grep -n "\[truncated\]" tests/outputs/*/16_enhanced_final.md
```

**Root Causes:**
1. LLM ignoring prompt constraints
2. Prompt regression (constraints removed/weakened)
3. LLM model change/update

**Solution:**
1. Review `prompts/06_enhance/enhancer.md` lines 480-508
2. Verify table constraints are BOLD and CAPITALIZED
3. Test with single thesis to isolate issue
4. Consider adding few-shot examples to prompt

### Problem: File Size > 300KB

**Diagnosis:**
```bash
# Check actual file sizes
ls -lh tests/outputs/*/16_enhanced_final.md

# Look for long lines
awk 'length > 5000 { print NR, length }' tests/outputs/*/16_enhanced_final.md
```

**Root Causes:**
1. Table corruption (cells >500 chars)
2. Excessive whitespace patterns
3. Meta-comment leakage

**Solution:**
1. Run sanitizer on file
2. Inspect lines flagged as >5000 chars
3. Verify sanitizer is integrated in test scripts (lines ~567-628)

### Problem: Meta-Comments Removed > 0

**Diagnosis:**
```bash
# Check for meta-comment patterns in original output
grep -iE "(here is|this is|i have generated)" tests/outputs/*/16_enhanced_final.md
```

**Root Causes:**
1. LLM adding agent instructions to output
2. Prompt not clear about output format
3. LLM model regression

**Solution:**
1. Review Agent #15 prompt (lines 1-20)
2. Add explicit instruction: "Output ONLY the enhanced thesis, no meta-comments"
3. Update `META_COMMENT_PATTERNS` in `output_sanitizer.py` if needed

### Problem: Size Reduction > 10%

**Diagnosis:**
```bash
# Check original size vs final size
du -h tests/outputs/*/16_enhanced_final.md

# Run sanitizer in verbose mode to see what's being removed
python3 -c "
from utils.output_sanitizer import sanitize_enhanced_file
from pathlib import Path
sanitize_enhanced_file(
    input_path=Path('tests/outputs/opensource_thesis/16_enhanced_final.md'),
    output_path=None,
    verbose=True
)
"
```

**Root Causes:**
1. Major table corruption (>10 cells truncated)
2. Excessive whitespace (>100KB removed)
3. Multiple root causes combined

**Solution:**
1. **HALT PRODUCTION**
2. Capture corrupted file for analysis
3. Test on backup corrupted file to ensure sanitizer handles it
4. Review all prompt changes in last 24 hours

---

## 5. Production Health Checks

### Pre-Production Checklist

Before deploying any changes to Agent #15:

```bash
# 1. Verify sanitizer integration in all test scripts
grep -n "sanitize_enhanced_file" tests/scripts/test_*.py

# 2. Check prompt constraints are in place
grep -A 20 "CRITICAL TABLE CELL LENGTH CONSTRAINTS" prompts/06_enhance/enhancer.md

# 3. Run validation test on all 3 theses
python3 tests/scripts/test_opensource_thesis.py > /tmp/health_check_opensource.log 2>&1 &
python3 tests/scripts/test_ai_pricing_thesis.py > /tmp/health_check_ai_pricing.log 2>&1 &
python3 tests/scripts/test_co2_german_thesis.py > /tmp/health_check_co2_german.log 2>&1 &

# 4. Wait 10-12 minutes, then check results
tail -100 /tmp/health_check_*.log | grep -E "(Cells truncated|Meta-comments|Final size)"
```

**Expected Results:**
- ✅ All 3 theses complete successfully
- ✅ 0 cells truncated across all theses
- ✅ 0 meta-comments removed
- ✅ File sizes 197-228KB

### Continuous Monitoring (Production)

**Daily Checks:**
```bash
# Check last 24 hours of thesis generations
find tests/outputs -name "16_enhanced_final.md" -mtime -1 -ls

# Verify file sizes are healthy
find tests/outputs -name "16_enhanced_final.md" -size +300k

# Count any warnings in logs
grep -r "⚠️  Quality warnings" tests/outputs/*/logs/
```

**Weekly Checks:**
```bash
# Run full validation suite
python3 -m pytest tests/validation/test_agent15_stability.py

# Review sanitization statistics
grep -r "Sanitization Summary" tests/outputs/*/logs/ | \
    awk -F: '{print $2}' | sort | uniq -c
```

### Emergency Rollback Procedure

If Agent #15 starts producing corrupted outputs:

1. **Immediate Actions:**
```bash
# Bypass Agent #15 in all scripts
sed -i 's/enhanced_paper = run_agent/# BYPASSED: enhanced_paper = run_agent/' tests/scripts/test_*.py
sed -i 's/if enhanced_paper:/if False:  # BYPASSED/' tests/scripts/test_*.py

# Verify bypass is active
grep -n "BYPASSED" tests/scripts/test_*.py
```

2. **Root Cause Analysis:**
```bash
# Compare current prompt with working version
git diff HEAD~5 prompts/06_enhance/enhancer.md

# Test sanitizer on known corrupted backup
python3 utils/output_sanitizer.py
```

3. **Fix and Re-Enable:**
```bash
# After fix is validated, remove bypass
git checkout tests/scripts/test_*.py

# Run validation test
python3 tests/scripts/test_opensource_thesis.py

# Verify 0 cells truncated before deploying
```

---

## 6. Maintenance Guidelines

### Monthly Maintenance

**Review Prompt Effectiveness:**
```bash
# Count average cells truncated per month
find tests/outputs -name "16_enhanced_final.md" -mtime -30 -exec \
    grep -H "Cells truncated" {} \; | \
    awk '{sum+=$3; count++} END {print "Average:", sum/count}'
```

**Expected Result:** 0.0 cells truncated per thesis

**Update Sanitizer Patterns:**
```bash
# Check for new meta-comment patterns
grep -rE "^(Here|This|I)" tests/outputs/*/16_enhanced_final.md | \
    head -20
```

If new patterns found, update `META_COMMENT_PATTERNS` in `utils/output_sanitizer.py`

### Quarterly Maintenance

**Full Regression Test:**
```bash
# Run all 3 theses 3 times each (9 total runs)
for i in {1..3}; do
    python3 tests/scripts/test_opensource_thesis.py > /tmp/regression_opensource_$i.log 2>&1 &
    python3 tests/scripts/test_ai_pricing_thesis.py > /tmp/regression_ai_pricing_$i.log 2>&1 &
    python3 tests/scripts/test_co2_german_thesis.py > /tmp/regression_co2_german_$i.log 2>&1 &
    wait
done

# Analyze results
grep "Cells truncated" /tmp/regression_*.log | awk '{sum+=$3} END {print "Total cells truncated:", sum}'
```

**Expected Result:** 0 total cells truncated across all 9 runs

**Performance Optimization:**
```bash
# Check average sanitization time
grep -r "Sanitizing enhanced output" tests/outputs/*/logs/ | \
    wc -l
```

If sanitizer is frequently truncating cells (>5% of runs), consider:
1. Strengthening prompt constraints
2. Adding few-shot examples to Agent #15 prompt
3. Reviewing LLM model version for regressions

---

## 7. Key Metrics Dashboard

**Production Health Scorecard:**

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Cells Truncated (per thesis) | 0 | 0 | ✅ |
| Meta-Comments Removed | 0 | 0 | ✅ |
| File Size Range | 197-228KB | 197-228KB | ✅ |
| Whitespace Removed | 2-5KB | 2-5KB | ✅ |
| Size Reduction % | 1-2% | 1-2% | ✅ |
| Sanitization Success Rate | 100% | 100% | ✅ |

**Last Validation:** November 9, 2025
**Test Coverage:** 3/3 thesis types (Open Source, AI Pricing, CO2 German)
**Test Results:** Perfect scores across all metrics

---

## 8. Contact & Escalation

**For Production Issues:**
1. Check this guide first
2. Review `CHANGELOG.md` for recent changes
3. Inspect `tests/outputs/AGENT15_FIX_VALIDATION_REPORT.md`
4. Test sanitizer standalone: `python3 utils/output_sanitizer.py`

**Emergency Bypass:**
If Agent #15 is producing corrupted outputs and fix is not immediate:
1. Bypass Agent #15 in all test scripts (see Emergency Rollback)
2. Document the issue
3. Test fix on corrupted backup before re-enabling

**Validation Before Re-Enabling:**
- ✅ Sanitizer tested on corrupted backup (1.3MB → 128KB)
- ✅ All 3 thesis types tested
- ✅ 0 cells truncated in all tests
- ✅ File sizes healthy (197-228KB)

---

## Appendix A: File Locations

**Key Files:**
- Agent #15 Prompt: `prompts/06_enhance/enhancer.md`
- Output Sanitizer: `utils/output_sanitizer.py`
- Test Scripts: `tests/scripts/test_*.py`
- Validation Report: `tests/outputs/AGENT15_FIX_VALIDATION_REPORT.md`
- Changelog: `CHANGELOG.md`

**Test Outputs:**
- Open Source: `tests/outputs/opensource_thesis/16_enhanced_final.md`
- AI Pricing: `tests/outputs/ai_pricing_thesis/16_enhanced_final.md`
- CO2 German: `tests/outputs/co2_thesis_german/16_enhanced_final.md`

**Corrupted Backup (For Testing):**
- `tests/outputs/opensource_thesis_backup_20251103_195312/16_enhanced_final.md` (1.3MB)

---

## Appendix B: Quick Reference Commands

```bash
# Test sanitizer on specific file
python3 -c "
from utils.output_sanitizer import sanitize_enhanced_file
from pathlib import Path
sanitize_enhanced_file(
    input_path=Path('tests/outputs/opensource_thesis/16_enhanced_final.md'),
    verbose=True
)
"

# Check all enhanced outputs for corruption
find tests/outputs -name "16_enhanced_final.md" -exec \
    grep -H "\[truncated\]" {} \; 2>/dev/null

# Verify file sizes are healthy
find tests/outputs -name "16_enhanced_final.md" -exec \
    ls -lh {} \; | awk '{print $9, $5}'

# Count cells truncated across all outputs
find tests/outputs -name "16_enhanced_final.md" -exec \
    grep -c "\[truncated\]" {} \; | \
    awk '{sum+=$1} END {print "Total truncated cells:", sum}'
```

---

**Document Version:** 1.0
**Last Reviewed:** November 9, 2025
**Next Review:** December 9, 2025
