#!/bin/bash
# ABOUTME: Day 10 citation filtering results inspection script
# ABOUTME: Compares citation quality before/after filtering and generates report

echo "================================================================================"
echo "📊 DAY 10 CITATION FILTERING RESULTS INSPECTION"
echo "================================================================================"
echo ""

# Check if regeneration is complete
if [ ! -f "tests/outputs/opensource_thesis/FINAL_THESIS.md" ]; then
    echo "❌ Error: Regeneration not complete yet"
    exit 1
fi

echo "📋 Checking for removal reports..."
echo ""

# Check each thesis for removal report
for thesis in opensource_thesis ai_pricing_thesis co2_thesis_german academic_ai_thesis; do
    report="tests/outputs/${thesis}/citation_database_removal_report.json"

    if [ -f "$report" ]; then
        echo "✅ ${thesis}:"

        # Extract stats using Python
        python3 << EOF
import json
with open('$report') as f:
    data = json.load(f)
    stats = data['stats']
    print(f"   Original: {stats['total_original']} citations")
    print(f"   Kept:     {stats['total_filtered']} citations ({stats['total_filtered']/stats['total_original']*100:.1f}%)")
    print(f"   Removed:  {stats['total_removed']} citations ({stats['total_removed']/stats['total_original']*100:.1f}%)")

    if stats['removal_reasons']:
        print("   Removal breakdown:")
        for reason, count in sorted(stats['removal_reasons'].items(), key=lambda x: x[1], reverse=True):
            print(f"     - {reason}: {count}")
    print("")
EOF
    else
        echo "⚠️  ${thesis}: No removal report found"
        echo ""
    fi
done

echo "================================================================================"
echo "🔍 BIBLIOGRAPHY QUALITY CHECK"
echo "================================================================================"
echo ""

# Check for bad citations in final theses
for thesis in opensource_thesis ai_pricing_thesis co2_thesis_german academic_ai_thesis; do
    md_file="tests/outputs/${thesis}/FINAL_THESIS.md"

    if [ -f "$md_file" ]; then
        echo "Checking ${thesis}..."

        # Check for domain-as-author patterns
        domain_citations=$(grep -o '\[^0-9\]*\]\.\(com\|org\|gov\|edu\|net\|io\|ai\)' "$md_file" | wc -l)

        # Check for error URLs
        error_urls=$(grep -o 'https\?://[^)]*\(403\|404\|error\)' "$md_file" | wc -l)

        if [ $domain_citations -gt 0 ] || [ $error_urls -gt 0 ]; then
            echo "  ⚠️  Found potential issues:"
            [ $domain_citations -gt 0 ] && echo "     - Domain citations: $domain_citations"
            [ $error_urls -gt 0 ] && echo "     - Error URLs: $error_urls"
        else
            echo "  ✅ Bibliography looks clean"
        fi
        echo ""
    fi
done

echo "================================================================================"
echo "📈 FILTERING EFFECTIVENESS SUMMARY"
echo "================================================================================"
echo ""

# Aggregate statistics
python3 << 'EOF'
import json
from pathlib import Path

theses = ['opensource_thesis', 'ai_pricing_thesis', 'co2_thesis_german', 'academic_ai_thesis']
total_original = 0
total_kept = 0
total_removed = 0

for thesis in theses:
    report_path = Path(f'tests/outputs/{thesis}/citation_database_removal_report.json')
    if report_path.exists():
        with open(report_path) as f:
            data = json.load(f)
            stats = data['stats']
            total_original += stats['total_original']
            total_kept += stats['total_filtered']
            total_removed += stats['total_removed']

if total_original > 0:
    print(f"Total citations across all 4 theses:")
    print(f"  Original:  {total_original}")
    print(f"  Kept:      {total_kept} ({total_kept/total_original*100:.1f}%)")
    print(f"  Removed:   {total_removed} ({total_removed/total_original*100:.1f}%)")
    print("")
    print(f"Average removal rate: {total_removed/total_original*100:.1f}%")
else:
    print("No filtering statistics found")
EOF

echo ""
echo "================================================================================"
echo "Done! Review removal reports in tests/outputs/*/citation_database_removal_report.json"
echo "================================================================================"
