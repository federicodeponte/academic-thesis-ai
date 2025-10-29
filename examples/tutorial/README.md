# Academic Thesis AI - Step-by-Step Tutorial

**Goal:** Learn how to write your first academic paper section using AI agents

**Time:** 30-60 minutes

**Prerequisites:**
- Academic Thesis AI installed (`./setup.sh`)
- API key configured (Claude, GPT, or Gemini)
- Basic familiarity with your IDE (Cursor or Claude Code)

---

## Tutorial Overview

In this tutorial, you'll:
1. Search for papers on a topic (Scout Agent)
2. Summarize a key paper (Scribe Agent)
3. Write an introduction section (Crafter Agent)
4. Polish your writing (Polish Agent)
5. Export to PDF

**Topic:** "AI in Education" (feel free to substitute your own topic)

---

## Step 1: Find Papers with Scout Agent (5-10 min)

### What You'll Do
Use the Scout Agent to find 10 relevant papers.

### Instructions

1. **Open the Scout Agent prompt:**
   ```bash
   # In your IDE
   open prompts/01_research/scout.md
   ```

2. **Read the prompt template** - It shows you exactly what to paste in your AI chat

3. **Customize the search request:**
   - Replace `[YOUR TOPIC]` with "artificial intelligence in education"
   - Replace `[NUMBER]` with "10"
   - Specify databases: "arXiv and Semantic Scholar"

4. **Paste into your AI chat** (Claude Code / Cursor)

5. **Expected Output:**
   ```
   1. Paper Title (Author, Year) - DOI: xxx
      Summary: [1-2 sentences]
      Relevance: 9/10

   2. [...]
   ```

6. **Save the output** to `examples/tutorial/01_scout_output.md`

### Tips
- If you get < 10 papers, broaden your search terms
- Look for papers with relevance scores 7+/10
- Note which papers seem most interesting

---

## Step 2: Deep Dive with Scribe Agent (10-15 min)

### What You'll Do
Pick ONE interesting paper from Step 1 and get a detailed summary.

### Instructions

1. **Choose a paper** from your Scout results (pick relevance score 8+)

2. **Open the Scribe Agent prompt:**
   ```bash
   open prompts/01_research/scribe.md
   ```

3. **Provide paper details:**
   - Title: [from Scout output]
   - Authors: [from Scout output]
   - DOI: [from Scout output]

4. **Paste and run** in your AI chat

5. **Expected Output:**
   - **Research Questions:** What the paper investigates
   - **Methodology:** How they did it
   - **Key Findings:** What they discovered
   - **Limitations:** Study weaknesses

6. **Save** to `examples/tutorial/02_scribe_output.md`

### What to Notice
- How the agent structures information (RQ, methods, findings, limitations)
- Direct quotes with page numbers
- Critical assessment of limitations

---

## Step 3: Write Your Introduction with Crafter Agent (15-20 min)

### What You'll Do
Use the Crafter Agent to write a 500-word introduction section.

### Instructions

1. **Gather your research notes:**
   - Scout output (list of papers)
   - Scribe output (deep summary)
   - Your own thoughts on the topic

2. **Open the Crafter Agent prompt:**
   ```bash
   open prompts/03_compose/crafter.md
   ```

3. **Fill in the template:**
   ```
   SECTION TO WRITE: Introduction

   CONTEXT:
   - Topic: AI in Education
   - Purpose: Introduce how AI is transforming learning
   - Target length: 500 words
   - Style: Academic, accessible
   - Include: Hook, background, research gap, paper purpose

   RESEARCH NOTES:
   [Paste your Scout and Scribe summaries here]

   INSTRUCTIONS:
   - Start with an engaging hook about education's future
   - Provide background on AI in education (cite 3-4 papers)
   - Identify what's missing in current research
   - State the purpose of this paper
   - Use APA 7th edition citations
   ```

4. **Run the agent**

5. **Review the output:**
   - Is it the right length (~500 words)?
   - Does it have proper citations?
   - Does it flow logically?

6. **Save** to `examples/tutorial/03_intro_draft.md`

### What You'll Learn
- How to provide effective context to the agent
- The importance of good research notes
- How to guide tone and style

---

## Step 4: Polish with Polish Agent (5-10 min)

### What You'll Do
Improve the introduction's grammar, flow, and academic tone.

### Instructions

1. **Open the Polish Agent prompt:**
   ```bash
   open prompts/05_refine/polish.md
   ```

2. **Paste your introduction** from Step 3

3. **Specify what to polish:**
   ```
   FOCUS AREAS:
   - Grammar and punctuation
   - Sentence variety
   - Transition smoothness
   - Academic tone (not too formal, not too casual)
   - Clear, concise language
   ```

4. **Run the agent**

5. **Compare before/after:**
   - What changed?
   - Is it clearer?
   - Does it sound more professional?

6. **Save** to `examples/tutorial/04_intro_polished.md`

### Tips
- Don't over-polish - keep some personality
- Make sure it still sounds like YOU
- Check that citations weren't removed

---

## Step 5: Export to PDF (5 min)

### What You'll Do
Convert your polished introduction to a professional PDF.

### Instructions

1. **Create a markdown file** with proper formatting:
   ```bash
   # examples/tutorial/my_first_section.md
   ```

   Add this content:
   ```markdown
   # AI in Education: A New Frontier

   **Author:** [Your Name]
   **Institution:** [Your University]
   **Date:** [Today's Date]

   ---

   ## Introduction

   [Paste your polished introduction here]

   ---

   ## References

   [Add your citations in APA format]
   ```

2. **Export to PDF:**
   ```bash
   python utils/export_professional.py \
       examples/tutorial/my_first_section.md \
       --pdf examples/tutorial/my_first_section.pdf \
       --title "AI in Education" \
       --author "Your Name" \
       --institution "Your University"
   ```

3. **Open the PDF** and admire your work!

### What You Created
- A publication-quality PDF
- With proper academic formatting
- Professional typography
- Page numbers and margins

---

## Next Steps

### You've Learned:
✅ How to find papers (Scout Agent)
✅ How to analyze papers (Scribe Agent)
✅ How to write sections (Crafter Agent)
✅ How to polish writing (Polish Agent)
✅ How to export to PDF

### Try This Next:

**Write a Full Paper:**
1. Use all 14 agents in sequence
2. Follow `prompts/00_WORKFLOW.md`
3. Build a complete 5,000-word paper

**Explore Other Agents:**
- **Signal Agent** - Find research gaps
- **Architect Agent** - Design paper structure
- **Skeptic Agent** - Critical review
- **Referee Agent** - Simulate peer review
- **Entropy Agent** - Make writing more natural

**Try Different Templates:**
- Literature review: `examples/templates/literature_review.md`
- Empirical study: `examples/templates/empirical_study.md`
- Theoretical paper: `examples/templates/theoretical_paper.md`

---

## Troubleshooting

**"Scout Agent didn't find papers"**
- Check your API key is configured
- Try broader search terms
- Make sure MCP servers are installed (`./mcp_servers/install_all.sh`)

**"Crafter Agent output is too generic"**
- Provide more detailed research notes
- Be specific about tone and style
- Include examples of what you want

**"PDF export failed"**
- Check Pandoc is installed: `which pandoc`
- Try different engine: `--engine libreoffice`
- Verify markdown file exists and is valid

**"Citations are wrong"**
- Use Verifier Agent: `prompts/04_validate/verifier.md`
- Double-check DOIs and author names
- Format manually in APA 7th edition if needed

---

## Resources

- **Full Workflow:** `prompts/00_WORKFLOW.md`
- **All Agent Prompts:** `prompts/` directory
- **Templates:** `examples/templates/`
- **Ethics Guide:** `ETHICS.md`
- **Test Examples:** `tests/outputs/real_thesis/`

---

**🎉 Congratulations!**

You've completed your first AI-assisted academic writing project. You now know the core workflow and can apply it to any research topic.

**Remember:** AI assists, YOU are the author. Always verify claims, check citations, and add your own insights.

---

**Questions or Issues?**
- Check `README.md` for documentation
- Review `ETHICS.md` for responsible use
- Open an issue on GitHub if you find bugs

Happy writing! 📚✨
