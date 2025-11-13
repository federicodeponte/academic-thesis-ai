#!/usr/bin/env python3
"""
ABOUTME: WeasyPrint-based PDF generation engine (legacy/fallback)
ABOUTME: Direct HTML-to-PDF conversion with Cairo graphics
"""

import markdown
from pathlib import Path

from .base import PDFEngine, PDFGenerationOptions, EngineResult

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


class WeasyPrintEngine(PDFEngine):
    """
    WeasyPrint-based PDF generation engine.

    Legacy engine with known limitations in font rendering.
    Visual OCR may misread "AI" as "Al" due to Cairo graphics rendering.

    Use only as last resort fallback when other engines unavailable.

    Requirements:
    - weasyprint library
    """

    def get_name(self) -> str:
        """Get engine name."""
        return "WeasyPrint"

    def get_priority(self) -> int:
        """
        Priority: 30/100

        Lowest priority due to known font rendering issues.
        Use only when LibreOffice and Pandoc are unavailable.
        """
        return 30

    def is_available(self) -> bool:
        """Check if WeasyPrint is installed."""
        return WEASYPRINT_AVAILABLE

    def generate(
        self,
        md_file: Path,
        output_pdf: Path,
        options: PDFGenerationOptions
    ) -> EngineResult:
        """
        Generate PDF using WeasyPrint.

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
            # Read markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # Convert to HTML
            html_content = markdown.markdown(
                md_content,
                extensions=['extra', 'nl2br']
            )

            # Generate CSS from options
            css_content = self._generate_css(options)

            # Generate PDF
            html = HTML(string=html_content)
            css = CSS(string=css_content)
            html.write_pdf(output_pdf, stylesheets=[css])

            warnings = [
                "WeasyPrint has known font rendering limitations",
                "Visual OCR may misread 'AI' as 'Al' in serif fonts",
                "Consider using LibreOffice or Pandoc engines for better quality"
            ]

            return EngineResult(
                success=True,
                engine_name=self.get_name(),
                output_path=output_pdf,
                warnings=warnings
            )

        except Exception as e:
            return EngineResult(
                success=False,
                engine_name=self.get_name(),
                error_message=f"PDF generation failed: {str(e)}"
            )

    def _generate_css(self, options: PDFGenerationOptions) -> str:
        """
        Generate CSS from options.

        Args:
            options: PDF generation options

        Returns:
            str: CSS stylesheet string
        """
        # Parse line spacing
        line_height = options.line_spacing

        # Parse font size
        font_size = options.font_size

        # Build CSS
        css = f"""
        @page {{
            size: {options.page_size};
            margin: {options.margins};
        }}

        body {{
            font-family: '{options.font_family}', serif;
            font-size: {font_size};
            line-height: {line_height};
            text-align: {options.text_align};
            color: #000;
        }}

        h1 {{
            font-size: 14pt;
            font-weight: 700;
            text-align: center;
            margin-top: 0;
            margin-bottom: 24pt;
            line-height: 1.5;
            page-break-after: avoid;
        }}

        h2 {{
            font-size: 13pt;
            font-weight: 700;
            text-align: left;
            font-style: normal;
            margin-top: 24pt;
            margin-bottom: 12pt;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 12pt;
            font-weight: normal;
            font-style: italic !important;
            text-align: left;
            margin-top: 18pt;
            margin-bottom: 6pt;
            page-break-after: avoid;
        }}

        p {{
            margin: 0;
            text-indent: {options.first_line_indent};
            orphans: 2;
            widows: 2;
        }}

        p:first-of-type,
        h2 + p,
        h3 + p {{
            text-indent: 0;
        }}

        strong {{
            font-weight: bold;
        }}

        em {{
            font-style: italic !important;
            font-weight: normal !important;
        }}

        hr {{
            border: none;
            border-top: 1px solid #000;
            margin: 24pt 0;
        }}
        """

        # Add page numbers if requested
        if options.page_numbers:
            position = options.page_number_position
            if 'center' in position:
                alignment = 'center'
            elif 'right' in position:
                alignment = 'right'
            else:
                alignment = 'left'

            css += f"""
        @page {{
            @bottom-{alignment} {{
                content: counter(page);
                font-family: '{options.font_family}', serif;
                font-size: 12pt;
            }}
        }}
        """

        return css
