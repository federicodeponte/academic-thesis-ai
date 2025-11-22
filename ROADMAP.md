# Project Roadmap

**Last Updated:** November 20, 2025
**Current Version:** 1.3.1
**Status:** 🟢 Active Development

This roadmap shows our plans for the next 6-12 months. Priorities may shift based on community feedback and contributions.

---

## 🎯 Vision

Build the world's most comprehensive open-source framework for AI-assisted academic writing, making high-quality research accessible to everyone.

---

## ✅ Recent Releases

### v1.3.1 (Nov 2025) - Production-Grade Reliability
- ✅ Automatic error recovery with retry mechanism
- ✅ Parallel thesis generation (4 theses in 30 min)
- ✅ Enhanced scraper reliability (3 auto-retries)
- ✅ 70 comprehensive unit tests (100% pass rate)
- ✅ Production validation with zero manual intervention

### v1.3.0 (Nov 2025) - Deep Research Mode
- ✅ Autonomous research planning (50+ systematic queries)
- ✅ Smart query routing for source diversity
- ✅ 95%+ citation success rate (4-tier API fallback)
- ✅ 152 citations across 4 example theses

### v1.2.0 (Nov 2025) - Agent #15 Stability
- ✅ Fixed table corruption issues
- ✅ Output sanitization (meta-comment removal)
- ✅ File bloat prevention
- ✅ PDF rendering fixes

---

## 🚀 Upcoming Releases

### v1.4.0 (Dec 2025) - Production Packaging [IN PROGRESS]

**Goal:** Make the project truly production-ready for open source release

**Status:** 🟡 Phase 1 Complete (5/5 critical blockers), Phase 2 In Progress

#### Phase 1: Critical Blockers ✅ COMPLETE
- [x] Package distribution (pyproject.toml, pip install)
- [x] Installation verification CLI
- [x] Comprehensive CI/CD (testing, linting, security)
- [x] Security contact (SECURITY.md)
- [x] Code cleanup (TODO audit - 0 actual markers found!)

#### Phase 2: High Priority 🔄 IN PROGRESS
- [x] QUICKSTART.md updated with pip installation
- [x] Privacy/telemetry disclosure in README
- [x] Improved CONTRIBUTING.md for beginners
- [x] Response time commitments documented
- [x] ROADMAP.md created (this file!)
- [ ] Reorganize documentation (23 root .md files → docs/ structure)
- [ ] Clarify license for example outputs

#### Phase 3: Polish & Marketing 📋 PLANNED
- [ ] Performance benchmarks in README
- [ ] Competitive analysis (vs Jenni.ai, Scholarcy, Elicit)
- [ ] Docker image published to Docker Hub
- [ ] Video demo or GIF walkthrough
- [ ] Test coverage and build status badges
- [ ] CITATION.cff for academic citations
- [ ] CONTRIBUTORS.md
- [ ] Google Colab demo notebook

**Target Date:** Mid-December 2025
**Help Wanted:** Documentation, testing, Docker expertise

---

### v1.5.0 (Jan 2026) - Enhanced Citation Management

**Goal:** Improve citation quality, diversity, and verification

**Planned Features:**
- [ ] **Citation clustering** - Group related papers by topic
- [ ] **Citation impact scores** - Highlight high-impact references
- [ ] **Multi-language citations** - Support non-English papers
- [ ] **Bibliography export formats** - BibTeX, RIS, EndNote
- [ ] **Citation relationship graphs** - Visualize paper connections
- [ ] **Duplicate citation detection** - Advanced fuzzy matching

**Target Date:** January 2026
**Help Wanted:** Citation format experts, research librarians

---

### v1.6.0 (Feb 2026) - Collaborative Features

**Goal:** Enable multi-author workflows and team collaboration

**Planned Features:**
- [ ] **Multi-author support** - Track individual contributions
- [ ] **Comment/review system** - Inline feedback on sections
- [ ] **Version tracking** - Git-like diff for thesis iterations
- [ ] **Role-based permissions** - Author, reviewer, advisor roles
- [ ] **Export co-author metadata** - Contribution tracking for publications

**Target Date:** February 2026
**Help Wanted:** Full-stack developers, Git integration experts

---

### v1.7.0 (Mar 2026) - Extended Database Integration

**Goal:** Add more academic databases and specialized sources

**Planned MCP Servers:**
- [ ] **IEEE Xplore** - Engineering and CS papers
- [ ] **ACM Digital Library** - Computer science
- [ ] **Springer** - Multidisciplinary journals
- [ ] **JSTOR** - Humanities and social sciences
- [ ] **Web of Science** - Citation indexing
- [ ] **Europe PMC** - Life sciences (EU focus)
- [ ] **bioRxiv/medRxiv** - Preprints

**Target Date:** March 2026
**Help Wanted:** API integration developers, database experts

---

### v2.0.0 (Q2 2026) - Major Expansion

**Goal:** Domain-specific agents and advanced features

**Planned Features:**

#### Domain-Specific Agents
- [ ] **Medical research agent** - Clinical trial formatting, medical terminology
- [ ] **Legal research agent** - Case citations, legal writing style
- [ ] **Engineering agent** - Technical specifications, standards
- [ ] **Social sciences agent** - Qualitative data, interview analysis
- [ ] **Humanities agent** - Primary source analysis, interpretive essays

#### Advanced Features
- [ ] **Multi-language support** - Generate theses in Spanish, French, German, etc.
- [ ] **Grant proposal templates** - NIH, NSF, ERC formats
- [ ] **Peer review response generator** - Address reviewer comments
- [ ] **Literature review automation** - Systematic review workflows
- [ ] **Research question refinement** - AI-assisted topic scoping

#### Infrastructure
- [ ] **Local LLM support** - Ollama, llama.cpp for privacy
- [ ] **Cloud deployment** - One-click Heroku/Vercel deployment
- [ ] **API endpoint** - RESTful API for programmatic access
- [ ] **Plugin system** - Community-built extensions

**Target Date:** Q2 2026 (April-June)
**Help Wanted:** Domain experts, LLM specialists, infrastructure engineers

---

## 🎁 Community Requests

Features requested by users (vote with 👍 on linked issues):

- [ ] Real-time collaboration (like Google Docs)
- [ ] Mobile app (thesis writing on-the-go)
- [ ] Voice dictation integration
- [ ] Zotero/Mendeley import
- [ ] LaTeX template library
- [ ] Institutional repository integration
- [ ] Plagiarism detection (Turnitin-like)
- [ ] Academic style guide checker (APA, MLA, Chicago strict validation)

**Want to see a feature?** [Create a Feature Request](../../issues/new?template=feature_request.yml)

---

## 🤝 How to Influence the Roadmap

1. **Vote on existing issues** - Add 👍 to features you want
2. **Create feature requests** - Explain your use case
3. **Contribute code** - PRs for planned features are welcome!
4. **Share feedback** - Tell us what's working and what's not
5. **Sponsor development** - Financial support accelerates features

---

## 📊 Metrics & Goals

### 2025 Goals (Q4)
- [x] Reach 100+ GitHub stars (Current: 120+)
- [ ] 50+ contributors
- [ ] 1,000+ thesis generated
- [ ] Featured in academic tool roundups

### 2026 Goals
- [ ] 1,000+ GitHub stars
- [ ] 200+ contributors
- [ ] Published in academic journal (JOSS, JOSE)
- [ ] Used in 10+ universities
- [ ] Integration with Overleaf/ShareLaTeX

---

## 🔄 Release Schedule

- **Patch releases** (1.x.x): Bug fixes, weekly as needed
- **Minor releases** (1.x.0): New features, monthly
- **Major releases** (x.0.0): Breaking changes, 6-12 months

---

## 💡 Ideas Under Consideration

Features we're exploring (not committed yet):

- Integration with reference managers (Zotero, Mendeley, EndNote)
- Jupyter Notebook integration for data science theses
- Thesis defense slide generation (PowerPoint/Beamer)
- Academic poster generation
- Literature review matrix visualization
- Paper recommendation system (based on topic + citations)
- Thesis outline templates by discipline
- Academic writing coach (style/clarity suggestions)

**Have an idea?** Start a [Discussion](../../discussions) to gather feedback!

---

## 🚫 Non-Goals

What we WON'T do (to maintain focus):

- ❌ Become a citation manager (use Zotero/Mendeley)
- ❌ Replace human judgment and critical thinking
- ❌ Support non-academic writing (novels, blogs, etc.)
- ❌ Guarantee publication acceptance
- ❌ Provide legal or medical advice
- ❌ Store user data in the cloud (privacy first!)

---

## 🙋 Get Involved

Want to help shape the future of OpenDraft?

- **Developers:** Check [good-first-issue](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) label
- **Researchers:** Share feedback on generated theses
- **Writers:** Improve documentation
- **Testers:** Beta test new features
- **Donors:** [Sponsor development](../../sponsors) (if available)

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

**Questions about the roadmap?** Ask in [Discussions](../../discussions)!

**Want to work on a feature?** Comment on the related issue or create one!
