#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 DEVIL'S ADVOCATE AUDIT - LANDING PAGE VS REPO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "1️⃣  AGENT COUNT:"
echo "   Claimed: 19 agents"
echo "   Actual:  $(find prompts -name "*.md" -not -name "00_WORKFLOW.md" | wc -l) agents"
echo "   Files:   $(find prompts -name "*.md" -not -name "00_WORKFLOW.md" -exec basename {} .md \; | sort)"
echo ""

echo "2️⃣  GENERATION TIME:"
echo "   Claimed: 15-25 minutes"
grep -E "15.*min|25.*min" README.md | head -3
echo ""

echo "3️⃣  TOTAL TIME:"
echo "   Claimed: 10-20 hours"
grep -E "10.*20.*hour|Time to Complete" README.md | head -3
echo ""

echo "4️⃣  COST CLAIMS:"
echo "   Claimed: \$10-50 for 20k words"
grep -E "\$10|\$50|Cost.*20k" README.md | head -3
echo ""

echo "5️⃣  CITATION SUCCESS:"
echo "   Claimed: 95%+"
grep -E "95%|citation.*success|Citation Success" README.md | head -3
echo ""

echo "6️⃣  RESEARCH PAPERS:"
echo "   Claimed: 200M+"
grep -E "200M" README.md | head -3
echo ""

echo "7️⃣  LICENSE:"
echo "   Claimed: MIT License"
head -5 LICENSE 2>/dev/null | head -1
echo ""

echo "8️⃣  TEST COVERAGE:"
echo "   Claimed: 100% tested"
grep -E "100%.*test|test.*100%" README.md | head -3
echo ""

