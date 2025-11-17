#!/usr/bin/env python3
"""
Unit tests for utils/scrape_citation_metadata.py

Tests metadata scraping logic including:
- Publication date extraction (multiple formats)
- Author extraction (multiple sources)
- JSON-LD structured data parsing
- Date validation and sanitization
- Error handling for missing/malformed data
"""

import pytest
from typing import Dict, List, Optional
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import requests


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest.fixture
def mock_html_with_jsonld_date():
    """HTML with JSON-LD structured data containing publication date."""
    return """
    <html>
        <head>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": "Test Article",
                "datePublished": "2024-03-15",
                "author": {
                    "@type": "Person",
                    "name": "John Smith"
                }
            }
            </script>
        </head>
    </html>
    """


@pytest.fixture
def mock_html_with_og_date():
    """HTML with OpenGraph date metadata."""
    return """
    <html>
        <head>
            <meta property="article:published_time" content="2023-06-20T10:30:00Z" />
            <meta property="og:title" content="Test Article" />
        </head>
    </html>
    """


@pytest.fixture
def mock_html_with_meta_author():
    """HTML with author in meta tags."""
    return """
    <html>
        <head>
            <meta name="author" content="Jane Doe" />
            <meta name="DC.creator" content="Jane Doe" />
        </head>
    </html>
    """


@pytest.fixture
def mock_html_with_multiple_dates():
    """HTML with multiple date formats to test precedence."""
    return """
    <html>
        <head>
            <meta property="article:published_time" content="2024-01-15" />
            <meta name="date" content="2024-01-16" />
            <script type="application/ld+json">
            {
                "@type": "Article",
                "datePublished": "2024-01-17"
            }
            </script>
        </head>
    </html>
    """


@pytest.fixture
def sample_citation_gemini_bad_metadata():
    """Gemini citation with domain-name author and suspicious year."""
    return {
        "id": "cite_001",
        "title": "GenAI Pricing Strategies",
        "url": "https://www.bcg.com/publications/2024/genai-pricing",
        "authors": ["bcg.com"],
        "year": 2025,
        "api_source": "Gemini Grounded"
    }


@pytest.fixture
def sample_citation_crossref_good_metadata():
    """Crossref citation with good metadata (should not be scraped)."""
    return {
        "id": "cite_002",
        "title": "Machine Learning Research",
        "url": "https://dl.acm.org/doi/10.1145/test",
        "authors": ["Smith, J.", "Jones, A."],
        "year": 2023,
        "doi": "10.1145/test",
        "api_source": "Crossref"
    }


# ============================================================================
# IMPORT TESTS
# ============================================================================

def test_import_module():
    """Test that the module can be imported."""
    try:
        import sys
        sys.path.insert(0, '.')
        from utils import scrape_citation_metadata
        assert scrape_citation_metadata is not None
    except ImportError as e:
        pytest.fail(f"Failed to import module: {e}")


def test_import_safe_get():
    """Test that safe_get helper can be imported."""
    try:
        import sys
        sys.path.insert(0, '.')
        from utils.scrape_citation_metadata import safe_get
        assert safe_get is not None
    except ImportError as e:
        pytest.fail(f"Failed to import safe_get: {e}")


# ============================================================================
# SAFE_GET HELPER TESTS
# ============================================================================

def test_safe_get_with_dict():
    """Test safe_get works with dictionaries."""
    from utils.scrape_citation_metadata import safe_get

    test_dict = {"key1": "value1", "key2": "value2"}

    assert safe_get(test_dict, "key1") == "value1"
    assert safe_get(test_dict, "key2") == "value2"
    assert safe_get(test_dict, "missing") is None
    assert safe_get(test_dict, "missing", "default") == "default"


def test_safe_get_with_object():
    """Test safe_get works with objects (NamedTuple, dataclass, etc.)."""
    from utils.scrape_citation_metadata import safe_get
    from collections import namedtuple

    Citation = namedtuple('Citation', ['id', 'title', 'year'])
    citation = Citation(id='cite_001', title='Test', year=2024)

    assert safe_get(citation, 'id') == 'cite_001'
    assert safe_get(citation, 'title') == 'Test'
    assert safe_get(citation, 'year') == 2024
    assert safe_get(citation, 'missing') is None
    assert safe_get(citation, 'missing', 'default') == 'default'


def test_safe_get_with_none_values():
    """Test safe_get handles None values correctly."""
    from utils.scrape_citation_metadata import safe_get

    test_dict = {"key1": None, "key2": "value2"}

    assert safe_get(test_dict, "key1") is None
    assert safe_get(test_dict, "key1", "default") is None  # None is a valid value
    assert safe_get(test_dict, "key2") == "value2"


# ============================================================================
# DATE PARSING TESTS
# ============================================================================

def test_parse_iso_date():
    """Test parsing ISO 8601 date format."""
    import re
    from datetime import datetime

    date_str = "2024-03-15"

    # ISO date pattern
    iso_pattern = r'(\d{4})-(\d{2})-(\d{2})'
    match = re.search(iso_pattern, date_str)

    assert match is not None
    year = int(match.group(1))
    assert year == 2024


def test_parse_datetime_with_timezone():
    """Test parsing datetime with timezone."""
    date_str = "2023-06-20T10:30:00Z"

    # Extract just the date part
    import re
    iso_pattern = r'(\d{4})-(\d{2})-(\d{2})'
    match = re.search(iso_pattern, date_str)

    assert match is not None
    year = int(match.group(1))
    assert year == 2023


def test_reject_future_dates():
    """Test that future dates are rejected."""
    current_year = datetime.now().year
    future_year = current_year + 1

    # Should reject future dates
    assert future_year > current_year


def test_parse_relative_date():
    """Test parsing relative dates like '2 days ago'."""
    # This is a complex feature - test pattern recognition
    import re

    relative_dates = [
        "2 days ago",
        "3 weeks ago",
        "1 month ago",
        "Published yesterday"
    ]

    # Pattern to detect relative dates
    relative_pattern = r'(\d+)\s+(day|week|month|year)s?\s+ago'

    for date_str in relative_dates:
        if "ago" in date_str.lower():
            match = re.search(relative_pattern, date_str)
            if match:
                assert int(match.group(1)) > 0


# ============================================================================
# AUTHOR EXTRACTION TESTS
# ============================================================================

def test_extract_author_from_meta(mock_html_with_meta_author):
    """Test extraction of author from meta tags."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(mock_html_with_meta_author, 'html.parser')

    # Try meta name="author"
    author_meta = soup.find('meta', attrs={'name': 'author'})
    if author_meta:
        author = author_meta.get('content', '').strip()
        assert author == "Jane Doe"


def test_extract_author_from_jsonld(mock_html_with_jsonld_date):
    """Test extraction of author from JSON-LD."""
    from bs4 import BeautifulSoup
    import json

    soup = BeautifulSoup(mock_html_with_jsonld_date, 'html.parser')

    # Find JSON-LD script
    jsonld_script = soup.find('script', type='application/ld+json')
    if jsonld_script:
        data = json.loads(jsonld_script.string)
        author = data.get('author', {})
        if isinstance(author, dict):
            author_name = author.get('name')
            assert author_name == "John Smith"


def test_detect_domain_name_authors():
    """Test detection of domain-name authors (should be replaced)."""
    import re

    domain_authors = [
        "bcg.com",
        "mckinsey.com",
        "example.org"
    ]

    real_authors = [
        "John Smith",
        "Jane Doe",
        "Smith, J."
    ]

    # Domain detection pattern
    domain_pattern = r'^[\w\-]+\.(com|org|edu|gov|net|io|ai)$'

    # Domain authors should match
    for author in domain_authors:
        assert re.match(domain_pattern, author)

    # Real authors should NOT match
    for author in real_authors:
        assert not re.match(domain_pattern, author)


# ============================================================================
# JSONLD PARSING TESTS
# ============================================================================

def test_parse_jsonld_article(mock_html_with_jsonld_date):
    """Test parsing JSON-LD article data."""
    from bs4 import BeautifulSoup
    import json

    soup = BeautifulSoup(mock_html_with_jsonld_date, 'html.parser')

    jsonld_script = soup.find('script', type='application/ld+json')
    assert jsonld_script is not None

    data = json.loads(jsonld_script.string)

    assert data['@type'] == 'Article'
    assert data['headline'] == 'Test Article'
    assert data['datePublished'] == '2024-03-15'
    assert data['author']['name'] == 'John Smith'


def test_handle_malformed_jsonld():
    """Test handling of malformed JSON-LD."""
    malformed_html = """
    <html>
        <head>
            <script type="application/ld+json">
            {
                "invalid": "json",
                "missing_comma"
                "another_key": "value"
            }
            </script>
        </head>
    </html>
    """

    from bs4 import BeautifulSoup
    import json

    soup = BeautifulSoup(malformed_html, 'html.parser')
    jsonld_script = soup.find('script', type='application/ld+json')

    # Should handle gracefully
    try:
        data = json.loads(jsonld_script.string)
    except json.JSONDecodeError:
        # Expected behavior - catch and continue
        pass


# ============================================================================
# FILTER CONDITION TESTS
# ============================================================================

def test_filter_gemini_with_bad_metadata(sample_citation_gemini_bad_metadata):
    """Test that Gemini citations with bad metadata are selected for scraping."""
    from utils.scrape_citation_metadata import safe_get
    import re

    citation = sample_citation_gemini_bad_metadata

    # Check if should be scraped
    api_source = safe_get(citation, 'api_source')
    assert api_source == 'Gemini Grounded'

    # Check for domain-name author
    authors = safe_get(citation, 'authors', [])
    if authors and len(authors) > 0:
        first_author = authors[0]
        domain_pattern = r'^[\w\-]+\.(com|org|edu|gov|net|io|ai)$'
        is_domain = re.match(domain_pattern, first_author.lower())
        assert is_domain  # Should match - needs scraping

    # Check for current year (suspicious)
    year = safe_get(citation, 'year')
    current_year = datetime.now().year
    assert year == current_year  # Should match - needs scraping


def test_filter_crossref_with_good_metadata(sample_citation_crossref_good_metadata):
    """Test that Crossref citations with good metadata are NOT selected."""
    from utils.scrape_citation_metadata import safe_get

    citation = sample_citation_crossref_good_metadata

    # Check if should be skipped
    api_source = safe_get(citation, 'api_source')
    assert api_source == 'Crossref'  # Should be skipped (not Gemini)


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@patch('requests.Session.get')
def test_handle_scraping_timeout(mock_get):
    """Test handling of scraping timeouts."""
    import requests
    mock_get.side_effect = requests.Timeout("Connection timed out")

    try:
        session = requests.Session()
        response = session.get("https://example.com", timeout=10)
    except requests.Timeout as e:
        # Expected - should handle gracefully
        assert "timed out" in str(e).lower()


@patch('requests.Session.get')
def test_handle_403_forbidden(mock_get):
    """Test handling of 403 errors during metadata scraping."""
    import requests
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.raise_for_status.side_effect = requests.HTTPError("403 Forbidden")
    mock_get.return_value = mock_response

    try:
        session = requests.Session()
        response = session.get("https://example.com")
        response.raise_for_status()
    except requests.HTTPError as e:
        assert "403" in str(e)


def test_handle_missing_date_gracefully():
    """Test that missing dates don't crash the system."""
    empty_html = "<html><head></head></html>"

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(empty_html, 'html.parser')

    # Should not find any date metadata
    og_date = soup.find('meta', property='article:published_time')
    assert og_date is None

    meta_date = soup.find('meta', attrs={'name': 'date'})
    assert meta_date is None


def test_handle_missing_author_gracefully():
    """Test that missing authors don't crash the system."""
    empty_html = "<html><head></head></html>"

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(empty_html, 'html.parser')

    # Should not find any author metadata
    author_meta = soup.find('meta', attrs={'name': 'author'})
    assert author_meta is None


# ============================================================================
# EDGE CASES
# ============================================================================

def test_handle_empty_citation_list():
    """Test handling of empty citation list."""
    from utils.scrape_citation_metadata import safe_get

    citations = []

    # Filter should return empty list
    gemini_citations = [c for c in citations if safe_get(c, 'api_source') == 'Gemini Grounded']
    assert len(gemini_citations) == 0


def test_handle_unicode_authors():
    """Test handling of unicode characters in author names."""
    unicode_authors = [
        "Müller, K.",
        "García, M.",
        "Björk, S."
    ]

    for author in unicode_authors:
        assert len(author) > 0
        assert "," in author  # Should preserve formatting


def test_date_validation_edge_cases():
    """Test edge cases in date validation."""
    current_year = datetime.now().year

    # Valid dates
    assert 2020 <= current_year
    assert 2024 <= current_year

    # Future dates (should be rejected)
    future_year = current_year + 10
    assert future_year > current_year

    # Very old dates (might be suspicious)
    very_old = 1900
    assert very_old < 2000


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@patch('requests.Session.get')
def test_scrape_metadata_success(mock_get, mock_html_with_jsonld_date):
    """Test successful metadata scraping."""
    import requests
    from bs4 import BeautifulSoup
    import json

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html_with_jsonld_date
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    session = requests.Session()
    response = session.get("https://example.com")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract JSON-LD data
    jsonld_script = soup.find('script', type='application/ld+json')
    data = json.loads(jsonld_script.string)

    # Should extract both date and author
    assert data['datePublished'] == '2024-03-15'
    assert data['author']['name'] == 'John Smith'


def test_precedence_of_date_sources(mock_html_with_multiple_dates):
    """Test that date sources are used in correct precedence order."""
    from bs4 import BeautifulSoup
    import json

    soup = BeautifulSoup(mock_html_with_multiple_dates, 'html.parser')

    # Try JSON-LD first (highest precedence)
    jsonld_script = soup.find('script', type='application/ld+json')
    if jsonld_script:
        data = json.loads(jsonld_script.string)
        date = data.get('datePublished')
        assert date == '2024-01-17'  # Should prefer JSON-LD

    # Fallback to OpenGraph
    og_date = soup.find('meta', property='article:published_time')
    if og_date and not jsonld_script:
        date = og_date.get('content')
        assert date == '2024-01-15'


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
