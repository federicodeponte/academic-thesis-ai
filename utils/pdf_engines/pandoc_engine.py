#!/usr/bin/env python3
"""
ABOUTME: Pandoc/LaTeX-based PDF generation engine for academic papers
ABOUTME: Professional typesetting using LaTeX with proper font rendering
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional

from .base import PDFEngine, PDFGenerationOptions, EngineResult


class PandocLatexEngine(PDFEngine):
    """
    Pandoc/LaTeX-based PDF generation engine.

    Uses Pandoc to convert markdown to LaTeX, then pdflatex to generate PDF.
    This is the academic standard for document typesetting with superior
    typography and font rendering.

    Advantages:
    - Best font rendering quality (solves AI vs Al visual issues)
    - Professional academic typesetting
    - Industry standard for research papers
    - Proper handling of italics, bold, and formatting
    - Clean separation of content and presentation

    Requirements:
    - pandoc
    - pdflatex (texlive-latex-base)
    - texlive-latex-recommended (for additional packages)
    """

    def get_name(self) -> str:
        """Get engine name."""
        return "Pandoc/LaTeX"

    def get_priority(self) -> int:
        """
        Priority: 85/100

        Highest priority due to superior typography and academic standards.
        Should be preferred over all other engines when available.
        """
        return 85

    def is_available(self) -> bool:
        """Check if pandoc and pdflatex are available."""
        return (
            shutil.which('pandoc') is not None and
            shutil.which('pdflatex') is not None
        )

    def generate(
        self,
        md_file: Path,
        output_pdf: Path,
        options: PDFGenerationOptions
    ) -> EngineResult:
        """
        Generate PDF via Markdown → LaTeX → PDF pipeline.

        Args:
            md_file: Input markdown file
            output_pdf: Output PDF path
            options: Generation options

        Returns:
            EngineResult with success/failure details
        """
        # Validate inputs
        error = self.validate_inputs(md_file, output_pdf)
        if error:
            return EngineResult(
                success=False,
                engine_name=self.get_name(),
                error_message=error
            )

        try:
            # Normalize YAML field names for Pandoc compatibility
            # (Pandoc only recognizes English field names like 'title', 'author', 'date')
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            md_content = self._normalize_yaml_for_pandoc(md_content)

            # Write normalized content to temporary file for Pandoc
            import tempfile
            temp_md = None
            temp_fd = None
            try:
                temp_fd, temp_path = tempfile.mkstemp(suffix='.md', text=True)
                temp_md = Path(temp_path)
                with open(temp_md, 'w', encoding='utf-8') as f:
                    f.write(md_content)
            finally:
                if temp_fd is not None:
                    import os
                    os.close(temp_fd)

            # Create LaTeX preamble for header customization
            latex_preamble = self._create_latex_preamble(options)
            preamble_path = output_pdf.parent / f"{output_pdf.stem}_preamble.tex"
            preamble_path = preamble_path.resolve()  # Get absolute path

            # Write preamble
            with open(preamble_path, 'w', encoding='utf-8') as f:
                f.write(latex_preamble)

            # Convert markdown to PDF using Pandoc + LaTeX (use normalized temp file)
            result = self._run_pandoc(temp_md, output_pdf, preamble_path, options)

            # Cleanup preamble file
            if preamble_path.exists():
                preamble_path.unlink()

            # Cleanup temporary markdown file
            if temp_md and temp_md.exists():
                temp_md.unlink()

            # Cleanup LaTeX auxiliary files
            self._cleanup_latex_files(output_pdf)

            return result

        except Exception as e:
            # Cleanup temp file on error
            if temp_md and temp_md.exists():
                temp_md.unlink()
            return EngineResult(
                success=False,
                engine_name=self.get_name(),
                error_message=f"Unexpected error: {str(e)}"
            )

    def _create_latex_preamble(self, options: PDFGenerationOptions) -> str:
        """
        Create LaTeX preamble for header customization.

        This is injected into Pandoc's default template, which is more robust
        than creating a full custom template.

        Args:
            options: PDF generation options

        Returns:
            str: LaTeX preamble content
        """
        # Parse line spacing for LaTeX (2.0 = double spacing)
        if options.line_spacing >= 1.9:
            spacing_command = r'\doublespacing'
        elif options.line_spacing >= 1.4:
            spacing_command = r'\onehalfspacing'
        else:
            spacing_command = r'\singlespacing'

        preamble = r'''\PassOptionsToPackage{hyphens}{url}
\usepackage{etoolbox}
\usepackage{setspace}
''' + spacing_command + r'''
\usepackage{indentfirst}
\setlength{\parindent}{0.5in}
\setlength{\parskip}{0pt}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\cfoot{\thepage}
\widowpenalty=10000
\clubpenalty=10000

% Fix Level 3 headings: italic (NOT bold) - APA 7th edition
\usepackage{titlesec}
% Use full \titleformat to override Pandoc's default bold formatting
\titleformat{\subsubsection}
  {\normalfont\normalsize\itshape}  % Format: normal weight (not bold), normal size, italic
  {}                                  % Label
  {0pt}                               % Sep
  {}                                  % Before-code

% Better table formatting - prevent truncation, auto-wrap cells
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{relsize}
% Set table margins to full text width
\setlength{\LTleft}{0pt}
\setlength{\LTright}{0pt}
% Reduce font size slightly for wide tables
\let\oldlongtable\longtable
\let\endoldlongtable\endlongtable
\renewenvironment{longtable}{\small\oldlongtable}{\endoldlongtable}
'''

        # Add APA 7th edition title page formatting if metadata provided
        if any([options.title, options.author, options.institution,
                options.course, options.instructor]):
            preamble += r'''
% APA 7th Edition Title Page Customization
\usepackage{titling}
% Title page formatting: centered, double-spaced
\pretitle{\begin{center}\LARGE\bfseries}
\posttitle{\par\end{center}\vskip 2em}
\preauthor{\begin{center}\large}
\postauthor{\par\end{center}}
\predate{\begin{center}\large}
\postdate{\par\end{center}}

% Add custom fields for APA title page
% These will be populated via Pandoc variables
'''

        # Add front matter page numbering (roman numerals) if TOC enabled
        if options.enable_toc:
            preamble += r'''
% Front matter page numbering (roman numerals for title page + TOC)
\usepackage{tocloft}
\pagenumbering{roman}
% Hook to switch to arabic numbering after TOC
\AfterPreamble{%
  \let\oldtableofcontents\tableofcontents
  \renewcommand{\tableofcontents}{%
    \clearpage
    \oldtableofcontents
    \cleardoublepage
    \pagenumbering{arabic}%
  }%
}
'''

        return preamble

    def _run_pandoc(
        self,
        md_file: Path,
        output_pdf: Path,
        preamble_path: Path,
        options: PDFGenerationOptions
    ) -> EngineResult:
        """
        Run Pandoc to convert markdown to PDF.

        Uses Pandoc's default template with custom preamble for robustness.

        Args:
            md_file: Input markdown file
            output_pdf: Output PDF path
            preamble_path: LaTeX preamble path
            options: Generation options

        Returns:
            EngineResult with success/failure
        """
        try:
            # Pandoc command with default template + custom preamble
            # This is more robust than a full custom template
            # Use absolute paths to avoid any path resolution issues
            margin = options.margins.replace('in', 'in').replace('cm', 'cm')

            cmd = [
                'pandoc',
                str(md_file.resolve()),
                '-o', str(output_pdf.resolve()),
                '--pdf-engine=pdflatex',
                '--include-in-header', str(preamble_path.resolve()),
                '--from', 'markdown',
                '--variable', f'geometry:margin={margin}',
                '--variable', f'fontsize={options.font_size}',
                '--variable', 'papersize:letter',
                '--variable', 'documentclass:article',
            ]

            # Add title page metadata if provided
            if options.title:
                cmd.extend(['--variable', f'title={options.title}'])
            if options.author:
                cmd.extend(['--variable', f'author={options.author}'])
            if options.date:
                cmd.extend(['--variable', f'date={options.date}'])
            # Note: institution, course, instructor are APA-specific and may need
            # custom template support. For now, we include them in subtitle if provided
            subtitle_parts = []
            if options.institution:
                subtitle_parts.append(options.institution)
            if options.course:
                subtitle_parts.append(options.course)
            if options.instructor:
                subtitle_parts.append(f'Instructor: {options.instructor}')
            if subtitle_parts:
                subtitle = r'\\'.join(subtitle_parts)
                cmd.extend(['--variable', f'subtitle={subtitle}'])

            # Add table of contents if enabled
            if options.enable_toc:
                cmd.append('--toc')
                cmd.extend(['--variable', f'toc-depth={options.toc_depth}'])
                cmd.extend(['--variable', 'toc-title=Table of Contents'])

            # Run Pandoc
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,  # 3 minute timeout for LaTeX compilation
                cwd=output_pdf.parent  # Run in output directory
            )

            if result.returncode != 0:
                # Extract useful error message from LaTeX output
                error_lines = result.stderr.split('\n')
                # Look for actual error messages (lines starting with !)
                latex_errors = [line for line in error_lines if line.startswith('!')]

                if latex_errors:
                    error_msg = '\n'.join(latex_errors[:3])  # First 3 errors
                else:
                    error_msg = result.stderr[-500:] if len(result.stderr) > 500 else result.stderr

                return EngineResult(
                    success=False,
                    engine_name=self.get_name(),
                    error_message=f"Pandoc/LaTeX compilation failed:\n{error_msg}"
                )

            if not output_pdf.exists():
                return EngineResult(
                    success=False,
                    engine_name=self.get_name(),
                    error_message="Pandoc did not generate PDF file"
                )

            # Check for warnings in LaTeX output
            warnings = []
            if 'Warning' in result.stdout or 'Warning' in result.stderr:
                warnings.append("LaTeX generated warnings (non-critical)")

            return EngineResult(
                success=True,
                engine_name=self.get_name(),
                output_path=output_pdf,
                warnings=warnings
            )

        except subprocess.TimeoutExpired:
            return EngineResult(
                success=False,
                engine_name=self.get_name(),
                error_message="Pandoc/LaTeX compilation timed out (>3 minutes)"
            )
        except Exception as e:
            return EngineResult(
                success=False,
                engine_name=self.get_name(),
                error_message=f"Pandoc execution failed: {str(e)}"
            )

    def _cleanup_latex_files(self, pdf_path: Path) -> None:
        """
        Clean up LaTeX auxiliary files.

        Args:
            pdf_path: Path to generated PDF (used to find auxiliary files)
        """
        # LaTeX generates many auxiliary files
        aux_extensions = ['.aux', '.log', '.out', '.toc', '.lof', '.lot']

        for ext in aux_extensions:
            aux_file = pdf_path.parent / f"{pdf_path.stem}{ext}"
            if aux_file.exists():
                try:
                    aux_file.unlink()
                except Exception:
                    pass  # Ignore cleanup errors

    def _normalize_yaml_for_pandoc(self, md_content: str) -> str:
        """
        Normalize YAML frontmatter field names to English for Pandoc compatibility.

        Pandoc only recognizes English field names (title, subtitle, author, date)
        for creating styled paragraphs in DOCX/PDF output. This function translates
        localized field names back to English while preserving the field values.

        Supported translations:
        - German: titel→title, untertitel→subtitle, autor→author, datum→date
        - Spanish: título→title, subtítulo→subtitle, autor→author, fecha→date
        - French: titre→title, sous-titre→subtitle, auteur→author, date→date

        Args:
            md_content: Markdown content with YAML frontmatter

        Returns:
            Markdown content with normalized YAML field names
        """
        import re

        # Translation map: localized → English
        field_translations = {
            # German (18 fields)
            'titel:': 'title:',
            'untertitel:': 'subtitle:',
            'autor:': 'author:',
            'datum:': 'date:',
            'wortzahl:': 'word_count:',
            'seitenzahl:': 'page_count:',
            'sprache:': 'language:',
            'thema:': 'topic:',
            'schlagwörter:': 'keywords:',
            'qualitäts_bewertung:': 'quality_score:',
            'system_ersteller:': 'system_creator:',
            'zitate_verifiziert:': 'citations_verified:',
            'visuelle_elemente:': 'visual_elements:',
            'generierungs_methode:': 'generation_method:',
            'beschreibung_showcase:': 'showcase_description:',
            'system_fähigkeiten:': 'system_capabilities:',
            'aufruf_zur_aktion:': 'call_to_action:',
            'lizenz:': 'license:',

            # Spanish (5 fields)
            'título:': 'title:',
            'subtítulo:': 'subtitle:',
            'fecha:': 'date:',
            'recuento_de_palabras:': 'word_count:',
            'idioma:': 'language:',

            # French (5 fields)
            'titre:': 'title:',
            'sous-titre:': 'subtitle:',
            'auteur:': 'author:',
            'nombre_de_mots:': 'word_count:',
            'langue:': 'language:',
        }

        # Only process if YAML frontmatter exists
        if not md_content.strip().startswith('---'):
            return md_content

        # Extract YAML frontmatter
        parts = md_content.split('---', 2)
        if len(parts) < 3:
            return md_content

        yaml_content = parts[1]
        rest_content = parts[2]

        # Translate field names (case-insensitive)
        for localized, english in field_translations.items():
            yaml_content = re.sub(
                f'^{re.escape(localized)}',
                english,
                yaml_content,
                flags=re.MULTILINE | re.IGNORECASE
            )

        # Strip custom fields that Pandoc doesn't recognize
        # Only keep: title, subtitle, author, date, abstract
        pandoc_recognized_fields = ['title', 'subtitle', 'author', 'date', 'abstract']
        yaml_lines = yaml_content.split('\n')
        filtered_lines = []

        for line in yaml_lines:
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith('#'):
                # Keep empty lines and comments
                filtered_lines.append(line)
                continue

            # Check if this line starts with a field name
            field_match = re.match(r'^(\w+):', line_stripped)
            if field_match:
                field_name = field_match.group(1).lower()
                if field_name in pandoc_recognized_fields:
                    filtered_lines.append(line)
                # Skip lines with unrecognized fields
            else:
                # Keep continuation lines (indented or quoted multi-line values)
                filtered_lines.append(line)

        yaml_content = '\n'.join(filtered_lines)

        # Reconstruct markdown
        return f'---{yaml_content}---{rest_content}'
