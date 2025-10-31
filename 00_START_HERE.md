# Welcome to Academic Thesis AI! 👋

**First time here? You're in the right place.**

This tool helps you write academic papers 50-70% faster using AI assistants. Think of it as having 14 research assistants helping you write.

---

## What You'll Do in the Next 10 Minutes

1. **Understand** what this tool does (2 min) → Section 1 below
2. **Set up** your API key (5 min) → Section 2 below
3. **Test** that it works (3 min) → Section 3 below

Then you'll be ready for the [30-minute tutorial](examples/tutorial/README.md)!

---

## 1. What Is This? (2 min read)

### The Problem
Writing academic papers is slow and tedious. You spend weeks:
- Finding and reading 20-50 papers
- Taking notes and organizing ideas
- Writing and rewriting sections
- Formatting citations
- Polishing language

### The Solution
This tool provides 14 specialized AI agents that help with each step:

```
You type prompts → AI helps research/write → You review/edit → Export to PDF
```

**Examples of what it does:**
- **Scout Agent**: Finds 20-50 relevant papers in minutes
- **Scribe Agent**: Summarizes papers and extracts key findings
- **Crafter Agent**: Drafts sections in academic style
- **Skeptic Agent**: Fact-checks claims and validates citations
- **Polish Agent**: Improves writing quality and flow

### What It Doesn't Do
- ❌ Write your entire paper without your input
- ❌ Replace critical thinking
- ❌ Submit work without your review

**You're still in control.** The AI assists, you decide.

### How It Works

```
┌─────────────────────────────────────────────────────┐
│  Your IDE (Cursor, Claude Code, VS Code)           │
│  ┌───────────────────────────────────────────────┐ │
│  │  You: Paste prompt from prompts/01_scout.md  │ │
│  │  AI: Searches academic databases              │ │
│  │  AI: Returns 20 relevant papers               │ │
│  │  You: Review and select papers                │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │  You: Paste prompt from prompts/02_scribe.md │ │
│  │  AI: Summarizes selected papers               │ │
│  │  You: Review summaries                        │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  ... and so on through 14 agents                   │
└─────────────────────────────────────────────────────┘
```

**This is NOT a web app.** You work directly in your coding IDE.

---

## 2. Setup (5 minutes)

### Prerequisites
- **Python 3.8+** (check: `python3 --version`)
- **IDE**: Cursor, Claude Code, or VS Code
- **1 API key** from Google/Anthropic/OpenAI (we'll get this next)

### Step 1: Clone & Install

```bash
# Clone this repository
git clone https://github.com/federicodeponte/academic-thesis-ai.git
cd academic-thesis-ai

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get a FREE API Key (5 minutes)

**👉 Follow this guide: [docs/API_KEYS.md](docs/API_KEYS.md)**

**Quick recommendation:** Start with **Google Gemini** (free tier, good quality)

**Cost estimates:**
- 6,000-word paper: $0-5 (Gemini) or $20-50 (Claude)
- Master's thesis: $10-20 (Gemini) or $50-100 (Claude)

### Step 3: Configure Your API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API key
# For Gemini: GOOGLE_API_KEY=your-key-here
# For Claude: ANTHROPIC_API_KEY=your-key-here
# For GPT: OPENAI_API_KEY=your-key-here
```

**Using .env.local (recommended):**
```bash
# Create .env.local for your real API key
# This file is gitignored so your key stays private
cp .env.example .env.local
# Edit .env.local and add your API key
```

---

## 3. Test It Works (3 minutes)

Run this command to verify your setup:

```bash
python examples/quick_test.py
```

**Expected output:**
```
🧪 Testing Academic Thesis AI Setup...

✅ All packages installed
✅ API key valid
✅ MCP servers configured

🎉 Setup successful!

Next step: Try the tutorial
→ examples/tutorial/README.md
```

**If you see errors:**
- API key invalid → Check [docs/API_KEYS.md](docs/API_KEYS.md)
- Import errors → Check [docs/INSTALLATION.md](docs/INSTALLATION.md)
- Other issues → See [FAQ.md](FAQ.md)

---

## 4. Next Steps

### ✅ Setup worked? Great! Choose your path:

**Path A: 30-Minute Tutorial (Recommended for First-Timers)**

👉 **[examples/tutorial/README.md](examples/tutorial/README.md)**

What you'll learn:
- How to use agents in your IDE
- Write your first introduction section
- Export to PDF
- Basic workflow

**Path B: Dive Into Full Workflow (For the Ambitious)**

👉 **[prompts/00_WORKFLOW.md](prompts/00_WORKFLOW.md)**

Complete 17-step process:
- Deep literature review
- Full paper structure
- All sections written
- Validation & fact-checking
- Professional export

**Path C: Explore on Your Own**

👉 **[README.md](README.md)**

Browse:
- All 14 agent descriptions
- Feature documentation
- Example outputs
- Troubleshooting

---

## Need Help?

### Documentation
- **Setup problems?** → [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **API key questions?** → [docs/API_KEYS.md](docs/API_KEYS.md)
- **General questions?** → [FAQ.md](FAQ.md)
- **How does it work?** → [README.md](README.md)

### Community & Support
- **Bug reports:** [GitHub Issues](https://github.com/federicodeponte/academic-thesis-ai/issues)
- **Feature requests:** [GitHub Discussions](https://github.com/federicodeponte/academic-thesis-ai/discussions)
- **Ethical guidelines:** [ETHICS.md](ETHICS.md)

### Quick Links
- [Examples Directory](examples/) - Sample outputs
- [Prompts Directory](prompts/) - All 14 agent prompts
- [Contributing Guide](CONTRIBUTING.md) - Help improve this project

---

## Success Stories

**"Wrote my master's thesis in 10 days instead of 3 months"** - See [tests/outputs/PRODUCTION_TEST_RESULTS.md](tests/outputs/PRODUCTION_TEST_RESULTS.md)

**Real output:** [67-page thesis PDF](examples/thesis_showcase.pdf)
- 14,567 words
- 66 verified citations
- Publication-ready quality
- Grade: A- (90/100)

---

## Ready to Start?

**Step 1:** Get your API key → [docs/API_KEYS.md](docs/API_KEYS.md)

**Step 2:** Run the test → `python examples/quick_test.py`

**Step 3:** Start the tutorial → [examples/tutorial/README.md](examples/tutorial/README.md)

---

**Questions?** Read the [FAQ](FAQ.md) or check [full documentation](README.md).

**Good luck with your paper!** 🎓
