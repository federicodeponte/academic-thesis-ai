#!/usr/bin/env python3
"""
Test script for LibreOffice engine inline markdown parser.
Tests bold, italic, code, and combined formatting.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from docx import Document
    from utils.pdf_engines.libreoffice_engine import LibreOfficeEngine
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("   Install python-docx: pip install python-docx")
    sys.exit(1)


def test_inline_markdown_parser():
    """Test the inline markdown parser."""
    print("=" * 70)
    print("TEST: LibreOffice Inline Markdown Parser")
    print("=" * 70)

    # Create engine instance
    engine = LibreOfficeEngine()

    # Test cases
    test_cases = [
        ("Plain text", "Plain text"),
        ("**bold**", "bold (should be bold)"),
        ("*italic*", "italic (should be italic)"),
        ("***bold italic***", "bold italic (should be both)"),
        ("`code`", "code (should be monospace)"),
        ("Mix **bold** and *italic* text", "mixed formatting"),
        ("Text with `code span` inline", "inline code"),
        ("**Bold** *italic* ***both*** `code`", "all formats"),
        ("No formatting at all", "plain"),
        ("Multiple **bold** and **bold** words", "multiple bold"),
    ]

    print("\nTesting inline markdown parsing...")
    doc = Document()

    for i, (markdown_text, description) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {description}")
        print(f"  Input:  {markdown_text}")

        # Create paragraph and process markdown
        para = doc.add_paragraph()
        engine._process_inline_markdown(para, markdown_text)

        # Check runs
        print(f"  Runs:   {len(para.runs)}")
        for j, run in enumerate(para.runs):
            formatting = []
            if run.bold:
                formatting.append("bold")
            if run.italic:
                formatting.append("italic")
            if run.font.name == 'Courier New':
                formatting.append("code")

            format_str = f" [{', '.join(formatting)}]" if formatting else " [plain]"
            print(f"    Run {j+1}: '{run.text}'{format_str}")

    # Save test document
    output_file = Path("tests/outputs/test_inline_markdown.docx")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_file)

    print(f"\n✅ Test complete!")
    print(f"   Output saved to: {output_file}")
    print(f"   Open the file to visually verify formatting.")
    print()

    return True


if __name__ == "__main__":
    try:
        success = test_inline_markdown_parser()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
