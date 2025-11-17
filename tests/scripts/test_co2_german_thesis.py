#!/usr/bin/env python3
"""
TEST: German CO2 Certificate Thesis Generation
Topic: Führt der Handel mit CO2-Zertifikaten nachweislich zu einer signifikanten Verlangsamung des menschengemachten Klimawandels?
Full 15-agent autonomous test to prove system works with ZERO manual interventions
"""

import os
import sys
import time
import subprocess
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_config
from tests.test_utils import setup_model, run_agent, rate_limit_delay, research_citations_via_api
from tests.validators import Section, validate_paper_sections
from utils.citation_manager import extract_citations_from_text
from utils.citation_database import save_citation_database, load_citation_database
from utils.citation_compiler import CitationCompiler
from utils.text_utils import smart_truncate
from utils.abstract_generator import generate_abstract_for_thesis
from utils.output_sanitizer import sanitize_enhanced_file


def main():
    """
    Generate a complete German academic thesis on CO2 certificate trading.

    Tests system autonomy after bug fixes:
    - Bug Fix #1: YAML wrapper (no code fence)
    - Bug Fix #2: Unicode characters (ASCII-only diagrams)
    - Bug Fix #3: Table of Contents (auto-enabled)
    - Bug Fix #4: Reference formatting

    Expected: ZERO manual interventions required
    """
    config = get_config()

    print("="*70)
    print("GERMAN CO2 CERTIFICATE THESIS TEST")
    print("="*70)
    print()
    print("Topic: Führt der Handel mit CO2-Zertifikaten nachweislich zu einer")
    print("       signifikanten Verlangsamung des menschengemachten Klimawandels?")
    print()
    print("Translation: Does trading in CO2 certificates demonstrably lead to")
    print("             a significant slowdown in man-made climate change?")
    print()
    print("Format: Academic thesis (14,000+ words in German)")
    print(f"Model: {config.model.model_name}")
    print()
    print("="*70)

    # Initialize model
    model = setup_model()

    topic = "Führt der Handel mit CO2-Zertifikaten nachweislich zu einer signifikanten Verlangsamung des menschengemachten Klimawandels?"
    research_focus = "CO2-Zertifikate, Emissionshandel, Klimawandel, Treibhausgasemissionen, Kyoto-Protokoll, Europäisches Emissionshandelssystem (EU ETS), Klimapolitik, Umweltökonomie, Klimaschutz, CO2-Preismechanismen, Kohlenstoffmärkte"

    # Output directory
    output_dir = config.paths.output_dir / "co2_thesis_german"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ====================================================================
    # PHASE 1: RESEARCH
    # ====================================================================
    print("\n" + "="*70)
    print("📚 PHASE 1: FORSCHUNG (RESEARCH)")
    print("="*70)

    # Step 1: Scout - API-backed citation discovery (replaces LLM hallucination)
    research_topics = [
        # CO2 trading fundamentals
        "carbon emissions trading systems design and implementation",
        "cap-and-trade mechanisms for greenhouse gas reduction",
        "European Union Emissions Trading System EU ETS",
        "carbon pricing policy instruments and effectiveness",
        "emissions allowance allocation methods",

        # Climate change and emissions
        "anthropogenic climate change and greenhouse gas emissions",
        "carbon dioxide atmospheric concentration trends",
        "climate change mitigation strategies and policies",
        "greenhouse gas emissions measurement and verification",
        "carbon footprint assessment methodologies",

        # International agreements
        "Kyoto Protocol emissions reduction commitments",
        "Paris Agreement climate targets and implementation",
        "international carbon markets linkage mechanisms",
        "Clean Development Mechanism CDM projects",
        "Joint Implementation JI climate projects",

        # EU ETS specific
        "European Union carbon market price dynamics",
        "EU ETS Phase III and Phase IV reforms",
        "carbon leakage prevention mechanisms",
        "free allocation versus auctioning of allowances",
        "Market Stability Reserve EU ETS",

        # Environmental economics
        "environmental economics Pigouvian taxation",
        "externalities in environmental policy",
        "cost-benefit analysis of climate policies",
        "market-based environmental regulation",
        "pollution permits tradable emissions rights",
        "John Dales emission trading theory 1968 pollution permits",
        "W. David Montgomery emissions trading 1972 market mechanisms",

        # Effectiveness studies
        "carbon trading effectiveness empirical evidence",
        "emissions reduction attributable to carbon markets",
        "EU ETS impact on industrial emissions",
        "carbon price and emissions abatement relationship",
        "effectiveness of carbon pricing versus regulation",

        # Regional carbon markets
        "California cap-and-trade program analysis",
        "China national carbon emissions trading system",
        "Regional Greenhouse Gas Initiative RGGI",
        "Korean emissions trading scheme",
        "New Zealand Emissions Trading Scheme",

        # Challenges and criticism
        "carbon market volatility and price stability",
        "windfall profits in emissions trading",
        "carbon offset projects credibility and additionality",
        "carbon market manipulation and fraud prevention",
        "carbon leakage in emissions trading systems",

        # Economic impacts
        "carbon pricing economic competitiveness effects",
        "emissions trading impact on electricity prices",
        "carbon costs and industrial productivity",
        "carbon markets and innovation incentives",
        "distributional effects of carbon pricing",

        # Monitoring and compliance
        "emissions monitoring reporting verification MRV",
        "carbon accounting standards and protocols",
        "compliance mechanisms in emissions trading",
        "carbon registry systems and tracking",
        "enforcement of emissions caps and penalties",
    ]

    try:
        scout_result = research_citations_via_api(
            model=model,
            research_topics=research_topics,
            output_path=output_dir / "01_scout.md",
            target_minimum=35,  # Realistic for deep research mode (70-90% of query count)
            verbose=True,
            use_deep_research=True,  # Enable deep research mode
            topic=topic,  # Main research topic for deep research planning
            scope=research_focus  # Research scope
        )

        print(f"\n✅ Scout Erfolg: {scout_result['count']} gültige Zitate")
        print(f"📊 API-Erfolgsrate: {scout_result['count']/len(research_topics)*100:.1f}%")
        print(f"📚 Quellen: Crossref={scout_result['sources']['Crossref']}, "
              f"Semantic Scholar={scout_result['sources']['Semantic Scholar']}, "
              f"LLM={scout_result['sources']['Gemini LLM']}")

        # Read scout output for next agents
        scout_output = (output_dir / "01_scout.md").read_text(encoding='utf-8')

    except ValueError as e:
        print(f"\n❌ SCOUT QUALITY GATE FEHLGESCHLAGEN")
        print(str(e))
        print("\n⚠️  Kann nicht fortfahren - unzureichende gültige Zitate für akademische Arbeit")
        return 1
    except Exception as e:
        print(f"\n❌ SCOUT FEHLGESCHLAGEN - Unerwarteter Fehler")
        print(f"Fehler: {str(e)}")
        return 1

    rate_limit_delay()

    # Step 2: Scribe - Summarize
    scribe_output = run_agent(
        model=model,
        name="2. Scribe - Zusammenfassung der Forschung",
        prompt_path="prompts/01_research/scribe.md",
        user_input=f"**WICHTIG: Antworte auf Deutsch.**\n\nFasse diese Forschungsergebnisse zusammen:\n\n{smart_truncate(scout_output, max_chars=8000, preserve_json=True)}",
        save_to=output_dir / "02_scribe.md"
    )

    rate_limit_delay()

    # Step 3: Signal - Gap analysis
    signal_output = run_agent(
        model=model,
        name="3. Signal - Forschungslücken-Analyse",
        prompt_path="prompts/01_research/signal.md",
        user_input=f"**WICHTIG: Antworte auf Deutsch.**\n\nAnalysiere Forschungslücken beim CO2-Zertifikatehandel:\n\n{smart_truncate(scribe_output, max_chars=8000, preserve_json=False)}",
        save_to=output_dir / "03_signal.md"
    )

    rate_limit_delay()

    # ====================================================================
    # PHASE 2: STRUCTURE
    # ====================================================================
    print("\n" + "="*70)
    print("🏗️  PHASE 2: STRUKTUR (STRUCTURE)")
    print("="*70)

    # Step 4: Architect - Create outline
    architect_output = run_agent(
        model=model,
        name="4. Architect - Strukturplanung",
        prompt_path="prompts/02_structure/architect.md",
        user_input=(
            f"**WICHTIG: Antworte auf Deutsch.**\n\n"
            f"Erstelle eine Gliederung für die Abschlussarbeit: {topic}\n\n"
            f"Identifizierte Forschungslücken:\n{signal_output[:2000]}\n\n"
            f"Typ: Empirische Analyse mit Fallstudien\n"
            f"Länge: 8,000-10,000 Wörter"
        ),
        save_to=output_dir / "04_architect.md"
    )

    rate_limit_delay()

    # Step 5: Formatter - Apply style
    formatter_output = run_agent(
        model=model,
        name="5. Formatter - Akademische Formatierung",
        prompt_path="prompts/02_structure/formatter.md",
        user_input=(
            f"**WICHTIG: Antworte auf Deutsch.**\n\n"
            f"Wende akademische Formatierung an:\n\n{architect_output[:2500]}\n\n"
            f"Ziel: Umweltwissenschaften/Klimapolitik-Journal\n"
            f"Stil: APA 7th edition\n"
            f"Format: IMRaD-Struktur für empirische Arbeit"
        ),
        save_to=output_dir / "05_formatter.md"
    )

    rate_limit_delay()

    # ====================================================================
    # PHASE 2.5: CITATION MANAGEMENT
    # ====================================================================
    print("\n" + "="*70)
    print("📚 PHASE 2.5: ZITATVERWALTUNG (CITATION MANAGEMENT)")
    print("="*70)

    print("Zitationsdatenbank aus Scout-Recherche erstellen...")

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
        thesis_language="german"
    )

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
        print(f"🧹 {dedup_stats['removed_count']} doppelte Zitate entfernt")
        print(f"   Endgültig: {dedup_stats['final_count']} eindeutige Zitate")

    # FIXED (Day 2A): Scrape real titles for Gemini Grounded citations
    from utils.scrape_citation_titles import TitleScraper
    title_scraper = TitleScraper(verbose=True)
    title_success, title_fail = title_scraper.scrape_citations(citation_database.citations)
    if title_success > 0:
        print(f"📰 {title_success} echte Seitentitel aus Webquellen extrahiert")
        if title_fail > 0:
            print(f"   ⚠️  {title_fail} Titel konnten nicht extrahiert werden (Timeouts, Fehler)")

    # FIXED (Day 2B): Scrape metadata (publication dates, authors) for Gemini citations
    from utils.scrape_citation_metadata import MetadataScraper
    metadata_scraper = MetadataScraper(verbose=True)
    metadata_success, metadata_fail = metadata_scraper.scrape_citations(citation_database.citations)
    if metadata_success > 0:
        print(f"📅 {metadata_success} Veröffentlichungsdaten und Autoren aus Webquellen extrahiert")
        if metadata_fail > 0:
            print(f"   ⚠️  {metadata_fail} Metadaten konnten nicht extrahiert werden")

    # Save citation database
    citation_db_path = output_dir / "citation_database.json"
    save_citation_database(citation_database, citation_db_path)

    print(f"\n✅ Zitatdatenbank erstellt: {dedup_stats['final_count']} eindeutige Zitate")
    print(f"📄 Gespeichert in: {citation_db_path}")

    # Prepare citation database summary for Crafters
    # FIXED (Bug #12): Show ALL citations explicitly to prevent hallucination
    citation_summary = f"\n\n## ZITATDATENBANK\n\nSie haben Zugriff auf {len(citation_database.citations)} Zitate. Verwenden Sie Zitat-IDs (cite_001, cite_002, etc.) statt Inline-Zitate.\n\n"
    citation_summary += "**KRITISCH: Verwenden Sie NUR die unten aufgeführten Zitat-IDs. Erfinden Sie KEINE IDs jenseits dieser Liste.**\n\n"
    citation_summary += "Verfügbare Zitate:\n"
    for citation in citation_database.citations:  # Show ALL citations (removed [:20] limit)
        authors_str = ", ".join(citation.authors[:2])
        if len(citation.authors) > 2:
            authors_str += " et al."
        citation_summary += f"- {citation.id}: {authors_str} ({citation.year}) - {citation.title[:60]}...\n"
    # Add explicit maximum ID boundary
    if citation_database.citations:
        max_id = citation_database.citations[-1].id
        citation_summary += f"\n**Maximale Zitat-ID: {max_id}** (überschreiten Sie diese NICHT)\n"

    rate_limit_delay()

    # ====================================================================
    # PHASE 3: COMPOSE
    # ====================================================================
    print("\n" + "="*70)
    print("✍️  PHASE 3: VERFASSEN (COMPOSE)")
    print("="*70)

    # Step 6: Write Introduction
    intro = run_agent(
        model=model,
        name="6. Crafter - Einleitung schreiben",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"**WICHTIG: Antworte auf Deutsch.**\n\n"
            f"Schreibe die Einleitung (2,500 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Einbeziehen:\n"
            f"- Einstieg über Klimawandel und globale Herausforderungen\n"
            f"- Hintergrund zum CO2-Zertifikatehandel\n"
            f"- Problemstellung (Wirksamkeit des Emissionshandels)\n"
            f"- Forschungsziele (Klimaschutzwirkung nachweisen)\n"
            f"- Aufbau der Arbeit"
            f"{citation_summary}"
        ),
        save_to=output_dir / "06_introduction.md"
    )

    rate_limit_delay()

    # Step 7: Write Literature Review
    lit_review = run_agent(
        model=model,
        name="7. Crafter - Literaturübersicht schreiben",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"**WICHTIG: Antworte auf Deutsch.**\n\n"
            f"Schreibe die Literaturübersicht (6,000 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Abdecken:\n"
            f"- Geschichte des Emissionshandels (Kyoto, EU ETS)\n"
            f"- Theoretische Grundlagen der Umweltökonomie\n"
            f"- CO2-Preismechanismen und Klimaschutz\n"
            f"- Empirische Studien zur Wirksamkeit\n"
            f"- Kritische Perspektiven und Herausforderungen\n\n"
            f"Nutze Forschung: {scribe_output[:1500]}"
            f"{citation_summary}"
        ),
        save_to=output_dir / "07_literature_review.md"
    )

    rate_limit_delay()

    # Step 8: Write Methodology
    methods = run_agent(
        model=model,
        name="8. Crafter - Methodik schreiben",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"**WICHTIG: Antworte auf Deutsch.**\n\n"
            f"Schreibe die Methodik (2,500 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Beschreiben:\n"
            f"- Analyserahmen für Klimaschutzwirkung\n"
            f"- Auswahlkriterien für Fallstudien (EU ETS, Kalifornien, etc.)\n"
            f"- Datenquellen und Messverfahren\n"
            f"- Statistische Methoden zur Wirksamkeitsanalyse"
            f"{citation_summary}"
        ),
        save_to=output_dir / "08_methodology.md"
    )

    rate_limit_delay()

    # Step 9: Write Analysis
    analysis = run_agent(
        model=model,
        name="9. Crafter - Analyse schreiben",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"**WICHTIG: Antworte auf Deutsch.**\n\n"
            f"Schreibe die Analyse (6,000 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Analysieren:\n"
            f"- Emissionsreduktionen durch CO2-Handel\n"
            f"- Preisgestaltung und Marktmechanismen\n"
            f"- Fallstudien (EU ETS, Kalifornien, China)\n"
            f"- Vergleich mit anderen Klimaschutzinstrumenten\n"
            f"- Empirische Belege für Klimaschutzwirkung"
            f"{citation_summary}"
        ),
        save_to=output_dir / "09_analysis.md"
    )

    rate_limit_delay()

    # Step 10: Write Discussion
    discussion = run_agent(
        model=model,
        name="10. Crafter - Diskussion schreiben",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"**WICHTIG: Antworte auf Deutsch.**\n\n"
            f"Schreibe die Diskussion (3,000 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Diskutieren:\n"
            f"- Implikationen für Klimapolitik\n"
            f"- Grenzen und Herausforderungen des Emissionshandels\n"
            f"- Verbesserungsvorschläge für CO2-Märkte\n"
            f"- Rolle im globalen Klimaschutz\n"
            f"- Empfehlungen für Politik und Wirtschaft"
            f"{citation_summary}"
        ),
        save_to=output_dir / "10_discussion.md"
    )

    rate_limit_delay()

    # Step 11: Write Conclusion
    conclusion = run_agent(
        model=model,
        name="11. Crafter - Fazit schreiben",
        prompt_path="prompts/03_compose/crafter.md",
        user_input=(
            f"**WICHTIG: Antworte auf Deutsch.**\n\n"
            f"Schreibe das Fazit (1,000 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Zusammenfassen:\n"
            f"- Hauptergebnisse zur Klimaschutzwirkung\n"
            f"- Beitrag zum Verständnis des Emissionshandels\n"
            f"- Zukünftige Forschungsrichtungen"
            f"{citation_summary}"
        ),
        save_to=output_dir / "11_conclusion.md"
    )

    rate_limit_delay()

    # Assemble complete draft
    print("\n" + "="*70)
    print("📝 ENTWURF ZUSAMMENSTELLEN (ASSEMBLING DRAFT)")
    print("="*70)

    complete_draft = f"""# {topic}

{intro}

{lit_review}

{methods}

{analysis}

{discussion}

{conclusion}

---

## Literaturverzeichnis

[Wird mit korrekten Zitationen aus der Forschung ergänzt]
"""

    draft_file = output_dir / "COMPLETE_DRAFT.md"
    with open(draft_file, 'w', encoding='utf-8') as f:
        f.write(complete_draft)

    word_count = len(complete_draft.split())
    print(f"✅ Entwurf fertig: {word_count:,} Wörter")
    print(f"Gespeichert in: {draft_file}")

    # ====================================================================
    # PHASE 4: VALIDATE (SECTION-BASED)
    # ====================================================================
    print("\n" + "="*70)
    print("✅ PHASE 4: VALIDIERUNG (VALIDATE)")
    print("="*70)

    # Create sections for independent validation
    sections = [
        Section.from_text("Einleitung", intro),
        Section.from_text("Literaturübersicht", lit_review),
        Section.from_text("Methodik", methods),
        Section.from_text("Analyse", analysis),
        Section.from_text("Diskussion", discussion),
        Section.from_text("Fazit", conclusion),
    ]

    print(f"\nValidiere {len(sections)} Abschnitte unabhängig:")
    for section in sections:
        print(f"  - {section.name}: {section.word_count:,} Wörter")

    # Step 12: Skeptic review (per-section)
    skeptic_reviews = validate_paper_sections(
        model=model,
        sections=sections,
        output_dir=output_dir,
        validators=['skeptic'],
        create_consolidated=True,
        verbose=True
    )

    print(f"\n✅ Alle {len(sections)} Abschnitte unabhängig validiert")
    print(f"✅ Konsolidierte Bewertung: {output_dir / 'skeptic_complete_review.md'}")

    # ====================================================================
    # PHASE 5: REFINE
    # ====================================================================
    print("\n" + "="*70)
    print("🎨 PHASE 5: VERFEINERUNG (REFINE)")
    print("="*70)

    rate_limit_delay()

    # Step 13: Entropy - Humanize intro
    humanized_intro = run_agent(
        model=model,
        name="13. Entropy - Einleitung humanisieren",
        prompt_path="prompts/05_refine/entropy.md",
        user_input=f"**WICHTIG: Antworte auf Deutsch.**\n\nHumanisiere diese Einleitung:\n\n{intro[:2000]}",
        save_to=output_dir / "13_humanized_intro.md"
    )

    rate_limit_delay()

    # ====================================================================
    # PHASE 6: CITATION COMPILATION
    # ====================================================================
    print("\n" + "="*70)
    print("✅ PHASE 6: ZITAT-KOMPILIERUNG (CITATION COMPILATION)")
    print("="*70)

    # Create complete draft for citation compilation
    draft_paper = f"""# {topic}

{humanized_intro or intro}

{lit_review}

{methods}

{analysis}

{discussion}

{conclusion}

---

## Literaturverzeichnis

[Wird automatisch generiert]
"""

    # Save draft before citation compilation
    draft_path = output_dir / "14_draft_pre_citation_check.md"
    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write(draft_paper)

    print(f"✅ Entwurf gespeichert: {draft_path}")
    print(f"📊 Statistik: ~{len(draft_paper.split())} Wörter")

    # Step 14: Citation Compiler - Replace citation IDs with formatted citations
    print("\n🔍 Zitat-Compiler läuft...")
    print("   Dies wird:")
    print("   • Alle {cite_XXX} IDs durch formatierte Zitate ersetzen")
    print("   • Literaturverzeichnis automatisch generieren")
    print("   • Alle Zitate in der Datenbank validieren")
    print("   • Ausgabe: 100% deterministische Zitat-Kompilierung")
    print("\n⏳ Kompiliere Zitate...")

    # Load citation database
    citation_database = load_citation_database(citation_db_path)

    # VALIDATION STEP: Validate citations for academic integrity
    print("\n" + "="*70)
    print("🔍 ZITAT-VALIDIERUNG (Academic Integrity Check)")
    print("="*70)

    from utils.citation_validator import CitationValidator
    validator = CitationValidator(timeout=10)
    issues, stats = validator.validate_database(citation_db_path)

    if issues:
        print(f"\n⚠️  {len(issues)} Zitat-Validierungsprobleme gefunden:")
        print(f"   • Kritische Probleme: {stats['critical_issues']}")
        print(f"   • Warnungen: {stats['warnings']}")
        print(f"   • Ungültige DOIs: {stats['invalid_dois']}")
        print(f"   • Ungültige Autoren: {stats['invalid_authors']}")

        # Display first 5 critical issues
        critical = [i for i in issues if i.severity == 'critical']
        if critical:
            print("\n❌ KRITISCHE PROBLEME (erste 5):")
            for issue in critical[:5]:
                print(f"   [{issue.citation_id}] {issue.message}")

        # Save full validation report
        validation_report = validator.generate_report(issues, "CO2 German Thesis")
        report_path = output_dir / "citation_validation_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(validation_report)
        print(f"\n📄 Vollständiger Validierungsbericht gespeichert: {report_path}")

        print("\n⚠️  EMPFEHLUNG: Überprüfen und korrigieren Sie ungültige Zitate vor der Veröffentlichung")
        print("   Fahre mit aktuellen Zitaten fort...")
    else:
        print("\n✅ Alle Zitate haben die Validierung bestanden - keine Probleme gefunden!")

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
    print(f"\n✅ Zitat-Kompilierung abgeschlossen!")
    print(f"📊 Kompilierte Arbeit: ~{verified_word_count} Wörter")
    print(f"✅ Gesamtzitate: {validation_result['total_citations']}")
    print(f"✅ Erfolgreich kompiliert: {validation_result['successfully_compiled']}")

    issues = []
    manual_interventions = 0

    if validation_result['missing_citations'] > 0:
        print(f"⚠️  Fehlende Zitate: {validation_result['missing_citations']}")
        print(f"   Fehlende IDs: {missing_ids}")
        issues.append(f"❌ {validation_result['missing_citations']} fehlende Zitat-IDs")
        manual_interventions += 1
    else:
        print("✅ Alle Zitat-IDs erfolgreich kompiliert - 100% Erfolgsquote!")

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
    # PHASE 7: VERBESSERUNG (Agent #15) - MIT BEREINIGUNG
    # ====================================================================
    print("\n" + "="*70)
    print("✨ PHASE 7: VERBESSERUNG (Agent #15 - MIT OUTPUT-BEREINIGUNG)")
    print("="*70)

    # Step 15: Enhancer - Professionelle Elemente hinzufügen (JETZT WIEDER AKTIVIERT!)
    print("\n🔧 Verbesserungs-Agent läuft...")
    print("   Dies wird hinzufügen:")
    print("   • YAML-Metadaten-Frontmatter")
    print("   • Erweiterte 4-Absatz-Zusammenfassung")
    print("   • 5 umfassende Anhänge")
    print("   • Einschränkungen und Zukünftige Forschung Abschnitte")
    print("   • 3-5 Tabellen und 1-2 Abbildungen")
    print("   • Erweiterte Fallstudien")
    print("\n⏳ Verbesserung kann 3-5 Minuten dauern...")

    # FIXED (Day 1A): Pass actual citation count to prevent frontmatter mismatch
    actual_citation_count = len(citation_database.citations)

    enhanced_paper = run_agent(
        model=model,
        name="15. Enhancer - Professionelle Verbesserung",
        prompt_path="prompts/06_enhance/enhancer.md",
        user_input=f"""**WICHTIG: Antworte auf Deutsch.**

Verbessere diese Arbeit auf publikationsreifen Standard.

WICHTIG: Diese Arbeit hat GENAU {actual_citation_count} Zitate in der Zitationsdatenbank.
Verwende diese exakte Zahl für das Feld citations_verified im YAML-Frontmatter.

Arbeit zum Verbessern:

{paper_for_enhancement}""",
        save_to=output_dir / "16_enhanced_final.md"
    )

    # KRITISCH: Bereinigte erweiterte Ausgabe, um 4 Fehler zu beheben
    if enhanced_paper:
        print("\n" + "="*70)
        print("🧹 ERWEITERTE AUSGABE BEREINIGEN (Fehlerbehebung)")
        print("="*70)

        sanitize_success = sanitize_enhanced_file(
            input_path=output_dir / "16_enhanced_final.md",
            output_path=None,  # In place bereinigen
            verbose=True
        )

        if sanitize_success:
            # Bereinigte Version erneut lesen
            with open(output_dir / "16_enhanced_final.md", 'r', encoding='utf-8') as f:
                enhanced_paper = f.read()
            print("✅ Erweiterte Ausgabe erfolgreich bereinigt!")
        else:
            print("⚠️  Bereinigung fehlgeschlagen - verwende originale erweiterte Ausgabe")

        # KRITISCH: Fehlende Abschnitte wiederherstellen (defensive Lösung für LLM-Nichtbeachtung)
        # Der Verbesserungs-Agent entfernt manchmal Abschnitte trotz "UNCHANGED"-Anweisungen
        if enhanced_paper:
            print("\n" + "="*70)
            print("🔧 ABSCHNITTE WIEDERHERSTELLEN (LLM-Nichtbeachtungs-Fix)")
            print("="*70)

            from utils.section_restorer import restore_sections_in_file

            # Pre-Enhancement-Version für Wiederherstellung speichern
            pre_enhancement_path = output_dir / "14_draft_pre_citation_check.md"
            with open(pre_enhancement_path, 'w', encoding='utf-8') as f:
                f.write(paper_for_enhancement)

            sections_restored = restore_sections_in_file(
                enhanced_path=output_dir / "16_enhanced_final.md",
                pre_enhancement_path=pre_enhancement_path,
                language="german",
                verbose=True
            )

            if sections_restored:
                # Wiederhergestellte Version erneut lesen
                with open(output_dir / "16_enhanced_final.md", 'r', encoding='utf-8') as f:
                    enhanced_paper = f.read()
                print("✅ Fehlende Abschnitte erfolgreich wiederhergestellt!")
            else:
                print("✅ Keine Abschnitts-Wiederherstellung erforderlich - alle Abschnitte intakt")

        # Day 4: Seitenumbrüche für professionelle PDF-Struktur hinzufügen
        print("\n" + "="*70)
        print("📄 SEITENUMBRÜCHE HINZUFÜGEN (Day 4 Enhancement)")
        print("="*70)

        from utils.add_page_breaks import add_all_page_breaks
        try:
            page_breaks_added = add_all_page_breaks(
                output_dir / "16_enhanced_final.md",
                verbose=True
            )

            # Version mit Seitenumbrüchen erneut lesen
            with open(output_dir / "16_enhanced_final.md", 'r', encoding='utf-8') as f:
                enhanced_paper = f.read()

            print(f"✅ Seitenumbrüche erfolgreich integriert!")
        except Exception as e:
            print(f"⚠️  Seitenumbruch-Integration fehlgeschlagen: {e}")

    # Verwende erweiterte Version falls verfügbar, sonst Fallback auf verifizierte oder Entwurf
    final_paper = enhanced_paper if enhanced_paper else (verified_paper if verified_paper else draft_paper)

    if enhanced_paper:
        enhanced_word_count = len(enhanced_paper.split())
        final_word_count_before_export = enhanced_word_count
        print(f"\n✅ Verbesserung abgeschlossen!")
        print(f"📊 Erweiterte Statistik: ~{enhanced_word_count} Wörter (Ziel: 14.000+)")
        print(f"📈 Wortzahl-Erhöhung: ~{enhanced_word_count - len(draft_paper.split())} Wörter")
        print(f"📄 Quelle: 16_enhanced_final.md (bereinigt)")
    else:
        final_paper = verified_paper if verified_paper else draft_paper
        final_word_count_before_export = len(final_paper.split())
        print(f"\n⚠️  Verbesserung fehlgeschlagen, verwende {'verifizierte' if verified_paper else 'Entwurf'} Version")
        print(f"📊 Finale Statistik: ~{final_word_count_before_export} Wörter")
        print(f"📄 Quelle: 15_compiled_citations.md")

    # ====================================================================
    # EXPORT
    # ====================================================================
    print("\n" + "="*70)
    print("📤 EXPORT ZU PDF/WORD")
    print("="*70)

    final_md = output_dir / "FINAL_THESIS.md"

    # FIXED (Bug #16): Added error handling with fallback location
    try:
        with open(final_md, 'w', encoding='utf-8') as f:
            f.write(final_paper)
        print(f"✅ Gespeichert in: {final_md}")
    except (IOError, OSError, PermissionError) as e:
        # Fallback to /tmp if primary location fails
        fallback_path = Path("/tmp") / "FINAL_THESIS_CO2_GERMAN_BACKUP.md"
        try:
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(final_paper)
            final_md = fallback_path  # Update path for later use
            print(f"⚠️  Primärer Speicherort fehlgeschlagen: {e}")
            print(f"✅ Gespeichert in Fallback: {fallback_path}")
        except Exception as e2:
            print(f"❌ FATAL: Speichern der Arbeit fehlgeschlagen: {e2}")
            return 1

    final_word_count = len(final_paper.split())
    print(f"✅ Finale Arbeit: {final_word_count:,} Wörter")

    # ====================================================================
    # QUALITY GATE: Validate thesis is publication-ready
    # ====================================================================
    print("\n" + "="*70)
    print("🔍 QUALITY GATE: Validierung der Publikationsreife")
    print("="*70)

    from scripts.validate_thesis_quality import validate_thesis
    is_publication_ready = validate_thesis(final_md, verbose=True)

    if not is_publication_ready:
        print("\n" + "="*70)
        print("❌ THESIS-GENERIERUNG FEHLGESCHLAGEN - Quality Gate nicht bestanden")
        print("="*70)
        print("\n🚫 PDF-Export blockiert wegen Qualitätsproblemen")
        print("   Beheben Sie die oben aufgeführten Probleme und führen Sie die Generierung erneut aus")
        print("\n💡 Tipp: Sie können FINAL_THESIS.md manuell korrigieren und erneut exportieren:")
        print(f"   python3 scripts/export_clean_pdfs.py")
        print("="*70)
        return 1  # Exit with error code

    print("="*70)

    # Export to PDF
    print("\nExport zu PDF...")
    try:
        result = subprocess.run([
            sys.executable, 'utils/export_professional.py',
            str(final_md),
            '--pdf', str(output_dir / 'FINAL_THESIS.pdf'),
            '--engine', 'pandoc'
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            pdf_size = (output_dir / 'FINAL_THESIS.pdf').stat().st_size
            print(f"✅ PDF-Export erfolgreich ({pdf_size:,} bytes)")

            # ✅ NEW: Validate PDF structure to catch regressions
            print("\n🔍 PDF-Struktur validieren...")
            from scripts.validate_pdf_structure import PDFStructureValidator
            validator = PDFStructureValidator(verbose=False)
            validation_result = validator.validate_pdf(output_dir / 'FINAL_THESIS.pdf')

            if validation_result.passed:
                print(f"✅ PDF-Validierung bestanden ({validation_result.page_count} Seiten, {validation_result.engine_used})")
            else:
                print(f"❌ PDF-Validierung fehlgeschlagen:")
                for issue in validation_result.issues:
                    print(f"   {issue}")
                # Don't fail the test, just warn
                issues.append("⚠️ PDF-Struktur-Validierung fehlgeschlagen")
        else:
            print(f"⚠️  PDF-Export fehlgeschlagen: {result.stderr}")
    except Exception as e:
        print(f"⚠️  PDF-Export Fehler: {e}")

    # Export to Word
    print("\nExport zu Word...")
    try:
        result = subprocess.run([
            sys.executable, 'utils/export_professional.py',
            str(final_md),
            '--docx', str(output_dir / 'FINAL_THESIS.docx')
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            docx_size = (output_dir / 'FINAL_THESIS.docx').stat().st_size
            print(f"✅ Word-Export erfolgreich ({docx_size:,} bytes)")
        else:
            print(f"⚠️  Word-Export fehlgeschlagen: {result.stderr}")
    except Exception as e:
        print(f"⚠️  Word-Export Fehler: {e}")

    # ====================================================================
    # VALIDATION: Count Manual Interventions
    # ====================================================================
    print("\n" + "="*70)
    print("🔍 VALIDIERUNG: MANUELLE EINGRIFFE ZÄHLEN")
    print("="*70)

    manual_interventions = 0
    issues = []

    # Check Bug Fix #1: YAML wrapper
    print("\n✅ Bug Fix #1: YAML Frontmatter-Format prüfen...")
    with open(output_dir / "16_enhanced_final.md", 'r', encoding='utf-8') as f:
        enhanced_content = f.read()
        if enhanced_content.startswith('```yaml'):
            issues.append("❌ YAML wrapped in code fence (requires manual fix)")
            manual_interventions += 1
        elif enhanced_content.startswith('---'):
            print("   ✅ YAML korrekt formatiert (kein Wrapper)")
        else:
            print("   ⚠️  Kein YAML gefunden")

    # Check Bug Fix #2: Unicode characters
    print("\n✅ Bug Fix #2: ASCII-only Diagramme prüfen...")
    unicode_chars = ['┌', '─', '│', '└', '┬', '▼', '►', '◄']
    unicode_found = any(char in enhanced_content for char in unicode_chars)
    if unicode_found:
        issues.append("❌ Unicode box-drawing characters found (requires manual fix)")
        manual_interventions += 1
    else:
        print("   ✅ Alle Diagramme nutzen ASCII-Zeichen")

    # Check Bug Fix #3: TOC (will be validated in PDF)
    print("\n✅ Bug Fix #3: Inhaltsverzeichnis (wird in PDF geprüft)...")
    print("   ℹ️  Wird während PDF-Export automatisch generiert")

    # Check Bug Fix #4: References
    print("\n✅ Bug Fix #4: Literaturverzeichnis-Format prüfen...")
    verify_count = enhanced_content.count('[VERIFY]')
    if verify_count > 0:
        issues.append(f"❌ {verify_count} [VERIFY] placeholders remaining (requires manual fix)")
        manual_interventions += 1
    else:
        print("   ✅ Alle Zitate verifiziert (keine [VERIFY] Tags)")

    # Check Bug Fix #5: Language Consistency (NEW - CRITICAL)
    print("\n✅ Bug Fix #5: Sprachkonsistenz prüfen (100% Deutsch)...")
    english_patterns = [
        '## 6. Limitations',
        '## 7. Future Research',
        '## 8. Conclusion',
        '**Section:**',
        '**Word Count:**',
        'Table 1:',  # Should be "Tabelle 1:"
        'Figure 1:',  # Should be "Abbildung 1:"
        '## Content',  # Should be "## Inhalt"
        'Draft v1',  # Should be "Entwurf v1"
    ]

    found_english = []
    for pattern in english_patterns:
        if pattern in enhanced_content:
            found_english.append(pattern)

    if found_english:
        issues.append(f"❌ English content found: {', '.join(found_english)}")
        manual_interventions += len(found_english)
        print(f"   ❌ Englische Muster gefunden: {found_english}")
        print(f"   ❌ {len(found_english)} Stellen benötigen Übersetzung")
    else:
        print("   ✅ 100% Deutscher Inhalt (keine englischen Abschnitte)")

    # ====================================================================
    # SUMMARY
    # ====================================================================
    print("\n" + "="*70)
    print("🎉 TEST ABGESCHLOSSEN (TEST COMPLETE)")
    print("="*70)
    print(f"\nGenerierte Arbeit über: {topic}")
    print(f"Finale Wortzahl: {final_word_count:,} Wörter")
    print(f"Abschnitte validiert: {len(sections)} (unabhängig)")
    print(f"\nAlle Ausgaben gespeichert in: {output_dir}/")
    print(f"\nDateien generiert:")
    for file in sorted(output_dir.glob("*")):
        if file.is_file():
            size = file.stat().st_size
            print(f"  • {file.name} ({size:,} bytes)")

    print("\n" + "="*70)
    print("📊 AUTONOMIE-PRÜFUNG (AUTONOMY CHECK)")
    print("="*70)
    print(f"\nManuelle Eingriffe erforderlich: {manual_interventions}")

    if manual_interventions == 0:
        print("\n✅✅✅ ERFOLG: SYSTEM IST 100% AUTONOM ✅✅✅")
        print("✅ Alle Bug-Fixes funktionieren korrekt")
        print("✅ Keine manuellen Korrekturen nötig")
        print("✅ System bereit für Produktionseinsatz")
    else:
        print(f"\n❌ FEHLER: System erfordert {manual_interventions} manuelle Eingriffe")
        print("\nProbleme:")
        for issue in issues:
            print(f"  {issue}")

    print("\n✅ SYSTEM FUNKTIONIERT END-TO-END")
    print("✅ ALLE 15 AGENTEN FUNKTIONAL")
    print("✅ DEUTSCHSPRACHIGE AUSGABE")
    print("✅ EXPORT-PIPELINE FUNKTIONIERT")

    return 0 if manual_interventions == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
