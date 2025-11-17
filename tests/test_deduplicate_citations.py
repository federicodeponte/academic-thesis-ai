#!/usr/bin/env python3
"""
Unit tests for utils/deduplicate_citations.py

Tests citation deduplication logic including:
- DOI-based matching
- URL-based matching
- Title similarity matching
- Keep-best and keep-first strategies
- Edge cases and error handling
"""

import pytest
from typing import List, Dict
from utils.deduplicate_citations import deduplicate_citations


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest.fixture
def sample_citations_with_doi_duplicates() -> List[Dict]:
    """Citations with exact DOI duplicates."""
    return [
        {
            "id": "cite_001",
            "title": "Machine Learning for Climate Science",
            "authors": ["Smith, J.", "Jones, A."],
            "year": 2023,
            "doi": "10.1145/3580305.3599318",
            "url": "https://dl.acm.org/doi/10.1145/3580305.3599318",
            "api_source": "Crossref"
        },
        {
            "id": "cite_002",
            "title": "Machine Learning for Climate Science",
            "authors": ["Smith, J.", "Jones, A."],
            "year": 2023,
            "doi": "10.1145/3580305.3599318",  # Same DOI - duplicate
            "url": "https://arxiv.org/abs/2305.12345",
            "api_source": "Semantic Scholar"
        },
        {
            "id": "cite_003",
            "title": "Unique Paper 1",
            "authors": ["Brown, T."],
            "year": 2024,
            "doi": "10.1038/s41586-024-07001-2",
            "url": "https://nature.com/articles/unique1",
            "api_source": "Crossref"
        }
    ]


@pytest.fixture
def sample_citations_with_url_duplicates() -> List[Dict]:
    """Citations with exact URL duplicates."""
    return [
        {
            "id": "cite_001",
            "title": "Open Source AI Frameworks",
            "authors": ["Brown, T."],
            "year": 2024,
            "doi": None,
            "url": "https://www.bcg.com/publications/2024/ai-frameworks",
            "api_source": "Gemini Grounded"
        },
        {
            "id": "cite_002",
            "title": "Open Source AI Frameworks - Full Report",
            "authors": ["Brown, T.", "Davis, M."],
            "year": 2024,
            "doi": None,
            "url": "https://www.bcg.com/publications/2024/ai-frameworks",  # Same URL - duplicate
            "api_source": "Gemini Grounded"
        },
        {
            "id": "cite_003",
            "title": "Unique Paper 2",
            "authors": ["Taylor, R."],
            "year": 2024,
            "doi": None,
            "url": "https://example.com/unique2",
            "api_source": "Semantic Scholar"
        }
    ]


@pytest.fixture
def sample_citations_with_title_duplicates() -> List[Dict]:
    """Citations with highly similar titles."""
    return [
        {
            "id": "cite_001",
            "title": "Pricing Models for Artificial Intelligence Services",
            "authors": ["Wilson, K."],
            "year": 2023,
            "doi": None,
            "url": "https://example.com/paper1",
            "api_source": "Semantic Scholar"
        },
        {
            "id": "cite_002",
            "title": "Pricing Models for AI Services",  # Very similar title
            "authors": ["Wilson, K."],
            "year": 2023,
            "doi": None,
            "url": "https://example.com/paper2",
            "api_source": "Gemini Grounded"
        },
        {
            "id": "cite_003",
            "title": "Completely Different Topic About Blockchain",
            "authors": ["Johnson, P."],
            "year": 2024,
            "doi": None,
            "url": "https://example.com/paper3",
            "api_source": "Crossref"
        }
    ]


# ============================================================================
# TEST DEDUPLICATION FUNCTION
# ============================================================================

def test_deduplicate_doi_duplicates(sample_citations_with_doi_duplicates):
    """Test that DOI duplicates are removed."""
    deduplicated, stats = deduplicate_citations(
        sample_citations_with_doi_duplicates,
        strategy='keep_best',
        verbose=False
    )

    # Original: 3 citations (2 duplicates + 1 unique)
    # Expected: 2 citations after removing 1 duplicate
    assert stats['original_count'] == 3
    assert stats['removed_count'] == 1
    assert stats['final_count'] == 2

    # Should keep cite_003 (unique)
    ids = [c["id"] for c in deduplicated]
    assert "cite_003" in ids

    # Should keep only one of cite_001 or cite_002
    assert ("cite_001" in ids) or ("cite_002" in ids)
    assert not (("cite_001" in ids) and ("cite_002" in ids))


def test_deduplicate_url_duplicates(sample_citations_with_url_duplicates):
    """Test that URL duplicates are removed."""
    deduplicated, stats = deduplicate_citations(
        sample_citations_with_url_duplicates,
        strategy='keep_best',
        verbose=False
    )

    # Original: 3 citations (2 duplicates + 1 unique)
    # Expected: 2 citations after removing 1 duplicate
    assert stats['original_count'] == 3
    assert stats['removed_count'] == 1
    assert stats['final_count'] == 2

    # Should keep cite_003 (unique)
    ids = [c["id"] for c in deduplicated]
    assert "cite_003" in ids

    # Should keep only one of cite_001 or cite_002
    assert ("cite_001" in ids) or ("cite_002" in ids)
    assert not (("cite_001" in ids) and ("cite_002" in ids))


def test_deduplicate_title_duplicates(sample_citations_with_title_duplicates):
    """Test that title similarity duplicates are removed."""
    deduplicated, stats = deduplicate_citations(
        sample_citations_with_title_duplicates,
        strategy='keep_best',
        verbose=False
    )

    # Original: 3 citations (2 similar titles + 1 unique)
    # Expected: 2 citations (might remove 1 if similarity > 90%)
    assert stats['original_count'] == 3
    assert stats['final_count'] >= 2  # At least 2 should remain

    # Should keep cite_003 (completely different)
    ids = [c["id"] for c in deduplicated]
    assert "cite_003" in ids


def test_deduplicate_statistics():
    """Test that statistics are calculated correctly."""
    citations = [
        {"id": "cite_001", "title": "Paper 1", "doi": "10.1234/test"},
        {"id": "cite_002", "title": "Paper 1", "doi": "10.1234/test"},  # Duplicate
        {"id": "cite_003", "title": "Paper 2", "doi": "10.5678/test"}
    ]

    deduplicated, stats = deduplicate_citations(
        citations,
        strategy='keep_best',
        verbose=False
    )

    # Verify statistics keys exist
    assert 'original_count' in stats
    assert 'final_count' in stats
    assert 'removed_count' in stats

    # Verify statistics values
    assert stats['original_count'] == 3
    assert stats['final_count'] == 2
    assert stats['removed_count'] == 1


def test_deduplicate_keep_best_strategy():
    """Test that keep_best strategy keeps higher quality citation."""
    citations = [
        {
            "id": "cite_001",
            "title": "Test Paper",
            "authors": [],  # Low quality - no authors
            "year": None,
            "doi": "10.1234/test",
            "api_source": "Gemini Grounded"
        },
        {
            "id": "cite_002",
            "title": "Test Paper",
            "authors": ["Smith, J.", "Jones, A."],  # High quality - has authors
            "year": 2023,
            "doi": "10.1234/test",
            "api_source": "Crossref"
        }
    ]

    deduplicated, stats = deduplicate_citations(
        citations,
        strategy='keep_best',
        verbose=False
    )

    # Should keep cite_002 (higher quality with authors)
    assert len(deduplicated) == 1
    assert deduplicated[0]["id"] == "cite_002"


def test_deduplicate_keep_first_strategy():
    """Test that keep_first strategy keeps first encountered citation."""
    citations = [
        {
            "id": "cite_001",
            "title": "Test Paper",
            "authors": [],
            "year": None,
            "doi": "10.1234/test",
            "api_source": "Gemini Grounded"
        },
        {
            "id": "cite_002",
            "title": "Test Paper",
            "authors": ["Smith, J."],
            "year": 2023,
            "doi": "10.1234/test",
            "api_source": "Crossref"
        }
    ]

    deduplicated, stats = deduplicate_citations(
        citations,
        strategy='keep_first',
        verbose=False
    )

    # Should keep cite_001 (first encountered), even though cite_002 is higher quality
    assert len(deduplicated) == 1
    assert deduplicated[0]["id"] == "cite_001"


def test_deduplicate_empty_list():
    """Test with empty citation list."""
    deduplicated, stats = deduplicate_citations(
        [],
        strategy='keep_best',
        verbose=False
    )

    assert len(deduplicated) == 0
    assert stats['original_count'] == 0
    assert stats['final_count'] == 0
    assert stats['removed_count'] == 0


def test_deduplicate_single_citation():
    """Test with single citation (no duplicates possible)."""
    citations = [
        {"id": "cite_001", "title": "Unique Paper", "doi": "10.1234/unique"}
    ]

    deduplicated, stats = deduplicate_citations(
        citations,
        strategy='keep_best',
        verbose=False
    )

    assert len(deduplicated) == 1
    assert stats['removed_count'] == 0
    assert deduplicated[0]["id"] == "cite_001"


def test_deduplicate_no_duplicates():
    """Test with all unique citations."""
    citations = [
        {"id": "cite_001", "title": "Paper 1", "doi": "10.1234/001"},
        {"id": "cite_002", "title": "Paper 2", "doi": "10.1234/002"},
        {"id": "cite_003", "title": "Paper 3", "doi": "10.1234/003"}
    ]

    deduplicated, stats = deduplicate_citations(
        citations,
        strategy='keep_best',
        verbose=False
    )

    assert len(deduplicated) == 3
    assert stats['removed_count'] == 0


def test_deduplicate_missing_fields():
    """Test citations with missing/None fields."""
    citations = [
        {"id": "cite_001", "title": "Paper 1"},  # Missing most fields
        {"id": "cite_002", "title": "Paper 2", "doi": None, "url": None},
        {"id": "cite_003", "title": "Paper 3", "authors": [], "year": None}
    ]

    # Should not crash, should handle gracefully
    deduplicated, stats = deduplicate_citations(
        citations,
        strategy='keep_best',
        verbose=False
    )

    assert len(deduplicated) == 3  # All unique
    assert stats['removed_count'] == 0


def test_deduplicate_unicode_titles():
    """Test citations with unicode characters in titles."""
    citations = [
        {
            "id": "cite_001",
            "title": "Künstliche Intelligenz und Klimawandel",
            "doi": "10.1234/de1",
            "authors": ["Müller, K."]
        },
        {
            "id": "cite_002",
            "title": "Künstliche Intelligenz und Klimawandel",  # Same German title
            "doi": "10.1234/de1",
            "authors": ["Müller, K."]
        },
        {
            "id": "cite_003",
            "title": "Aprendizaje automático para ciencia climática",
            "doi": "10.1234/es1",
            "authors": ["García, M."]
        }
    ]

    deduplicated, stats = deduplicate_citations(
        citations,
        strategy='keep_best',
        verbose=False
    )

    # Should handle unicode correctly
    assert stats['removed_count'] == 1  # German duplicate removed
    assert len(deduplicated) == 2


def test_deduplicate_preserves_citation_structure():
    """Test that citation structure is preserved after deduplication."""
    citations = [
        {
            "id": "cite_001",
            "title": "Test Paper",
            "authors": ["Smith, J."],
            "year": 2023,
            "doi": "10.1234/test",
            "url": "https://example.com/test",
            "api_source": "Crossref",
            "journal": "Nature",
            "custom_field": "custom_value"  # Extra field
        }
    ]

    deduplicated, stats = deduplicate_citations(
        citations,
        strategy='keep_best',
        verbose=False
    )

    # Should preserve all fields
    assert deduplicated[0]["id"] == "cite_001"
    assert deduplicated[0]["title"] == "Test Paper"
    assert deduplicated[0]["authors"] == ["Smith, J."]
    assert deduplicated[0]["year"] == 2023
    assert deduplicated[0]["doi"] == "10.1234/test"
    assert deduplicated[0]["custom_field"] == "custom_value"


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
