# System Limitations & Transparency

**OpenDraft** is a powerful research and writing assistant, but it's important to understand its limitations. This document provides transparent information about what the system can and cannot do.

---

## Core Limitations

### 1. LLM Hallucination Risk

**Claim:** "Zero hallucination" is an **aspirational goal**, not a current reality.

**Reality:**
- ✅ The system uses multiple verification layers to reduce hallucinations
- ✅ Citation verification helps catch false references
- ⚠️ **LLMs can still generate plausible-sounding but incorrect information**
- ⚠️ **Human review is MANDATORY** - never trust AI output without verification

**Mitigation:**
- 95%+ citation accuracy (based on 4 production theses)
- Multi-agent verification (Skeptic, Verifier, Referee agents)
- 4-tier API fallback for citations (Crossref → Semantic Scholar → Gemini → LLM)
- **User responsibility:** Always fact-check claims against original sources

### 2. Research Paper Access

**Claim:** "200M+ research papers"

**Reality:**
- ✅ Access to 200M+ papers via API integrations (Semantic Scholar, arXiv, PubMed, Crossref)
- ⚠️ **Not all 200M papers are locally indexed** - accessed via public APIs
- ⚠️ **API rate limits** may affect search speed during peak usage
- ⚠️ **Not all papers have full-text access** - many are metadata-only
- ⚠️ **Paywalled papers** require institutional access or separate subscriptions

**What this means:**
- You can **search** 200M+ papers
- You can **access metadata** (titles, abstracts, citations) for most
- You may **not get full-text** for paywalled journals without separate access
- **Recency:** Paper databases update at different rates (arXiv: daily, Semantic Scholar: weekly)

### 3. Citation Verification Accuracy

**Performance:** 95% citation accuracy (based on 152 citations across 4 production theses)

**What this means:**
- ✅ Most citations (95%) are real, correctly formatted, and relevant
- ⚠️ **5% of citations may be incorrect, misformatted, or irrelevant**
- ⚠️ **You MUST verify all citations** before submission

**Common citation errors:**
- Wrong publication year (e.g., 2023 vs 2024)
- Incorrect page numbers
- Author name variations
- Outdated DOIs or URLs

**Best practice:** Check every citation against the original source.

### 4. Quality Variation by Field

**Performance varies significantly by academic discipline:**

**Strong performance (8.5-9.5/10):**
- ✅ Computer Science / AI / Machine Learning
- ✅ Business / Economics
- ✅ Education / Educational Technology
- ✅ General Science / Technology topics

**Moderate performance (7.0-8.5/10):**
- ⚠️ Social Sciences (Psychology, Sociology)
- ⚠️ Humanities (Literature, History, Philosophy)
- ⚠️ Interdisciplinary topics

**Limited performance (5.0-7.0/10):**
- ⚠️ Highly specialized medical research (e.g., clinical trials, pharmacology)
- ⚠️ Law / Legal research (case law, statutes)
- ⚠️ Pure Mathematics (theorem proofs, advanced topology)
- ⚠️ Niche regional topics (local history, minority languages)

**Reason:** Training data, API coverage, and agent specialization favor mainstream academic topics.

### 5. Up-to-Dateness Limitations

**Research database freshness:**

| Database | Update Frequency | Typical Lag |
|----------|------------------|-------------|
| arXiv | Daily | 1-2 days |
| Semantic Scholar | Weekly | 7-14 days |
| PubMed | Daily | 1-3 days |
| Crossref | Real-time (for new DOIs) | 0-24 hours |
| Google Scholar (via API limits) | Variable | Unknown |

**What this means:**
- ⚠️ **Very recent papers (last 1-2 weeks) may not appear in searches**
- ⚠️ **Breaking research developments** may not be captured
- ⚠️ **Conference papers** may lag behind preprints

**Best practice:** For cutting-edge topics, manually search arXiv and Google Scholar to supplement.

### 6. Language & Translation Limitations

**Supported languages:**
- ✅ **Full support:** English
- ⚠️ **Partial support:** German, Spanish, French (thesis generation works, quality may vary)
- ⚠️ **Limited support:** Other European languages
- ❌ **No support:** Non-Latin scripts (Arabic, Chinese, Japanese, etc.)

**Translation quality:**
- Research papers in non-English languages may be translated with lower accuracy
- Technical terminology may not translate perfectly
- Citations in non-English sources may have formatting issues

### 7. Originality & Creativity

**What AI can do:**
- ✅ Synthesize existing research
- ✅ Identify trends and gaps
- ✅ Organize and structure arguments
- ✅ Improve writing clarity

**What AI cannot do:**
- ❌ Generate truly novel hypotheses (requires human insight)
- ❌ Design original experiments (requires domain expertise)
- ❌ Provide ethical judgment or nuanced interpretation
- ❌ Replace critical thinking and scholarly rigor

**Bottom line:** AI is a **research assistant**, not a **researcher**. Original contribution must come from you.

### 8. Export Format Limitations

**Supported formats:**
- ✅ PDF (fully supported, production-ready)
- ✅ DOCX (Word - good compatibility with MS Word 2016+)
- ✅ LaTeX (requires local LaTeX distribution for compilation)

**Format-specific limitations:**
- **PDF:** No interactive elements, fixed layout
- **DOCX:** Complex equations may need manual adjustment, footnote/endnote placement varies by Word version
- **LaTeX:** Requires `pdflatex` or similar compiler, template customization needed for specific journal/university formats

**Compliance:**
- ⚠️ **University thesis formatting** may require manual adjustments (e.g., specific margins, title page layout)
- ⚠️ **Journal submission formats** often need tweaking (e.g., APA 7th vs 6th, reference style variations)
- ✅ Basic formatting (headings, paragraphs, citations) is production-ready

### 9. Processing Time & Resource Limits

**Generation time (20,000-word thesis):**
- ✅ **AI generation:** 20-25 minutes (average)
- ⚠️ **May be slower during:**
  - Peak API usage hours
  - Complex interdisciplinary topics
  - When fallback citation APIs are used
  - First-time setup (model loading)

**System requirements:**
- Python 3.9+ (3.11+ recommended)
- 8GB RAM minimum (16GB recommended for large theses)
- Internet connection (required for API calls)
- LLM API access (Gemini, Claude, or GPT)

**Cost limitations:**
- API costs vary by provider: $10-$35 per 20k-word thesis (Gemini 2.5)
- Free tier API limits may restrict usage (e.g., Gemini has daily quotas)

### 10. Known Technical Issues

**Current bugs/limitations (as of 2025-11-22):**

1. **Citation clustering not yet implemented** (planned v1.5.0)
2. **Multi-author collaboration features** not available (planned v1.6.0)
3. **Domain-specific agents** (medical, legal) not yet built (planned v2.0.0)
4. **Real authentication system** not implemented (currently mock auth)
5. **Row Level Security (RLS)** not active in database
6. **Rate limiting** not yet implemented (planned)

**Workarounds:**
- Use manual reference management for complex citation graphs
- Single-author workflow recommended for now
- General-purpose agents work across domains, but quality varies
- Run locally (no auth required)

---

## Transparency Commitments

### What We Track

✅ **We collect:**
- Usage statistics (thesis count, word count, generation time)
- Error logs (for debugging)
- Citation accuracy metrics

❌ **We do NOT collect:**
- Thesis content
- Personal information
- API keys
- User-identifiable data

### Performance Metrics (Real Data)

**From 4 production theses (111,665 words total):**
- **Generation time:** 18-25 min (avg 22 min)
- **Citation accuracy:** 95% (152 citations total)
- **Word count range:** 23,038 - 32,165 words
- **Quality score:** 8.5/10 average (self-reported)
- **Cost:** $10-$35 per thesis (Gemini 2.5)

**Sample size:** 181 test runs, 4 production theses

### Limitations We're Working On

**Roadmap priorities:**

**v1.4.0 (Dec 2025):**
- PyPI package for easier installation
- Enhanced documentation

**v1.5.0 (Jan 2026):**
- Citation clustering & impact scores
- Better quality metrics

**v1.6.0 (Feb 2026):**
- Multi-author collaboration support

**v2.0.0 (Q2 2026):**
- Domain-specific agents (medical, legal, etc.)
- Multilingual support improvements

---

## When to Use (and Not Use) This Tool

### ✅ Good Use Cases

1. **Master's thesis / PhD dissertation** (general topics)
2. **Literature review** (any academic field)
3. **Research paper drafts** (non-clinical)
4. **Essay writing support** (undergrad/grad level)
5. **Citation management** (organizing references)

### ⚠️ Use with Caution

1. **Highly specialized topics** (medical, legal, niche fields)
2. **Non-English theses** (quality may vary)
3. **Very recent research** (last 1-2 weeks)
4. **Topics requiring nuanced cultural interpretation**

### ❌ Do NOT Use For

1. **Clinical medical research** (risk of harm if errors)
2. **Legal briefs or case analysis** (requires legal expertise)
3. **Pure mathematics proofs** (requires rigorous formal verification)
4. **Work that violates your institution's AI policy**
5. **Submitting unedited AI output** (always review!)

---

## User Responsibility

**You are responsible for:**
- ✅ Verifying all citations
- ✅ Fact-checking all claims
- ✅ Ensuring compliance with institutional policies
- ✅ Understanding all content deeply
- ✅ Disclosing AI assistance when required
- ✅ Maintaining academic integrity

**We provide:**
- ✅ Tools to assist research and writing
- ✅ Transparent limitations documentation
- ✅ Ethical guidelines and best practices
- ✅ Technical support via GitHub issues

**We do NOT provide:**
- ❌ Guarantees of publication acceptance
- ❌ Academic advising or mentorship
- ❌ Institutional policy compliance verification
- ❌ Warranty of fitness for specific use cases

---

## Questions & Support

**If you encounter limitations:**
1. Check this document for known issues
2. Review [ETHICS.md](../ETHICS.md) for usage guidance
3. Consult [docs/guides/FAQ.md](guides/FAQ.md) for common questions
4. Open a GitHub issue for technical problems
5. Discuss with your advisor for academic guidance

**Reporting issues:**
- GitHub: https://github.com/federicodeponte/opendraft/issues
- Include: thesis topic, error messages, expected vs actual behavior
- Be specific about limitations you've encountered

---

## Final Note

This tool is **powerful but imperfect**. Understanding its limitations helps you use it effectively and responsibly.

**We believe in transparency over marketing hype.** If a feature doesn't work well, we'll tell you. If there's a limitation, we'll document it. If there's a better manual approach for your specific use case, we'll recommend it.

**Use this tool as a research assistant, not a replacement for scholarship.**

---

**Last Updated:** 2025-11-22
**Based on:** 4 production theses, 181 test runs, 111,665 words generated
**Transparency Level:** 100% - All metrics verifiable from real data

**Questions?** Read [ETHICS.md](../ETHICS.md) | [FAQ](guides/FAQ.md) | [GitHub Issues](https://github.com/federicodeponte/opendraft/issues)
