#!/usr/bin/env python3
"""
ABOUTME: Production-grade thesis cleanup script
ABOUTME: Removes draft metadata, warnings, and checklists from final theses
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple
import argparse


class ThesisCleanup:
    """Clean up draft artifacts from thesis markdown files."""

    def __init__(self, filepath: Path, update_word_count: bool = True):
        self.filepath = filepath
        self.update_word_count = update_word_count
        self.changes_made: List[str] = []

    def read_file(self) -> str:
        """Read thesis file content."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def write_file(self, content: str) -> None:
        """Write cleaned content back to file."""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def remove_draft_metadata_sections(self, content: str) -> str:
        """Remove ## Citations Used, ## Notes for Revision, ## Word Count Breakdown sections."""
        sections_to_remove = [
            (r'^## Citations Used\n.*?(?=^##|\Z)', 'Citations Used'),
            (r'^## Notes for Revision\n.*?(?=^##|\Z)', 'Notes for Revision'),
            (r'^## Word Count Breakdown\n.*?(?=^##|\Z)', 'Word Count Breakdown'),
        ]

        original_content = content
        for pattern, section_name in sections_to_remove:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            if matches:
                self.changes_made.append(f"Removed {len(matches)} '{section_name}' sections")
            content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)

        return content

    def remove_checklist_items(self, content: str) -> str:
        """Remove all [ ] and [x] checklist items."""
        # Match lines that start with - [ ] or - [x] (with any amount of leading whitespace)
        pattern = r'^\s*-\s*\[(x| )\].*$\n?'

        matches = re.findall(pattern, content, re.MULTILINE)
        if matches:
            self.changes_made.append(f"Removed {len(matches)} checklist items")

        content = re.sub(pattern, '', content, flags=re.MULTILINE)
        return content

    def remove_critical_warnings(self, content: str) -> str:
        """Remove CRITICAL:, WARNING:, ERROR:, ALERT: messages."""
        # Match lines containing these warning markers
        patterns = [
            r'^\s*-?\s*\[(x| )\]?\s*\*\*CRITICAL:\*\*.*$\n?',
            r'^\s*-?\s*\*\*CRITICAL:\*\*.*$\n?',
            r'^\s*-?\s*\*\*WARNING:\*\*.*$\n?',
            r'^\s*-?\s*\*\*ERROR:\*\*.*$\n?',
            r'^\s*-?\s*\*\*ALERT:\*\*.*$\n?',
        ]

        total_removed = 0
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            total_removed += len(matches)
            content = re.sub(pattern, '', content, flags=re.MULTILINE)

        if total_removed > 0:
            self.changes_made.append(f"Removed {total_removed} critical warning messages")

        return content

    def remove_draft_status_markers(self, content: str) -> str:
        """Remove **Status:** Draft v1 and similar markers."""
        pattern = r'\*\*Status:\*\*\s*(?:Draft|Entwurf)\s+v\d+'

        matches = re.findall(pattern, content)
        if matches:
            self.changes_made.append(f"Removed {len(matches)} draft status markers")

        content = re.sub(pattern, '**Status:** Final', content)
        return content

    def remove_section_metadata(self, content: str) -> str:
        """Remove **Section:**, **Word Count:**, **Wortzahl:** markers."""
        patterns = [
            r'^\*\*Section:\*\*.*$\n?',
            r'^\*\*Abschnitt:\*\*.*$\n?',
            r'^\*\*Word Count:\*\*.*$\n?',
            r'^\*\*Wortzahl:\*\*.*$\n?',
        ]

        total_removed = 0
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            total_removed += len(matches)
            content = re.sub(pattern, '', content, flags=re.MULTILINE)

        if total_removed > 0:
            self.changes_made.append(f"Removed {total_removed} section metadata markers")

        return content

    def clean_up_excessive_newlines(self, content: str) -> str:
        """Replace 3+ consecutive newlines with exactly 2."""
        content = re.sub(r'\n{3,}', '\n\n', content)
        return content

    def update_yaml_word_count(self, content: str) -> Tuple[str, int]:
        """Update word count in YAML frontmatter."""
        if not self.update_word_count:
            return content, 0

        # Count actual words (excluding YAML frontmatter)
        # Split by --- to get content after frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            actual_content = parts[2]
            actual_word_count = len(actual_content.split())

            # Update word_count: or wortzahl: in YAML
            # English pattern
            pattern_en = r'(word_count:\s*")(\d+)(\s+words)'
            if re.search(pattern_en, content):
                old_count = int(re.search(pattern_en, content).group(2))
                content = re.sub(pattern_en, rf'\g<1>{actual_word_count}\g<3>', content)
                self.changes_made.append(f"Updated word count: {old_count} → {actual_word_count}")
                return content, actual_word_count

            # German pattern
            pattern_de = r'(wortzahl:\s*")(\d+)(\s+Wörter)'
            if re.search(pattern_de, content):
                old_count = int(re.search(pattern_de, content).group(2))
                content = re.sub(pattern_de, rf'\g<1>{actual_word_count}\g<3>', content)
                self.changes_made.append(f"Updated word count: {old_count} → {actual_word_count}")
                return content, actual_word_count

        return content, 0

    def cleanup(self) -> Tuple[str, List[str]]:
        """Run all cleanup operations."""
        print(f"\nCleaning up: {self.filepath}")
        print("=" * 60)

        content = self.read_file()
        original_size = len(content)

        # Run all cleanup operations
        content = self.remove_draft_metadata_sections(content)
        content = self.remove_checklist_items(content)
        content = self.remove_critical_warnings(content)
        content = self.remove_draft_status_markers(content)
        content = self.remove_section_metadata(content)
        content = self.clean_up_excessive_newlines(content)
        content, word_count = self.update_yaml_word_count(content)

        # Write back
        self.write_file(content)

        final_size = len(content)
        size_reduction = original_size - final_size

        print(f"\nChanges made:")
        for change in self.changes_made:
            print(f"  ✓ {change}")

        print(f"\nSize reduction: {size_reduction:,} bytes")
        print(f"Final size: {final_size:,} bytes")
        print(f"Status: {'✅ CLEANED' if self.changes_made else '⚠️ NO CHANGES NEEDED'}")

        return content, self.changes_made


def main():
    parser = argparse.ArgumentParser(description='Clean up draft artifacts from thesis markdown files')
    parser.add_argument('filepath', type=str, help='Path to thesis FINAL_THESIS.md file')
    parser.add_argument('--no-word-count-update', action='store_true',
                        help='Skip updating word count in YAML')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be changed without modifying file')

    args = parser.parse_args()

    filepath = Path(args.filepath)

    if not filepath.exists():
        print(f"❌ Error: File not found: {filepath}")
        sys.exit(1)

    if not filepath.name == 'FINAL_THESIS.md':
        print(f"⚠️ Warning: Expected FINAL_THESIS.md, got {filepath.name}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

    # Create backup
    backup_path = filepath.parent / f"{filepath.stem}_backup_before_cleanup{filepath.suffix}"
    import shutil
    shutil.copy2(filepath, backup_path)
    print(f"📋 Backup created: {backup_path}")

    # Run cleanup
    cleanup = ThesisCleanup(filepath, update_word_count=not args.no_word_count_update)

    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made")
        content = cleanup.read_file()
        # Run cleanup operations without writing
        original_cleanup_func = cleanup.write_file
        cleanup.write_file = lambda x: None  # No-op
        cleanup.cleanup()
        cleanup.write_file = original_cleanup_func
    else:
        cleanup.cleanup()

    print("\n" + "=" * 60)
    print(f"✅ Cleanup complete: {filepath}")
    print("=" * 60)


if __name__ == '__main__':
    main()
