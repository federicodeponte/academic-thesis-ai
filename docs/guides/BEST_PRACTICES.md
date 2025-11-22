# Best Practices for Responsible AI-Assisted Academic Writing

**Academic Thesis AI** is designed to be a research assistant, not a replacement for scholarship. This guide helps you use AI responsibly while maintaining academic integrity.

**Based on:** 4 production theses and 111,665 words of generated content

---

## 📋 Table of Contents

1. [Core Principle](#core-principle)
2. [Working with Your Advisor](#1-working-with-your-advisor)
3. [Revising AI-Generated Drafts](#2-revising-ai-generated-drafts)
4. [Avoiding Plagiarism](#3-avoiding-plagiarism)
5. [When to Use AI vs When to Write Yourself](#4-when-to-use-ai-vs-when-to-write-yourself)
6. [Quality Control Checklist](#5-quality-control-checklist)
7. [Citation Verification Workflow](#6-citation-verification-workflow)
8. [Maintaining Academic Rigor](#7-maintaining-academic-rigor)
9. [Institutional Compliance](#8-institutional-compliance)
10. [When NOT to Use This Tool](#9-when-not-to-use-this-tool)
11. [Getting Help](#10-getting-help)

---

## Core Principle

> **AI is your research assistant, YOU are the author.**

You are responsible for every word in your thesis. AI can help you write faster, but you must understand, verify, and own all content.

---

## 1. Working with Your Advisor

### Choose the Right LLM

**For beginners / tight budget:**
- ✅ Google Gemini 2.5 Flash
- Cost: $10-20 per thesis
- Quality: B+ to A-
- Free tier: 1,500 requests/day

**For important submissions:**
- ✅ Anthropic Claude Sonnet 4.5
- Cost: $50-100 per thesis
- Quality: A- to A+
- Best citation accuracy

**Avoid:**
- ❌ Gemini 1.5 (outdated, lower quality)
- ❌ GPT-3.5 (too generic for academic writing)
- ❌ Mixing LLMs mid-thesis (inconsistent style)

**Best practice:** Start with Gemini for drafts, use Claude for final version.

---

### Define Your Topic Clearly

**Good topics (specific, researchable):**
- ✅ "AI-driven dynamic pricing models in SaaS companies (2020-2025)"
- ✅ "Impact of renewable energy policies on CO2 emissions in Germany"
- ✅ "Machine learning applications in cancer diagnosis: A systematic review"

**Bad topics (too broad, vague):**
- ❌ "Artificial intelligence"
- ❌ "Climate change"
- ❌ "Healthcare technology"

**Template:**
```
Topic: [Specific subject] + [Scope/constraint] + [Time period/region]
Example: "Pricing strategies for agentic AI systems in enterprise markets (2023-2025)"
```

---

### Set Realistic Expectations

**What the AI CAN do well:**
- ✅ Literature review (50+ papers in 2-3 hours)
- ✅ Outline structure (perfect academic formatting)
- ✅ First drafts (80-90% complete)
- ✅ Citation research (95%+ success rate)
- ✅ Consistent writing style

**What the AI STRUGGLES with:**
- ⚠️ Original insights (you must add these)
- ⚠️ Nuanced arguments (requires human review)
- ⚠️ Niche topics (< 10 papers available)
- ⚠️ Recent events (< 3 months old)
- ⚠️ Interdisciplinary synthesis (needs guidance)

**Rule of thumb:** AI gets you 80-90% there. You provide the final 10-20%.

---

## 🔍 Research Phase

### Scout Agent: Research Planning

**Best practices:**
1. **Be specific about scope**
   ```
   Good: "Focus on peer-reviewed journals from 2020-2025"
   Bad: "Find papers about AI"
   ```

2. **Specify databases**
   ```
   Good: "Search Semantic Scholar and arXiv for STEM papers"
   Bad: "Search the internet"
   ```

3. **Limit breadth**
   ```
   Good: "3-5 key themes"
   Bad: "Everything related to my topic"
   ```

**Expected output:** Research plan with 3-5 themes, 10-15 search queries

---

### Scribe Agent: Literature Review

**Best practices:**
1. **Quality over quantity**
   - ✅ 20-30 high-quality papers
   - ❌ 100+ mediocre papers

2. **Prioritize recent papers**
   ```
   Ideal: 70% from last 5 years, 30% foundational classics
   ```

3. **Verify papers exist**
   - Check DOIs with Verifier agent
   - Flag missing papers immediately

**Expected output:** 5,000-8,000 word literature review with 30-50 citations

---

### Signal Agent: Citation Discovery

**Best practices:**
1. **Use multiple databases**
   - Crossref (broad coverage)
   - Semantic Scholar (ML/CS papers)
   - arXiv (preprints)
   - PubMed (medical/biology)

2. **Verify citation metadata**
   ```python
   Required fields:
   - Title
   - Authors
   - Year
   - DOI or URL
   - Publication venue
   ```

3. **Flag hallucinated citations**
   - Check if DOI resolves
   - Verify author names
   - Confirm publication venue exists

**Expected output:** 40-60 verified citations with complete metadata

---

## ✍️ Writing Phase

### Architect Agent: Structure Design

**Best practices:**
1. **Follow field conventions**
   - STEM: IMRaD (Introduction, Methods, Results, Discussion)
   - Humanities: Thematic chapters
   - Social sciences: Mixed

2. **Balance section lengths**
   ```
   Introduction: 10-15%
   Literature review: 20-25%
   Methodology: 15-20%
   Results/Analysis: 30-35%
   Discussion: 10-15%
   Conclusion: 5-10%
   ```

3. **Plan for 20,000-30,000 words**
   - Undergrad thesis: 15,000-20,000
   - Master's thesis: 20,000-30,000
   - PhD dissertation: 50,000-80,000

**Expected output:** Detailed outline with 5-8 chapters, 15-25 subsections

---

### Crafter Agent: Section Writing

**Best practices:**
1. **Write in iterations**
   - First pass: Rough draft (fast, don't edit)
   - Second pass: Structure review
   - Third pass: Polish

2. **Maintain consistent voice**
   ```
   Academic tone:
   ✅ "This study examines..."
   ❌ "Let's look at..."

   ✅ "Results indicate..."
   ❌ "I think the results show..."
   ```

3. **Include transitions**
   - Between paragraphs
   - Between sections
   - Between chapters

**Expected output:** 15,000-25,000 words (first draft)

---

### Thread Agent: Coherence Checking

**Best practices:**
1. **Check logical flow**
   - Does each paragraph connect to the next?
   - Are transitions smooth?
   - Is the argument progressive?

2. **Eliminate contradictions**
   - Flag opposing claims
   - Reconcile or explain discrepancies

3. **Verify consistency**
   - Terminology
   - Abbreviations
   - Citation style

**Expected output:** Marked-up draft with coherence issues flagged

---

## ✅ Quality Assurance

### Skeptic Agent: Fact-Checking

**Best practices:**
1. **Challenge every claim**
   - Is this statement supported by citations?
   - Are statistics accurate?
   - Are interpretations valid?

2. **Flag weasel words**
   - "Some studies suggest..." → Which studies?
   - "It is widely believed..." → By whom?
   - "Recent research shows..." → Which papers?

3. **Verify numbers**
   - Recalculate percentages
   - Check sample sizes
   - Confirm dates

**Expected output:** List of unsupported claims with suggested fixes

---

### Verifier Agent: Citation Validation

**Best practices:**
1. **Check EVERY citation**
   - Does DOI resolve?
   - Do authors match?
   - Is year correct?
   - Does title match?

2. **Use automated tools**
   ```bash
   python utils/citation_verifier.py --input thesis.md
   ```

3. **Target 95%+ success rate**
   - 40 citations → max 2 errors
   - 60 citations → max 3 errors

**Expected output:** Validation report with pass/fail for each citation

---

### Referee Agent: Peer Review Simulation

**Best practices:**
1. **Review as if you're a journal editor**
   - Is the contribution novel?
   - Are methods sound?
   - Are conclusions supported?

2. **Check against rubric**
   - Originality: 20%
   - Methodology: 25%
   - Analysis: 25%
   - Writing quality: 15%
   - Citations: 15%

3. **Provide actionable feedback**
   ```
   Good: "Section 3.2 lacks evidence for claim X. Add citations from Y and Z."
   Bad: "Section 3.2 needs improvement."
   ```

**Expected output:** Detailed review with scores and improvement suggestions

---

## 💰 Cost Optimization

### Minimize API Costs

**Strategy 1: Use Free Tier**
- Gemini 2.5 Flash: 1,500 requests/day (free)
- Covers: 1-2 full theses per month
- Best for: Students, experiments

**Strategy 2: Batch Operations**
```python
# Bad: 50 separate API calls
for paper in papers:
    summarize(paper)  # 50 calls × $0.01 = $0.50

# Good: 1 batched API call
summarize_batch(papers)  # 1 call × $0.05 = $0.05
```

**Strategy 3: Cache Results**
- Save Scout research plan → reuse for multiple drafts
- Save Scribe summaries → don't regenerate
- Save Signal citations → update incrementally

**Strategy 4: Progressive Quality**
```
Draft 1: Gemini 2.5 Flash ($10)
Draft 2: Gemini 2.5 Flash ($5 for revisions)
Final: Claude Sonnet 4.5 ($50 for polish)
Total: $65 (vs $100 if using Claude throughout)
```

---

### Monitor Spending

**Set hard limits:**
```bash
# Gemini
gcloud alpha billing budgets create \
  --billing-account=[ACCOUNT] \
  --display-name="Thesis Budget" \
  --budget-amount=50

# Claude
# Set at https://console.anthropic.com/settings/limits
Monthly limit: $100

# OpenAI
# Set at https://platform.openai.com/account/limits
Hard limit: $50
```

**Track costs per phase:**
```
Research (Scout + Scribe + Signal): $5-10
Structure (Architect + Formatter): $1-2
Writing (Crafter + Thread + Narrator): $10-20
QA (Skeptic + Verifier + Referee): $5-10
Polish (Voice + Entropy + Polish): $2-5
Total: $23-47
```

---

## 🎓 Academic Integrity

### Disclosure & Attribution

**When to disclose AI use:**
1. ✅ If your institution requires it
2. ✅ If submitting to a journal
3. ✅ If presenting at a conference
4. ✅ When in doubt

**How to disclose:**
```markdown
## Acknowledgments

This thesis was written with assistance from Academic Thesis AI,
an open-source tool that uses large language models to support
academic research and writing. All AI-generated content was
reviewed, verified, and edited by the author. Citations were
validated against academic databases.
```

**In your methods section:**
```markdown
## AI Assistance

Literature review and initial drafts were supported by Academic
Thesis AI (version 1.3.1), which queries academic databases
(Crossref, Semantic Scholar, arXiv) and uses Google Gemini 2.5
Flash for text generation. All outputs were manually reviewed
and fact-checked by the author.
```

---

### Add Your Own Analysis

**AI provides structure. You provide insights.**

**Example:**

**AI draft (80%):**
> "Results show a 15% increase in efficiency. This is significant."

**Your revision (100%):**
> "Results show a 15% increase in efficiency (p < 0.05), which
> is statistically significant and aligns with findings from
> Zhang et al. (2023). However, this contradicts earlier work
> by Kumar (2021), possibly due to differences in sample size
> and methodology. The practical implications suggest..."

**What you added:**
- Statistical significance
- Comparison to prior work
- Critical analysis
- Practical implications

---

### Verify Everything

**The "Trust but Verify" checklist:**

- [ ] **Citations:** All DOIs resolve correctly
- [ ] **Statistics:** Recalculated and confirmed
- [ ] **Quotes:** Checked against original sources
- [ ] **Methods:** Feasible and correctly described
- [ ] **Results:** Internally consistent
- [ ] **Conclusions:** Supported by evidence
- [ ] **References:** Properly formatted (APA/MLA/Chicago)

**If you can't verify it, don't include it.**

---

## ⚠️ Common Pitfalls

### Pitfall 1: Accepting First Draft

**Problem:** AI generates 20k words. You submit without review.

**Why it's bad:**
- Hallucinated citations (5-10%)
- Logical inconsistencies
- Missing your unique insights
- Violates academic integrity

**Solution:**
1. Review every section
2. Verify all citations
3. Add your own analysis
4. Run through QA agents

**Time investment:** 10-20 hours review (vs 0 hours)

---

### Pitfall 2: Vague Prompts

**Problem:** "Write about AI"

**Why it's bad:**
- Generic, unfocused output
- Low-quality citations
- Wasted API costs

**Solution:** Use specific prompts
```
Good prompt:
"Write a 5,000-word literature review on dynamic pricing models
in SaaS companies, focusing on AI-driven approaches from 2020-2025.
Include 20-30 citations from peer-reviewed journals and industry
reports. Structure: Overview, Traditional models, AI innovations,
Case studies, Future trends."

Bad prompt:
"Write about AI pricing"
```

---

### Pitfall 3: Ignoring Field Conventions

**Problem:** Using STEM structure for humanities thesis

**Why it's bad:**
- Reviewers expect field-specific formats
- Violates journal submission guidelines
- Appears unprofessional

**Solution:** Research your field's norms
```
STEM: IMRaD (Introduction, Methods, Results, Discussion)
Humanities: Thematic chapters, narrative flow
Social Sciences: Mixed (theory → methods → findings → discussion)
Business: Problem → Analysis → Solution → Recommendation
```

---

### Pitfall 4: Over-reliance on AI

**Problem:** AI writes 100%, you do 0% thinking

**Why it's bad:**
- No original contribution
- Ethical violations
- Poor quality (AI can't do deep analysis)

**Solution:** 80/20 rule
```
AI contribution: 80% (structure, citations, drafts)
Your contribution: 20% (insights, analysis, critique)
```

**Your 20% is the most valuable part.**

---

### Pitfall 5: Not Checking Citations

**Problem:** Assuming all 50 citations are correct

**Why it's bad:**
- 5-10% hallucination rate → 2-5 fake citations
- Academic misconduct if discovered
- Damages credibility

**Solution:** Verify EVERY citation
```bash
# Automated verification
python utils/citation_verifier.py --input thesis.md

# Manual spot-checks
- Check 10 random DOIs
- Verify author names
- Confirm publication venues
```

---

## 🚀 Advanced Tips

### Tip 1: Iterative Refinement

**Don't aim for perfection on first pass.**

**Workflow:**
```
Pass 1: Gemini Flash → Rough draft (fast, cheap)
Pass 2: Review + edit → Fix major issues
Pass 3: Gemini Flash → Rewrite weak sections
Pass 4: Review + edit → Add your insights
Pass 5: Claude Sonnet → Final polish (slow, expensive)
```

**Cost:** $15 (Gemini) + $50 (Claude) = $65 total
**vs:** $150 if using Claude for everything

---

### Tip 2: Use Version Control

**Track changes with Git:**
```bash
git init
git add thesis.md
git commit -m "Initial draft from Crafter agent"

# After each revision
git commit -m "Added analysis to Section 3.2"
git commit -m "Fixed citations from Verifier feedback"
```

**Benefits:**
- Revert to earlier versions
- Track progress over time
- Recover from mistakes

---

### Tip 3: Create Custom Agents

**Add domain-specific expertise:**

**Example: Medical AI Agent**
```markdown
# Medical Fact-Checker Agent

You are a medical fact-checker with expertise in clinical research.

**Task:** Review medical claims in the thesis and verify:
1. Drug dosages (are they within therapeutic ranges?)
2. Medical terminology (correct usage?)
3. Clinical trial citations (properly referenced?)
4. Statistical significance (appropriate tests used?)

**Flag:**
- Unsubstantiated medical claims
- Incorrect terminology
- Missing ethical considerations
```

**Save as:** `prompts/medical_fact_checker.md`

---

### Tip 4: Batch Process Multiple Theses

**For researchers writing multiple papers:**

```python
# batch_thesis_generator.py
topics = [
    "AI pricing models in SaaS",
    "Machine learning in healthcare",
    "Climate change policy effectiveness"
]

for topic in topics:
    # Generate research plan
    scout_result = run_agent("scout", topic)

    # Generate literature review
    scribe_result = run_agent("scribe", scout_result)

    # Generate full thesis
    thesis = run_full_workflow(topic, scout_result, scribe_result)

    # Save output
    save_thesis(f"output/{topic.replace(' ', '_')}.md", thesis)
```

**Cost savings:** Reuse Scout results across related topics

---

### Tip 5: Integrate with Zotero

**Export citations to Zotero:**

```python
# utils/export_to_zotero.py
import json

def export_citations(thesis_file, zotero_library):
    citations = extract_citations(thesis_file)

    for citation in citations:
        zotero_library.add_item({
            "itemType": "journalArticle",
            "title": citation["title"],
            "creators": parse_authors(citation["authors"]),
            "date": citation["year"],
            "DOI": citation["doi"]
        })
```

**Benefits:**
- Centralized citation management
- Easy re-use across papers
- Integration with Word/LaTeX

---

## 📊 Quality Metrics

**Aim for these targets:**

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Citation Success** | 95%+ | `python utils/citation_verifier.py` |
| **Word Count** | 20,000-30,000 | `wc -w thesis.md` |
| **Readability** | Grade 14-16 | Flesch-Kincaid score |
| **Originality** | 20%+ | Your unique insights |
| **Review Time** | 10-20 hours | Time log |
| **Cost** | < $50 | API usage tracking |

---

## ✅ Final Checklist

Before submitting your thesis:

**Content:**
- [ ] All citations verified (95%+ success rate)
- [ ] Your own analysis added (20%+ of content)
- [ ] Logical flow checked (Thread agent)
- [ ] Facts verified (Skeptic agent)
- [ ] Peer review completed (Referee agent)

**Format:**
- [ ] Citation style consistent (APA/MLA/Chicago)
- [ ] Formatting correct (margins, fonts, spacing)
- [ ] Figures/tables numbered
- [ ] References properly formatted

**Ethics:**
- [ ] AI use disclosed (if required)
- [ ] All sources attributed
- [ ] Originality verified (no plagiarism)
- [ ] Advisor approval obtained

**Technical:**
- [ ] Exported to required format (PDF/Word/LaTeX)
- [ ] File size < 20MB (if submitting online)
- [ ] Metadata complete (title, author, date)
- [ ] Backup saved (version control)

---

## 📚 Additional Resources

**Documentation:**
- [FAQ](FAQ.md) - Common questions
- [Architecture](../architecture/) - How agents work
- [Ethics Guide](../../ETHICS.md) - Responsible use

**Community:**
- [GitHub Discussions](https://github.com/federicodeponte/academic-thesis-ai/discussions)
- [Best Thesis Examples](../../examples/GALLERY.md)

---

**Last Updated:** 2025-11-22
**Based on:** 4 production theses, 111,665 words generated, real user feedback

**For comprehensive responsible usage guidance, see:**
- [Full Best Practices Guide](#) - This document
- [ETHICS.md](../../ETHICS.md) - Academic integrity guidelines
- [LIMITATIONS.md](../LIMITATIONS.md) - Transparent system capabilities
- [TERMS_OF_SERVICE.md](../../TERMS_OF_SERVICE.md) - Legal responsibilities
