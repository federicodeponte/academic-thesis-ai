"""
Create high-quality screenshots from the showcase PDF for landing page.
Uses pdf2image to convert PDF pages to PNG images.
"""
from pathlib import Path
import subprocess

def create_screenshots():
    """Convert PDF pages to high-quality PNG screenshots"""
    
    pdf_file = Path("showcase_thesis/SHOWCASE_THESIS.pdf")
    output_dir = Path("showcase_thesis/screenshots")
    output_dir.mkdir(exist_ok=True)
    
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_file}")
        return False
    
    # Use pdftoppm to convert PDF to PNG (better quality than imagemagick)
    # -png: PNG format
    # -r 300: 300 DPI for high quality
    # -singlefile: One file per page with page number suffix
    
    pages_to_extract = [1, 2, 3, 5, 10]  # Title, TOC, intro, methodology, results
    
    for page_num in pages_to_extract:
        output_file = output_dir / f"thesis_page_{page_num:02d}.png"
        
        cmd = [
            "pdftoppm",
            "-png",
            "-r", "200",  # 200 DPI - good balance of quality and file size
            "-f", str(page_num),  # From page
            "-l", str(page_num),  # To page
            "-singlefile",
            str(pdf_file),
            str(output_file.with_suffix(''))  # pdftoppm adds .png automatically
        ]
        
        try:
            print(f"🔄 Generating screenshot for page {page_num}...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Check if file was created
            if output_file.exists():
                file_size = output_file.stat().st_size / 1024
                print(f"✅ Created: {output_file.name} ({file_size:.1f} KB)")
            else:
                print(f"⚠️  File not created: {output_file}")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generating page {page_num}:")
            print(f"   {e.stderr}")
        except FileNotFoundError:
            print(f"❌ pdftoppm not found. Install with: sudo apt-get install poppler-utils")
            return False
    
    return True

if __name__ == "__main__":
    print("🎨 Creating landing page screenshots...\n")
    create_screenshots()
    print("\n✅ Done! Screenshots saved in showcase_thesis/screenshots/")

