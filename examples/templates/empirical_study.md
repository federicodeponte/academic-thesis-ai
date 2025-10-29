# [Your Study Title]: An Empirical Investigation

**Author:** [Your Name]
**Institution:** [Your University]
**Course:** [Course Code]
**Date:** [Current Date]

---

## Abstract

**Purpose:** [1 sentence on research objective]

**Design/Methodology/Approach:** [1-2 sentences on research method]

**Findings:** [2-3 sentences on key results]

**Research Limitations/Implications:** [1 sentence]

**Originality/Value:** [1 sentence on contribution]

**Keywords:** [keyword1, keyword2, keyword3, keyword4, keyword5]

---

## 1. Introduction

### 1.1 Background and Motivation

[Why is this research important? What problem are you addressing?]

### 1.2 Research Questions and Hypotheses

**Research Questions:**
1. **RQ1:** [Your first research question]
2. **RQ2:** [Your second research question]

**Hypotheses:**
- **H1:** [Hypothesis 1]
- **H2:** [Hypothesis 2]
- **H3:** [Hypothesis 3]

### 1.3 Contribution

This study contributes to the literature by:
1. [Contribution 1]
2. [Contribution 2]
3. [Contribution 3]

### 1.4 Paper Structure

[Brief overview of remaining sections]

---

## 2. Literature Review

### 2.1 Theoretical Framework

[What theory/theories underpin your study?]

### 2.2 Related Work

#### 2.2.1 [Topic Area 1]

[Review relevant literature on first topic]

#### 2.2.2 [Topic Area 2]

[Review relevant literature on second topic]

#### 2.2.3 [Topic Area 3]

[Review relevant literature on third topic]

### 2.3 Research Gap

[What gap does your study address? How does it extend prior work?]

---

## 3. Methodology

### 3.1 Research Design

**Type:** [Experimental / Quasi-experimental / Survey / Case study / etc.]

**Approach:** [Quantitative / Qualitative / Mixed methods]

[Justify your methodological choices]

### 3.2 Participants/Sample

**Population:** [Target population]

**Sample size:** [N = number]

**Sampling method:** [Random / Stratified / Convenience / etc.]

**Demographics:**
- Age: [Range or mean]
- Gender: [Distribution]
- Other relevant characteristics: [...]

### 3.3 Data Collection

**Data sources:**
1. [Source 1]: [Description]
2. [Source 2]: [Description]

**Instruments:**
- [Instrument 1]: [Description, reliability, validity]
- [Instrument 2]: [Description]

**Procedure:**
[Step-by-step data collection process]

### 3.4 Variables

**Independent Variables:**
- **IV1:** [Name] - [Operationalization]
- **IV2:** [Name] - [Operationalization]

**Dependent Variables:**
- **DV1:** [Name] - [Operationalization]
- **DV2:** [Name] - [Operationalization]

**Control Variables:**
- [CV1], [CV2], [CV3]

### 3.5 Data Analysis

**Statistical methods:**
- [Method 1]: [Purpose]
- [Method 2]: [Purpose]

**Software:** [SPSS / R / Python / etc.]

### 3.6 Ethical Considerations

[IRB approval, informed consent, data privacy, etc.]

---

## 4. Results

### 4.1 Descriptive Statistics

[Present summary statistics, demographics, preliminary findings]

**Table 1: Descriptive Statistics**

| Variable | Mean | SD | Min | Max |
|----------|------|----|----|-----|
| [Var 1] | | | | |
| [Var 2] | | | | |

### 4.2 Hypothesis Testing

#### 4.2.1 H1: [Hypothesis 1]

[Present statistical test results]

**Result:** H1 is [supported / not supported] (t = [value], p = [value])

[Interpretation]

#### 4.2.2 H2: [Hypothesis 2]

[Repeat for each hypothesis]

### 4.3 Additional Findings

[Any unexpected or secondary findings]

---

## 5. Discussion

### 5.1 Summary of Findings

[Recap main results in plain language]

### 5.2 Theoretical Implications

[How do your findings contribute to theory?]

### 5.3 Practical Implications

[What should practitioners take away from this?]

**For practitioners:**
- [Implication 1]
- [Implication 2]

**For policymakers:**
- [Implication 1]
- [Implication 2]

### 5.4 Comparison with Prior Research

[How do your findings align with or differ from existing literature?]

**Consistent with:**
- [Finding 1] aligns with Author (Year)
- [Finding 2] supports Author (Year)

**Contrasts with:**
- [Finding 3] differs from Author (Year) - [possible explanation]

---

## 6. Limitations

[Be honest about study limitations]

1. **[Limitation 1]:** [Description and impact]
2. **[Limitation 2]:** [Description and impact]
3. **[Limitation 3]:** [Description and impact]

---

## 7. Conclusion

### 7.1 Key Takeaways

[3-5 main conclusions from your study]

### 7.2 Future Research Directions

[What should researchers explore next?]

### 7.3 Final Remarks

[Closing thoughts on significance of your work]

---

## References

[APA 7th edition formatted references]

---

## Appendices

### Appendix A: Survey Instrument

[Include questionnaire, interview protocol, etc.]

### Appendix B: Additional Statistical Tables

[Any supplementary analyses]

---

**How to Use This Template with Academic Thesis AI:**

1. **Scout Agent** - Find relevant empirical studies: `prompts/01_research/scout.md`
2. **Scribe Agent** - Extract methodologies and findings: `prompts/01_research/scribe.md`
3. **Signal Agent** - Identify research gaps: `prompts/01_research/signal.md`
4. **Architect Agent** - Structure your study: `prompts/02_structure/architect.md`
5. **Formatter Agent** - Apply formatting (IMRaD): `prompts/02_structure/formatter.md`
6. **Crafter Agent** - Write each section: `prompts/03_compose/crafter.md`
7. **Thread Agent** - Ensure consistency: `prompts/03_compose/thread.md`
8. **Narrator Agent** - Unify voice: `prompts/03_compose/narrator.md`
9. **Skeptic Agent** - Critical review: `prompts/04_validate/skeptic.md`
10. **Verifier Agent** - Check claims and citations: `prompts/04_validate/verifier.md`
11. **Referee Agent** - Simulate peer review: `prompts/04_validate/referee.md`
12. **Voice Agent** - Match your writing style: `prompts/05_refine/voice.md`
13. **Entropy Agent** - Humanize text: `prompts/05_refine/entropy.md`
14. **Polish Agent** - Final grammar check: `prompts/05_refine/polish.md`

**Export to PDF:**
```bash
python utils/export_professional.py examples/templates/empirical_study.md \
    --pdf my_empirical_study.pdf \
    --title "Your Study Title" \
    --author "Your Name" \
    --institution "Your University"
```
