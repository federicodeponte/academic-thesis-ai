# [Your Review Title]: A Systematic Literature Review

**Author:** [Your Name]
**Institution:** [Your University]
**Course:** [Course Code]
**Date:** [Current Date]

---

## Abstract

[2-3 paragraphs summarizing your review: research questions, methods, key findings, and implications]

**Keywords:** [keyword1, keyword2, keyword3, keyword4, keyword5]

---

## 1. Introduction

### 1.1 Background

[Introduce your topic. Why is this area of research important? What makes it relevant now?]

### 1.2 Research Questions

This literature review addresses the following research questions:

1. **RQ1:** [Your first research question]
2. **RQ2:** [Your second research question]
3. **RQ3:** [Your third research question]

### 1.3 Scope and Limitations

[Define what's included and excluded in your review]

---

## 2. Methodology

### 2.1 Search Strategy

**Databases searched:**
- Semantic Scholar
- arXiv
- PubMed
- Google Scholar

**Keywords:** [list search terms used]

**Time period:** [e.g., 2018-2025]

### 2.2 Selection Criteria

**Inclusion criteria:**
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

**Exclusion criteria:**
- [Criterion 1]
- [Criterion 2]

### 2.3 Papers Reviewed

**Total papers found:** [number]
**Papers included:** [number]
**Papers excluded:** [number]

---

## 3. Literature Review

### 3.1 Theme 1: [First Major Theme]

[Overview of this theme]

#### 3.1.1 Key Findings

[Summarize major findings from papers addressing this theme]

**Representative works:**
- Author et al. (Year) - [Key contribution]
- Author et al. (Year) - [Key contribution]
- Author et al. (Year) - [Key contribution]

#### 3.1.2 Research Gaps

[What's missing in this area?]

### 3.2 Theme 2: [Second Major Theme]

[Repeat structure for each theme]

### 3.3 Theme 3: [Third Major Theme]

[Repeat structure for each theme]

---

## 4. Synthesis and Analysis

### 4.1 Cross-Cutting Themes

[Patterns that emerge across multiple themes]

### 4.2 Methodological Approaches

[What methods are researchers using? Trends?]

### 4.3 Theoretical Frameworks

[What theories underpin this research?]

---

## 5. Research Gaps and Future Directions

### 5.1 Identified Gaps

1. **Gap 1:** [Description]
2. **Gap 2:** [Description]
3. **Gap 3:** [Description]

### 5.2 Recommendations for Future Research

[What should researchers focus on next?]

---

## 6. Conclusion

### 6.1 Summary of Findings

[Recap main insights from your review]

### 6.2 Implications

**For theory:** [Theoretical contributions]

**For practice:** [Practical applications]

**For policy:** [Policy recommendations, if applicable]

### 6.3 Concluding Remarks

[Final thoughts on the state of this field]

---

## References

[APA 7th edition formatted references]

Author, A. A., & Author, B. B. (Year). Title of article. *Journal Name*, *Volume*(Issue), pages. https://doi.org/xxx

---

## Appendices

### Appendix A: Complete List of Reviewed Papers

[Table with all papers reviewed]

| Author(s) | Year | Title | Journal/Conference | Key Findings |
|-----------|------|-------|-------------------|--------------|
| | | | | |

---

**How to Use This Template with Academic Thesis AI:**

1. **Scout Agent** - Find 20-50 papers: Use `prompts/01_research/scout.md`
2. **Scribe Agent** - Summarize each paper: Use `prompts/01_research/scribe.md`
3. **Signal Agent** - Identify themes and gaps: Use `prompts/01_research/signal.md`
4. **Architect Agent** - Refine structure: Use `prompts/02_structure/architect.md`
5. **Formatter Agent** - Apply APA formatting: Use `prompts/02_structure/formatter.md`
6. **Crafter Agent** - Write each section: Use `prompts/03_compose/crafter.md`
7. **Thread Agent** - Check consistency: Use `prompts/03_compose/thread.md`
8. **Narrator Agent** - Unify voice: Use `prompts/03_compose/narrator.md`
9. **Skeptic Agent** - Critical review: Use `prompts/04_validate/skeptic.md`
10. **Verifier Agent** - Check citations: Use `prompts/04_validate/verifier.md`
11. **Referee Agent** - Peer review: Use `prompts/04_validate/referee.md`
12. **Voice Agent** - Match your style: Use `prompts/05_refine/voice.md`
13. **Entropy Agent** - Humanize text: Use `prompts/05_refine/entropy.md`
14. **Polish Agent** - Final polish: Use `prompts/05_refine/polish.md`

**Export to PDF:**
```bash
python utils/export_professional.py examples/templates/literature_review.md \
    --pdf my_literature_review.pdf \
    --engine pandoc
```
