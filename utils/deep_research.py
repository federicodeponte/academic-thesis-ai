#!/usr/bin/env python3
"""
ABOUTME: Autonomous deep research planner with seed reference expansion
ABOUTME: Two-phase approach: planning (Gemini) → execution (orchestrator)
"""

import json
import logging
import os
from typing import List, Dict, Any, Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from .citation_database import Citation

logger = logging.getLogger(__name__)


class DeepResearchPlanner:
    """
    Autonomous research planner for comprehensive literature reviews.

    Uses Gemini to create research strategy from seed references,
    then executes queries through citation orchestrator.

    Two-phase approach:
    1. Planning: Gemini autonomously plans research strategy
    2. Execution: Orchestrator runs planned queries through fallback chain

    Benefits:
    - 50+ sources vs 20-30 typical
    - Seed reference expansion
    - Autonomous gap identification
    - Systematic coverage
    """

    def __init__(
        self,
        gemini_model: Optional[Any] = None,
        api_key: Optional[str] = None,
        min_sources: int = 50,
        verbose: bool = True
    ):
        """
        Initialize deep research planner.

        Args:
            gemini_model: Gemini model for planning (optional, will create if None)
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
            min_sources: Minimum number of sources to research
            verbose: Print progress to console
        """
        self.min_sources = min_sources
        self.verbose = verbose

        # Initialize Gemini for planning
        if gemini_model:
            self.model = gemini_model
        else:
            if not genai:
                raise ImportError(
                    "google-generativeai not installed. "
                    "Run: pip install google-generativeai>=0.8.0"
                )

            api_key = api_key or os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError(
                    "GOOGLE_API_KEY not found. Set via environment variable or constructor."
                )

            genai.configure(api_key=api_key)
            # Use Gemini 2.5 Flash for cost-effective planning
            self.model = genai.GenerativeModel('gemini-2.5-flash')

    def create_research_plan(
        self,
        topic: str,
        scope: Optional[str] = None,
        seed_references: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create autonomous research plan with Gemini.

        Phase 1: Planning
        - Analyzes topic and scope
        - Expands from seed references
        - Identifies research queries
        - Creates structured outline

        Args:
            topic: Main research topic
            scope: Optional scope/constraints (e.g., "EU focus; B2C and B2B")
            seed_references: Optional list of anchor papers to expand from

        Returns:
            Dict with keys:
                - queries: List[str] - Research queries to execute
                - outline: str - Structured research outline
                - strategy: str - Research strategy description
        """
        if self.verbose:
            print(f"\n🔍 Creating deep research plan for: {topic}")
            if scope:
                print(f"   Scope: {scope}")

        # Build planning prompt
        prompt = self._build_planning_prompt(topic, scope, seed_references)

        try:
            # Call Gemini for autonomous planning
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,  # Lower temperature for systematic planning
                    max_output_tokens=8192
                )
            )

            # Parse JSON response
            plan_text = response.text.strip()

            # Remove markdown code blocks if present
            if plan_text.startswith("```"):
                plan_text = plan_text.split("```")[1]
                if plan_text.startswith("json"):
                    plan_text = plan_text[4:]
                plan_text = plan_text.strip()

            plan = json.loads(plan_text)

            if self.verbose:
                print(f"   ✓ Plan created: {len(plan.get('queries', []))} research queries")

            return plan

        except Exception as e:
            logger.error(f"Research planning failed: {e}")
            raise

    def _build_planning_prompt(
        self,
        topic: str,
        scope: Optional[str],
        seed_references: Optional[List[str]]
    ) -> str:
        """Build planning prompt for Gemini."""

        prompt = f"""You are a systematic research planning assistant.

**Topic:** {topic}
"""

        if scope:
            prompt += f"**Scope:** {scope}\n"

        prompt += f"""
**Task:** Create a comprehensive research plan to find {self.min_sources}+ high-quality sources.

**Instructions:**
1. Plan research strategy (what to search for; which source types to prioritize)
2. Generate specific research queries (author:term, title:keyword, topic phrases)
3. Draft structured outline with section headings for evidence-based report

**Quality Requirements:**
- Minimum {self.min_sources} primary sources (peer-reviewed journals, standards, regulations)
- **Source Diversity:** Balance academic AND industry sources for comprehensive coverage
  - Academic: Peer-reviewed journals, conference papers, dissertations
  - Industry: Consulting reports (McKinsey, Gartner, BCG), think tanks (Brookings, RAND), regulatory bodies (WHO, OECD, European Commission), standards (ISO, IEEE)
- Avoid: Blogs, press releases, marketing materials (unless no alternative)
- Include: Recent work (last 5 years) AND foundational papers
- Coverage: Multiple perspectives, interdisciplinary if relevant

"""

        # Add seed references if provided
        if seed_references and len(seed_references) > 0:
            prompt += "**Seed References** (expand from these):\n"
            for ref in seed_references:
                prompt += f"- {ref}\n"
            prompt += "\nUse these as starting points. Find related work, citing papers, and recent developments.\n\n"

        prompt += """**Output Format:**
Return JSON with keys:
- strategy: Brief research strategy description (2-3 paragraphs)
- queries: List of specific search queries to execute (aim for 50+)
- outline: Structured outline with section headings

**Query Diversity:** Generate mix of academic AND industry queries for source diversity:

Academic-focused queries (route to Crossref/Semantic Scholar):
- "peer-reviewed studies on [topic]"
- "systematic review of [topic]"
- "author:Smith [topic]"
- "title:empirical analysis [topic]"
- "meta-analysis [topic]"

Industry-focused queries (route to Gemini Grounded/web search):
- "McKinsey report [topic]"
- "Gartner analysis [topic]"
- "WHO guidelines [topic]"
- "OECD [topic] framework"
- "European Commission [topic] regulation"
- "BCG white paper [topic]"
- "IEEE standards [topic]"
- "NIST [topic] best practices"

Return ONLY valid JSON, no markdown blocks or explanations.
"""

        return prompt

    def estimate_coverage(self, queries: List[str]) -> int:
        """
        Estimate number of sources likely to be found.

        Heuristic:
        - Specific queries (author:X, title:Y): ~1-2 sources each
        - Topic queries: ~2-5 sources each
        - Broad queries: ~5-10 sources each

        Args:
            queries: List of research queries

        Returns:
            Estimated source count
        """
        estimate = 0
        for query in queries:
            if 'author:' in query or 'title:' in query:
                estimate += 1.5  # Specific queries
            elif len(query.split()) <= 3:
                estimate += 3  # Topic queries
            else:
                estimate += 6  # Broad queries

        return int(estimate)

    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate research plan meets quality requirements.

        Args:
            plan: Research plan from create_research_plan()

        Returns:
            True if plan is valid, False otherwise
        """
        # Check required keys
        if not all(k in plan for k in ['queries', 'outline', 'strategy']):
            logger.warning("Plan missing required keys")
            return False

        # Check query count
        queries = plan.get('queries', [])
        if len(queries) < 10:
            logger.warning(f"Too few queries: {len(queries)} < 10")
            return False

        # Estimate coverage
        estimated = self.estimate_coverage(queries)
        if estimated < self.min_sources * 0.7:  # 70% of target
            logger.warning(
                f"Estimated coverage too low: {estimated} < {self.min_sources * 0.7}"
            )
            return False

        return True

    def refine_plan(
        self,
        plan: Dict[str, Any],
        feedback: str
    ) -> Dict[str, Any]:
        """
        Refine research plan based on feedback.

        Args:
            plan: Original research plan
            feedback: Feedback on what to improve

        Returns:
            Refined research plan
        """
        if self.verbose:
            print(f"\n🔄 Refining research plan...")

        prompt = f"""You are refining a research plan based on feedback.

**Original Plan:**
{json.dumps(plan, indent=2)}

**Feedback:**
{feedback}

**Task:** Improve the plan addressing the feedback while maintaining quality requirements.

Return updated JSON with same structure (strategy, queries, outline).
Return ONLY valid JSON, no markdown blocks.
"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=8192
                )
            )

            plan_text = response.text.strip()
            if plan_text.startswith("```"):
                plan_text = plan_text.split("```")[1]
                if plan_text.startswith("json"):
                    plan_text = plan_text[4:]
                plan_text = plan_text.strip()

            refined_plan = json.loads(plan_text)

            if self.verbose:
                print(f"   ✓ Plan refined: {len(refined_plan.get('queries', []))} queries")

            return refined_plan

        except Exception as e:
            logger.error(f"Plan refinement failed: {e}")
            return plan  # Return original if refinement fails
