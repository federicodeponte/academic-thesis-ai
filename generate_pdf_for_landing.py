"""
Generate a beautiful PDF from the showcase thesis for landing page screenshots.
"""
import subprocess
import sys
from pathlib import Path

def convert_to_pdf():
    """Convert markdown to PDF using pandoc with LaTeX"""
    
    md_file = Path("showcase_thesis/SHOWCASE_THESIS.md")
    pdf_file = Path("showcase_thesis/SHOWCASE_THESIS.pdf")
    
    if not md_file.exists():
        print(f"❌ Markdown file not found: {md_file}")
        return False
    
    # Use pandoc to convert to PDF with nice formatting
    cmd = [
        "pandoc",
        str(md_file),
        "-o", str(pdf_file),
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=12pt",
        "-V", "documentclass=article",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "urlcolor=blue",
        "-V", "citecolor=blue",
        "--toc",
        "--toc-depth=3",
        "--number-sections",
    ]
    
    try:
        print(f"🔄 Converting {md_file} to PDF...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ PDF created: {pdf_file}")
        print(f"   📦 Size: {pdf_file.stat().st_size / 1024:.1f} KB")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting to PDF:")
        print(f"   {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ pandoc not found. Trying alternative method...")
        return False

def convert_with_md2pdf():
    """Alternative: Try using md2pdf if available"""
    try:
        import markdown
        from weasyprint import HTML
        
        md_file = Path("showcase_thesis/SHOWCASE_THESIS.md")
        pdf_file = Path("showcase_thesis/SHOWCASE_THESIS.pdf")
        
        # Read markdown
        with open(md_file) as f:
            md_content = f.read()
        
        # Convert to HTML
        html_content = markdown.markdown(md_content, extensions=['extra', 'toc'])
        
        # Add CSS styling
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: 'Georgia', serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 40px auto;
                    padding: 20px;
                }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                h3 {{ color: #555; }}
                a {{ color: #3498db; text-decoration: none; }}
                code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Convert to PDF
        HTML(string=styled_html).write_pdf(str(pdf_file))
        print(f"✅ PDF created using weasyprint: {pdf_file}")
        return True
        
    except ImportError as e:
        print(f"❌ Required package not available: {e}")
        return False

# Try pandoc first, fall back to weasyprint
if not convert_to_pdf():
    print("\n🔄 Trying alternative method (weasyprint)...")
    convert_with_md2pdf()

