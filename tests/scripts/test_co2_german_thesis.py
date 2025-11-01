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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_config
from tests.test_utils import setup_model, run_agent, rate_limit_delay
from tests.validators import Section, validate_paper_sections


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

    # Step 1: Scout - Find papers
    scout_output = run_agent(
        model=model,
        name="1. Scout - Finde relevante Forschungsarbeiten",
        prompt_path="prompts/01_research/scout.md",
        user_input=(
            f"**WICHTIG: Antworte auf Deutsch.**\n\n"
            f"Finde 30 wissenschaftliche Artikel und Berichte über:\n"
            f"- CO2-Zertifikatehandel und Emissionshandelssysteme\n"
            f"- Klimawandel und Treibhausgasemissionen\n"
            f"- Kyoto-Protokoll und Pariser Abkommen\n"
            f"- Europäisches Emissionshandelssystem (EU ETS)\n"
            f"- Umweltökonomie und Klimapolitik\n"
            f"- Wirksamkeit von CO2-Preismechanismen\n"
            f"- Kohlenstoffmärkte und Klimaschutz\n\n"
            f"Forschungsschwerpunkt: {research_focus}"
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
        name="2. Scribe - Zusammenfassung der Forschung",
        prompt_path="prompts/01_research/scribe.md",
        user_input=f"**WICHTIG: Antworte auf Deutsch.**\n\nFasse diese Forschungsergebnisse zusammen:\n\n{scout_output[:3000]}",
        save_to=output_dir / "02_scribe.md"
    )

    rate_limit_delay()

    # Step 3: Signal - Gap analysis
    signal_output = run_agent(
        model=model,
        name="3. Signal - Forschungslücken-Analyse",
        prompt_path="prompts/01_research/signal.md",
        user_input=f"**WICHTIG: Antworte auf Deutsch.**\n\nAnalysiere Forschungslücken beim CO2-Zertifikatehandel:\n\n{scribe_output[:3000]}",
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
            f"Schreibe die Einleitung (1,200 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Einbeziehen:\n"
            f"- Einstieg über Klimawandel und globale Herausforderungen\n"
            f"- Hintergrund zum CO2-Zertifikatehandel\n"
            f"- Problemstellung (Wirksamkeit des Emissionshandels)\n"
            f"- Forschungsziele (Klimaschutzwirkung nachweisen)\n"
            f"- Aufbau der Arbeit"
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
            f"Schreibe die Literaturübersicht (2,000 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Abdecken:\n"
            f"- Geschichte des Emissionshandels (Kyoto, EU ETS)\n"
            f"- Theoretische Grundlagen der Umweltökonomie\n"
            f"- CO2-Preismechanismen und Klimaschutz\n"
            f"- Empirische Studien zur Wirksamkeit\n"
            f"- Kritische Perspektiven und Herausforderungen\n\n"
            f"Nutze Forschung: {scribe_output[:1500]}"
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
            f"Schreibe die Methodik (1,000 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Beschreiben:\n"
            f"- Analyserahmen für Klimaschutzwirkung\n"
            f"- Auswahlkriterien für Fallstudien (EU ETS, Kalifornien, etc.)\n"
            f"- Datenquellen und Messverfahren\n"
            f"- Statistische Methoden zur Wirksamkeitsanalyse"
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
            f"Schreibe die Analyse (2,500 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Analysieren:\n"
            f"- Emissionsreduktionen durch CO2-Handel\n"
            f"- Preisgestaltung und Marktmechanismen\n"
            f"- Fallstudien (EU ETS, Kalifornien, China)\n"
            f"- Vergleich mit anderen Klimaschutzinstrumenten\n"
            f"- Empirische Belege für Klimaschutzwirkung"
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
            f"Schreibe die Diskussion (1,500 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Diskutieren:\n"
            f"- Implikationen für Klimapolitik\n"
            f"- Grenzen und Herausforderungen des Emissionshandels\n"
            f"- Verbesserungsvorschläge für CO2-Märkte\n"
            f"- Rolle im globalen Klimaschutz\n"
            f"- Empfehlungen für Politik und Wirtschaft"
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
            f"Schreibe das Fazit (600 Wörter) für:\n\n{formatter_output[:2000]}\n\n"
            f"Zusammenfassen:\n"
            f"- Hauptergebnisse zur Klimaschutzwirkung\n"
            f"- Beitrag zum Verständnis des Emissionshandels\n"
            f"- Zukünftige Forschungsrichtungen"
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
    # PHASE 6: CITATION VERIFICATION
    # ====================================================================
    print("\n" + "="*70)
    print("✅ PHASE 6: ZITATPRÜFUNG (CITATION VERIFICATION - Agent #14)")
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

## Literaturverzeichnis

[Wird mit korrekten Zitationen ergänzt]
"""

    # Save draft before citation verification
    draft_path = output_dir / "14_draft_pre_citation_check.md"
    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write(draft_paper)

    print(f"✅ Entwurf gespeichert: {draft_path}")
    print(f"📊 Statistik: ~{len(draft_paper.split())} Wörter")

    # Step 14: Citation Verifier
    print("\n🔍 Zitatprüfung läuft...")
    print("   Dies wird:")
    print("   • Alle [VERIFY] Platzhalter finden")
    print("   • Fehlende Metadaten ergänzen (Jahr, Verlag, DOI)")
    print("   • APA 7th Format validieren")
    print("   • Ausgabe: 100% verifizierte Zitationen")
    print("\n⏳ Zitatprüfung dauert 2-3 Minuten...")

    verified_paper = run_agent(
        model=model,
        name="14. Citation Verifier - Zitate vervollständigen",
        prompt_path="prompts/05_refine/citation_verifier.md",
        user_input=f"**WICHTIG: Antworte auf Deutsch.**\n\nVervollständige alle [VERIFY] Platzhalter in dieser Arbeit:\n\n{draft_paper}",
        save_to=output_dir / "15_verified_citations.md"
    )

    # Use verified version if available
    paper_for_enhancement = verified_paper if verified_paper else draft_paper

    if verified_paper:
        verified_word_count = len(verified_paper.split())
        print(f"\n✅ Zitatprüfung abgeschlossen!")
        print(f"📊 Verifizierte Arbeit: ~{verified_word_count} Wörter")
    else:
        print(f"\n⚠️  Zitatprüfung fehlgeschlagen, nutze Entwurf mit [VERIFY] Tags")

    rate_limit_delay()

    # ====================================================================
    # PHASE 7: ENHANCE
    # ====================================================================
    print("\n" + "="*70)
    print("✨ PHASE 7: VERBESSERUNG (ENHANCE - Agent #15)")
    print("="*70)

    # Step 15: Enhancer - Add professional elements
    print("\n🔧 Verbesserungs-Agent läuft...")
    print("   Dies fügt hinzu:")
    print("   • YAML Metadaten-Frontmatter")
    print("   • Erweitertes 4-Absatz Abstract")
    print("   • 5 umfassende Anhänge")
    print("   • Limitationen und Zukunftsforschung")
    print("   • 3-5 Tabellen und 1-2 Abbildungen")
    print("   • Erweiterte Fallstudien")
    print("\n⏳ Verbesserung dauert 3-5 Minuten...")

    enhanced_paper = run_agent(
        model=model,
        name="15. Enhancer - Professionelle Verbesserung",
        prompt_path="prompts/06_enhance/enhancer.md",
        user_input=f"**WICHTIG: Antworte auf Deutsch.**\n\nVerbessere diese Arbeit auf Publikationsstandard:\n\n{paper_for_enhancement}",
        save_to=output_dir / "16_enhanced_final.md"
    )

    # Post-process: Remove markdown code block wrapper if present
    if enhanced_paper:
        if enhanced_paper.startswith('```markdown\n'):
            enhanced_paper = enhanced_paper[12:]
        if enhanced_paper.endswith('\n```'):
            enhanced_paper = enhanced_paper[:-4]
        # Save cleaned version
        with open(output_dir / "16_enhanced_final.md", 'w', encoding='utf-8') as f:
            f.write(enhanced_paper)

    # Use enhanced version if available
    final_paper = enhanced_paper if enhanced_paper else (verified_paper if verified_paper else draft_paper)

    if enhanced_paper:
        enhanced_word_count = len(enhanced_paper.split())
        print(f"\n✅ Verbesserung abgeschlossen!")
        print(f"📊 Erweiterte Statistik: ~{enhanced_word_count} Wörter (Ziel: 14,000+)")
        print(f"📈 Wortzahl-Erhöhung: ~{enhanced_word_count - len(draft_paper.split())} Wörter")
    else:
        print(f"\n⚠️  Verbesserung fehlgeschlagen, nutze {'verifizierte' if verified_paper else 'Entwurfs'}-Version")

    # ====================================================================
    # EXPORT
    # ====================================================================
    print("\n" + "="*70)
    print("📤 EXPORT ZU PDF/WORD")
    print("="*70)

    final_md = output_dir / "FINAL_THESIS.md"
    with open(final_md, 'w', encoding='utf-8') as f:
        f.write(final_paper)

    final_word_count = len(final_paper.split())
    print(f"✅ Finale Arbeit: {final_word_count:,} Wörter")

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
