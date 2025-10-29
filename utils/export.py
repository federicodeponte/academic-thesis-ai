#!/usr/bin/env python3
"""
ABOUTME: Legacy export utilities for markdown to PDF, Word, and LaTeX conversion
ABOUTME: For production use, prefer utils/export_professional.py with multi-engine support
"""

import argparse
import os
import sys
import markdown
from pathlib import Path

try:
    from weasyprint import HTML, CSS
    WEASY_AVAILABLE = True
except ImportError:
    WEASY_AVAILABLE = False
    print("Warning: WeasyPrint not installed. PDF export unavailable.")

try:
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("Warning: python-docx not installed. Word export unavailable.")


def markdown_to_html(md_content):
    """Convert Markdown to HTML"""
    md = markdown.Markdown(extensions=[
        'extra',
        'codehilite',
        'tables',
        'toc',
        'footnotes'
    ])
    return md.convert(md_content)


def export_pdf(input_file, output_file):
    """Export Markdown to PDF using WeasyPrint"""
    if not WEASY_AVAILABLE:
        print("ERROR: WeasyPrint not installed. Run: pip install weasyprint")
        return False
    
    # Read Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown_to_html(md_content)
    
    # Academic CSS styling
    css = CSS(string='''
        @page {
            size: A4;
            margin: 2.5cm;
        }
        body {
            font-family: "Times New Roman", serif;
            font-size: 12pt;
            line-height: 1.6;
            text-align: justify;
        }
        h1 {
            font-size: 16pt;
            font-weight: bold;
            margin-top: 24pt;
            margin-bottom: 12pt;
        }
        h2 {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 18pt;
            margin-bottom: 9pt;
        }
        h3 {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 12pt;
            margin-bottom: 6pt;
        }
        p {
            margin-bottom: 12pt;
            text-indent: 0.5in;
        }
        blockquote {
            margin-left: 0.5in;
            margin-right: 0.5in;
            font-style: italic;
        }
        code {
            font-family: "Courier New", monospace;
            background-color: #f5f5f5;
            padding: 2px 4px;
        }
        pre {
            font-family: "Courier New", monospace;
            background-color: #f5f5f5;
            padding: 10px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 12pt 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f5f5f5;
            font-weight: bold;
        }
    ''')
    
    # Generate PDF
    HTML(string=html_content).write_pdf(output_file, stylesheets=[css])
    print(f"✅ PDF exported successfully: {output_file}")
    return True


def export_docx(input_file, output_file):
    """Export Markdown to Word (.docx)"""
    if not DOCX_AVAILABLE:
        print("ERROR: python-docx not installed. Run: pip install python-docx")
        return False
    
    # Read Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create Word document
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # Parse Markdown (simple line-by-line conversion)
    lines = md_content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # Headings
        if line.startswith('# '):
            doc.add_heading(line[2:], level=1)
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=3)
        
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            doc.add_paragraph(line[2:], style='List Bullet')
        elif line.startswith('1. ') or line.startswith('2. '):
            doc.add_paragraph(line[3:], style='List Number')
        
        # Code blocks
        elif line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_text = '\n'.join(code_lines)
            p = doc.add_paragraph(code_text)
            p.style = 'No Spacing'
            p_format = p.paragraph_format
            p_format.left_indent = Inches(0.5)
        
        # Regular paragraphs
        else:
            doc.add_paragraph(line)
        
        i += 1
    
    # Save
    doc.save(output_file)
    print(f"✅ Word document exported successfully: {output_file}")
    return True


def export_latex(input_file, output_file):
    """Export Markdown to LaTeX"""
    # Read Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # LaTeX preamble
    latex_content = r'''\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{cite}
\usepackage{amsmath}
\usepackage{booktabs}

\title{Your Paper Title}
\author{Your Name}
\date{\today}

\begin{document}

\maketitle

'''
    
    # Simple Markdown to LaTeX conversion
    lines = md_content.split('\n')
    for line in lines:
        line = line.strip()
        
        if not line:
            latex_content += '\n'
            continue
        
        # Headings
        if line.startswith('# '):
            latex_content += f'\\section{{{line[2:]}}}\n'
        elif line.startswith('## '):
            latex_content += f'\\subsection{{{line[3:]}}}\n'
        elif line.startswith('### '):
            latex_content += f'\\subsubsection{{{line[4:]}}}\n'
        
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            if '\\begin{itemize}' not in latex_content.split('\n')[-2]:
                latex_content += '\\begin{itemize}\n'
            latex_content += f'\\item {line[2:]}\n'
        
        # Regular text
        else:
            # Close itemize if needed
            if '\\begin{itemize}' in latex_content and '\\end{itemize}' not in latex_content.split('\n')[-2]:
                latex_content += '\\end{itemize}\n'
            
            # Escape special characters
            line = line.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')
            latex_content += line + '\n\n'
    
    latex_content += '\n\\end{document}\n'
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"✅ LaTeX exported successfully: {output_file}")
    print(f"   Compile with: pdflatex {output_file}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Export Markdown to PDF, Word, or LaTeX',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python export.py --format pdf --output paper.pdf final_thesis.md
  python export.py --format docx --output paper.docx final_thesis.md
  python export.py --format latex --output paper.tex final_thesis.md
        '''
    )
    parser.add_argument('input', help='Input Markdown file')
    parser.add_argument('--format', '-f', choices=['pdf', 'docx', 'latex'], required=True,
                        help='Output format')
    parser.add_argument('--output', '-o', required=True,
                        help='Output file path')
    
    args = parser.parse_args()
    
    # Check input file exists
    if not os.path.exists(args.input):
        print(f"ERROR: Input file not found: {args.input}")
        sys.exit(1)
    
    # Export
    success = False
    if args.format == 'pdf':
        success = export_pdf(args.input, args.output)
    elif args.format == 'docx':
        success = export_docx(args.input, args.output)
    elif args.format == 'latex':
        success = export_latex(args.input, args.output)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
