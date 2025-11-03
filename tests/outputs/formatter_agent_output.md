```markdown
# Formatted Paper Outline

**Format Applied:** IMRaD
**Target Journal:** Nature
**Word Limit:** 8000 words (approx. for main text + extended methods/data, typical for a research article)
**Citation Style:** APA 7th Edition

---

## Formatting Requirements

### Manuscript Specifications
- **Font:** Arial 11pt (Common for scientific journals like Nature)
- **Line Spacing:** Double
- **Margins:** 1 inch all sides
- **Page Numbers:** Bottom right
- **Headings:** Numbered

### Section Heading Levels
- **Level 1:** Bold, Centered, Title Case
- **Level 2:** Bold, Left-Aligned, Title Case
- **Level 3:** Bold, Indented, Sentence case

### Citation Format
- **In-text:** (Author, Year)
- **Bibliography:** Full format specification (APA 7th Edition)

### ⚠️ CITATION REQUIREMENTS - CRITICAL

**Specify citation style early and communicate to ALL Crafter agents:**

**Default Style:** APA 7th Edition (unless specified otherwise)

**In-text citation format:**
```
✅ CORRECT: (Author, Year)
✅ CORRECT: (Author & Co-Author, Year)
✅ CORRECT: (Author et al., Year)
❌ WRONG: (Author [VERIFY]) - missing year
```

**Reference list requirements:**
- Use DOI when available: `https://doi.org/xxxxx`
- Consistent formatting for all entries
- Alphabetical order by first author
- Complete metadata (author, year, title, publisher/journal, DOI/URL)

**For table footnotes and data sources:**
```
✅ CORRECT: *Source: Adapted from Author (Year) and Organization (Year).*
❌ WRONG: *Source: Author (Year) [VERIFY].*
```

**[VERIFY] placeholder usage:**
- Crafters should ONLY use [VERIFY] if source year/details truly unknown
- Prefer using research context sources without [VERIFY]
- Agent #14 (Citation Verifier) will complete any [VERIFY] tags

**Language-specific adaptations:**
- German theses: Use German punctuation but keep APA structure
- Spanish/French: Adapt punctuation while maintaining APA format
- Always specify language requirements to Crafter agents

**Communicate to Crafter agents:**
"All citations must follow APA 7th format. Use (Author, Year) in-text. Only add [VERIFY] if you cannot determine the year from research context."

---

## Formatted Structure

### Title
**Format:** Bold, Centered, 14pt
**Max Length:** 100 characters (Nature prefers concise titles)
**Suggested:** AI-Enhanced Climate Modeling: Advancing Predictions and Efficiency

### Author Information
**Format:**
- Name(s): Full Name, superscript for affiliations
- Affiliation(s): Department, University, City, Country
- Email(s): Corresponding author email clearly marked
- ORCID: Required for all authors

### Abstract
**Heading:** Bold, Centered
**Length:** 150-250 words (Nature often has ~150 words for main text abstracts)
**Structure:**
- Background (1-2 sentences): Context of climate modeling challenges.
- Objective (1 sentence): State the aim of using AI for climate modeling.
- Methods (2-3 sentences): Briefly describe the AI approach, data, and model.
- Results (2-3 sentences): Summarize key findings on accuracy, efficiency, and uncertainty.
- Conclusions (1-2 sentences): Highlight the significance and implications.

**Keywords:** 3-6 keywords (e.g., Artificial Intelligence, Climate Change, Machine Learning, Earth System Modeling, Predictive Analytics, Uncertainty Quantification)

---

## 1. Introduction
**Section Number:** 1
**Length:** 800-1200 words
**Subsections:**

### 1.1 Background and Motivation
**Content:** Background on climate modeling, its importance, and the increasing urgency for accurate predictions. Introduce the general concept of leveraging advanced computational methods.
**Format specifications:** Standard paragraph text, with clear topic sentences and logical flow.

### 1.2 Problem Statement
**Content:** Limitations of traditional physics-based models (e.g., computational cost, resolution constraints, inability to capture complex non-linear interactions). Articulate the specific gaps that current methods face.
**Format specifications:** Focused paragraphs outlining the challenges and the need for novel solutions.

### 1.3 Research Objectives
**Content:** Clearly state the aims of the study, specifically how AI addresses the identified limitations.
**List format:**
1. To develop and evaluate an AI-driven framework for enhanced climate modeling.
2. To assess the predictive accuracy and computational efficiency of the proposed AI model compared to traditional approaches.
3. To quantify the uncertainty associated with AI-based climate predictions.

### 1.4 Contributions
**Content:** Highlight the novel aspects and significance of the work.
**Bullet format:**
- Introduction of a novel AI architecture tailored for specific climate phenomena.
- Demonstration of significant improvements in predictive accuracy and computational speed.
- A robust framework for quantifying uncertainty in AI-driven climate predictions.
- Providing a pathway for integrating AI into operational climate forecasting systems.

### 1.5 Paper Organization
**Content:** Briefly describe the structure of the remainder of the paper.
**Format specifications:** Standard paragraph.

---

## 2. Related Work / Literature Review
**Section Number:** 2
**Length:** 1500-2500 words (Note: For Nature, extensive literature review is often integrated into the Introduction to establish context, and then in the Discussion for comparison. This section might be significantly condensed or integrated in a strict Nature submission, but is included here as per the prompt's template.)
**Organization:** Thematic subsections, focusing on how prior work informs the current study and what gaps remain.

### 2.1 Traditional Climate Models: Foundations and Challenges
**Content:** Overview of traditional physics-based climate models, their evolution, successes, and inherent limitations relevant to this study.
**Format: narrative + comparison table (if applicable for specific model types)**

### 2.2 Machine Learning Applications in Climate Science
**Content:** Review of existing machine learning applications in various aspects of climate science (e.g., weather prediction, downscaling, parameterization, extreme event detection). Categorize by approach or application area.

**Table 1:** Summary of Related Work on AI in Climate Modeling
| Study | AI Method | Climate Application | Key Findings | Limitations |
|-------|-----------|---------------------|--------------|-------------|
| (Author, Year) [1] | CNNs              | Cloud parameterization | Improved accuracy | Limited generalizability |
| (Author, Year) [2] | LSTMs             | ENSO prediction     | Enhanced long-term forecasts | Data dependency |
| (Author, Year) [3] | GANs              | Climate downscaling | Generated high-res data | Mode collapse issues |

### 2.3 Hybrid Approaches and Model Coupling
**Content:** Discuss efforts to combine traditional physics models with AI components, highlighting the advantages and challenges of such integrations.

### 2.4 Summary and Gap Analysis
**Content:** Synthesize the reviewed literature, identifying the current state-of-the-art and explicitly articulating the research gap that this paper aims to fill.
**Format: synthesis paragraph**

---

## 3. Methodology (Materials & Methods)
**Section Number:** 3
**Length:** 1000-1500 words (Can be extensive for Nature; often includes supplementary methods)

### 3.1 Research Design and Overall Framework
**Content:** Describe the overall approach, including the rationale for choosing an AI-driven methodology. Explain the conceptual flow from data input to model output.
**Format: paragraph + diagram**

**Figure 1:** Research Framework for AI-Enhanced Climate Modeling
[Placeholder for a conceptual diagram illustrating the AI model's architecture, data flow, and integration points with climate data.]
**Caption format:** Figure 1. Conceptual framework of the AI-enhanced climate modeling system. This diagram illustrates the data input, processing layers, AI model components, and output generation, highlighting key interactions and feedback loops.

### 3.2 Data Collection and Preprocessing
**Content:** Detail the datasets used (e.g., reanalysis data, observational data, climate model outputs), their sources, spatial and temporal resolutions, and the specific variables included. Describe preprocessing steps (e.g., normalization, feature engineering, spatio-temporal alignment).
**Format: narrative + specification table**

**Table 2:** Dataset Specifications for Climate Model Training
| Attribute | Description |
|-----------|-------------|
| Source    | ERA5 reanalysis (ECMWF), CMIP6 model outputs |
| Period    | 1979-2022 (training), 2023-2024 (validation/test) |
| Variables | Temperature, Precipitation, Geopotential Height, Wind Components, Sea Surface Temperature |
| Resolution | 0.25° x 0.25° spatial, 6-hourly temporal |
| Size      | ~5 TB raw data |

### 3.3 Model Architecture and Training
**Content:** Provide a detailed description of the AI model architecture (e.g., type of neural network, number of layers, activation functions, specific components). Explain the training procedure, including optimization algorithms, loss functions, batch size, epochs, and hardware used.
**Format: detailed narrative, potentially with pseudo-code or small architectural diagrams**

### 3.4 Evaluation Metrics and Validation Procedures
**Content:** Specify the metrics used to evaluate model performance (e.g., RMSE, MAE, R-squared, skill scores). Describe the cross-validation strategy, independent test sets, and any specific validation protocols.
**Format: numbered steps, clear definitions of metrics**
1. **Root Mean Squared Error (RMSE):** Used to quantify the average magnitude of the errors. `RMSE = sqrt(mean((y_pred - y_true)^2))`
2. **Mean Absolute Error (MAE):** Provides a linear measure of average error. `MAE = mean(|y_pred - y_true|)`
3. **Correlation Coefficient (R):** Measures the linear relationship between predicted and observed values.
4. **Skill Scores:** Employed for specific climate phenomena, such as anomaly correlation coefficient (ACC) for forecasting.
5. **Computational Cost Analysis:** Measured in GPU-hours and inference time per forecast.

---

## 4. Results
**Section Number:** 4
**Length:** 1500-2000 words

### 4.1 Descriptive Statistics and Baseline Performance
**Content:** Present initial data characteristics and the performance of baseline models (e.g., persistence model, simple statistical models, or a traditional climate model output) against which the AI model will be compared.
**Format: text + table**

**Table 3:** Descriptive Statistics of Key Climate Variables in Training Data
| Variable | Mean | Std. Dev. | Min | Max |
|----------|------|-----------|-----|-----|
| Temp (°C)| 15.2 | 8.1       | -30 | 45  |
| Precip (mm/day) | 2.5 | 3.2       | 0   | 150 |

### 4.2 Prediction Accuracy and Performance Comparison
**Content:** Present the core results demonstrating the AI model's predictive accuracy across various climate variables and timescales. Compare its performance quantitatively against traditional models or other state-of-the-art AI approaches.
**Format: subsection per finding + visualization (e.g., time series plots, spatial error maps)**

**Figure 2:** Comparison of Predicted vs. Observed Temperature Anomalies
[Placeholder for a line graph showing observed temperature anomalies alongside predictions from the AI model and a traditional model over a specific period, with error bands.]
**Caption format:** Figure 2. Time series of global average surface air temperature anomalies (relative to 1981-2010 mean) from observations (black line), the AI model (blue line), and a control climate model (red dashed line) for the period 2020-2024. Shaded areas represent 95% confidence intervals.

### 4.3 Computational Efficiency Analysis
**Content:** Detail the computational benefits of the AI model, including training time, inference speed, and resource utilization, showcasing its advantage over computationally intensive physics-based models.
**Format: text + bar charts or tables comparing runtimes**

### 4.4 Uncertainty Quantification
**Content:** Present the results of the uncertainty quantification analysis, illustrating the confidence intervals of the predictions and identifying regions or scenarios with higher uncertainty.
**Format: text + supplementary figures (e.g., ensemble spread maps, prediction interval plots)**

---

## 5. Discussion
**Section Number:** 5
**Length:** 1500-2000 words

### 5.1 Interpretation of Findings
**Content:** Interpret the main results in the context of the research objectives. Explain *why* the AI model performs as it does, discussing the implications of its accuracy, efficiency, and uncertainty characteristics.
**Format: narrative with citations supporting the interpretations**

### 5.2 Comparison with Prior Work
**Content:** Discuss how the findings align with, contradict, or extend existing research in AI for climate modeling and traditional climate science. Emphasize the unique contributions of this study.
**Format: comparative discussion, referring back to literature review**

### 5.3 Theoretical Implications
**Content:** Explore the broader theoretical implications of integrating AI into climate modeling. How does this work advance our understanding of climate system predictability or the potential for data-driven discovery in Earth sciences?
**Format: paragraph, conceptual discussion**

### 5.4 Practical Implications
**Content:** Discuss the real-world applications and societal benefits of this research. How can these AI models be used in climate change mitigation, adaptation strategies, policy-making, or operational forecasting?
**Format: bullet points or paragraphs, focusing on actionable insights**

### 5.5 Limitations and Future Work
**Content:** Acknowledge the limitations of the current study (e.g., data availability, model complexity, specific regional focus). Suggest concrete directions for future research, building upon the current findings.
**Format: honest assessment, constructive suggestions**

---

## 6. Conclusion
**Section Number:** 6
**Length:** 500-700 words

[No subsections - continuous narrative]

**Required elements:**
- **Restate problem and approach:** Briefly re-emphasize the challenge of climate modeling and how this study's AI approach addressed it.
- **Summarize key findings:** Concisely reiterate the most important results regarding improved accuracy, efficiency, and uncertainty quantification.
- **Emphasize contributions:** Clearly state the novel contributions of the research to the field of climate science and AI.
- **Suggest future directions:** Briefly outline promising avenues for future research building on this work.

---

## Acknowledgments
[If applicable - funding bodies, institutional support, specific contributors, data providers. Nature often requires a concise Acknowledgments section.]

---

## References
**Format:** APA 7th Edition
**Minimum:** 20 references for empirical, 50+ for review (Aim for 40-60 for a Nature research article, focusing on high-impact and relevant works.)

**Categories:**
- Foundational works (pre-2019): (~20%)
- Recent works (2020-2024): (~80%)
- Including own prior work: (Optional, max 10%)

---

## Appendices
[If applicable - for supplementary information like extended methods, additional figures/tables, code snippets, detailed proofs. Nature often uses "Extended Data" sections.]
- Appendix A: Extended Data Figures
- Appendix B: Supplementary Methods and Algorithms
- Appendix C: Full Dataset Description

---

## Journal-Specific Requirements

### Nature

**Mandatory sections:**
- [X] Data Availability Statement (Crucial for Nature, must specify where data can be accessed or how to reproduce)
- [X] Conflict of Interest Statement (Must be declared for all authors)
- [X] Author Contributions (Detailed description of each author's role)
- [X] Funding Statement (Specific grant numbers and funding bodies)
- [X] Ethics Statement (If applicable, for human or animal subjects)
- [X] Code Availability Statement (Where code used in the study can be accessed)

**Formatting specifics:**
- Figures: PNG/TIFF, min 300dpi (often 600dpi for line art), vector graphics preferred for clarity. Figures often have panels (a, b, c).
- Tables: Editable format (e.g., Word, Excel), not images. Concise and self-explanatory.
- Equations: Numbered, right-aligned (e.g., (1)). Use MathType or Equation Editor.
- Article Length: Main text ~2000-3000 words, but significant content can be in Methods, References, and Extended Data.
- Abstract: Max 150 words.
- In-text Citations: Numbered [1], [2,3], [4-6] (Nature's default, *not* APA).
    **Correction for Nature:** While the user specified APA, Nature's standard is numerical in-text citations. I will keep APA as per user's request for *this* formatting task, but note that Nature typically uses numerical style. I will stick to the user's explicit request for APA for the formatting agent's output.
    *Self-correction: The prompt explicitly states "Citation Style: [APA | MLA | Chicago | IEEE]" and then "Default Style: APA 7th Edition (unless specified otherwise)". The user specified APA. So, I must enforce APA 7th, even if Nature typically uses numerical. This agent's job is to apply the *specified* style.*

**Submission checklist:**
- [X] Cover letter (explaining significance, why Nature, potential reviewers)
- [X] Highlights (often not a separate section for Nature, but key findings are emphasized in the cover letter/abstract)
- [X] Graphical abstract (Optional, but often beneficial for promotion)
- [X] Supplementary materials (Extended Data, Supplementary Information)
- [X] Main text, figures, tables, references, and all mandatory statements as separate files or integrated as per portal.

---

## Length Targets by Section

| Section | Words | % of Total |
|---------|-------|------------|
| Abstract | 200 | 2.5% |
| Introduction | 1000 | 12.5% |
| Related Work / Lit Review | 2000 | 25% |
| Methodology | 1500 | 18.75% |
| Results | 1800 | 22.5% |
| Discussion | 1200 | 15% |
| Conclusion | 300 | 3.75% |
| **Total** | **8000** | **100%** |

---

## Quality Checklist

### Structure
- [X] All required sections present
- [X] Logical flow between sections
- [X] Appropriate section lengths

### Formatting
- [X] Consistent heading styles
- [X] Proper citation format (APA 7th Edition)
- [X] Figures/tables numbered correctly
- [X] Captions complete and descriptive

### Content
- [X] Abstract summarizes whole paper
- [X] Introduction states clear RQ
- [X] Methods enable replication
- [X] Results presented objectively
- [X] Discussion interprets findings
- [X] Conclusion emphasizes contribution

---

## Style Guide

### Academic Tone
- ✅ **Use:** "The results indicate...", "We observed...", "This suggests..."
- ❌ **Avoid:** "Obviously...", "Clearly...", "It's interesting that..."

### Tense Usage
- **Introduction:** Present tense (current state)
- **Literature Review:** Past tense (what others found)
- **Methods:** Past tense (what you did)
- **Results:** Past tense (what you found)
- **Discussion:** Present tense (what it means)

### Voice
- **Active vs Passive:** Prefer active for clarity, passive for objectivity
- ✅ "We analyzed the data" (active, clear)
- ✅ "The data were analyzed" (passive, objective)

---

## Next Steps

After formatting:
1. Review against journal guidelines (especially Nature's specific citation style and section requirements, noting the APA request here).
2. Ensure all placeholders are noted
3. Proceed to Compose phase with clear structure
4. Save to `outline_formatted.md`

```