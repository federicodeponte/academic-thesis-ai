#!/usr/bin/env python3
"""
ABOUTME: Citation suggestion engine for topic-aware citation recommendations
ABOUTME: Suggests relevant citations based on keyword matching with section topics
"""

import re
from typing import List, Set, Dict, Tuple
from utils.citation_database import Citation, CitationDatabase


def extract_keywords(text: str, min_length: int = 4) -> Set[str]:
    """
    Extract meaningful keywords from text.

    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length (default: 4)

    Returns:
        set: Normalized keywords
    """
    # Remove common words (stopwords)
    stopwords = {
        'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have', 'been',
        'were', 'are', 'was', 'been', 'their', 'they', 'these', 'those',
        'about', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'under', 'again', 'further', 'then', 'once'
    }

    # Extract words (alphanumeric + hyphens)
    words = re.findall(r'[a-zA-Z0-9\-]+', text.lower())

    # Filter by length and stopwords
    keywords = {
        word for word in words
        if len(word) >= min_length and word not in stopwords
    }

    return keywords


def score_citation_relevance(
    citation: Citation,
    topic_keywords: Set[str]
) -> Tuple[int, List[str]]:
    """
    Score citation relevance to topic based on keyword overlap.

    Args:
        citation: Citation to score
        topic_keywords: Keywords from section topic

    Returns:
        tuple: (score, list_of_matching_keywords)
    """
    # Extract keywords from citation metadata
    citation_text = f"{citation.title} {citation.journal or ''}"
    citation_keywords = extract_keywords(citation_text)

    # Calculate overlap
    matches = topic_keywords & citation_keywords

    # Score based on match count
    score = len(matches)

    return score, sorted(matches)


def suggest_citations(
    database: CitationDatabase,
    section_topic: str,
    max_suggestions: int = 5
) -> List[Dict]:
    """
    Suggest relevant citations for a section topic.

    Args:
        database: Citation database
        section_topic: Section topic or description
        max_suggestions: Maximum number of suggestions to return

    Returns:
        list: Suggested citations with scores and reasons
    """
    # Extract keywords from topic
    topic_keywords = extract_keywords(section_topic)

    if not topic_keywords:
        return []

    # Score all citations
    scored_citations = []
    for citation in database.citations:
        score, matches = score_citation_relevance(citation, topic_keywords)

        if score > 0:  # Only include citations with matches
            scored_citations.append({
                'citation': citation,
                'score': score,
                'matching_keywords': matches,
            })

    # Sort by score (descending)
    scored_citations.sort(key=lambda x: x['score'], reverse=True)

    # Return top N
    return scored_citations[:max_suggestions]


def format_citation_suggestions(
    suggestions: List[Dict],
    section_name: str
) -> str:
    """
    Format citation suggestions as markdown.

    Args:
        suggestions: List of suggestion dictionaries
        section_name: Name of the section

    Returns:
        str: Formatted markdown
    """
    if not suggestions:
        return f"## Suggested Citations for {section_name}\n\nNo relevant citations found.\n"

    output = f"## Suggested Citations for {section_name}\n\n"
    output += "Based on keyword matching, these citations may be relevant:\n\n"

    for i, suggestion in enumerate(suggestions, 1):
        citation = suggestion['citation']
        score = suggestion['score']
        matches = suggestion['matching_keywords']

        # Format authors
        authors_str = ", ".join(citation.authors[:2])
        if len(citation.authors) > 2:
            authors_str += " et al."

        # Truncate title if too long
        title = citation.title
        if len(title) > 60:
            title = title[:57] + "..."

        output += f"{i}. **{citation.id}**: {authors_str} ({citation.year}) - {title}\n"
        output += f"   - Relevance score: {score}\n"
        output += f"   - Matching keywords: {', '.join(matches)}\n\n"

    return output


def generate_suggestions_for_sections(
    database: CitationDatabase,
    sections: List[Tuple[str, str]],
    max_per_section: int = 5
) -> str:
    """
    Generate citation suggestions for multiple sections.

    Args:
        database: Citation database
        sections: List of (section_name, section_topic) tuples
        max_per_section: Max suggestions per section

    Returns:
        str: Formatted markdown with all suggestions
    """
    all_suggestions = []

    for section_name, section_topic in sections:
        suggestions = suggest_citations(database, section_topic, max_per_section)
        formatted = format_citation_suggestions(suggestions, section_name)
        all_suggestions.append(formatted)

    # Combine all sections
    output = "# Citation Suggestions by Section\n\n"
    output += "\n---\n\n".join(all_suggestions)

    return output
