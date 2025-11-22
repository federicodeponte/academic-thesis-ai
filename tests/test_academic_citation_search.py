#!/usr/bin/env python3
"""
Unit tests for academic_citation_search module.

Tests all academic API integrations:
- Semantic Scholar API
- CrossRef API
- arXiv API
- Citation validation
- Quality scoring
"""

import pytest
import sys
sys.path.insert(0, '.')

from utils.academic_citation_search import (
    Citation,
    search_semantic_scholar,
    search_crossref,
    search_arxiv,
    validate_doi,
    validate_citation_quality,
    _parse_semantic_scholar_paper,
    _parse_crossref_item,
    _parse_arxiv_entry
)


class TestCitation:
    """Test Citation dataclass and methods."""

    def test_citation_creation(self):
        """Test creating a citation with all fields."""
        citation = Citation(
            title="Example Paper",
            authors=["John Doe", "Jane Smith"],
            year=2020,
            venue="Example Conference",
            doi="10.1234/example",
            url="https://doi.org/10.1234/example",
            citation_count=100,
            api_source="Test",
            abstract="This is an example abstract.",
            arxiv_id="2001.12345"
        )

        assert citation.title == "Example Paper"
        assert len(citation.authors) == 2
        assert citation.year == 2020
        assert citation.doi is not None
        assert citation.arxiv_id is not None

    def test_citation_to_dict(self):
        """Test converting citation to dictionary."""
        citation = Citation(
            title="Example Paper",
            authors=["John Doe"],
            year=2020,
            venue="Example Venue",
            doi="10.1234/example"
        )

        citation_dict = citation.to_dict()
        assert isinstance(citation_dict, dict)
        assert citation_dict["title"] == "Example Paper"
        assert citation_dict["authors"] == ["John Doe"]

    def test_quality_score_high_quality(self):
        """Test quality score for high-quality citation."""
        citation = Citation(
            title="High Quality Paper",
            authors=["Expert Author"],
            year=2020,
            venue="Top Journal",
            doi="10.1234/example",
            url="https://doi.org/10.1234/example",
            citation_count=500,
            api_source="Semantic Scholar",
            abstract="Comprehensive abstract describing the research.",
            arxiv_id="2001.12345"
        )

        score = citation.quality_score()
        # Has DOI (2) + arXiv ID (1) + venue (2) + cites>10 (1) + abstract (1) = 7
        assert score == 7.0

    def test_quality_score_low_quality(self):
        """Test quality score for low-quality citation."""
        citation = Citation(
            title="Low Quality Paper",
            authors=["Unknown Author"],
            year=2020,
            venue="Unknown",
            url="https://example.com"
        )

        score = citation.quality_score()
        # No DOI, no arXiv, no abstract, low cites, unknown venue
        assert score < 2.0

    def test_quality_score_with_venue(self):
        """Test quality score includes venue points."""
        citation = Citation(
            title="Paper with Venue",
            authors=["Author"],
            year=2020,
            venue="Nature",
            doi="10.1038/example"
        )

        score = citation.quality_score()
        assert score >= 4.0  # DOI (2) + venue (2) = 4

    def test_quality_score_high_citations(self):
        """Test quality score bonus for high citation count."""
        citation = Citation(
            title="Highly Cited Paper",
            authors=["Popular Author"],
            year=2015,
            venue="Science",
            doi="10.1126/science.example",
            citation_count=1000
        )

        score = citation.quality_score()
        assert score >= 5.0  # DOI (2) + venue (2) + citations>10 (1) = 5


class TestSemanticScholar:
    """Test Semantic Scholar API integration."""

    def test_search_semantic_scholar_returns_citations(self):
        """Test that Semantic Scholar search returns citations."""
        citations = search_semantic_scholar("machine learning", limit=5)

        assert isinstance(citations, list)
        assert len(citations) > 0
        assert len(citations) <= 5

        # Check first citation structure
        c = citations[0]
        assert isinstance(c, Citation)
        assert c.title
        assert len(c.authors) > 0
        assert c.api_source == "Semantic Scholar"

    def test_search_semantic_scholar_empty_query(self):
        """Test that empty query raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            search_semantic_scholar("", limit=5)

    def test_search_semantic_scholar_invalid_limit(self):
        """Test that invalid limit raises ValueError."""
        with pytest.raises(ValueError, match="between 1 and 100"):
            search_semantic_scholar("test", limit=0)

        with pytest.raises(ValueError, match="between 1 and 100"):
            search_semantic_scholar("test", limit=101)

    def test_search_semantic_scholar_has_dois(self):
        """Test that most Semantic Scholar results have DOIs."""
        citations = search_semantic_scholar("deep learning", limit=10)

        with_doi = sum(1 for c in citations if c.doi)
        # At least 50% should have DOIs
        assert with_doi >= len(citations) * 0.5

    def test_parse_semantic_scholar_paper_valid(self):
        """Test parsing valid Semantic Scholar paper JSON."""
        paper = {
            "title": "Example Paper",
            "authors": [{"name": "John Doe"}, {"name": "Jane Smith"}],
            "year": 2020,
            "venue": "Example Conference",
            "externalIds": {"DOI": "10.1234/example"},
            "citationCount": 100,
            "url": "https://www.semanticscholar.org/paper/abc123",
            "abstract": "This is an abstract."
        }

        citation = _parse_semantic_scholar_paper(paper)

        assert citation is not None
        assert citation.title == "Example Paper"
        assert len(citation.authors) == 2
        assert citation.doi == "10.1234/example"
        assert citation.citation_count == 100

    def test_parse_semantic_scholar_paper_no_authors(self):
        """Test that papers without authors are skipped."""
        paper = {
            "title": "Paper Without Authors",
            "authors": [],
            "year": 2020
        }

        citation = _parse_semantic_scholar_paper(paper)
        assert citation is None

    def test_parse_semantic_scholar_paper_with_arxiv(self):
        """Test parsing paper with arXiv ID."""
        paper = {
            "title": "arXiv Paper",
            "authors": [{"name": "Researcher"}],
            "year": 2021,
            "venue": "arXiv preprint",
            "externalIds": {"ArXiv": "2101.12345"},
            "citationCount": 50
        }

        citation = _parse_semantic_scholar_paper(paper)

        assert citation is not None
        assert citation.arxiv_id == "2101.12345"
        assert "arxiv" in citation.url.lower()


class TestCrossRef:
    """Test CrossRef API integration."""

    def test_search_crossref_returns_citations(self):
        """Test that CrossRef search returns citations."""
        citations = search_crossref("artificial intelligence", limit=5)

        assert isinstance(citations, list)
        assert len(citations) > 0
        assert len(citations) <= 5

        # Check first citation
        c = citations[0]
        assert isinstance(c, Citation)
        assert c.api_source == "CrossRef"

    def test_search_crossref_empty_query(self):
        """Test that empty query raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            search_crossref("", limit=5)

    def test_search_crossref_invalid_limit(self):
        """Test that invalid limit raises ValueError."""
        with pytest.raises(ValueError, match="between 1 and 100"):
            search_crossref("test", limit=0)

    def test_search_crossref_all_have_dois(self):
        """Test that all CrossRef results have DOIs."""
        citations = search_crossref("computer science", limit=10)

        for c in citations:
            assert c.doi is not None
            assert c.doi.startswith("10.")

    def test_parse_crossref_item_valid(self):
        """Test parsing valid CrossRef item JSON."""
        item = {
            "title": ["Example Paper Title"],
            "author": [
                {"given": "John", "family": "Doe"},
                {"given": "Jane", "family": "Smith"}
            ],
            "published": {"date-parts": [[2020, 1, 15]]},
            "container-title": ["Example Journal"],
            "DOI": "10.1234/example.2020.001",
            "abstract": "This is the abstract."
        }

        citation = _parse_crossref_item(item)

        assert citation is not None
        assert citation.title == "Example Paper Title"
        assert len(citation.authors) == 2
        assert citation.year == 2020
        assert citation.venue == "Example Journal"
        assert citation.doi == "10.1234/example.2020.001"

    def test_parse_crossref_item_no_authors(self):
        """Test that items without authors are skipped."""
        item = {
            "title": ["Paper Without Authors"],
            "DOI": "10.1234/noauthor"
        }

        citation = _parse_crossref_item(item)
        assert citation is None

    def test_parse_crossref_item_family_name_only(self):
        """Test parsing author with only family name."""
        item = {
            "title": ["Paper"],
            "author": [{"family": "Smith"}],
            "published": {"date-parts": [[2020]]},
            "container-title": ["Journal"],
            "DOI": "10.1234/test"
        }

        citation = _parse_crossref_item(item)

        assert citation is not None
        assert "Smith" in citation.authors[0]


class TestArXiv:
    """Test arXiv API integration."""

    def test_search_arxiv_returns_citations(self):
        """Test that arXiv search returns citations."""
        citations = search_arxiv("neural networks", limit=5)

        assert isinstance(citations, list)
        assert len(citations) > 0
        assert len(citations) <= 5

        # Check first citation
        c = citations[0]
        assert isinstance(c, Citation)
        assert c.api_source == "arXiv"
        assert "arxiv" in c.venue.lower()

    def test_search_arxiv_empty_query(self):
        """Test that empty query raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            search_arxiv("", limit=5)

    def test_search_arxiv_invalid_limit(self):
        """Test that invalid limit raises ValueError."""
        with pytest.raises(ValueError, match="between 1 and 100"):
            search_arxiv("test", limit=0)

    def test_search_arxiv_all_have_arxiv_ids(self):
        """Test that all arXiv results have arXiv IDs."""
        citations = search_arxiv("quantum computing", limit=10)

        for c in citations:
            assert c.arxiv_id is not None
            assert "arxiv" in c.url.lower()


class TestDOIValidation:
    """Test DOI validation."""

    def test_validate_doi_valid(self):
        """Test validating a real DOI."""
        # This is a real DOI from a Nature paper
        valid_doi = "10.1038/nature12373"
        assert validate_doi(valid_doi) is True

    def test_validate_doi_invalid(self):
        """Test validating a fake DOI."""
        invalid_doi = "10.1234/fake.doi.that.does.not.exist"
        assert validate_doi(invalid_doi) is False

    def test_validate_doi_empty(self):
        """Test that empty DOI returns False."""
        assert validate_doi("") is False
        assert validate_doi("   ") is False

    def test_validate_doi_malformed(self):
        """Test that malformed DOI returns False."""
        assert validate_doi("not-a-doi") is False


class TestCitationQualityValidation:
    """Test citation quality validation."""

    def test_validate_high_quality_citation(self):
        """Test validating a high-quality citation."""
        citation = Citation(
            title="High Quality Paper",
            authors=["Dr. Expert"],
            year=2020,
            venue="Nature",
            doi="10.1038/example",
            url="https://doi.org/10.1038/example",
            citation_count=500,
            api_source="Semantic Scholar",
            abstract="Comprehensive abstract."
        )

        assert validate_citation_quality(citation) is True

    def test_validate_citation_no_title(self):
        """Test that citation without title fails validation."""
        citation = Citation(
            title="",
            authors=["Author"],
            year=2020,
            venue="Venue",
            doi="10.1234/example"
        )

        assert validate_citation_quality(citation) is False

    def test_validate_citation_untitled(self):
        """Test that 'Untitled' citation fails validation."""
        citation = Citation(
            title="Untitled",
            authors=["Author"],
            year=2020,
            venue="Venue",
            doi="10.1234/example"
        )

        assert validate_citation_quality(citation) is False

    def test_validate_citation_no_authors(self):
        """Test that citation without authors fails validation."""
        citation = Citation(
            title="Paper",
            authors=[],
            year=2020,
            venue="Venue",
            doi="10.1234/example"
        )

        assert validate_citation_quality(citation) is False

    def test_validate_citation_domain_as_author(self):
        """Test that domain name as author fails validation."""
        citation = Citation(
            title="Paper",
            authors=["example.com"],
            year=2020,
            venue="Venue",
            doi="10.1234/example"
        )

        assert validate_citation_quality(citation) is False

    def test_validate_citation_invalid_year_too_old(self):
        """Test that citation with year < 1950 fails validation."""
        citation = Citation(
            title="Paper",
            authors=["Author"],
            year=1900,
            venue="Venue",
            doi="10.1234/example"
        )

        assert validate_citation_quality(citation) is False

    def test_validate_citation_invalid_year_future(self):
        """Test that citation with year > 2025 fails validation."""
        citation = Citation(
            title="Paper",
            authors=["Author"],
            year=2030,
            venue="Venue",
            doi="10.1234/example"
        )

        assert validate_citation_quality(citation) is False

    def test_validate_citation_no_doi_or_arxiv(self):
        """Test that citation without DOI or arXiv ID fails validation."""
        citation = Citation(
            title="Paper",
            authors=["Author"],
            year=2020,
            venue="Venue",
            url="https://example.com"
        )

        assert validate_citation_quality(citation) is False

    def test_validate_citation_with_arxiv_id(self):
        """Test that citation with arXiv ID passes (even without DOI)."""
        citation = Citation(
            title="arXiv Preprint",
            authors=["Researcher"],
            year=2021,
            venue="arXiv preprint",
            url="https://arxiv.org/abs/2101.12345",
            arxiv_id="2101.12345",
            abstract="Abstract text"
        )

        # Quality score: arXiv ID (1) + venue (2) + abstract (1) = 4.0
        assert citation.quality_score() == 4.0
        assert validate_citation_quality(citation) is True

    def test_validate_citation_low_quality_score(self):
        """Test that citation with quality score < 4.0 fails validation."""
        citation = Citation(
            title="Low Quality Paper",
            authors=["Unknown"],
            year=2020,
            venue="Unknown",
            doi="10.1234/example"
        )

        # Quality score: DOI (2) only = 2.0 < 4.0
        assert citation.quality_score() < 4.0
        assert validate_citation_quality(citation) is False

    def test_validate_citation_edge_case_quality_score(self):
        """Test citation exactly at quality threshold."""
        citation = Citation(
            title="Marginal Quality Paper",
            authors=["Author"],
            year=2020,
            venue="Conference",
            doi="10.1234/example"
        )

        # Quality score: DOI (2) + venue (2) = 4.0 (exactly at threshold)
        assert citation.quality_score() == 4.0
        assert validate_citation_quality(citation) is True


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
