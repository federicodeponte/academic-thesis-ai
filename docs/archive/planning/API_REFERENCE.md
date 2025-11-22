# API Reference

This document provides comprehensive API documentation for the OpenDraft project.

## Table of Contents

- [Core Modules](#core-modules)
- [Utilities](#utilities)
- [MCP Servers](#mcp-servers)
- [Concurrency](#concurrency)
- [Configuration](#configuration)
- [PDF Engines](#pdf-engines)
- [Formatting](#formatting)

---

## Core Modules

### config.py

Project-wide configuration management.

**Key Functions:**

```python
def load_config() -> dict:
    """
    Load configuration from environment variables and config files.

    Returns:
        dict: Configuration dictionary with API keys and settings

    Environment Variables:
        - GEMINI_API_KEY: Google Gemini API key
        - ANTHROPIC_API_KEY: Anthropic Claude API key
        - OPENAI_API_KEY: OpenAI API key
    """
```

---

## Utilities

### utils/text_utils.py

Text processing and manipulation utilities.

**Functions:**

```python
def clean_text(text: str) -> str:
    """
    Clean and normalize text content.

    Args:
        text (str): Input text to clean

    Returns:
        str: Cleaned text with normalized whitespace and characters
    """

def extract_keywords(text: str, top_n: int = 10) -> list:
    """
    Extract key terms from text.

    Args:
        text (str): Input text
        top_n (int): Number of keywords to extract (default: 10)

    Returns:
        list: List of extracted keywords
    """

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list:
    """
    Split text into overlapping chunks for processing.

    Args:
        text (str): Input text
        chunk_size (int): Maximum characters per chunk
        overlap (int): Number of overlapping characters between chunks

    Returns:
        list: List of text chunks
    """
```

---

### utils/academic_citation_search.py

Academic database search and citation retrieval.

**Functions:**

```python
def search_papers(query: str, max_results: int = 10, source: str = "all") -> list:
    """
    Search academic papers across databases.

    Args:
        query (str): Search query
        max_results (int): Maximum number of results
        source (str): Database source ("scholar", "pubmed", "arxiv", "all")

    Returns:
        list: List of paper metadata dictionaries

    Example:
        >>> papers = search_papers("machine learning", max_results=5)
        >>> for paper in papers:
        ...     print(paper['title'], paper['authors'])
    """

def get_paper_metadata(paper_id: str, source: str) -> dict:
    """
    Retrieve detailed metadata for a specific paper.

    Args:
        paper_id (str): Paper identifier (DOI, arXiv ID, etc.)
        source (str): Database source

    Returns:
        dict: Paper metadata including title, authors, abstract, citations

    Raises:
        ValueError: If paper_id is invalid
        APIError: If database API fails
    """
```

---

### utils/scrape_citation_metadata.py

Citation metadata scraping and enrichment.

**Functions:**

```python
def enrich_citation(citation: str) -> dict:
    """
    Enrich a citation with additional metadata.

    Args:
        citation (str): Raw citation string

    Returns:
        dict: Enriched citation data with DOI, abstract, etc.
    """

def validate_citation_format(citation: str, style: str = "APA") -> bool:
    """
    Validate citation format.

    Args:
        citation (str): Citation string
        style (str): Citation style ("APA", "MLA", "Chicago", "IEEE")

    Returns:
        bool: True if citation format is valid
    """
```

---

### utils/citation_validation.py

Citation format validation and correction.

**Functions:**

```python
def validate_citations(text: str, style: str = "APA") -> dict:
    """
    Validate all citations in a document.

    Args:
        text (str): Document text
        style (str): Expected citation style

    Returns:
        dict: Validation results with errors and suggestions
            {
                'valid': bool,
                'errors': list,
                'suggestions': list,
                'citation_count': int
            }
    """

def auto_correct_citations(text: str, style: str = "APA") -> str:
    """
    Automatically correct citation formatting.

    Args:
        text (str): Document text
        style (str): Target citation style

    Returns:
        str: Text with corrected citations
    """
```

---

### utils/deduplicate_citations.py

Citation deduplication utilities.

**Functions:**

```python
def deduplicate_citations(citations: list) -> list:
    """
    Remove duplicate citations.

    Args:
        citations (list): List of citation dictionaries

    Returns:
        list: Deduplicated citation list

    Note:
        Uses fuzzy matching to identify near-duplicate citations
    """
```

---

### utils/output_sanitizer.py

Output cleaning and sanitization.

**Functions:**

```python
def sanitize_output(text: str, remove_ai_artifacts: bool = True) -> str:
    """
    Clean AI-generated output.

    Args:
        text (str): Raw output text
        remove_ai_artifacts (bool): Remove common AI generation markers

    Returns:
        str: Sanitized text
    """
```

---

### utils/ai_detection.py

AI-generated text detection.

**Functions:**

```python
def detect_ai_content(text: str) -> dict:
    """
    Detect if text appears AI-generated.

    Args:
        text (str): Text to analyze

    Returns:
        dict: Detection results
            {
                'is_ai_generated': bool,
                'confidence': float,  # 0-1
                'indicators': list    # Detected AI patterns
            }
    """
```

---

### utils/export.py

Document export utilities.

**Functions:**

```python
def export_to_format(content: str, format: str, output_path: str, **kwargs) -> str:
    """
    Export content to various formats.

    Args:
        content (str): Document content (Markdown, HTML, etc.)
        format (str): Target format ("pdf", "docx", "html", "latex")
        output_path (str): Output file path
        **kwargs: Format-specific options

    Returns:
        str: Path to exported file

    Raises:
        ValueError: If format is unsupported
        IOError: If export fails

    Example:
        >>> export_to_format(
        ...     content="# My Paper\\n\\nContent here",
        ...     format="pdf",
        ...     output_path="paper.pdf",
        ...     template="academic"
        ... )
        '/path/to/paper.pdf'
    """
```

---

### utils/logging_config.py

Logging configuration and utilities.

**Functions:**

```python
def setup_logging(log_level: str = "INFO", log_file: str = None) -> logging.Logger:
    """
    Configure application logging.

    Args:
        log_level (str): Logging level ("DEBUG", "INFO", "WARNING", "ERROR")
        log_file (str): Optional log file path

    Returns:
        logging.Logger: Configured logger instance
    """
```

---

### utils/section_restorer.py

Document section restoration and recovery.

**Functions:**

```python
def restore_sections(document: str, backup: str) -> str:
    """
    Restore document sections from backup.

    Args:
        document (str): Current document content
        backup (str): Backup document content

    Returns:
        str: Restored document
    """
```

---

## PDF Engines

Located in `utils/pdf_engines/`

### base.py

```python
class BasePDFEngine(ABC):
    """
    Abstract base class for PDF generation engines.

    Methods:
        convert(input_path: str, output_path: str) -> str
            Convert document to PDF

        is_available() -> bool
            Check if engine is available on system
    """
```

### weasyprint_engine.py

```python
class WeasyPrintEngine(BasePDFEngine):
    """
    PDF generation using WeasyPrint.

    Supports:
        - HTML/CSS to PDF
        - Modern CSS layout
        - Good typography support
    """
```

### pandoc_engine.py

```python
class PandocEngine(BasePDFEngine):
    """
    PDF generation using Pandoc.

    Supports:
        - Markdown to PDF (via LaTeX)
        - Multiple input formats
        - Citation processing
    """
```

### libreoffice_engine.py

```python
class LibreOfficeEngine(BasePDFEngine):
    """
    PDF generation using LibreOffice.

    Supports:
        - DOCX/ODT to PDF
        - Complex document layouts
    """
```

### factory.py

```python
def get_pdf_engine(engine_name: str = "auto") -> BasePDFEngine:
    """
    Get appropriate PDF engine.

    Args:
        engine_name (str): Engine name or "auto" for best available

    Returns:
        BasePDFEngine: PDF engine instance

    Example:
        >>> engine = get_pdf_engine("weasyprint")
        >>> engine.convert("paper.html", "paper.pdf")
    """
```

---

## Formatting

Located in `utils/formatting/`

### academic_formatter.py

```python
def format_academic_text(text: str, style: str = "APA") -> str:
    """
    Format text according to academic style guidelines.

    Args:
        text (str): Input text
        style (str): Academic style ("APA", "MLA", "Chicago")

    Returns:
        str: Formatted text
    """

def format_title(title: str, style: str = "APA") -> str:
    """
    Format title according to style guide.

    Args:
        title (str): Raw title
        style (str): Academic style

    Returns:
        str: Properly formatted title
    """

def format_bibliography(citations: list, style: str = "APA") -> str:
    """
    Generate formatted bibliography.

    Args:
        citations (list): List of citation dictionaries
        style (str): Citation style

    Returns:
        str: Formatted bibliography
    """
```

---

## MCP Servers

Model Context Protocol server implementations for academic database integration.

Located in `mcp_servers/`

### Structure

Each MCP server provides:
- Database connection
- Search capabilities
- Metadata retrieval
- Citation formatting

### Common Interface

```python
class MCPServer:
    """
    Base MCP server interface.

    Methods:
        search(query: str, **kwargs) -> list
            Search database

        get_document(doc_id: str) -> dict
            Retrieve document metadata

        format_citation(doc: dict, style: str) -> str
            Format citation for document
    """
```

---

## Concurrency

Located in `concurrency/`

Concurrent processing utilities for batch operations.

```python
def process_batch(items: list, processor_func: callable, max_workers: int = 4) -> list:
    """
    Process items concurrently.

    Args:
        items (list): Items to process
        processor_func (callable): Function to apply to each item
        max_workers (int): Maximum concurrent workers

    Returns:
        list: Processed results

    Example:
        >>> def process_paper(paper):
        ...     return extract_citations(paper)
        >>> results = process_batch(papers, process_paper, max_workers=8)
    """
```

---

## Error Handling

### Common Exceptions

```python
class APIError(Exception):
    """Raised when external API call fails."""
    pass

class ValidationError(Exception):
    """Raised when validation fails."""
    pass

class ExportError(Exception):
    """Raised when export operation fails."""
    pass
```

### Retry Logic

```python
from utils.retry import retry_with_backoff

@retry_with_backoff(max_retries=3, backoff_factor=2)
def call_api(endpoint: str, params: dict) -> dict:
    """
    Make API call with automatic retry on failure.

    Decorator handles:
        - Rate limiting
        - Temporary network failures
        - API overload
    """
```

---

## Rate Limiting

```python
from concurrency.concurrency_config import RateLimiter

limiter = RateLimiter(calls_per_second=10)

@limiter.limit
def search_database(query: str) -> list:
    """
    Rate-limited database search.
    """
```

---

## Configuration Examples

### Environment Variables

```bash
# API Keys
GEMINI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Rate Limiting
MAX_CONCURRENT_REQUESTS=10
RATE_LIMIT_CALLS_PER_SECOND=5

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=5

# PDF Generation
DEFAULT_PDF_ENGINE=weasyprint
PDF_TEMPLATE=academic
```

---

## Best Practices

### Error Handling

```python
from utils.retry import retry_with_backoff
import logging

logger = logging.getLogger(__name__)

@retry_with_backoff(max_retries=3)
def fetch_paper_metadata(paper_id: str) -> dict:
    try:
        metadata = api_call(paper_id)
        return metadata
    except APIError as e:
        logger.error(f"API error fetching {paper_id}: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise
```

### Resource Management

```python
from contextlib import contextmanager

@contextmanager
def pdf_engine():
    """Context manager for PDF engine resources."""
    engine = get_pdf_engine()
    try:
        yield engine
    finally:
        engine.cleanup()

# Usage
with pdf_engine() as engine:
    engine.convert("input.md", "output.pdf")
```

### Batch Processing

```python
from concurrency import process_batch

def process_papers_efficiently(papers: list) -> list:
    """Process multiple papers with rate limiting."""
    def process_one(paper):
        return {
            'citations': extract_citations(paper),
            'summary': summarize(paper),
            'keywords': extract_keywords(paper)
        }

    return process_batch(
        papers,
        process_one,
        max_workers=8  # Adjust based on API limits
    )
```

---

## Testing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for testing guidelines.

### Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/test_utils/test_citation_validation.py

# With coverage
pytest --cov=utils --cov-report=html
```

---

## Further Reading

- [README.md](../README.md) - Project overview
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development guidelines
- [Examples/](../Examples/) - Usage examples
- [ETHICS.md](../ETHICS.md) - Ethical usage guidelines

---

**Last Updated:** November 2025
**Version:** 1.0
