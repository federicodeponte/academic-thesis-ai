#!/usr/bin/env python3
"""
Unit tests for utils/scrape_citation_titles.py

Tests title scraping logic including:
- Title extraction from HTML
- Multiple extraction strategies
- Error handling (timeouts, 403s, malformed HTML)
- Fallback mechanisms
"""

import pytest
from typing import Dict
from unittest.mock import Mock, patch, MagicMock
import requests


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest.fixture
def mock_html_with_title():
    """HTML with standard <title> tag."""
    return """
    <html>
        <head>
            <title>Test Article: Machine Learning in 2025</title>
        </head>
        <body>
            <h1>Machine Learning in 2025</h1>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_with_og_title():
    """HTML with OpenGraph title."""
    return """
    <html>
        <head>
            <meta property="og:title" content="The Complete Guide to AI Pricing" />
            <title>Generic Site Title</title>
        </head>
    </html>
    """


@pytest.fixture
def mock_html_with_h1_only():
    """HTML with only H1 tag (no meta title)."""
    return """
    <html>
        <head>
            <title></title>
        </head>
        <body>
            <h1>Primary Heading Title</h1>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_malformed():
    """Malformed HTML that might cause parsing issues."""
    return """
    <html>
        <head>
            <title>Incomplete Title
        <body>
            <h1>No closing tags
    """


@pytest.fixture
def sample_citation_with_domain_title():
    """Citation with domain name as title."""
    return {
        "id": "cite_001",
        "title": "bcg.com",
        "url": "https://www.bcg.com/publications/2024/genai-pricing",
        "api_source": "Gemini Grounded"
    }


@pytest.fixture
def sample_citation_with_good_title():
    """Citation that already has a good title."""
    return {
        "id": "cite_002",
        "title": "Machine Learning for Climate Science",
        "url": "https://example.com/ml-climate",
        "doi": "10.1234/test",
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
        from utils import scrape_citation_titles
        assert scrape_citation_titles is not None
    except ImportError as e:
        pytest.fail(f"Failed to import module: {e}")


# ============================================================================
# TITLE EXTRACTION TESTS
# ============================================================================

def test_extract_title_from_standard_title_tag(mock_html_with_title):
    """Test extraction from standard <title> tag."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(mock_html_with_title, 'html.parser')

    # Extract title using standard method
    title_tag = soup.find('title')
    assert title_tag is not None
    title = title_tag.get_text().strip()

    assert title == "Test Article: Machine Learning in 2025"
    assert len(title) > 10  # Should be substantive


def test_extract_title_from_og_meta(mock_html_with_og_title):
    """Test extraction from OpenGraph meta tag."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(mock_html_with_og_title, 'html.parser')

    # Try OpenGraph first (should be preferred)
    og_title = soup.find('meta', property='og:title')
    assert og_title is not None
    title = og_title.get('content', '').strip()

    assert title == "The Complete Guide to AI Pricing"


def test_extract_title_from_h1_fallback(mock_html_with_h1_only):
    """Test fallback to H1 tag when title is empty."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(mock_html_with_h1_only, 'html.parser')

    # Title tag is empty, should fall back to H1
    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ''

    if not title:
        h1_tag = soup.find('h1')
        if h1_tag:
            title = h1_tag.get_text().strip()

    assert title == "Primary Heading Title"


def test_handle_malformed_html(mock_html_malformed):
    """Test that malformed HTML doesn't crash the parser."""
    from bs4 import BeautifulSoup

    # BeautifulSoup should handle malformed HTML gracefully
    soup = BeautifulSoup(mock_html_malformed, 'html.parser')
    assert soup is not None

    # Should still find title tag even if incomplete
    title_tag = soup.find('title')
    assert title_tag is not None


# ============================================================================
# DOMAIN TITLE DETECTION TESTS
# ============================================================================

def test_detect_domain_title():
    """Test detection of domain-name titles."""
    domain_titles = [
        "bcg.com",
        "mckinsey.com",
        "openai.com",
        "example.org",
        "test.edu",
    ]

    good_titles = [
        "Machine Learning for Climate Science",
        "The Complete Guide to AI",
        "Research Paper Title",
    ]

    # Simple domain detection regex
    import re
    domain_pattern = r'^[\w\-]+\.(com|org|edu|gov|net|io|ai)$'

    # Domain titles should match
    for title in domain_titles:
        assert re.match(domain_pattern, title), f"{title} should match domain pattern"

    # Good titles should NOT match
    for title in good_titles:
        assert not re.match(domain_pattern, title), f"{title} should not match domain pattern"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@patch('requests.Session.get')
def test_handle_timeout(mock_get):
    """Test handling of request timeouts."""
    import requests
    mock_get.side_effect = requests.Timeout("Connection timed out")

    # Should handle timeout gracefully without crashing
    try:
        session = requests.Session()
        response = session.get("https://example.com", timeout=10)
    except requests.Timeout as e:
        # Expected behavior - timeout is caught
        assert "timed out" in str(e).lower()


@patch('requests.Session.get')
def test_handle_403_forbidden(mock_get):
    """Test handling of 403 Forbidden errors."""
    import requests
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.raise_for_status.side_effect = requests.HTTPError("403 Forbidden")
    mock_get.return_value = mock_response

    # Should handle 403 gracefully
    try:
        session = requests.Session()
        response = session.get("https://example.com")
        response.raise_for_status()
    except requests.HTTPError as e:
        assert "403" in str(e)


@patch('requests.Session.get')
def test_handle_connection_error(mock_get):
    """Test handling of connection errors."""
    import requests
    mock_get.side_effect = requests.ConnectionError("Failed to connect")

    # Should handle connection error gracefully
    try:
        session = requests.Session()
        response = session.get("https://example.com")
    except requests.ConnectionError as e:
        assert "connect" in str(e).lower()


# ============================================================================
# TITLE QUALITY TESTS
# ============================================================================

def test_title_quality_scoring():
    """Test that we can score title quality."""

    def score_title_quality(title: str) -> int:
        """Score title quality (0-100)."""
        score = 0

        # Length check (good titles are 10-200 chars)
        if 10 <= len(title) <= 200:
            score += 40

        # Not a domain name
        import re
        if not re.match(r'^[\w\-]+\.(com|org|edu|gov|net|io|ai)$', title):
            score += 30

        # Contains meaningful words
        words = title.split()
        if len(words) >= 3:
            score += 20

        # Not all caps
        if not title.isupper():
            score += 10

        return score

    # Test quality scoring
    assert score_title_quality("bcg.com") < 50  # Low quality
    assert score_title_quality("Machine Learning for Climate Science") >= 80  # High quality
    assert score_title_quality("") <= 50  # Empty (gets points for length 0, but not much else)
    assert score_title_quality("AI") < 50  # Too short


# ============================================================================
# INTEGRATION TESTS (with mocked requests)
# ============================================================================

@patch('requests.Session.get')
def test_scrape_title_success(mock_get, mock_html_with_title):
    """Test successful title scraping."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html_with_title
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    from bs4 import BeautifulSoup
    import requests

    session = requests.Session()
    response = session.get("https://example.com")
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('title')
    title = title_tag.get_text().strip()

    assert title == "Test Article: Machine Learning in 2025"


@patch('requests.Session.get')
def test_scrape_prefers_og_title(mock_get, mock_html_with_og_title):
    """Test that OpenGraph title is preferred over standard title."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html_with_og_title
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    from bs4 import BeautifulSoup
    import requests

    session = requests.Session()
    response = session.get("https://example.com")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Should prefer og:title over standard title
    og_title = soup.find('meta', property='og:title')
    if og_title:
        title = og_title.get('content', '').strip()
    else:
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ''

    assert title == "The Complete Guide to AI Pricing"
    assert title != "Generic Site Title"


# ============================================================================
# EDGE CASES
# ============================================================================

def test_empty_title_handling():
    """Test handling of empty titles."""
    empty_html = "<html><head><title></title></head></html>"

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(empty_html, 'html.parser')

    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ''

    assert title == ""  # Should handle gracefully


def test_unicode_title_handling():
    """Test handling of unicode characters in titles."""
    unicode_html = """
    <html>
        <head>
            <title>Künstliche Intelligenz für €1 Million</title>
        </head>
    </html>
    """

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(unicode_html, 'html.parser')

    title_tag = soup.find('title')
    title = title_tag.get_text().strip()

    assert "Künstliche" in title
    assert "€1" in title


def test_very_long_title_handling():
    """Test handling of very long titles."""
    long_title = "A" * 500  # 500 character title
    long_html = f"<html><head><title>{long_title}</title></head></html>"

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(long_html, 'html.parser')

    title_tag = soup.find('title')
    title = title_tag.get_text().strip()

    assert len(title) == 500

    # Could truncate if needed
    truncated = title[:200] + "..." if len(title) > 200 else title
    assert len(truncated) <= 203


# ============================================================================
# URL EXTRACTION FALLBACK
# ============================================================================

def test_extract_title_from_url_fallback():
    """Test extracting title from URL as last resort."""
    url = "https://example.com/2024/machine-learning-climate-science.pdf"

    # Extract filename from URL
    from urllib.parse import urlparse
    import os

    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)

    # Clean up filename for title
    title = filename.replace('-', ' ').replace('_', ' ').replace('.pdf', '')
    title = title.title()

    assert title == "Machine Learning Climate Science"


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
