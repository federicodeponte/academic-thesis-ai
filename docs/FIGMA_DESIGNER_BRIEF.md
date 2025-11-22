# Figma Designer Brief: Multi-Agent Architecture Diagram

**Project:** OpenDraft - System Architecture Visualization
**Client:** OpenDraft (Open Source Project)
**Designer Deliverable:** Static diagram showing 15-agent AI system
**Timeline:** 2-4 hours
**Date:** 2025-11-22

---

## 🎯 What You're Designing

A **technical/engineering-style diagram** that visualizes our AI thesis generation system.

**Think:** System architecture diagram meets data flow visualization (like AWS architecture diagrams or microservices maps).

**NOT:** Marketing infographic, cartoon illustration, or stock photo AI brain.

---

## 📋 Quick Brief (TL;DR)

**What:** Horizontal workflow diagram showing 5 phases with 15 specialized AI agents
**Style:** Dark background, clean nodes, phase-color-coded, technical aesthetic
**Format:** Static image (PNG + SVG)
**Canvas:** 1920×1080px (16:9 landscape)
**Vibe:** "This is serious engineering" not "Look how fun AI is!"

**Use Cases:**
- GitHub README (main project page)
- Landing page hero section
- Social media (LinkedIn, Twitter)
- Documentation

---

## 🎨 Design Goals

When someone sees this diagram in 3 seconds, they should understand:

1. **This is systematic** (5 clear phases, left-to-right flow)
2. **This is intelligent** (15 specialized agents, not one generic AI)
3. **This is production-ready** (real metrics: 99% faster, 95% accuracy)

**Emotional Response:**
- "These people built a real system."
- "This is engineered AI, not a chatbot wrapper."
- "I trust this is well-architected."

---

## 🚀 Quick Start (5-Minute Setup)

### Step 1: Create New Figma File
- Canvas: **1920×1080px**
- Background: Dark gradient (#0f172a → #1e293b)

### Step 2: Set Up Color Styles
Create these 5 color variables:

| Name | Hex | Used For |
|------|-----|----------|
| `Phase/Research` | `#3b82f6` | Blue - Research agents |
| `Phase/Structure` | `#8b5cf6` | Purple - Structure agents |
| `Phase/Writing` | `#f59e0b` | Orange - Writing agents |
| `Phase/QA` | `#ef4444` | Red - QA agents |
| `Phase/Polish` | `#10b981` | Green - Polish agents |

### Step 3: Create Agent Node Component
**Component Name:** `Agent-Node`

**Structure:**
```
Frame (180×120px, rounded 12px)
├─ Icon (24×24px emoji, top-left)
├─ Agent Name (16px bold, white)
└─ Description (12px regular, gray)
```

**Border:** 2px, color = phase variable
**Background:** #2a2a3e (80% opacity)

### Step 4: Layout Grid
Enable layout grid:
- **Columns:** 5 (one per phase)
- **Gutter:** 50px
- **Margin:** 50px

---

## 📐 Detailed Layout

### Overall Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1    PHASE 2     PHASE 3      PHASE 4      PHASE 5      │
│  Research   Structure   Writing      QA           Polish        │
│  (Blue)     (Purple)    (Orange)     (Red)        (Green)       │
│                                                                  │
│  🔍 Scout   🏛️ Arch     ✒️ Craft     🤔 Skeptic   🎙️ Voice    │
│  📝 Scribe  📐 Format   🧵 Thread    ✔️ Verify    🔄 Entropy   │
│  📡 Signal              📖 Narrate   ⚖️ Referee   ✨ Polish     │
│                                                    🚀 Enhance    │
│      ↓          ↓           ↓            ↓            ↓         │
│  [Arrows connecting phases left-to-right]                       │
│                                                                  │
│                                        [Stats Overlay: Top-R]   │
└─────────────────────────────────────────────────────────────────┘
```

**Flow:** Left → Right (Research → Polish → Output)

---

## 🧩 Components Breakdown

### 1. Phase Headers

**For Each Phase (5 total):**

**Position:** Top of each column (Y: 50px)
**Text Example:** "📚 RESEARCH PHASE"
**Font:** 24px bold, phase color
**Subtitle:** "Discover and synthesize papers" (14px, gray)

**All 5 Phase Headers:**
1. "📚 RESEARCH PHASE" → "Discover and synthesize academic papers"
2. "🏗️ STRUCTURE PHASE" → "Design thesis architecture"
3. "✍️ WRITING PHASE" → "Generate academic content"
4. "✅ QUALITY ASSURANCE" → "Verify and validate content"
5. "💎 POLISH PHASE" → "Refine to publication quality"

---

### 2. Agent Nodes (15 Total)

**Template:**
```
┌─────────────────────┐
│  🔍 [Emoji Icon]    │
│  [Agent Name]       │
│  ─────────────      │
│  [Description]      │
└─────────────────────┘
```

**Dimensions:** 180×120px
**Border Radius:** 12px
**Border:** 2px solid [phase color]
**Background:** #2a2a3e (semi-transparent)
**Padding:** 12px

**Text Styles:**
- Agent Name: 16px, bold, white (#ffffff)
- Description: 12px, regular, light gray (#cccccc)

---

### Agent Details (Copy-Paste Ready)

#### Phase 1: Research (Blue #3b82f6)

**1. Scout** (X: 50, Y: 150)
- Icon: 🔍
- Name: Scout
- Description: Research Planning

**2. Scribe** (X: 50, Y: 300)
- Icon: 📝
- Name: Scribe
- Description: Literature Review

**3. Signal** (X: 50, Y: 450)
- Icon: 📡
- Name: Signal
- Description: Citation Discovery

---

#### Phase 2: Structure (Purple #8b5cf6)

**4. Architect** (X: 400, Y: 250)
- Icon: 🏛️
- Name: Architect
- Description: Outline Design

**5. Formatter** (X: 400, Y: 400)
- Icon: 📐
- Name: Formatter
- Description: Style Compliance

---

#### Phase 3: Writing (Orange #f59e0b)

**6. Crafter** (X: 750, Y: 150)
- Icon: ✒️
- Name: Crafter
- Description: Section Writing

**7. Thread** (X: 750, Y: 300)
- Icon: 🧵
- Name: Thread
- Description: Coherence Check

**8. Narrator** (X: 750, Y: 450)
- Icon: 📖
- Name: Narrator
- Description: Voice Consistency

---

#### Phase 4: QA (Red #ef4444)

**9. Skeptic** (X: 1100, Y: 150)
- Icon: 🤔
- Name: Skeptic
- Description: Fact-Checking

**10. Verifier** (X: 1100, Y: 300)
- Icon: ✔️
- Name: Verifier
- Description: Citation Validation

**11. Referee** (X: 1100, Y: 450)
- Icon: ⚖️
- Name: Referee
- Description: Peer Review Sim

---

#### Phase 5: Polish (Green #10b981)

**12. Voice** (X: 1450, Y: 120)
- Icon: 🎙️
- Name: Voice
- Description: Tone Refinement

**13. Entropy** (X: 1450, Y: 250)
- Icon: 🔄
- Name: Entropy
- Description: Variation Analysis

**14. Polish** (X: 1450, Y: 380)
- Icon: ✨
- Name: Polish
- Description: Final Refinement

**15. Enhancer** (X: 1450, Y: 510)
- Icon: 🚀
- Name: Enhancer
- Description: Quality Boost

---

### 3. Connection Arrows

**Phase-to-Phase Arrows:**
- Style: Dashed line, 3px thick
- Color: Outgoing phase color
- Arrow head: 20×15px triangle
- Example: Research (blue) → Structure (purple) uses blue dashed arrow

**Parallel Execution Indicators:**

**Research Phase (3 agents run in parallel):**
- Dotted lines connecting Scout ↔ Scribe ↔ Signal
- Color: Light Blue (#60a5fa, 50% opacity)
- Style: 1px dotted
- Label: "Parallel execution" (10px, italic)

**QA Phase (3 agents run in parallel):**
- Dotted lines connecting Skeptic ↔ Verifier ↔ Referee
- Color: Light Red (#f87171, 50% opacity)

**Polish Phase (4 agents run in parallel):**
- Dotted lines connecting all 4 agents
- Color: Light Green (#34d399, 50% opacity)

---

### 4. Stats Overlay (Top-Right Corner)

**Position:** X: 1650px, Y: 20px
**Size:** 250×180px
**Background:** Dark semi-transparent (#1e293b, 90% opacity)
**Border Radius:** 12px
**Padding:** 20px

**Content:**
```
⚡ SYSTEM PERFORMANCE

🚀 99% faster than manual writing
💰 95% cheaper than hiring
📚 200M+ papers accessible
✅ 95% citation accuracy
🔄 181 test runs completed
📄 4 production theses
📝 111,665 words generated
```

**Styling:**
- Title: "SYSTEM PERFORMANCE" (14px bold, white)
- Icons: 12px
- Text: 11px regular, white
- Numbers: Bold, Electric Blue (#3b82f6)

---

### 5. Final Output Box

**Position:** X: 1700px, Y: 300px
**Size:** 200×180px
**Background:** Gradient (Green #10b981 → Teal #14b8a6)
**Border Radius:** 16px
**Shadow:** 0px 10px 30px rgba(16, 185, 129, 0.3)

**Content:**
```
📄 PUBLICATION-READY
    THESIS

✅ 20,000-30,000 words
✅ 40-60 verified citations
✅ 95%+ citation accuracy
✅ APA/MLA/Chicago formatted
✅ PDF/DOCX/LaTeX export

⏱️ 20-25 minutes
💰 $10-$35
```

**Styling:**
- Title: 14px bold, white, centered
- Checklist items: 11px regular, white
- Stats at bottom: 12px bold

---

## 🎨 Design Tips

### Color Usage Rules

**DO:**
- Use phase colors for borders and headers
- Use white/light gray for all text
- Use dark backgrounds (#1e293b, #2a2a3e)
- Use subtle shadows for depth

**DON'T:**
- Mix phase colors (each agent only uses its phase color)
- Use bright backgrounds
- Use more than 5 accent colors

### Typography

**Font Stack (in order of preference):**
1. Inter (Google Fonts)
2. SF Pro Display (macOS)
3. Segoe UI (Windows)
4. System default

**Hierarchy:**
- Phase Headers: 24px bold
- Agent Names: 16px bold
- Descriptions: 12px regular
- Stats/Details: 11px regular

### Spacing

**Consistent spacing system:**
- 8px (tight spacing, within cards)
- 12px (padding inside agent nodes)
- 20px (padding in overlay boxes)
- 50px (spacing between phases)

**Pro Tip:** Use Auto Layout in Figma for agent nodes so spacing is automatic.

---

## 📦 Deliverables Checklist

### Main Diagram (Required)

- [ ] **PNG Export** (README version)
  - Size: 1920×1080px
  - DPI: 72 (web resolution)
  - Background: Dark (#1a1a2e) or transparent
  - Filename: `architecture-diagram.png`

- [ ] **SVG Export** (Landing page version)
  - Size: Original (1920×1080px)
  - Outline all text
  - Filename: `architecture-diagram.svg`

### Social Media Adaptations (Optional)

- [ ] **Instagram/LinkedIn Square** (1080×1080px)
  - Vertical stack instead of horizontal
  - Larger text (1.5× sizing)
  - Filename: `architecture-instagram.png`

- [ ] **Twitter/X Banner** (1500×500px)
  - Horizontal compact version
  - Icon + name only (no descriptions)
  - Filename: `architecture-twitter.png`

### Figma File Organization

- [ ] Layer names follow convention: `Phase-[N]-[Name]/Agent-[Name]`
- [ ] All colors saved as Figma styles
- [ ] Agent node created as component
- [ ] Phase header created as component
- [ ] Arrow created as component

---

## ✅ Quality Checklist (Before Handoff)

### Visual Quality

- [ ] All text is readable at 100% zoom
- [ ] Icons are aligned consistently (24×24px)
- [ ] Border thickness is uniform (2px)
- [ ] Spacing between elements is consistent
- [ ] Arrows connect properly to nodes
- [ ] Gradients render smoothly

### Accessibility

- [ ] Text contrast ratio meets WCAG AA (4.5:1 minimum)
- [ ] Tested with Figma color blind simulation
- [ ] All important info visible without color (not relying on color alone)

### Technical

- [ ] PNG files under 500KB (compress with TinyPNG if needed)
- [ ] SVG files optimized (use SVGO or Figma's export optimization)
- [ ] Transparent background option available
- [ ] No missing fonts (all text outlined in SVG)

### Content Accuracy

- [ ] All 15 agents present
- [ ] Agent names spelled correctly
- [ ] Stats match source data:
  - 99% faster (not 98% or 95%)
  - 95% citation accuracy (not 95.2%)
  - $10-$35 cost range
  - 4 production theses
  - 111,665 words

---

## 🔧 Figma Workflow Recommendations

### Component Architecture

**Create 3 Master Components:**

1. **`Agent-Node-Template`**
   - Default state with placeholder text
   - Instance for each of 15 agents
   - Override: icon, name, description, border color

2. **`Phase-Header-Template`**
   - Default state with placeholder
   - Override: text, color, emoji

3. **`Connection-Arrow-Template`**
   - Default style
   - Override: color, dash style

**Benefits:**
- Consistency across all agents
- Easy to update (change component, all instances update)
- Faster iteration

### Layer Organization

```
📁 Multi-Agent-Architecture
├─ 📁 Background
│  └─ Gradient Fill
├─ 📁 Phase-1-Research
│  ├─ Phase-Header-Research
│  ├─ Agent-Scout
│  ├─ Agent-Scribe
│  └─ Agent-Signal
├─ 📁 Phase-2-Structure
│  ├─ Phase-Header-Structure
│  ├─ Agent-Architect
│  └─ Agent-Formatter
├─ 📁 Phase-3-Writing
│  └─ [3 agents]
├─ 📁 Phase-4-QA
│  └─ [3 agents]
├─ 📁 Phase-5-Polish
│  └─ [4 agents]
├─ 📁 Connections
│  ├─ Arrow-Phase1-to-Phase2
│  ├─ Arrow-Phase2-to-Phase3
│  └─ [etc.]
├─ 📁 Overlays
│  ├─ Stats-Overlay
│  └─ Output-Box
└─ 📁 Labels
   └─ Parallel-Execution-Labels
```

### Auto Layout Tips

**For Agent Nodes:**
1. Create frame (180×120px)
2. Enable Auto Layout (Shift+A)
3. Direction: Vertical
4. Spacing: 8px
5. Padding: 12px
6. Alignment: Top-left

**For Stats Overlay:**
1. Frame with Auto Layout
2. Direction: Vertical
3. Spacing: 4px (tight for list items)
4. Padding: 20px

**Benefits:** Easy to add/remove lines, automatically maintains spacing.

---

## 📚 Reference Materials

**Inspiration (similar style):**
- AWS Architecture Diagrams (clean, technical)
- Kubernetes system diagrams (node-based)
- Database schema visualizations (structured flow)
- Microservices architecture maps (component-based)

**Color Palette Examples:**
- [Tailwind CSS Colors](https://tailwindcss.com/docs/customizing-colors) (we're using their blue, purple, orange, red, green)
- GitHub dark mode UI (similar dark background aesthetic)

**Icon Resources:**
- Use standard emoji (cross-platform support)
- If custom icons needed: Heroicons, Lucide Icons (MIT licensed)

---

## 🤝 Collaboration & Feedback

### How to Share Work-in-Progress

**Figma Share Link:**
- Set permissions to "Anyone with link can view"
- Enable commenting
- Share link for feedback rounds

**Export Iterations:**
- Version naming: `architecture-diagram-v1.png`, `v2`, etc.
- Include version notes in file name if major changes

### Expected Feedback Rounds

**Round 1:** Layout and spacing review
**Round 2:** Color and typography refinement
**Round 3:** Final polish and export

**Typical changes:**
- Agent positioning tweaks
- Text sizing adjustments
- Color balance refinement
- Arrow routing improvements

---

## ❓ FAQ for Designers

### Q: Can I use custom fonts?
**A:** Prefer web-safe fonts (Inter, SF Pro, Segoe UI) for maximum compatibility. If using custom fonts, provide both regular and bold weights.

### Q: Should the background be transparent or dark?
**A:** Export both versions:
- Dark background for social media
- Transparent for flexibility on landing page

### Q: How strict are the positioning coordinates?
**A:** Use them as a starting point. If something looks off visually, trust your design eye. The goal is visual balance, not pixel-perfect placement.

### Q: Can I simplify the agent descriptions?
**A:** The descriptions must stay as-is (they're technically accurate). But if they don't fit, you can:
- Reduce font size to 11px
- Abbreviate with "..." if absolutely necessary

### Q: What if 15 agents don't fit?
**A:** They will fit with the specified layout. If struggling:
- Check canvas size (must be 1920×1080px)
- Verify agent node size (180×120px max)
- Use specified spacing (50px between phases)

### Q: Emojis not rendering correctly?
**A:** In Figma, emojis are text. If issues:
- Use "Apple Color Emoji" font
- Or convert to SVG icons (find on Noun Project, Heroicons)

---

## 🎓 Design Principles Recap

**Clarity over cleverness**
→ Every element serves a purpose

**Technical over trendy**
→ Engineering diagram aesthetic, not marketing fluff

**Dark and modern**
→ Dark backgrounds convey technical sophistication

**Color-coded intelligence**
→ Each phase has its color, no mixing

**Data-driven design**
→ Show real metrics, not vague claims

---

## 📞 Questions or Stuck?

**Technical Specs Reference:** See `VISUALIZATION_SPECS.md` (full technical documentation)

**Design Questions:**
- "Is this spacing correct?" → If it looks balanced, it's correct
- "Should I use this color?" → Stick to the 5 phase colors
- "Can I change this text?" → Agent names and descriptions are fixed, everything else is flexible

**Remember:** Your design intuition is valuable. The specs are a guide, not a prison. If something looks off, adjust it. The goal is a clear, professional diagram that communicates intelligence and systematic design.

---

**Ready to start?** Create that Figma file and drop in those agent nodes!

**Timeline Estimate:**
- Setup (colors, components): 30 min
- Layout agents: 60 min
- Add arrows and connections: 30 min
- Stats overlay and final output box: 30 min
- Polish and export: 30 min

**Total:** 3 hours (fast designer), 4-5 hours (thorough designer)

**Good luck! 🚀**

---

**Document Version:** 1.0
**Date:** 2025-11-22
**For:** Figma Designers
**Project:** OpenDraft Architecture Visualization
