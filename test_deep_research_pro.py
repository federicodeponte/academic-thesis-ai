#!/usr/bin/env python3
"""
Isolated test for DeepResearchPlanner with Gemini 2.5 Pro.
Tests autonomous research planning and query generation.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from utils.deep_research import DeepResearchPlanner

def test_deep_research_pro():
    """Test DeepResearchPlanner with Gemini 2.5 Pro."""

    print("=" * 80)
    print("DEEP RESEARCH PLANNER (2.5 PRO) ISOLATED TEST")
    print("=" * 80)

    topic = "AI pricing models in enterprise software"
    scope = "Focus on B2B SaaS pricing strategies; last 5 years"
    seed_references = [
        "OpenAI pricing tiers and token-based models",
        "Anthropic Claude pricing structure"
    ]

    print(f"\n📝 Topic: {topic}")
    print(f"🎯 Scope: {scope}")
    print(f"📚 Seed References: {len(seed_references)}")
    print(f"🤖 Model: gemini-2.5-pro")
    print(f"🎲 Min Sources: 50\n")

    planner = DeepResearchPlanner(
        min_sources=50,
        verbose=True
    )

    print("🔍 Creating research plan...\n")

    try:
        plan = planner.create_research_plan(
            topic=topic,
            scope=scope,
            seed_references=seed_references
        )

        print("\n" + "=" * 80)
        print("RESEARCH PLAN CREATED")
        print("=" * 80)

        if plan and 'queries' in plan:
            queries = plan['queries']
            print(f"\n✅ SUCCESS - Generated {len(queries)} research queries")

            print(f"\n📊 Plan Structure:")
            print(f"   - Total Queries: {len(queries)}")
            print(f"   - Outline Sections: {len(plan.get('outline', []))}")

            print(f"\n📋 Sample Queries (first 5):")
            for i, query in enumerate(queries[:5], 1):
                print(f"   {i}. {query}")

            if len(queries) > 5:
                print(f"   ... and {len(queries) - 5} more")

            return True
        else:
            print("❌ FAILED - No queries generated")
            print(f"Plan keys: {list(plan.keys()) if plan else 'None'}")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n" + "=" * 80)

if __name__ == '__main__':
    success = test_deep_research_pro()
    sys.exit(0 if success else 1)
