#!/usr/bin/env python3
"""
ABOUTME: Citation validation utility for thesis generation pipeline
ABOUTME: Validates that Agent #14 successfully removed all [VERIFY] placeholders
"""

from typing import Dict, List, Tuple


def validate_citation_verification(
    verified_paper: str,
    language: str = "english"
) -> Dict[str, any]:
    """
    Validate that citation verification completed successfully.

    Checks if any [VERIFY] placeholders remain after Agent #14 runs.
    Returns detailed information about remaining placeholders for debugging.

    Args:
        verified_paper: Thesis text after Agent #14 verification
        language: Thesis language ('english', 'german', 'spanish', 'french')

    Returns:
        dict with:
            - success: bool (True if no [VERIFY] tags remain)
            - count: int (number of [VERIFY] placeholders found)
            - locations: list of (line_num, line_text) tuples (first 10)

    Example:
        >>> result = validate_citation_verification(thesis_text, language='german')
        >>> if not result['success']:
        ...     print(f"⚠️  {result['count']} [VERIFY] tags remain!")
        ...     for line_num, line in result['locations']:
        ...         print(f"  Line {line_num}: {line[:80]}...")
    """
    # Count [VERIFY] placeholders
    verify_count = verified_paper.count('[VERIFY]')

    # Extract locations (line number and text) for first 10
    locations = []
    if verify_count > 0:
        lines_with_verify = [
            (i + 1, line.strip())
            for i, line in enumerate(verified_paper.split('\n'))
            if '[VERIFY]' in line
        ]
        locations = lines_with_verify[:10]  # Limit to first 10

    return {
        'success': verify_count == 0,
        'count': verify_count,
        'locations': locations,
        'language': language
    }


def print_validation_report(
    result: Dict[str, any],
    verbose: bool = True
) -> None:
    """
    Print formatted validation report.

    Args:
        result: Dict from validate_citation_verification()
        verbose: If True, show detailed locations

    Example:
        >>> result = validate_citation_verification(thesis)
        >>> print_validation_report(result)
    """
    # Language-specific messages
    messages = {
        'english': {
            'success': "✅ All [VERIFY] placeholders successfully removed!",
            'warning': "⚠️  WARNING: {count} [VERIFY] placeholders remain!",
            'locations': "📍 Locations:",
            'incomplete': "⚠️  Citation verification INCOMPLETE - manual review required"
        },
        'german': {
            'success': "✅ Alle [VERIFY] Platzhalter erfolgreich entfernt!",
            'warning': "⚠️  WARNUNG: {count} [VERIFY] Platzhalter verbleiben!",
            'locations': "📍 Fundorte:",
            'incomplete': "⚠️  Zitatprüfung UNVOLLSTÄNDIG - manuelle Überprüfung erforderlich"
        },
        'spanish': {
            'success': "✅ Todos los marcadores [VERIFY] eliminados exitosamente!",
            'warning': "⚠️  ADVERTENCIA: {count} marcadores [VERIFY] permanecen!",
            'locations': "📍 Ubicaciones:",
            'incomplete': "⚠️  Verificación de citas INCOMPLETA - revisión manual requerida"
        },
        'french': {
            'success': "✅ Tous les marqueurs [VERIFY] supprimés avec succès!",
            'warning': "⚠️  ATTENTION: {count} marqueurs [VERIFY] restent!",
            'locations': "📍 Emplacements:",
            'incomplete': "⚠️  Vérification des citations INCOMPLÈTE - révision manuelle requise"
        }
    }

    lang = result.get('language', 'english')
    msg = messages.get(lang, messages['english'])

    if result['success']:
        print(f"\n{msg['success']}")
    else:
        print(f"\n{msg['warning'].format(count=result['count'])}")

        if verbose and result['locations']:
            print(f"\n{msg['locations']}")
            for line_num, line in result['locations']:
                preview = line[:100] + "..." if len(line) > 100 else line
                print(f"  Line {line_num}: {preview}")

            print(f"\n{msg['incomplete']}")
