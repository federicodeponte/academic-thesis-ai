#!/bin/bash

# Create a visual screenshot of the comparison table using HTML and puppeteer/playwright
# For now, we'll extract the table section from the PDF

cd ~/academic-thesis-ai
# Find a page that might have the comparison table
pdftotext public/examples/academic_ai_thesis_reference.pdf - | grep -A 50 "Feature\|Academic Thesis AI\|Professional Editing" | head -30

