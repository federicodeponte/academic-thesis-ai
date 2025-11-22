#!/bin/bash

# Extract high-quality screenshots from the reference PDF
PDF_FILE="public/examples/academic_ai_thesis_reference.pdf"
OUTPUT_DIR="public/examples/new_screenshots"

mkdir -p "$OUTPUT_DIR"

echo "📸 Extracting screenshots from reference PDF..."

# Key pages to extract:
# Page 1: Title page
# Page 3: Abstract/TOC
# Page 5: Introduction
# Page 15: Literature review with citations
# Page 30: Methodology
# Page 50: Results/Analysis
# Page 80: Conclusion

pages=(1 3 5 15 30 50 80)
names=("title" "abstract" "introduction" "literature" "methodology" "results" "conclusion")

for i in "${!pages[@]}"; do
    page=${pages[$i]}
    name=${names[$i]}
    output="$OUTPUT_DIR/thesis_${name}.png"
    
    echo "  → Extracting page $page ($name)..."
    
    pdftoppm -png -r 200 -f "$page" -l "$page" -singlefile "$PDF_FILE" "$OUTPUT_DIR/thesis_${name}"
    
    if [ -f "$output" ]; then
        size=$(du -h "$output" | cut -f1)
        echo "    ✅ Created: thesis_${name}.png ($size)"
    else
        echo "    ❌ Failed to create $name"
    fi
done

echo ""
echo "✅ Done! Screenshots saved in $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR"/*.png

