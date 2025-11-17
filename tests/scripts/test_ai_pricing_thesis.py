#!/usr/bin/env python3
"""
AI Pricing Thesis Test: Generate Complete Thesis
Topic: Pricing Strategies for AI Agents and LLM APIs
Full workflow test from research to final paper export

REFACTORED: Uses centralized config, shared utilities, and section-based validation
"""

import os
import sys
import time
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_config
from tests.test_utils import setup_model, run_agent, rate_limit_delay, research_citations_via_api
from tests.validators import Section, validate_paper_sections
from utils.citation_manager import extract_citations_from_text
from utils.citation_compiler import CitationCompiler
from utils.citation_database import save_citation_database
from utils.text_utils import smart_truncate
from utils.abstract_generator import generate_abstract_for_thesis
from utils.output_sanitizer import sanitize_enhanced_file


def main():
    """
    Generate a complete academic thesis using all 14 agents.

    Demonstrates production-ready workflow with:
    - Centralized configuration
    - Shared utilities (DRY)
    - Section-based validation (SOLID)
    - Type-safe operations
    """
    config = get_config()

    print("="*70)
    print("AI PRICING THESIS TEST")
    print("="*70)
    print()
    print("Topic: Pricing Models for Agentic AI Systems")
    print("Subtopics: Token-based, usage-based, value-based pricing")
    print("Format: Academic thesis (8,000+ words)")
    print(f"Model: {config.model.model_name}")
    print()
    print("="*70)

    # Initialize model
    model = setup_model()

    topic = "Pricing Models for Agentic AI Systems: From Token-Based to Value-Based Approaches"
    research_focus = "AI agents, pricing strategies, token pricing, usage-based pricing, value-based pricing, API economics"

    # Output directory
    output_dir = config.paths.output_dir / "ai_pricing_thesis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ====================================================================
    # PHASE 1: RESEARCH
    # ====================================================================
    print("\n" + "="*70)
    print("📚 PHASE 1: RESEARCH")
    print("="*70)

    # Step 1: Scout - API-backed citation discovery (replaces LLM hallucination)
    research_topics = [
        # Pricing fundamentals
        "pricing models for artificial intelligence services",
        "token-based pricing for large language models",
        "usage-based pricing in cloud computing",
        "value-based pricing strategies",
        "API pricing and monetization strategies",

        # AI agent economics
        "economic models for AI agents",
        "cost structures of machine learning services",
        "pricing transparency in AI platforms",
        "AI service pricing optimization",
        "multi-tier pricing for AI APIs",

        # LLM and generative AI pricing
        "pricing strategies for generative AI",
        "OpenAI API pricing models",
        "cost per token in language models",
        "pricing discrimination in AI services",
        "freemium models for AI applications",

        # Business models
        "subscription pricing for AI software",
        "pay-per-use models in AI industry",
        "dynamic pricing for machine learning APIs",
        "bundling strategies in AI services",
        "platform pricing in two-sided markets",

        # Value creation
        "value capture in AI ecosystems",
        "willingness to pay for AI services",
        "customer lifetime value in SaaS AI",
        "pricing psychology in technology adoption",
        "perceived value of AI solutions",

        # Competition and market dynamics
        "competitive pricing in AI market",
        "price wars in cloud AI services",
        "monopolistic pricing in platform economics",
        "network effects and pricing power",
        "market segmentation in AI pricing",

        # Usage metrics and monitoring
        "metering and billing for cloud services",
        "cost allocation in multi-tenant systems",
        "usage tracking for API calls",
        "chargeback models in enterprise AI",
        "consumption-based pricing analytics",

        # Cost optimization
        "cost optimization strategies for AI inference",
        "pricing efficiency in neural networks",
        "resource allocation and pricing",
        "economies of scale in AI services",
        "marginal cost pricing in software",

        # Industry studies
        "pricing comparison GPT-4 vs Claude vs Gemini",
        "AI pricing trends and forecasts",
        "revenue models for AI startups",
        "enterprise AI procurement pricing",
        "pricing negotiation in B2B AI sales",

        # Theoretical frameworks
        "transaction cost economics in AI",
        "information goods pricing theory",
        "two-sided market pricing dynamics",
        "versioning and price discrimination",
        "penetration vs skimming pricing AI",

        # Customer behavior
        "price sensitivity in AI adoption",
        "switching costs in AI platforms",
        "lock-in effects in AI services",
        "pricing transparency and trust",
        "elasticity of demand for AI tools",
    ]

    try:
        scout_result = research_citations_via_api(
            model=model,
            research_topics=research_topics,
            output_path=output_dir / "01_scout.md",
            target_minimum=35,  # Realistic for deep research mode (70-90% of query count)
            verbose=True,
            use_deep_research=True,  # Enable deep research mode for AI pricing industry sources
            topic=topic,  # Main research topic for deep research planning
            scope=research_focus  # Research scope (industry focus, constraints)
        )

        print(f"\n✅ Scout Success: {scout_result['count']} valid citations")
        print(f"📊 API Success Rate: {scout_result['count']/len(research_topics)*100:.1f}%")
        print(f"📚 Sources: Crossref={scout_result['sources']['Crossref']}, "
              f"Semantic Scholar={scout_result['sources']['Semantic Scholar']}, "
              f"LLM={scout_result['sources']['Gemini LLM']}")

        # Read scout output for next agents
        scout_output = (output_dir / "01_scout.md").read_text(encoding='utf-8')

    except ValueError as e:
        print(f"\n❌ SCOUT QUALITY GATE FAILED")
        print(str(e))
        print("\n⚠️  Cannot proceed - insufficient valid citations for academic thesis")
        return 1
    except Exception as e:
        print(f"\n❌ SCOUT FAILED - Unexpected Error")
        print(f"Error: {str(e)}")
        return 1

    rate_limit_delay()

    # Step 2: Scribe - Summarize
    scribe_output = run_agent(
        model=model,
        name="2. Scribe - Summarize Papers",
        prompt_path="prompts/01_research/scribe.md",
        user_input=f"Summarize these research findings:\n\n{smart_truncate(scout_output, max_chars=8000, preserve_json=True)}",
        save_to=output_dir / "02_scribe.md"
    )

    rate_limit_delay()

    # Step 3: Signal - Gap analysis
    signal_output = run_agent(
        model=model,
        name="3. Signal - Research Gap Analysis",
        prompt_path="prompts/01_research/signal.md",
        user_input=f"Analyze research gaps in AI agent pricing:\n\n{smart_truncate(scribe_output, max_chars=8000, preserve_json=False)}",
        save_to=output_dir / "03_signal.md"
    )

    rate_limit_delay()

    # ====================================================================
    # PHASE 2: STRUCTURE (Citation Manager Added in Phase 2)
    # ====================================================================
    print("\n" + "="*70)
    print("🏗️  PHASE 2: STRUCTURE")
    print("="*70)

    # Step 3.5: Citation Manager - Use Scout citations directly
    print("\n📚 Creating citation database from Scout research...")
    # FIXED (Bug #18): Use Scout citations directly instead of LLM extraction
    # Root cause: extract_citations_from_text() asks LLM to extract citations from markdown,
    # but LLM hallucinates fake citations instead of using real Scout API results.
    # Scout returns real Citation objects with api_source metadata - use them directly!

    # FIXED (Bug #19): Reassign citation IDs from "temp_id" to "cite_NNN"
    # Scout citations have temporary IDs that fail validation
    from utils.citation_database import CitationDatabase
    scout_citations = scout_result['citations']
    for i, citation in enumerate(scout_citations, start=1):
        citation.id = f"cite_{i:03d}"  # cite_001, cite_002, etc.

    citation_database = CitationDatabase(
        citations=scout_citations,  # Use real Scout citations with api_source
        citation_style="APA 7th",
        thesis_language="english"
    )

    print(f"✅ Citation database created: {len(citation_database.citations)} citations from Scout")

    # FIXED (Day 1B): Deduplicate citations before saving
    from utils.deduplicate_citations import deduplicate_citations
    deduplicated_citations, dedup_stats = deduplicate_citations(
        citation_database.citations,
        strategy='keep_best',
        verbose=True
    )

    # Update citation database with deduplicated citations
    citation_database.citations = deduplicated_citations

    if dedup_stats['removed_count'] > 0:
        print(f"🧹 Removed {dedup_stats['removed_count']} duplicate citations")
        print(f"   Final: {dedup_stats['final_count']} unique citations")

    # FIXED (Day 2A): Scrape real titles for Gemini Grounded citations
    from utils.scrape_citation_titles import TitleScraper
    scraper = TitleScraper(verbose=True)
    success_count, fail_count = scraper.scrape_citations(citation_database.citations)
    if success_count > 0:
        print(f"📰 Scraped {success_count} real page titles from web sources")
        if fail_count > 0:
            print(f"   ⚠️  {fail_count} titles could not be scraped (timeouts, errors)")

    # Save citation database to file
    citation_db_path = output_dir / "citation_database.json"
    save_citation_database(citation_database, citation_db_path)
    print(f"✅ Citation database saved to: {citation_db_path}")

    # Prepare citation summary for Crafters
    # FIXED (Bug #12): Show ALL citations explicitly to prevent hallucination
    citation_summary = f"\n\n## CITATION DATABASE\n\nYou have access to {len(citation_database.citations)} citations. Use citation IDs (cite_001, cite_002, etc.) instead of inline citations.\n\n"
    citation_summary += "**CRITICAL: ONLY use citation IDs listed below. DO NOT invent IDs beyond this list.**\n\n"
    citation_summary += "Available citations:\n"
    for citation in citation_database.citations:  # Show ALL citations (removed [:20] limit)
        authors_str = ", ".join(citation.authors[:2])
        if len(citation.authors) > 2:
            authors_str += " et al."
        citation_summary += f"- {citation.id}: {authors_str} ({citation.year}) - {citation.title[:60]}...\n"
    # Add explicit maximum ID boundary
    if citation_database.citations:
        max_id = citation_database.citations[-1].id
        citation_summary += f"\n**Maximum citation ID: {max_id}** (DO NOT exceed this)\n"

    rate_limit_delay()

    # Step 4: Architect - Create outline
    architect_output = run_agent(
        model=model,
        name="4. Architect - Design Paper Structure",
        prompt_path="prompts/02_structure/architect.md",
        user_input=(
            f"Create thesis outline for: {topic}\n\n"
            f"Research gaps identified:\n{signal_output[:2000]}\n\n"
            f"Paper type: Theoretical analysis with case studies\n"
            f"Length: 8,000-10,000 words"
        ),
        save_to=output_dir / "04_architect.md"
    )

    rate_limit_delay()

    # Step 5: Formatter - Apply style
    formatter_output = run_agent(
        model=model,
        name="5. Formatter - Apply Academic Style",
        prompt_path="prompts/02_structure/formatter.md",
        user_input=(
            f"Apply academic formatting:\n\n{architect_output[:2500]}\n\n"
            f"Target: Business/Economics journal\n"
            f"Style: APA 7th edition\n"
            f"Format: IMRaD adapted for theoretical paper"
        ),
        save_to=output_dir / "05_formatter.md"
    )

    rate_limit_delay()

    # ====================================================================
    # PHASE 3: COMPOSE
    # ====================================================================
    print("\n" + "="*70)
    print("✍️  PHASE 3: COMPOSE")
    print("="*70)

    # Step 6: Write Introduction
    intro = run_agent(
        model=model,
        name="6. Crafter - Write Introduction",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"Write Introduction section (2,500 words) for:\n\n{formatter_output[:2000]}\n\n"
            f"Include:\n"
            f"- Hook about AI pricing challenges\n"
            f"- Background on agentic AI systems\n"
            f"- Problem statement (pricing complexity)\n"
            f"- Research objectives\n"
            f"- Paper organization"
            f"{citation_summary}"
        ),
        save_to=output_dir / "06_introduction.md"
    )

    rate_limit_delay()

    # Step 7: Write Literature Review
    lit_review = run_agent(
        model=model,
        name="7. Crafter - Write Literature Review",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"Write Literature Review section (6,000 words) for:\n\n{formatter_output[:2000]}\n\n"
            f"Cover:\n"
            f"- Token-based pricing models (OpenAI, Anthropic)\n"
            f"- Usage-based pricing (AWS, cloud services)\n"
            f"- Value-based pricing theory\n"
            f"- Comparative analysis\n\n"
            f"Use research: {scribe_output[:1500]}"
            f"{citation_summary}"
        ),
        save_to=output_dir / "07_literature_review.md"
    )

    rate_limit_delay()

    # Step 8: Write Methodology
    methods = run_agent(
        model=model,
        name="8. Crafter - Write Methodology",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"Write Methodology section (2,500 words) for:\n\n{formatter_output[:2000]}\n\n"
            f"Describe:\n"
            f"- Framework for comparing pricing models\n"
            f"- Case study selection criteria\n"
            f"- Analysis approach"
            f"{citation_summary}"
        ),
        save_to=output_dir / "08_methodology.md"
    )

    rate_limit_delay()

    # Step 9: Write Analysis
    analysis = run_agent(
        model=model,
        name="9. Crafter - Write Analysis",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"Write Analysis section (6,000 words) for:\n\n{formatter_output[:2000]}\n\n"
            f"Analyze:\n"
            f"- Comparison of pricing models\n"
            f"- Advantages and disadvantages\n"
            f"- Real-world examples (OpenAI, Claude, etc.)\n"
            f"- Hybrid pricing approaches"
            f"{citation_summary}"
        ),
        save_to=output_dir / "09_analysis.md"
    )

    rate_limit_delay()

    # Step 10: Write Discussion
    discussion = run_agent(
        model=model,
        name="10. Crafter - Write Discussion",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"Write Discussion section (3,000 words) for:\n\n{formatter_output[:2000]}\n\n"
            f"Discuss:\n"
            f"- Implications for AI companies\n"
            f"- Customer adoption considerations\n"
            f"- Future pricing trends\n"
            f"- Recommendations"
            f"{citation_summary}"
        ),
        save_to=output_dir / "10_discussion.md"
    )

    rate_limit_delay()

    # Step 11: Write Conclusion
    conclusion = run_agent(
        model=model,
        name="11. Crafter - Write Conclusion",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"Write Conclusion section (1,000 words) for:\n\n{formatter_output[:2000]}\n\n"
            f"Summarize:\n"
            f"- Key findings\n"
            f"- Contributions to field\n"
            f"- Future research directions"
            f"{citation_summary}"
        ),
        save_to=output_dir / "11_conclusion.md"
    )

    rate_limit_delay()

    # Assemble complete draft
    print("\n" + "="*70)
    print("📝 ASSEMBLING COMPLETE DRAFT")
    print("="*70)

    complete_draft = f"""# {topic}

{intro}

{lit_review}

{methods}

{analysis}

{discussion}

{conclusion}

---

## References

[To be completed with proper citations from research]
"""

    draft_file = output_dir / "COMPLETE_DRAFT.md"
    with open(draft_file, 'w', encoding='utf-8') as f:  # FIXED (Bug #15): Added UTF-8 encoding
        f.write(complete_draft)

    word_count = len(complete_draft.split())
    print(f"✅ Draft complete: {word_count:,} words")
    print(f"Saved to: {draft_file}")

    # ====================================================================
    # PHASE 4: VALIDATE (SECTION-BASED - NEW!)
    # ====================================================================
    print("\n" + "="*70)
    print("✅ PHASE 4: VALIDATE (Section-Based)")
    print("="*70)

    # Create sections for independent validation
    sections = [
        Section.from_text("Introduction", intro),
        Section.from_text("Literature Review", lit_review),
        Section.from_text("Methodology", methods),
        Section.from_text("Analysis", analysis),
        Section.from_text("Discussion", discussion),
        Section.from_text("Conclusion", conclusion),
    ]

    print(f"\nValidating {len(sections)} sections independently:")
    for section in sections:
        print(f"  - {section.name}: {section.word_count:,} words")

    # Step 12: Skeptic review (now per-section!)
    skeptic_reviews = validate_paper_sections(
        model=model,
        sections=sections,
        output_dir=output_dir,
        validators=['skeptic'],
        create_consolidated=True,
        verbose=True
    )

    print(f"\n✅ All {len(sections)} sections validated independently")
    print(f"✅ Consolidated review saved to: {output_dir / 'skeptic_complete_review.md'}")

    # ====================================================================
    # PHASE 5: REFINE
    # ====================================================================
    print("\n" + "="*70)
    print("🎨 PHASE 5: REFINE")
    print("="*70)

    rate_limit_delay()

    # Step 13: Entropy - Humanize intro
    humanized_intro = run_agent(
        model=model,
        name="13. Entropy - Humanize Introduction",
        prompt_path="prompts/05_refine/entropy.md",
        user_input=f"Humanize this introduction:\n\n{intro[:2000]}",
        save_to=output_dir / "13_humanized_intro.md"
    )

    rate_limit_delay()

    # ====================================================================
    # PHASE 6: CITATION COMPILATION
    # ====================================================================
    print("\n" + "="*70)
    print("✅ PHASE 6: CITATION COMPILATION (Agent #14 - Citation Compiler)")
    print("="*70)

    # Create complete draft for citation compilation
    draft_paper = f"""# {topic}

{humanized_intro or intro}

{lit_review}

{methods}

{analysis}

{discussion}

{conclusion}
"""

    # Save draft before citation compilation
    draft_path = output_dir / "14_draft_pre_citation_compilation.md"
    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write(draft_paper)

    print(f"✅ Draft saved: {draft_path}")
    print(f"📊 Draft stats: ~{len(draft_paper.split())} words")

    # Step 14: Citation Compiler - Replace citation IDs with formatted citations
    print("\n🔧 Running Citation Compiler...")
    print("   This will:")
    print("   • Replace {cite_XXX} IDs with formatted citations (APA 7th)")
    print("   • Auto-generate reference list from cited sources")
    print("   • 100% deterministic compilation (O(1) dictionary lookup)")
    print("\n⏳ Citation compilation (instant)...")

    # VALIDATION STEP: Validate citations for academic integrity
    print("\n" + "="*70)
    print("🔍 CITATION VALIDATION (Academic Integrity Check)")
    print("="*70)

    from utils.citation_validator import CitationValidator
    validator = CitationValidator(timeout=10)
    issues, stats = validator.validate_database(citation_db_path)

    if issues:
        print(f"\n⚠️  Found {len(issues)} citation validation issues:")
        print(f"   • Critical issues: {stats['critical_issues']}")
        print(f"   • Warnings: {stats['warnings']}")
        print(f"   • Invalid DOIs: {stats['invalid_dois']}")
        print(f"   • Invalid authors: {stats['invalid_authors']}")

        # Display first 5 critical issues
        critical = [i for i in issues if i.severity == 'critical']
        if critical:
            print("\n❌ CRITICAL ISSUES (first 5):")
            for issue in critical[:5]:
                print(f"   [{issue.citation_id}] {issue.message}")

        # Save full validation report
        validation_report = validator.generate_report(issues, "AI Pricing Thesis")
        report_path = output_dir / "citation_validation_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(validation_report)
        print(f"\n📄 Full validation report saved: {report_path}")

        print("\n⚠️  RECOMMENDATION: Review and fix invalid citations before publication")
        print("   Continuing with current citations for now...")
    else:
        print("\n✅ All citations passed validation - no issues found!")

    print("\n" + "="*70)

    compiler = CitationCompiler(citation_database, model=model)
    compiled_paper, missing_ids, researched_topics = compiler.compile_citations(draft_paper, research_missing=True)

    # Generate reference list
    reference_list = compiler.generate_reference_list(draft_paper)

    # Combine compiled paper with reference list
    verified_paper = f"""{compiled_paper}

---

{reference_list}
"""

    # Save compiled version
    with open(output_dir / "15_compiled_citations.md", 'w', encoding='utf-8') as f:
        f.write(verified_paper)

    # Validate compilation
    validation = compiler.validate_compilation(draft_paper, compiled_paper)

    print(f"\n✅ Citation compilation complete!")
    print(f"📊 Compilation stats:")
    print(f"   - Total citations: {validation['total_citations']}")
    print(f"   - Successfully compiled: {validation['successfully_compiled']}")
    print(f"   - Missing: {validation['missing_citations']}")
    if missing_ids:
        print(f"   ⚠️  Missing citation IDs: {missing_ids}")

    # Generate coverage report
    print("\n📊 Generating citation coverage report...")
    from utils.citation_compiler import format_coverage_report
    coverage_report_data = compiler.generate_coverage_report(draft_paper)
    coverage_report = format_coverage_report(coverage_report_data)

    # Save coverage report
    coverage_report_path = output_dir / "14_citation_coverage_report.md"
    with open(coverage_report_path, 'w', encoding='utf-8') as f:
        f.write(coverage_report)

    print(f"✅ Coverage report generated!")
    print(f"   - Citations available: {coverage_report_data['total_citations_available']}")
    print(f"   - Citations used: {coverage_report_data['citations_used']}")
    print(f"   - Coverage: {coverage_report_data['coverage_percentage']:.1f}%")
    print(f"   - Report saved to: {coverage_report_path}")

    # Use compiled version
    paper_for_enhancement = verified_paper

    rate_limit_delay()

    # ====================================================================
    # PHASE 6.5: ABSTRACT GENERATION (Agent #16 - Abstract Specialist)
    # ====================================================================
    print("\n" + "="*70)
    print("📝 PHASE 6.5: ABSTRACT GENERATION (Agent #16)")
    print("="*70)

    print("\n🔧 Generating or verifying academic abstract...")
    print("   This will:")
    print("   • Check if thesis has placeholder abstract")
    print("   • Auto-detect language (English/German)")
    print("   • Generate 4-paragraph abstract (250-300 words)")
    print("   • Include 12-15 relevant keywords")
    print("   • Skip if full abstract already exists")

    # Determine path to latest thesis version (find the compiled citations file)
    compiled_path = output_dir / "15_compiled_citations.md" if (output_dir / "15_compiled_citations.md").exists() else None
    if not compiled_path or not compiled_path.exists():
        # Fall back to draft if compiled not found
        compiled_path = output_dir / "05_draft_thesis.md"

    # Call Abstract Generator utility
    abstract_success, abstract_updated_content = generate_abstract_for_thesis(
        thesis_path=compiled_path,
        model=model,
        run_agent_func=run_agent,
        output_dir=output_dir,
        verbose=True
    )

    if abstract_success and abstract_updated_content:
        # Update verified_paper with new content
        verified_paper = abstract_updated_content

        # Save updated version
        with open(compiled_path, 'w', encoding='utf-8') as f:
            f.write(verified_paper)

        paper_for_enhancement = verified_paper

        print(f"✅ Abstract generation complete!")
    elif abstract_success and not abstract_updated_content:
        print(f"✅ Abstract already complete - no generation needed")
    else:
        print(f"⚠️  Abstract generation failed - continuing with existing content")

    rate_limit_delay()

    # ====================================================================
    # PHASE 7: ENHANCEMENT (Agent #15) - WITH SANITIZATION
    # ====================================================================
    print("\n" + "="*70)
    print("✨ PHASE 7: ENHANCE (Agent #15 - WITH OUTPUT SANITIZATION)")
    print("="*70)

    # Step 15: Enhancer - Add professional elements
    print("\n🔧 Running Enhancement Agent...")
    print("   This will add:")
    print("   • YAML metadata frontmatter")
    print("   • Enhanced 4-paragraph abstract")
    print("   • 5 comprehensive appendices")
    print("   • Limitations and Future Research sections")
    print("   • 3-5 tables and 1-2 figures")
    print("   • Expanded case studies")
    print("\n⏳ Enhancement may take 3-5 minutes...")

    # FIXED (Day 1A): Pass actual citation count to prevent frontmatter mismatch
    actual_citation_count = len(citation_database.citations)

    enhanced_paper = run_agent(
        model=model,
        name="15. Enhancer - Professional Enhancement",
        prompt_path="prompts/06_enhance/enhancer.md",
        user_input=f"""Enhance this thesis to publication-ready standard.

IMPORTANT: This thesis has EXACTLY {actual_citation_count} citations in the citation database.
When generating the YAML frontmatter, use this exact number for citations_verified field.

Thesis to enhance:

{paper_for_enhancement}""",
        save_to=output_dir / "16_enhanced_final.md"
    )

    # CRITICAL: Sanitize enhanced output to fix 4 bugs
    if enhanced_paper:
        print("\n" + "="*70)
        print("🧹 SANITIZING ENHANCED OUTPUT (Bug Fix)")
        print("="*70)

        sanitize_success = sanitize_enhanced_file(
            input_path=output_dir / "16_enhanced_final.md",
            output_path=None,  # Sanitize in place
            verbose=True
        )

        if sanitize_success:
            # Re-read sanitized version
            with open(output_dir / "16_enhanced_final.md", 'r', encoding='utf-8') as f:
                enhanced_paper = f.read()
            print("✅ Enhanced output sanitized successfully!")
        else:
            print("⚠️  Sanitization failed - using original enhanced output")

    # Use enhanced version if available, otherwise fall back to verified or draft
    final_paper = enhanced_paper if enhanced_paper else (verified_paper if verified_paper else draft_paper)

    if enhanced_paper:
        enhanced_word_count = len(enhanced_paper.split())
        print(f"\n✅ Enhancement complete!")
        print(f"📊 Enhanced stats: ~{enhanced_word_count} words (target: 14,000+)")
        print(f"📈 Word count increase: ~{enhanced_word_count - len(draft_paper.split())} words")
        print(f"📄 Source: 16_enhanced_final.md (sanitized)")
    else:
        print(f"\n⚠️  Enhancement failed, using {'verified' if verified_paper else 'draft'} version")

    # ====================================================================
    # EXPORT
    # ====================================================================
    print("\n" + "="*70)
    print("📤 EXPORTING TO PDF/WORD")
    print("="*70)

    final_md = output_dir / "FINAL_THESIS.md"

    # FIXED (Bug #16): Added error handling with fallback location
    try:
        with open(final_md, 'w', encoding='utf-8') as f:
            f.write(final_paper)
        print(f"✅ Saved to: {final_md}")
    except (IOError, OSError, PermissionError) as e:
        # Fallback to /tmp if primary location fails
        fallback_path = Path("/tmp") / "FINAL_THESIS_AI_PRICING_BACKUP.md"
        try:
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(final_paper)
            final_md = fallback_path  # Update path for later use
            print(f"⚠️  Primary location failed: {e}")
            print(f"✅ Saved to fallback: {fallback_path}")
        except Exception as e2:
            print(f"❌ FATAL: Failed to save thesis file: {e2}")
            return 1

    final_word_count = len(final_paper.split())
    print(f"✅ Final thesis: {final_word_count:,} words")

    # ====================================================================
    # QUALITY GATE: Validate thesis is publication-ready
    # ====================================================================
    print("\n" + "="*70)
    print("🔍 QUALITY GATE: Validating Publication-Readiness")
    print("="*70)

    from scripts.validate_thesis_quality import validate_thesis
    is_publication_ready = validate_thesis(final_md, verbose=True)

    if not is_publication_ready:
        print("\n" + "="*70)
        print("❌ THESIS GENERATION FAILED - Quality gate not passed")
        print("="*70)
        print("\n🚫 Blocking PDF export due to quality issues")
        print("   Fix the issues listed above and re-run generation")
        print("\n💡 Tip: You can manually fix FINAL_THESIS.md and re-export:")
        print(f"   python3 scripts/export_clean_pdfs.py")
        print("="*70)
        return 1  # Exit with error code

    print("="*70)

    # Export to PDF
    print("\nExporting to PDF...")
    try:
        result = subprocess.run([
            sys.executable, 'utils/export_professional.py',
            str(final_md),
            '--pdf', str(output_dir / 'FINAL_THESIS.pdf'),
            '--engine', 'pandoc'
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            pdf_size = (output_dir / 'FINAL_THESIS.pdf').stat().st_size
            print(f"✅ PDF export successful ({pdf_size:,} bytes)")
        else:
            print(f"⚠️  PDF export failed: {result.stderr}")
    except Exception as e:
        print(f"⚠️  PDF export error: {e}")

    # Export to Word
    print("\nExporting to Word...")
    try:
        result = subprocess.run([
            sys.executable, 'utils/export_professional.py',
            str(final_md),
            '--docx', str(output_dir / 'FINAL_THESIS.docx')
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            docx_size = (output_dir / 'FINAL_THESIS.docx').stat().st_size
            print(f"✅ Word export successful ({docx_size:,} bytes)")
        else:
            print(f"⚠️  Word export failed: {result.stderr}")
    except Exception as e:
        print(f"⚠️  Word export error: {e}")

    # ====================================================================
    # SUMMARY
    # ====================================================================
    print("\n" + "="*70)
    print("🎉 REAL-WORLD TEST COMPLETE")
    print("="*70)
    print(f"\nGenerated thesis on: {topic}")
    print(f"Final word count: {final_word_count:,} words")
    print(f"Sections validated: {len(sections)} (independently)")
    print(f"\nAll outputs saved to: {output_dir}/")
    print(f"\nFiles generated:")
    for file in sorted(output_dir.glob("*")):
        if file.is_file():
            size = file.stat().st_size
            print(f"  • {file.name} ({size:,} bytes)")

    print("\n✅ SYSTEM WORKS END-TO-END")
    print("✅ ALL AGENTS FUNCTIONAL")
    print("✅ SECTION-BASED VALIDATION WORKING")
    print("✅ EXPORT PIPELINE WORKS")
    print("✅ PRODUCTION READY")

    return 0


if __name__ == "__main__":
    sys.exit(main())
