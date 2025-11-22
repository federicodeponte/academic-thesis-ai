# Frequently Asked Questions (FAQ)

Quick answers to common questions about OpenDraft.

---

## Getting Started

### Do I need to know how to code?

**No!** You need to:
- Copy/paste prompts from files
- Edit text in your IDE
- Run 1-2 simple Python commands

If you can use Google Docs, you can use this tool.

### Which AI should I use?

**For beginners:** Google Gemini (free tier, good quality)

**For important papers:** Claude Sonnet 4.5 (best quality, ~$20-50 per paper)

See [docs/API_KEYS.md](docs/API_KEYS.md) for detailed comparison.

### How much does this cost?

**Typical costs:**
- 6,000-word paper: $0-5 (Gemini) or $20-50 (Claude)
- Master's thesis (20k words): $10-20 (Gemini) or $50-100 (Claude)
- PhD dissertation (50k+ words): $50-100 (Gemini) or $100-300 (Claude)

Gemini has a generous free tier that covers 1-2 papers.

### What IDE should I use?

**Recommended:**
- **Cursor** - Best experience, built for AI
- **Claude Code** - Official Anthropic CLI
- **VS Code** - Free and popular

All three work great with this tool.

### Can I use this for my thesis?

**Check with your advisor first!**

Academic integrity varies by institution. Some considerations:
- Is AI-assisted writing allowed?
- Do you need to disclose AI use?
- What counts as "your own work"?

See [ETHICS.md](ETHICS.md) for guidelines.

---

## Usage

### How long does it take to write a paper?

**Typical timeline:**
- Literature review (20-50 papers): 2-4 hours
- Outline and structure: 30 minutes
- Writing all sections: 4-8 hours
- Validation and fact-checking: 2-3 hours
- Refinement and polish: 2-4 hours

**Total: 10-20 hours** (vs 2-3 months manually)

Real example: [67-page master's thesis in 10 days](tests/outputs/PRODUCTION_TEST_RESULTS.md)

### Do I have to use all 14 agents?

**No!** Use what you need.

**Minimum viable workflow (5 agents):**
1. Scout - Find papers
2. Scribe - Summarize papers
3. Architect - Create outline
4. Crafter - Write sections
5. Polish - Final improvements

Skip agents like Skeptic, Verifier, etc. if you're doing quick drafts.

### Can I write in languages other than English?

**Yes!** The AI can write in most major languages.

Just specify in your prompts: "Write in Spanish" or "Write in Mandarin"

Quality may vary - Claude and GPT-4 are best for non-English.

### Can I switch AI models mid-project?

**Yes!** Change `DEFAULT_LLM` in `.env.local` anytime.

Your progress is saved in markdown files, not tied to any specific AI.

### How do I know the AI isn't hallucinating facts?

**Use the validation agents:**
- **Skeptic** - Challenges claims and asks for evidence
- **Verifier** - Fact-checks statistical claims
- **Referee** - Validates citations against academic databases

The system includes a [citation verifier](utils/citation_verifier.py) that checks against CrossRef and arXiv.

**Always review AI output yourself!** You're responsible for accuracy.

---

## Technical

### What Python version do I need?

**Python 3.8 or higher**

Check your version:
```bash
python3 --version
```

### Do I need to install LaTeX?

**No!** This tool uses:
- **WeasyPrint** for PDFs (no LaTeX needed)
- **python-docx** for Word documents
- **Pandoc** (optional, for advanced formatting)

### What are MCP servers?

**MCP = Model Context Protocol**

MCP servers connect your AI to academic databases:
- **Semantic Scholar** - 200M+ papers across all fields
- **arXiv** - 2M+ STEM papers
- **PubMed** - 35M+ medical/biology papers
- **Google Scholar** - Billions of papers

**Do I need them?** No, but they make research MUCH faster.

**Setup:** Run `./mcp_servers/install_all.sh` (5 minutes)

### Can I run this offline?

**Partially:**
- Writing and editing: Yes (works offline)
- AI agents: No (requires internet to call APIs)
- PDF export: Yes (works offline)

You need internet to use the AI, but you can work offline between AI sessions.

### Where is my data stored?

**Everything is local:**
- Papers you download: `research/papers/`
- Your writing: `sections/` or wherever you save markdown
- Exports: `output/` or `examples/`

**Nothing is sent to cloud except:**
- Your prompts to AI APIs (Gemini/Claude/OpenAI)
- MCP requests to academic databases (if you use them)

Your thesis never leaves your computer except through these controlled API calls.

---

## Quality & Ethics

### Is the output plagiarism?

**No, but be careful:**

The AI generates original text based on your prompts. However:
- ✅ AI-generated text is not plagiarism (it's new text)
- ❌ Using AI might violate academic honesty policies
- ❌ Copying AI output without review/editing is lazy
- ✅ Using AI as a research/writing assistant is acceptable at most institutions

**Best practice:** Treat AI like a co-writer, not a ghost-writer.

### Will my professor know I used AI?

**Possibly.**

AI detection tools exist but are unreliable. Better approach:
- Disclose AI use if required by your institution
- Review and edit all AI output heavily
- Add your own analysis and insights
- Use AI as助手 (assistant), not replacement

See [ETHICS.md](ETHICS.md) for detailed guidelines.

### What quality can I expect?

**Typical output quality:**
- Gemini 2.5 Flash: B+ to A- (good for drafts)
- Gemini 2.5 Pro: A- to A (solid quality)
- Claude Sonnet 4.5: A- to A+ (best quality)

Real example: [67-page thesis graded A- (90/100)](examples/thesis_showcase.pdf)

**Quality depends on:**
- Your prompts (better prompts = better output)
- Your review/editing (AI is a starting point)
- Topic complexity (AI is better at some topics than others)

### Can I publish papers written with this?

**Maybe - check journal policies.**

Some journals:
- ✅ Allow AI-assisted writing (must disclose)
- ⚠️  Allow with restrictions (human must verify everything)
- ❌ Prohibit AI-generated content

**Always:**
- Review all AI output
- Verify all facts and citations
- Add your own analysis
- Disclose AI use if required

---

## Troubleshooting

### "API key invalid" error

**Check:**
1. Key is in `.env.local` (not `.env`)
2. No typos or extra spaces
3. Key starts with correct prefix:
   - Gemini: `AIzaSy...`
   - Claude: `sk-ant-...`
   - OpenAI: `sk-...`
4. Billing is set up (for Claude/OpenAI)

See [docs/API_KEYS.md](docs/API_KEYS.md#troubleshooting) for detailed help.

### "Module not found" error

**Solution:**
```bash
# Make sure you're in virtual environment
source venv/bin/activate  # Or: venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "Rate limit exceeded" error

**You hit usage limits.**

**Solutions:**
1. Wait a few minutes and try again
2. For Gemini free tier: Wait 24 hours or upgrade to paid
3. For Claude/OpenAI: Add more credit to account

### PDF export fails

**Common causes:**
1. WeasyPrint not installed: `pip install weasyprint`
2. Missing fonts: Install system fonts
3. Malformed markdown: Check for syntax errors

Try: `python -m weasyprint --help` to verify installation

### MCP servers not working

**Check:**
1. Node.js installed: `node --version` (need v18+)
2. MCP servers installed: `./mcp_servers/install_all.sh`
3. Config file exists: `.claude/mcp.json`

MCP servers are optional - you can use the tool without them.

---

## Advanced

### Can I customize the prompts?

**Yes!** All prompts are in `prompts/` directory.

Edit them to:
- Change writing style
- Focus on specific fields
- Add your institution's requirements
- Use different citation styles

### Can I add my own agents?

**Yes!** Create a new file in `prompts/`:

```markdown
# My Custom Agent

You are an expert in [domain].

[Instructions for what the agent should do]

[Input format]

[Output format]
```

Then use it like any other agent.

### Can I batch process multiple papers?

**Not built-in, but possible.**

You can write a simple script:
```python
topics = ["Topic 1", "Topic 2", "Topic 3"]
for topic in topics:
    # Call scout agent
    # Call scribe agent
    # etc.
```

See `tests/scripts/` for examples.

### Can I integrate with other tools?

**Yes!** The system is modular.

**Possible integrations:**
- Zotero (citation management)
- Overleaf (LaTeX editing)
- Notion (note-taking)
- GitHub (version control)

Everything is markdown files, so integration is straightforward.

---

## Billing & Costs

### How are API costs calculated?

**Charged per token (word ≈ 1.3 tokens):**

**Gemini:**
- Free tier: 1,500 requests/day
- Paid: $0.0001 per 1,000 tokens (very cheap)

**Claude:**
- $3 per million input tokens
- $15 per million output tokens

**OpenAI:**
- Varies by model
- GPT-4: ~$10 per million tokens

See API provider websites for current pricing.

### Can I set a spending limit?

**Yes!**

**Gemini:** Set quotas in Google Cloud Console

**Claude:** Set monthly limit at https://console.anthropic.com/settings/limits

**OpenAI:** Set hard limit at https://platform.openai.com/account/limits

**Recommended:** Start with $10-20 limit until you understand costs.

### What if I run out of credits mid-paper?

**Your progress is saved!**

All your work is in local markdown files. Just:
1. Add more credits
2. Continue where you left off

Nothing is lost.

---

## Community & Support

### How do I report bugs?

**GitHub Issues:** https://github.com/federicodeponte/opendraft/issues

Please include:
- What you tried to do
- What happened instead
- Error messages
- Your environment (OS, Python version)

### How do I request features?

**GitHub Discussions:** https://github.com/federicodeponte/opendraft/discussions

Or open a feature request issue.

### Can I contribute?

**Yes! Contributions welcome.**

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas that need help:
- Documentation improvements
- New agent prompts
- Bug fixes
- Test coverage
- Example papers

### Is there a community forum?

**Currently:**
- GitHub Discussions
- GitHub Issues

**Planned:**
- Discord server (coming soon)
- User showcase gallery

---

## Still Have Questions?

**Documentation:**
- [Setup Guide](00_START_HERE.md) - Getting started
- [API Keys](docs/API_KEYS.md) - Configuration help
- [Installation](docs/INSTALLATION.md) - Troubleshooting
- [README](README.md) - Full documentation

**Community:**
- [GitHub Issues](https://github.com/federicodeponte/opendraft/issues) - Bug reports
- [GitHub Discussions](https://github.com/federicodeponte/opendraft/discussions) - Q&A

**Can't find your answer?**

Open a GitHub Discussion - we're here to help!
