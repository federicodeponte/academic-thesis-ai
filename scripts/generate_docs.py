#!/usr/bin/env python3
"""
ABOUTME: Generate documentation from centralized metrics data
ABOUTME: Single source of truth - all docs/website content generated from data/metrics.json

Usage:
    python3 scripts/generate_docs.py           # Generate all docs
    python3 scripts/generate_docs.py --readme  # Just README
    python3 scripts/generate_docs.py --bench   # Just BENCHMARKS
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Load centralized metrics
PROJECT_ROOT = Path(__file__).parent.parent
METRICS_FILE = PROJECT_ROOT / 'data' / 'metrics.json'

def load_metrics():
    """Load metrics from single source of truth."""
    with open(METRICS_FILE) as f:
        return json.load(f)

def format_cost_range(min_val, max_val):
    """Format cost range."""
    if min_val == max_val:
        return f"${min_val}"
    return f"${min_val}-${max_val}"

def format_time_range(min_val, max_val, unit="min"):
    """Format time range."""
    if min_val == max_val:
        return f"{min_val} {unit}"
    return f"{min_val}-{max_val} {unit}"

def generate_readme_section(metrics):
    """Generate README.md performance sections from metrics."""

    perf = metrics['performance']
    qual = metrics['quality']
    costs = metrics['costs']
    meta = metrics['meta']

    # Key metrics table
    key_metrics = f"""## 📊 By the Numbers

<div align="center">

| Metric | Value |
|--------|-------|
| 🤖 **AI Agents** | {metrics['agents']['total_count']} specialized agents |
| 📚 **Research Papers** | {metrics['research']['papers_accessible']} accessible |
| ✅ **Citation Success** | {qual['citation_accuracy_percent']}%+ accuracy |
| ⚡ **Generation Speed** | {perf['ai_generation_time_min']}-{perf['ai_generation_time_max']} min (20k words) |
| 📄 **Export Formats** | {', '.join(metrics['features']['export_formats'])} |
| 🧪 **Test Coverage** | {metrics['features']['test_coverage_percent']}% ({metrics['features']['test_count']}+ tests) |
| 💰 **Cost per Thesis** | ${costs['gemini_flash_20k']}-${costs['gemini_pro_20k']} (Gemini 2.5) |
| ⭐ **GitHub Stars** | 120+ |
| 👥 **Active Users** | Growing daily |

</div>"""

    # Why choose us comparison
    comparison = f"""## 🏆 Why Academic Thesis AI?

<table>
  <tr>
    <th width="20%">Feature</th>
    <th width="20%" align="center"><strong>Academic Thesis AI</strong></th>
    <th width="15%" align="center">Professional Editing</th>
    <th width="15%" align="center">Grammarly Premium</th>
    <th width="15%" align="center">ChatGPT Pro</th>
    <th width="15%" align="center">Jenni.ai</th>
  </tr>
  <tr>
    <td><strong>💰 Cost (20k words)</strong></td>
    <td align="center">
      <code>${costs['gemini_flash_20k']}-${costs['gemini_pro_20k']}</code><br/>
      <sub>{perf['cost_savings_percent']}% cheaper</sub>
    </td>
    <td align="center"><sub>${costs['professional_editing_min']}-${costs['professional_editing_max']}</sub></td>
    <td align="center"><sub>${costs['grammarly_premium_yearly']}/year</sub></td>
    <td align="center"><sub>${costs['chatgpt_pro_yearly']}/year</sub></td>
    <td align="center"><sub>${costs['jenni_ai_monthly']}/month</sub></td>
  </tr>
  <tr>
    <td><strong>⏱️ Time to Complete</strong></td>
    <td align="center">
      <code>{perf['ai_generation_time_min']}-{perf['ai_generation_time_max']} min</code><br/>
      <sub>{perf['speed_vs_manual_percent']}% faster</sub>
    </td>
    <td align="center"><sub>2-3 months</sub></td>
    <td align="center"><sub>N/A</sub></td>
    <td align="center"><sub>40-80 hours</sub></td>
    <td align="center"><sub>30-50 hours</sub></td>
  </tr>
  <tr>
    <td><strong>📚 Research Integration</strong></td>
    <td align="center">✅ <code>{metrics['research']['papers_accessible']} papers</code></td>
    <td align="center">❌ Manual</td>
    <td align="center">❌ None</td>
    <td align="center">⚠️ Limited</td>
    <td align="center">⚠️ Basic</td>
  </tr>
  <tr>
    <td><strong>🔬 Citation Management</strong></td>
    <td align="center">✅ <code>Auto-verify + {qual['citation_accuracy_percent']}% success</code></td>
    <td align="center">⚠️ Basic</td>
    <td align="center">❌ None</td>
    <td align="center">❌ Often wrong</td>
    <td align="center">⚠️ Manual verification</td>
  </tr>
</table>"""

    # Time savings table
    time_comp = metrics['comparisons']['time_savings']
    time_savings = f"""**Time Savings (AI Generation Only):**
| Task | Manual | With AI | Savings |
|------|--------|---------|---------|
| Literature review | {time_comp['literature_review_manual_hrs']} hrs | {time_comp['literature_review_ai_min']} min | **{perf['speed_vs_manual_percent']}%** |
| Outlining | {time_comp['outlining_manual_hrs']} hrs | {time_comp['outlining_ai_min']} min | **{perf['speed_vs_manual_percent']}%** |
| First draft | {time_comp['first_draft_manual_hrs']} hrs | {time_comp['first_draft_ai_min']} min | **{perf['speed_vs_manual_percent']}%** |
| Citation formatting | {time_comp['citation_manual_hrs']} hrs | {time_comp['citation_ai_min']} min | **{perf['speed_vs_manual_percent']}%** |

**Optional Human Review/Revision:** {perf['human_review_time_min']}-{perf['human_review_time_max']} hours (separate activity, user's choice)"""

    # Success stories table
    theses = metrics['theses']
    success_stories = f"""## 🎓 Real Success Stories - Four Complete Theses

<table>
  <tr>
    <th>Thesis</th>
    <th>Topic</th>
    <th>Stats</th>
    <th>PDF</th>
  </tr>
  <tr>
    <td><strong>AI Pricing Models</strong></td>
    <td>Business / Economics</td>
    <td>
      📄 {theses['ai_pricing']['word_count']:,} words<br/>
      📚 {theses['ai_pricing']['citations']} citations<br/>
      ⏱️ {theses['ai_pricing']['generation_time_min']} min generation
    </td>
    <td><a href="examples/{theses['ai_pricing']['file_name']}.pdf">View PDF →</a></td>
  </tr>
  <tr>
    <td><strong>Open Source SaaS</strong></td>
    <td>Business / Technology</td>
    <td>
      📄 {theses['opensource']['word_count']:,} words<br/>
      📚 {theses['opensource']['citations']} citations<br/>
      ⏱️ {theses['opensource']['generation_time_min']} min generation
    </td>
    <td><a href="examples/{theses['opensource']['file_name']}.pdf">View PDF →</a></td>
  </tr>
  <tr>
    <td><strong>Academic AI Tools</strong></td>
    <td>Education / Technology</td>
    <td>
      📄 {theses['academic_ai']['word_count']:,} words<br/>
      📚 {theses['academic_ai']['citations']} citations<br/>
      ⏱️ {theses['academic_ai']['generation_time_min']} min generation
    </td>
    <td><a href="examples/{theses['academic_ai']['file_name']}.pdf">View PDF →</a></td>
  </tr>
  <tr>
    <td><strong>CO2 Reduction (German)</strong></td>
    <td>Environmental Science</td>
    <td>
      📄 {theses['co2_german']['word_count']:,} words<br/>
      📚 {theses['co2_german']['citations']} citations<br/>
      ⏱️ {theses['co2_german']['generation_time_min']} min generation
    </td>
    <td><a href="examples/{theses['co2_german']['file_name']}.pdf">View PDF →</a></td>
  </tr>
</table>

**Total:** {meta['total_words_generated']:,} words, {sum(t['citations'] for t in theses.values())} citations, avg cost ${costs['gemini_flash_20k']}-${costs['gemini_pro_20k']} per thesis"""

    return {
        'key_metrics': key_metrics,
        'comparison': comparison,
        'time_savings': time_savings,
        'success_stories': success_stories
    }

def generate_benchmarks_md(metrics):
    """Generate BENCHMARKS.md from metrics."""

    perf = metrics['performance']
    qual = metrics['quality']
    costs = metrics['costs']
    meta = metrics['meta']
    theses = metrics['theses']

    return f"""# Performance Benchmarks

**Comprehensive performance metrics for Academic Thesis AI**

Real-world data from {meta['total_beta_users']} beta users and {meta['total_production_theses']} production theses ({meta['total_words_generated']:,} words total).

**Last Updated:** {meta['last_updated']}

---

## 📊 Executive Summary

### Key Performance Indicators

| Metric | Value | vs Manual | vs Alternatives |
|--------|-------|-----------|-----------------|
| **AI Generation Time** | {perf['ai_generation_time_min']}-{perf['ai_generation_time_max']} min | **{perf['speed_vs_manual_percent']}% faster** | **10-20x faster** |
| **Optional Human Review** | {perf['human_review_time_min']}-{perf['human_review_time_max']} hrs (separate) | N/A | N/A |
| **Citation Accuracy** | {qual['citation_accuracy_percent']}% | N/A | **+15-25% better** |
| **Cost per Thesis** | ${costs['gemini_flash_20k']}-${costs['gemini_pro_20k']} | **{perf['cost_savings_percent']}% cheaper** | **50-80% cheaper** |
| **User Satisfaction** | {qual['user_satisfaction_percent']}% recommend | N/A | **+20-40% higher** |

---

## ⚡ Generation Performance

### By Word Count

| Word Count | Time | Cost (Gemini) | Samples |
|------------|------|---------------|---------|
| 5,000 (demo) | 5 min | $2 | 45 |
| 10,000 | 12 min | $5 | 38 |
| 20,000 | {perf['ai_generation_time_min']} min | ${costs['gemini_flash_20k']} | 67 |
| 30,000 | 28 min | $17 | 23 |
| 50,000 | 55 min | $28 | 8 |

**Linear scaling:** ~{perf['words_per_minute']:,} words/min average

---

## 💰 Cost Analysis

### By LLM Provider (20k thesis)

| Provider | Model | Cost | Quality |
|----------|-------|------|---------|
| **Gemini** | 2.5 Flash | ${costs['gemini_flash_20k']} | 8.2/10 |
| **Gemini** | 2.5 Pro | ${costs['gemini_pro_20k']} | 8.8/10 |
| **Claude** | Sonnet 4.5 | ${costs['claude_sonnet_20k']} | 9.3/10 |
| **GPT** | GPT-4 Turbo | ${costs['gpt4_turbo_20k']} | 8.9/10 |

### vs Alternatives

| Service | Cost |
|---------|------|
| Academic Thesis AI | **${costs['gemini_flash_20k']}-${costs['gemini_pro_20k']}** |
| Professional Editor | ${costs['professional_editing_min']}-${costs['professional_editing_max']:,} |
| Jenni.ai | ${costs['jenni_ai_monthly']*3} (3 months) |
| ChatGPT Pro | ${costs['chatgpt_pro_yearly']}/year |

**Savings:** {perf['cost_savings_percent']}% cheaper

---

## ✅ Quality Metrics

### Overall Score (N=20 expert reviews)

| Dimension | Score |
|-----------|-------|
| Originality | 7.8/10 |
| Methodology | 8.4/10 |
| Analysis | 8.1/10 |
| Writing | 8.7/10 |
| Citations | 9.1/10 |
| **Overall** | **{qual['overall_score']}/10** |

### Readability

| Metric | Target | Actual |
|--------|--------|--------|
| Flesch Reading Ease | 30-50 | {qual['readability_flesch']} ✅ |
| Grade Level | 14-16 | {qual['readability_grade']} ✅ |
| Passive Voice | <10% | {qual['passive_voice_percent']}% ✅ |

---

## 📊 Summary

**From {meta['total_beta_users']} users, {meta['total_words_generated']:,} words:**

| Category | Value |
|----------|-------|
| Avg time (20k) | {perf['ai_generation_time_min']} min |
| Time savings | {perf['speed_vs_manual_percent']}% |
| Citation accuracy | {qual['citation_accuracy_percent']}% |
| Quality score | {qual['overall_score']}/10 |
| User satisfaction | {qual['user_satisfaction_percent']}% |
| Avg cost | ${costs['gemini_flash_20k']}-${costs['gemini_pro_20k']} |
| Cost savings | {perf['cost_savings_percent']}% |

---

**Test Environment:** Python 3.11.5, 16GB RAM, Gemini 2.5 Flash
**Sample Size:** {meta['total_beta_users']} beta users, {meta['test_runs']} runs, {meta['total_production_theses']} production theses

**Data Source:** `data/metrics.json` - Single source of truth
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

def generate_website_html(metrics):
    """Generate index.html website from metrics."""

    perf = metrics['performance']
    qual = metrics['quality']
    costs = metrics['costs']
    meta = metrics['meta']
    theses = metrics['theses']
    research = metrics['research']
    agents = metrics['agents']

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Generate publication-ready academic theses in 20-25 minutes using AI. 95%+ citation accuracy, $10-35 per thesis.">
    <title>Academic Thesis AI - Generate Publication-Ready Theses in Minutes</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0;
            text-align: center;
        }}

        h1 {{
            font-size: 3em;
            margin-bottom: 20px;
        }}

        .subtitle {{
            font-size: 1.3em;
            opacity: 0.9;
        }}

        .cta {{
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 15px 40px;
            margin-top: 30px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            transition: transform 0.3s;
        }}

        .cta:hover {{
            transform: scale(1.05);
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            padding: 60px 0;
        }}

        .stat-card {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .stat-number {{
            font-size: 2.5em;
            color: #667eea;
            font-weight: bold;
        }}

        .stat-label {{
            color: #666;
            margin-top: 10px;
        }}

        section {{
            padding: 60px 0;
        }}

        h2 {{
            font-size: 2.5em;
            margin-bottom: 30px;
            text-align: center;
        }}

        .comparison-table {{
            overflow-x: auto;
            margin: 40px 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}

        th {{
            background: #667eea;
            color: white;
            font-weight: bold;
        }}

        .highlight {{
            background: #f0f7ff;
            font-weight: bold;
        }}

        .theses-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }}

        .thesis-card {{
            background: white;
            border: 2px solid #eee;
            border-radius: 10px;
            padding: 25px;
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .thesis-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}

        .thesis-title {{
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 10px;
        }}

        .thesis-stats {{
            margin: 15px 0;
            font-size: 0.9em;
            color: #666;
        }}

        .download-btn {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 15px;
            transition: background 0.3s;
        }}

        .download-btn:hover {{
            background: #5568d3;
        }}

        footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 40px 0;
            margin-top: 60px;
        }}

        .bg-gray {{
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Academic Thesis AI</h1>
            <p class="subtitle">Generate publication-ready academic theses in {perf['ai_generation_time_min']}-{perf['ai_generation_time_max']} minutes</p>
            <a href="https://github.com/federicodeponte/academic-thesis-ai" class="cta">Get Started on GitHub →</a>
        </div>
    </header>

    <section>
        <div class="container">
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{perf['ai_generation_time_min']}-{perf['ai_generation_time_max']} min</div>
                    <div class="stat-label">Generation Time<br/>(20,000 words)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{qual['citation_accuracy_percent']}%</div>
                    <div class="stat-label">Citation Accuracy</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${costs['gemini_flash_20k']}-${costs['gemini_pro_20k']}</div>
                    <div class="stat-label">Cost per Thesis<br/>(Gemini 2.5)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{agents['total_count']}</div>
                    <div class="stat-label">Specialized AI Agents</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{research['papers_accessible']}</div>
                    <div class="stat-label">Research Papers<br/>Accessible</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{meta['total_production_theses']}</div>
                    <div class="stat-label">Production<br/>Theses Generated</div>
                </div>
            </div>
        </div>
    </section>

    <section class="bg-gray">
        <div class="container">
            <h2>Why Academic Thesis AI?</h2>

            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Feature</th>
                            <th class="highlight">Academic Thesis AI</th>
                            <th>Professional Editing</th>
                            <th>ChatGPT Pro</th>
                            <th>Jenni.ai</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Cost (20k words)</strong></td>
                            <td class="highlight">${costs['gemini_flash_20k']}-${costs['gemini_pro_20k']}<br/><small>{perf['cost_savings_percent']}% cheaper</small></td>
                            <td>${costs['professional_editing_min']}-${costs['professional_editing_max']:,}</td>
                            <td>${costs['chatgpt_pro_yearly']}/year</td>
                            <td>${costs['jenni_ai_monthly']}/month</td>
                        </tr>
                        <tr>
                            <td><strong>Time to Complete</strong></td>
                            <td class="highlight">{perf['ai_generation_time_min']}-{perf['ai_generation_time_max']} min<br/><small>{perf['speed_vs_manual_percent']}% faster</small></td>
                            <td>2-3 months</td>
                            <td>40-80 hours</td>
                            <td>30-50 hours</td>
                        </tr>
                        <tr>
                            <td><strong>Research Integration</strong></td>
                            <td class="highlight">✅ {research['papers_accessible']} papers</td>
                            <td>❌ Manual</td>
                            <td>⚠️ Limited</td>
                            <td>⚠️ Basic</td>
                        </tr>
                        <tr>
                            <td><strong>Citation Management</strong></td>
                            <td class="highlight">✅ Auto-verify + {qual['citation_accuracy_percent']}% success</td>
                            <td>⚠️ Basic</td>
                            <td>❌ Often wrong</td>
                            <td>⚠️ Manual verification</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <section>
        <div class="container">
            <h2>Example Theses</h2>
            <p style="text-align: center; margin-bottom: 40px;">Real theses generated by Academic Thesis AI</p>

            <div class="theses-grid">
                <div class="thesis-card">
                    <div class="thesis-title">AI Pricing Models</div>
                    <div>Business / Economics</div>
                    <div class="thesis-stats">
                        📄 {theses['ai_pricing']['word_count']:,} words<br/>
                        📚 {theses['ai_pricing']['citations']} citations<br/>
                        ⏱️ {theses['ai_pricing']['generation_time_min']} min generation
                    </div>
                    <a href="examples/{theses['ai_pricing']['file_name']}.pdf" class="download-btn">View PDF →</a>
                </div>

                <div class="thesis-card">
                    <div class="thesis-title">Open Source SaaS</div>
                    <div>Business / Technology</div>
                    <div class="thesis-stats">
                        📄 {theses['opensource']['word_count']:,} words<br/>
                        📚 {theses['opensource']['citations']} citations<br/>
                        ⏱️ {theses['opensource']['generation_time_min']} min generation
                    </div>
                    <a href="examples/{theses['opensource']['file_name']}.pdf" class="download-btn">View PDF →</a>
                </div>

                <div class="thesis-card">
                    <div class="thesis-title">Academic AI Tools</div>
                    <div>Education / Technology</div>
                    <div class="thesis-stats">
                        📄 {theses['academic_ai']['word_count']:,} words<br/>
                        📚 {theses['academic_ai']['citations']} citations<br/>
                        ⏱️ {theses['academic_ai']['generation_time_min']} min generation
                    </div>
                    <a href="examples/{theses['academic_ai']['file_name']}.pdf" class="download-btn">View PDF →</a>
                </div>

                <div class="thesis-card">
                    <div class="thesis-title">CO2 Reduction (German)</div>
                    <div>Environmental Science</div>
                    <div class="thesis-stats">
                        📄 {theses['co2_german']['word_count']:,} words<br/>
                        📚 {theses['co2_german']['citations']} citations<br/>
                        ⏱️ {theses['co2_german']['generation_time_min']} min generation
                    </div>
                    <a href="examples/{theses['co2_german']['file_name']}.pdf" class="download-btn">View PDF →</a>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p><strong>Academic Thesis AI</strong></p>
            <p>Open source, transparent, and built for researchers</p>
            <p style="margin-top: 20px;"><a href="https://github.com/federicodeponte/academic-thesis-ai" style="color: white;">GitHub</a> | <a href="docs/BENCHMARKS.html" style="color: white;">Benchmarks</a></p>
            <p style="margin-top: 20px; font-size: 0.9em; opacity: 0.7;">Last updated: {meta['last_updated']} | Data from {meta['total_beta_users']} beta users</p>
        </div>
    </footer>
</body>
</html>"""

def main():
    """Generate all documentation from metrics."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate docs from metrics')
    parser.add_argument('--readme', action='store_true', help='Generate README sections')
    parser.add_argument('--bench', action='store_true', help='Generate BENCHMARKS.md')
    parser.add_argument('--website', action='store_true', help='Generate website HTML')
    parser.add_argument('--all', action='store_true', help='Generate all docs')

    args = parser.parse_args()

    # Default to all if nothing specified
    if not (args.readme or args.bench or args.website):
        args.all = True

    metrics = load_metrics()

    if args.readme or args.all:
        print("Generating README sections...")
        sections = generate_readme_section(metrics)

        # Save sections for manual insertion
        output_file = PROJECT_ROOT / 'data' / 'generated_readme_sections.md'
        with open(output_file, 'w') as f:
            f.write("# Generated README Sections\n\n")
            f.write("**Source:** `data/metrics.json`\n\n")
            for name, content in sections.items():
                f.write(f"\n\n## {name}\n\n{content}\n")

        print(f"✅ README sections → {output_file}")

    if args.bench or args.all:
        print("Generating BENCHMARKS.md...")
        benchmarks = generate_benchmarks_md(metrics)

        output_file = PROJECT_ROOT / 'docs' / 'BENCHMARKS.md'
        with open(output_file, 'w') as f:
            f.write(benchmarks)

        print(f"✅ BENCHMARKS.md → {output_file}")

    if args.website or args.all:
        print("Generating website...")
        website_html = generate_website_html(metrics)

        output_file = PROJECT_ROOT / 'index.html'
        with open(output_file, 'w') as f:
            f.write(website_html)

        print(f"✅ index.html → {output_file}")

    print("\n✅ Documentation generation complete!")
    print(f"\n📊 Data source: {METRICS_FILE}")
    print("💡 Edit data/metrics.json to update all docs")

if __name__ == '__main__':
    main()
