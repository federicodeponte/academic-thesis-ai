# Visual Assets Creation Guide

**Purpose:** This document specifies all visual assets needed for the README to achieve maximum GitHub visibility and "scroll-stopping" impact.

**Created:** November 21, 2025
**Status:** Awaiting manual creation
**Priority:** HIGH (Day 1 of sprint to 10/10)

---

## 📹 Demo Video/GIF (Hero Section)

**Location:** `docs/assets/demo.gif`
**Referenced in:** README.md line 10

### Specifications
- **Duration:** 30-60 seconds
- **Format:** Animated GIF (or link to YouTube/Vimeo)
- **Resolution:** 1280x720 (720p) minimum
- **File size:** < 10MB for GIF (GitHub limits)
- **Frame rate:** 15-20 fps

### Content Flow (30-60 seconds)
```
[0:00-0:10] Terminal: Installation
  $ pip install -e .
  $ opendraft verify
  ✅ All checks passed!

[0:10-0:20] Terminal: Running generation
  $ python tests/scripts/test_ai_pricing_thesis.py
  🤖 Scout researching...
  📚 Scribe reviewing literature...
  ✍️ Crafter writing sections...

[0:20-0:40] Progress animation
  Show agents working in parallel
  Citation count increasing (0 → 37)
  Word count increasing (0 → 28,543)
  Progress bar: [████████████] 100%

[0:40-0:50] PDF output
  Open examples/ai_pricing_thesis.pdf
  Scroll through professional formatting
  Show citations, tables, structure

[0:50-0:60] End screen
  "20,000-word thesis in 22 minutes"
  "37 verified citations"
  "Publication-ready PDF"
  GitHub star button CTA
```

### Technical Setup
1. **Terminal Recording:** Use asciinema + agg (converts to GIF)
   ```bash
   asciinema rec demo.cast
   agg demo.cast demo.gif
   ```
2. **Screen Recording:** Use OBS Studio or QuickTime (Mac)
3. **Editing:** Use ffmpeg to trim/optimize
   ```bash
   ffmpeg -i input.mov -vf "fps=15,scale=1280:-1" -loop 0 demo.gif
   ```

### Color Palette
- Terminal background: Dark (#1e1e1e)
- Success messages: Green (#00ff00)
- Agent names: Cyan (#00ffff)
- Progress bars: Blue (#0080ff)

---

## 📸 Screenshots (4 required)

### 1. Terminal Verification Output
**Location:** `docs/assets/screenshots/terminal-verify.png`
**Referenced in:** README.md line 48 (grid position 1)

**Content:**
```
$ opendraft verify

🔍 OpenDraft - Installation Verification
═══════════════════════════════════════════════════

✅ Python 3.11.5 (>= 3.9 required)
✅ All dependencies installed (45/45)
✅ API Keys configured:
   • GEMINI_API_KEY: ✓ Valid
   • ANTHROPIC_API_KEY: ✓ Valid
✅ PDF engine: WeasyPrint 62.3
✅ Project structure: Valid

🎉 Installation verified! Ready to generate theses.
```

**How to capture:**
1. Run `opendraft verify` in terminal
2. Screenshot the output
3. Crop to just the output (no menu bar)
4. Resolution: 1200x800 minimum

---

### 2. Generated Thesis PDF (First Page)
**Location:** `docs/assets/screenshots/thesis-pdf-first-page.png`
**Referenced in:** README.md line 48 (grid position 2)

**Content:**
- Open `examples/ai_pricing_thesis.pdf`
- Screenshot the first page (title page)
- Should show:
  - Title: "Pricing Models for Agentic AI Systems..."
  - Author information
  - Date
  - Professional academic formatting
  - University/institution styling

**How to capture:**
1. Open PDF in Preview/Adobe Reader
2. Zoom to 100%
3. Screenshot first page
4. Crop to just the page (no UI)
5. Resolution: 800x1100 (A4 aspect ratio)

---

### 3. Citation Database Integration
**Location:** `docs/assets/screenshots/citation-database.png`
**Referenced in:** README.md line 48 (grid position 3)

**Content:**
- Terminal showing citation lookup process
- Example:
```
🔍 Researching: "reinforcement learning pricing"

📚 Crossref API → 12 papers found
📚 Semantic Scholar → 8 papers found
📚 arXiv → 5 papers found

✅ 37 citations verified (95% success rate)

Top papers:
1. "Deep Reinforcement Learning for Dynamic Pricing" (2023)
   Authors: Zhang et al.
   Citations: 142
   DOI: 10.1145/3580305.3599428

2. "AI-Driven Pricing Models in SaaS" (2024)
   Authors: Kumar & Lee
   Citations: 89
   DOI: 10.1109/CLOUD55607.2024.00042
```

**How to capture:**
1. Run thesis generation with verbose logging
2. Capture citation lookup phase
3. Highlight successful API calls
4. Resolution: 1200x800 minimum

---

### 4. Before/After Comparison
**Location:** `docs/assets/screenshots/before-after.png`
**Referenced in:** README.md line 48 (grid position 4)

**Content:**
- Side-by-side comparison
- **BEFORE (left):** Empty markdown file or basic outline
- **AFTER (right):** Fully formatted thesis PDF

**Layout:**
```
┌─────────────────┬─────────────────┐
│     BEFORE      │      AFTER      │
├─────────────────┼─────────────────┤
│                 │                 │
│ # My Thesis     │  [PDF page      │
│                 │   with proper   │
│ ## Introduction │   formatting,   │
│ TODO: write     │   citations,    │
│                 │   tables, etc.] │
│                 │                 │
└─────────────────┴─────────────────┘
```

**How to capture:**
1. Create split-screen mockup
2. Use image editing software (Figma, Photoshop, or GIMP)
3. Left: Screenshot of basic markdown outline
4. Right: Screenshot of generated PDF
5. Add labels "BEFORE" and "AFTER"
6. Resolution: 1600x800 (2:1 aspect ratio)

---

## 🎨 Screenshot Grid Layout

**Target layout in README:**
```markdown
<table>
  <tr>
    <td width="50%">
      <img src="docs/assets/screenshots/terminal-verify.png" alt="Terminal verification">
      <p align="center"><strong>1. Verification Output</strong></p>
    </td>
    <td width="50%">
      <img src="docs/assets/screenshots/thesis-pdf-first-page.png" alt="Generated PDF">
      <p align="center"><strong>2. Generated Thesis</strong></p>
    </td>
  </tr>
  <tr>
    <td>
      <img src="docs/assets/screenshots/citation-database.png" alt="Citation database">
      <p align="center"><strong>3. Citation Integration</strong></p>
    </td>
    <td>
      <img src="docs/assets/screenshots/before-after.png" alt="Before/After">
      <p align="center"><strong>4. Before/After</strong></p>
    </td>
  </tr>
</table>
```

---

## 🎥 Demo Video (YouTube/Vimeo)

**Location:** External (embed link in README)
**Referenced in:** README.md line 56

### Specifications
- **Duration:** 3 minutes
- **Platform:** YouTube (unlisted or public)
- **Resolution:** 1920x1080 (1080p)
- **Audio:** Optional voice-over or text overlays

### Script Outline (3 minutes)
```
[0:00-0:20] Introduction
  - What is OpenDraft?
  - Problem: Writing 20k-word theses takes months
  - Solution: AI assistance in 15-25 minutes

[0:20-1:00] Installation Demo
  - pip install -e .
  - opendraft verify
  - Show all checks passing

[1:00-1:40] Generation Demo
  - python tests/scripts/test_ai_pricing_thesis.py
  - Show agent workflow
  - Highlight citation research (200M+ papers)

[1:40-2:20] Output Review
  - Open generated PDF
  - Show professional formatting
  - Navigate through sections
  - Point out verified citations

[2:20-2:50] Features Highlight
  - 15 specialized agents
  - 95%+ citation success
  - Multiple export formats
  - $10-50 cost per thesis

[2:50-3:00] Call to Action
  - Star on GitHub
  - Try the quickstart
  - Join discussions
```

### Tools
- **Recording:** OBS Studio, Camtasia, or ScreenFlow
- **Editing:** DaVinci Resolve (free), iMovie, or Premiere Pro
- **Voice-over:** Descript or Audacity
- **Thumbnail:** Canva (1280x720)

---

## 📊 Statistics Dashboard (Optional)

**Location:** `docs/assets/screenshots/statistics.png`
**Future enhancement**

Create visual dashboard showing:
- Total theses generated
- Average generation time
- Citation success rate over time
- Cost savings vs. alternatives
- User growth chart

Use tools: Chart.js, D3.js, or Google Sheets → Screenshot

---

## ✅ Asset Checklist

**Required (Day 1):**
- [ ] Hero demo GIF (30-60 seconds)
- [ ] Screenshot 1: Terminal verification
- [ ] Screenshot 2: PDF first page
- [ ] Screenshot 3: Citation database
- [ ] Screenshot 4: Before/After comparison

**Recommended (Day 2-3):**
- [ ] 3-minute YouTube demo video
- [ ] Video thumbnail (1280x720)
- [ ] Gallery images for examples/GALLERY.md

**Optional (Day 4-5):**
- [ ] Statistics dashboard screenshot
- [ ] Agent workflow diagram
- [ ] Architecture visualization

---

## 🛠️ Tools & Resources

### Free Tools
- **Terminal recording:** asciinema (https://asciinema.org/)
- **GIF conversion:** agg (https://github.com/asciinema/agg)
- **Screen recording:** OBS Studio (https://obsproject.com/)
- **Image editing:** GIMP (https://www.gimp.org/)
- **Video editing:** DaVinci Resolve (https://www.blackmagicdesign.com/products/davinciresolve)
- **Mockups:** Figma (free tier, https://figma.com/)

### Paid Tools (Optional)
- **Screen recording:** ScreenFlow (Mac), Camtasia
- **Video editing:** Adobe Premiere Pro
- **Image editing:** Adobe Photoshop
- **Mockups:** Sketch, Adobe XD

---

## 📝 File Naming Conventions

```
docs/assets/
├── screenshots/
│   ├── terminal-verify.png           # Verification output
│   ├── thesis-pdf-first-page.png     # PDF first page
│   ├── citation-database.png         # Citation lookup
│   ├── before-after.png              # Before/After comparison
│   └── gallery-*.png                 # Gallery thumbnails
├── gifs/
│   └── demo.gif                      # Hero demo GIF
└── videos/
    └── README.md                     # Links to external videos
```

**Naming rules:**
- Lowercase, hyphen-separated
- Descriptive, not generic
- PNG for screenshots (lossless)
- GIF for animations
- Keep file sizes reasonable (<5MB per image)

---

## 🎯 Success Criteria

**A visual asset is successful when:**
1. **It loads fast** - < 2 seconds on 3G connection
2. **It's readable** - Text is legible at GitHub's default zoom
3. **It tells a story** - Viewer understands what's happening
4. **It looks professional** - No UI clutter, clean cropping
5. **It drives action** - Makes viewer want to try the tool

**README is scroll-stopping when:**
- Hero GIF starts playing immediately (auto-play on GitHub)
- First scroll reveals statistics and comparison table
- Second scroll shows real thesis examples
- Third scroll has screenshot grid
- Every section has visual interest

---

## 📧 Next Steps

1. **Prioritize** the hero demo GIF (highest impact)
2. **Batch create** screenshots in one session (faster)
3. **Test on GitHub** by pushing to a branch and viewing
4. **Iterate** based on how it looks on different screen sizes
5. **Get feedback** from beta users before final launch

**Estimated time:**
- Hero GIF: 2 hours (recording + editing)
- 4 screenshots: 1 hour (setup + capture)
- YouTube video: 3-4 hours (recording + editing + upload)
- **Total:** 6-7 hours for all Day 1 assets

---

**Questions?** See Day 1 sprint plan in session notes or ask in GitHub Discussions.
