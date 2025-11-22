#!/bin/bash
# ABOUTME: Day 10 regeneration periodic monitor - checks every 10 minutes
# ABOUTME: Automatically runs inspection when regeneration completes

echo "================================================================================"
echo "🔍 DAY 10 REGENERATION MONITOR - Starting periodic checks"
echo "================================================================================"
echo "Start time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

check_count=0
max_checks=12  # 12 checks * 10 min = 2 hours max

while [ $check_count -lt $max_checks ]; do
    check_count=$((check_count + 1))
    current_time=$(date '+%H:%M:%S')

    echo ""
    echo "================================================================================"
    echo "[$current_time] CHECK #$check_count of $max_checks"
    echo "================================================================================"

    # Check if processes are still running
    if pgrep -f "regenerate_theses_parallel.py" > /dev/null; then
        echo "✅ Status: RUNNING"
        echo ""

        # Check for completion markers (FINAL_THESIS.md modified recently)
        echo "📁 Thesis progress:"
        completed=0
        for thesis in opensource_thesis ai_pricing_thesis co2_thesis_german academic_ai_thesis; do
            final="tests/outputs/${thesis}/FINAL_THESIS.md"
            if [ -f "$final" ]; then
                # Check if modified in last 10 minutes
                if [ $(find "$final" -mmin -10 2>/dev/null | wc -l) -gt 0 ]; then
                    size=$(stat -c %s "$final" 2>/dev/null)
                    size_kb=$((size / 1024))
                    echo "   ✅ $thesis: Updated (${size_kb} KB)"
                    completed=$((completed + 1))
                else
                    size=$(stat -c %s "$final" 2>/dev/null)
                    size_kb=$((size / 1024))
                    echo "   ⏳ $thesis: Stable (${size_kb} KB)"
                fi
            else
                echo "   ⌛ $thesis: Not started"
            fi
        done

        echo ""
        echo "📊 Activity: $completed/4 theses updated in last 10 minutes"

        # Check for removal reports
        echo ""
        echo "🔍 Citation filtering:"
        reports=$(find tests/outputs/*/citation_database_removal_report.json -mmin -60 2>/dev/null | wc -l)
        if [ $reports -gt 0 ]; then
            echo "   Found $reports removal reports (filtering active!)"
            for report in tests/outputs/*/citation_database_removal_report.json; do
                if [ -f "$report" ]; then
                    thesis=$(echo $report | cut -d'/' -f3)
                    echo "   - $thesis: Report exists"
                fi
            done
        else
            echo "   No removal reports yet (filtering not reached)"
        fi

        # Check log files
        echo ""
        echo "📝 Latest log activity:"
        newest_log=$(ls -t logs/thesis_regeneration/*.log 2>/dev/null | head -1)
        if [ -n "$newest_log" ]; then
            log_time=$(stat -c %y "$newest_log" | cut -d' ' -f2 | cut -d'.' -f1)
            echo "   Latest log: $(basename $newest_log) at $log_time"
        fi

    else
        echo "✅ Status: COMPLETED!"
        echo ""
        echo "================================================================================"
        echo "📊 REGENERATION COMPLETE - Running inspection..."
        echo "================================================================================"
        echo ""

        # Run inspection script
        if [ -f "scripts/inspect_day10_results.sh" ]; then
            bash scripts/inspect_day10_results.sh
        else
            echo "⚠️  Inspection script not found: scripts/inspect_day10_results.sh"
        fi

        echo ""
        echo "================================================================================"
        echo "✅ Day 10 regeneration and inspection COMPLETE!"
        echo "Completion time: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "================================================================================"
        exit 0
    fi

    # Wait 10 minutes before next check (unless last check)
    if [ $check_count -lt $max_checks ]; then
        echo ""
        echo "⏰ Next check in 10 minutes (at $(date -d '+10 minutes' '+%H:%M:%S'))..."
        sleep 600
    fi
done

echo ""
echo "================================================================================"
echo "⚠️  Maximum monitoring time reached (2 hours)"
echo "================================================================================"
echo "Check processes manually if regeneration is still running:"
echo "  pgrep -f regenerate_theses_parallel.py"
echo "  tail -f logs/day10_monitor.log"
