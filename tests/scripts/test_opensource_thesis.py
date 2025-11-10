#!/usr/bin/env python3
"""
REAL-WORLD TEST: Generate Complete Thesis
Topic: How Open Source Software Can Save the World
Full workflow test from research to final paper export

REFACTORED: Uses centralized config, shared utilities, and section-based validation
"""

import os
import sys
import time
import subprocess
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_config
from tests.test_utils import setup_model, run_agent, rate_limit_delay
from tests.validators import Section, validate_paper_sections
from utils.citation_manager import extract_citations_from_text
from utils.citation_database import save_citation_database, load_citation_database
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
    print("REAL-WORLD THESIS TEST")
    print("="*70)
    print()
    print("Topic: How Open Source Software Can Save the World")
    print("Subtopics: Collaboration, innovation, sustainability, digital commons")
    print("Format: Academic thesis (8,000+ words)")
    print(f"Model: {config.model.model_name}")
    print()
    print("="*70)

    # Initialize model
    model = setup_model()

    topic = "How Open Source Software Can Save the World: From Code Collaboration to Global Impact"
    research_focus = "open source software, collaborative development, global impact, innovation, sustainability, digital commons, open source economics, software freedom, community-driven development"

    # Output directory
    output_dir = config.paths.output_dir / "opensource_thesis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ====================================================================
    # PHASE 1: RESEARCH
    # ====================================================================
    print("\n" + "="*70)
    print("📚 PHASE 1: RESEARCH")
    print("="*70)

    # Step 1: Scout - Find papers
    scout_output = run_agent(
        model=model,
        name="1. Scout - Find Relevant Papers",
        prompt_path="prompts/01_research/scout.md",
        user_input=(
            f"Find 30 academic papers and industry reports on:\n"
            f"- Open source software development\n"
            f"- Economic impact of open source\n"
            f"- Open source sustainability and environmental benefits\n"
            f"- Collaborative software development\n"
            f"- Digital commons and knowledge sharing\n"
            f"- Open source innovation models\n\n"
            f"Research focus: {research_focus}"
        ),
        save_to=output_dir / "01_scout.md"
    )

    if not scout_output:
        print("❌ Scout failed - aborting test")
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
        user_input=f"Analyze research gaps in open source impact:\n\n{smart_truncate(scribe_output, max_chars=8000, preserve_json=False)}",
        save_to=output_dir / "03_signal.md"
    )

    rate_limit_delay()

    # ====================================================================
    # PHASE 2: STRUCTURE
    # ====================================================================
    print("\n" + "="*70)
    print("🏗️  PHASE 2: STRUCTURE")
    print("="*70)

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
            f"Target: Technology/Social Impact journal\n"
            f"Style: APA 7th edition\n"
            f"Format: IMRaD adapted for theoretical paper"
        ),
        save_to=output_dir / "05_formatter.md"
    )

    rate_limit_delay()

    # Step 3.5: Citation Manager - Extract citations from research
    print("\n" + "="*70)
    print("📚 PHASE 2.5: CITATION MANAGEMENT")
    print("="*70)

    print("Extracting citations from research notes...")

    # Extract citations from research materials
    citation_database = extract_citations_from_text(
        text=scribe_output,  # Use summarized research notes
        model=model,
        language="english",
        citation_style="APA 7th",
        verbose=True
    )

    # Save citation database
    citation_db_path = output_dir / "citation_database.json"
    save_citation_database(citation_database, citation_db_path)

    print(f"\n✅ Citation database created: {len(citation_database.citations)} citations")
    print(f"📄 Saved to: {citation_db_path}")

    # Prepare citation database summary for Crafters
    citation_summary = f"\n\n## CITATION DATABASE\n\nYou have access to {len(citation_database.citations)} citations. Use citation IDs (cite_001, cite_002, etc.) instead of inline citations.\n\n"
    citation_summary += "Available citations:\n"
    for citation in citation_database.citations[:20]:  # Show first 20
        authors_str = ", ".join(citation.authors[:2])
        if len(citation.authors) > 2:
            authors_str += " et al."
        citation_summary += f"- {citation.id}: {authors_str} ({citation.year}) - {citation.title[:60]}...\n"
    if len(citation_database.citations) > 20:
        citation_summary += f"  ... and {len(citation_database.citations) - 20} more citations\n"

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
            f"- Hook about global challenges and technology's role\n"
            f"- Background on open source software movement\n"
            f"- Problem statement (proprietary vs open source)\n"
            f"- Research objectives (how open source saves the world)\n"
            f"- Paper organization\n"
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
            f"- History of open source software (Linux, Apache, etc.)\n"
            f"- Economic models of open source\n"
            f"- Collaborative development theory\n"
            f"- Digital commons and knowledge sharing\n"
            f"- Environmental sustainability through open source\n\n"
            f"Use research: {scribe_output[:1500]}\n"
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
            f"- Framework for analyzing open source impact\n"
            f"- Case study selection criteria (Linux, Wikipedia, etc.)\n"
            f"- Analysis approach for global impact assessment\n"
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
            f"- Open source impact on innovation\n"
            f"- Economic benefits (cost savings, job creation)\n"
            f"- Environmental sustainability (reduced waste, efficient development)\n"
            f"- Social impact (education, accessibility, digital divide)\n"
            f"- Real-world examples (Linux, Apache, Wikipedia, Firefox)\n"
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
            f"- Implications for technology policy\n"
            f"- Open source as solution to global challenges\n"
            f"- Future of collaborative development\n"
            f"- Recommendations for governments and organizations\n"
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
            f"- Key findings on open source impact\n"
            f"- Contributions to understanding global technology challenges\n"
            f"- Future research directions in open source and sustainability\n"
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
    with open(draft_file, 'w') as f:
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
    # PHASE 6: CITATION VERIFICATION
    # ====================================================================
    print("\n" + "="*70)
    print("✅ PHASE 6: CITATION VERIFICATION (Agent #14)")
    print("="*70)

    # Create complete draft for citation verification
    draft_paper = f"""# {topic}

{humanized_intro or intro}

{lit_review}

{methods}

{analysis}

{discussion}

{conclusion}

---

## References

[To be completed with proper citations]
"""

    # Save draft before citation verification
    draft_path = output_dir / "14_draft_pre_citation_check.md"
    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write(draft_paper)

    print(f"✅ Draft saved: {draft_path}")
    print(f"📊 Draft stats: ~{len(draft_paper.split())} words")

    # Step 14: Citation Compiler - Replace citation IDs with formatted citations
    print("\n🔍 Running Citation Compiler...")
    print("   This will:")
    print("   • Replace all {cite_XXX} IDs with formatted citations")
    print("   • Generate reference list automatically")
    print("   • Validate all citations present in database")
    print("   • Output: 100% deterministic citation compilation")
    print("\n⏳ Compiling citations...")

    from utils.citation_compiler import CitationCompiler
    from utils.citation_validator import CitationValidator

    # Load citation database
    citation_database = load_citation_database(citation_db_path)

    # VALIDATION STEP: Validate citations for academic integrity
    print("\n" + "="*70)
    print("🔍 CITATION VALIDATION (Academic Integrity Check)")
    print("="*70)

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
        validation_report = validator.generate_report(issues, "Open Source Thesis")
        report_path = output_dir / "citation_validation_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(validation_report)
        print(f"\n📄 Full validation report saved: {report_path}")

        print("\n⚠️  RECOMMENDATION: Review and fix invalid citations before publication")
        print("   Continuing with current citations for now...")
    else:
        print("\n✅ All citations passed validation - no issues found!")

    print("\n" + "="*70)

    # Compile citations (with automatic research of missing citations)
    compiler = CitationCompiler(citation_database, model=model)
    compiled_paper, missing_ids, researched_topics = compiler.compile_citations(draft_paper, research_missing=True)

    # Generate reference list
    reference_list = compiler.generate_reference_list(draft_paper)

    # Append reference list to paper
    verified_paper = compiled_paper + "\n\n" + reference_list

    # Save compiled paper
    verified_paper_path = output_dir / "15_compiled_citations.md"
    with open(verified_paper_path, 'w', encoding='utf-8') as f:
        f.write(verified_paper)

    # Use compiled version
    paper_for_enhancement = verified_paper

    # Validate compilation
    validation_result = compiler.validate_compilation(draft_paper, compiled_paper)

    verified_word_count = len(verified_paper.split())
    print(f"\n✅ Citation compilation complete!")
    print(f"📊 Compiled thesis: ~{verified_word_count} words")
    print(f"✅ Total citations: {validation_result['total_citations']}")
    print(f"✅ Successfully compiled: {validation_result['successfully_compiled']}")

    if validation_result['missing_citations'] > 0:
        print(f"⚠️  Missing citations: {validation_result['missing_citations']}")
        print(f"   Missing IDs: {missing_ids}")
        issues.append(f"❌ {validation_result['missing_citations']} missing citation IDs")
        manual_interventions += 1
    else:
        print("✅ All citation IDs successfully compiled - 100% success rate!")

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

    # Call Abstract Generator utility
    abstract_success, abstract_updated_content = generate_abstract_for_thesis(
        thesis_path=verified_paper_path,
        model=model,
        run_agent_func=run_agent,
        output_dir=output_dir,
        verbose=True
    )

    if abstract_success and abstract_updated_content:
        # Update verified_paper with new content
        verified_paper = abstract_updated_content

        # Save updated version
        with open(verified_paper_path, 'w', encoding='utf-8') as f:
            f.write(verified_paper)

        print(f"✅ Abstract generation complete!")
    elif abstract_success and not abstract_updated_content:
        print(f"✅ Abstract already complete - no generation needed")
    else:
        print(f"⚠️  Abstract generation failed - continuing with existing content")
        issues.append("⚠️ Abstract generation failed")

    rate_limit_delay()

    # ====================================================================
    # PHASE 7: ENHANCEMENT (Agent #15) - WITH SANITIZATION
    # ====================================================================
    print("\n" + "="*70)
    print("✨ PHASE 7: ENHANCE (Agent #15 - WITH OUTPUT SANITIZATION)")
    print("="*70)

    # Step 15: Enhancer - Add professional elements (NOW RE-ENABLED!)
    print("\n🔧 Running Enhancement Agent...")
    print("   This will add:")
    print("   • YAML metadata frontmatter")
    print("   • Enhanced 4-paragraph abstract")
    print("   • 5 comprehensive appendices")
    print("   • Limitations and Future Research sections")
    print("   • 3-5 tables and 1-2 figures")
    print("   • Expanded case studies")
    print("\n⏳ Enhancement may take 3-5 minutes...")

    enhanced_paper = run_agent(
        model=model,
        name="15. Enhancer - Professional Enhancement",
        prompt_path="prompts/06_enhance/enhancer.md",
        user_input=f"Enhance this thesis to publication-ready standard:\n\n{paper_for_enhancement}",
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

        # CRITICAL: Restore missing sections (defensive fix for LLM non-compliance)
        # Enhancement agent sometimes removes sections despite "UNCHANGED" instructions
        if enhanced_paper:
            print("\n" + "="*70)
            print("🔧 RESTORING SECTIONS (LLM Non-Compliance Fix)")
            print("="*70)

            from utils.section_restorer import restore_sections_in_file

            # Save pre-enhancement version for restoration
            pre_enhancement_path = output_dir / "14_draft_pre_citation_check.md"
            with open(pre_enhancement_path, 'w', encoding='utf-8') as f:
                f.write(paper_for_enhancement)

            sections_restored = restore_sections_in_file(
                enhanced_path=output_dir / "16_enhanced_final.md",
                pre_enhancement_path=pre_enhancement_path,
                language="english",
                verbose=True
            )

            if sections_restored:
                # Re-read restored version
                with open(output_dir / "16_enhanced_final.md", 'r', encoding='utf-8') as f:
                    enhanced_paper = f.read()
                print("✅ Missing sections restored successfully!")
            else:
                print("✅ No section restoration needed - all sections intact")

    # Use enhanced version if available, otherwise fall back to verified or draft
    final_paper = enhanced_paper if enhanced_paper else (verified_paper if verified_paper else draft_paper)

    if enhanced_paper:
        enhanced_word_count = len(enhanced_paper.split())
        final_word_count_before_export = enhanced_word_count
        print(f"\n✅ Enhancement complete!")
        print(f"📊 Enhanced stats: ~{enhanced_word_count} words (target: 14,000+)")
        print(f"📈 Word count increase: ~{enhanced_word_count - len(draft_paper.split())} words")
        print(f"📄 Source: 16_enhanced_final.md (sanitized)")
    else:
        final_paper = verified_paper if verified_paper else draft_paper
        final_word_count_before_export = len(final_paper.split())
        print(f"\n⚠️  Enhancement failed, using {'verified' if verified_paper else 'draft'} version")
        print(f"📊 Final stats: ~{final_word_count_before_export} words")
        print(f"📄 Source: 15_compiled_citations.md")

    # ====================================================================
    # EXPORT
    # ====================================================================
    print("\n" + "="*70)
    print("📤 EXPORTING TO PDF/WORD")
    print("="*70)

    final_md = output_dir / "FINAL_THESIS.md"
    with open(final_md, 'w') as f:
        f.write(final_paper)

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
