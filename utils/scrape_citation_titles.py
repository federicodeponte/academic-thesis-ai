#!/usr/bin/env python3
"""
ABOUTME: Web scraper for extracting real page titles from citation URLs
ABOUTME: Fixes Gemini Grounded citations with domain-name titles (bcg.com, mckinsey.com, etc.)

This module provides utilities to scrape real page titles from web URLs
and update citation databases with accurate, descriptive titles.

Design Principles:
- Defensive: Handles network errors, timeouts, malformed HTML gracefully
- Efficient: Uses connection pooling, respects rate limits
- Accurate: Extracts <title>, <meta> tags, fallback to <h1>
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import time
import re


class TitleScraper:
    """
    Scrapes page titles from URLs with intelligent fallbacks.
    """

    def __init__(
        self,
        timeout: int = 10,
        user_agent: str = "Academic-Thesis-AI/1.0 (Citation Metadata Scraper)",
        rate_limit_delay: float = 1.0,
        verbose: bool = False
    ):
        """
        Initialize scraper.

        Args:
            timeout: HTTP request timeout in seconds
            user_agent: User agent string for requests
            rate_limit_delay: Delay between requests in seconds
            verbose: Print detailed information
        """
        self.timeout = timeout
        self.user_agent = user_agent
        self.rate_limit_delay = rate_limit_delay
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})

    def scrape_title(self, url: str) -> Optional[str]:
        """
        Scrape page title from URL.

        Tries multiple strategies:
        1. <title> tag
        2. <meta property="og:title"> (Open Graph)
        3. <meta name="twitter:title"> (Twitter Card)
        4. <h1> tag (first one)
        5. URL path (last resort)

        Args:
            url: URL to scrape

        Returns:
            Page title or None if scraping failed
        """
        if self.verbose:
            print(f"   🌐 Scraping: {url[:80]}...")

        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Strategy 1: <title> tag
            title_tag = soup.find('title')
            if title_tag and title_tag.string:
                title = title_tag.string.strip()
                if self._is_valid_title(title):
                    if self.verbose:
                        print(f"      ✅ Title: {title[:60]}...")
                    return self._clean_title(title)

            # Strategy 2: Open Graph title
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                title = og_title['content'].strip()
                if self._is_valid_title(title):
                    if self.verbose:
                        print(f"      ✅ OG Title: {title[:60]}...")
                    return self._clean_title(title)

            # Strategy 3: Twitter Card title
            twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
            if twitter_title and twitter_title.get('content'):
                title = twitter_title['content'].strip()
                if self._is_valid_title(title):
                    if self.verbose:
                        print(f"      ✅ Twitter Title: {title[:60]}...")
                    return self._clean_title(title)

            # Strategy 4: First <h1> tag
            h1_tag = soup.find('h1')
            if h1_tag:
                title = h1_tag.get_text().strip()
                if self._is_valid_title(title):
                    if self.verbose:
                        print(f"      ✅ H1 Title: {title[:60]}...")
                    return self._clean_title(title)

            # Strategy 5: URL path (last resort)
            parsed = urlparse(url)
            path_title = parsed.path.rstrip('/').split('/')[-1]
            if path_title and len(path_title) > 3:
                title = path_title.replace('-', ' ').replace('_', ' ').title()
                if self.verbose:
                    print(f"      ⚠️  Fallback (URL): {title[:60]}...")
                return self._clean_title(title)

            if self.verbose:
                print(f"      ❌ No title found")

            return None

        except requests.exceptions.Timeout:
            if self.verbose:
                print(f"      ❌ Timeout")
            return None
        except requests.exceptions.RequestException as e:
            if self.verbose:
                print(f"      ❌ Request error: {str(e)[:50]}")
            return None
        except Exception as e:
            if self.verbose:
                print(f"      ❌ Unexpected error: {str(e)[:50]}")
            return None

    def _is_valid_title(self, title: str) -> bool:
        """
        Check if title is valid (not empty, not too short, not just a domain).

        Args:
            title: Title to validate

        Returns:
            True if valid, False otherwise
        """
        if not title or len(title) < 5:
            return False

        # Reject if it's just a domain name
        if re.match(r'^[\w\-]+\.(com|org|edu|gov|net|io|ai)$', title.lower()):
            return False

        # Reject common generic titles
        generic = {'home', 'index', 'main', 'page', 'untitled', 'document', 'website'}
        if title.lower() in generic:
            return False

        return True

    def _clean_title(self, title: str) -> str:
        """
        Clean and normalize title.

        Args:
            title: Raw title

        Returns:
            Cleaned title
        """
        # Remove common suffixes
        suffixes = [
            ' | McKinsey',
            ' - McKinsey',
            ' | BCG',
            ' - BCG',
            ' | OECD',
            ' - OECD',
            ' | World Bank',
            ' - World Bank',
            ' - YouTube',
            ' | Gartner',
            ' - Gartner',
        ]

        for suffix in suffixes:
            if title.endswith(suffix):
                title = title[:-len(suffix)].strip()

        # Collapse whitespace
        title = re.sub(r'\s+', ' ', title)

        # Limit length
        if len(title) > 200:
            title = title[:197] + '...'

        return title

    def scrape_citations(
        self,
        citations: List[Dict],
        filter_condition: Optional[callable] = None
    ) -> Tuple[int, int]:
        """
        Scrape titles for multiple citations.

        Args:
            citations: List of citation dictionaries
            filter_condition: Optional function to filter which citations to scrape
                             (default: only Gemini Grounded with bad titles)

        Returns:
            Tuple of (successful_count, failed_count)
        """
        if filter_condition is None:
            # Default: Gemini Grounded with domain-name titles
            def default_filter(c):
                if c.get('api_source') != 'Gemini Grounded':
                    return False
                title = c.get('title', '')
                # Bad title indicators
                return (
                    title.endswith('.com') or
                    title.endswith('.org') or
                    title.endswith('.edu') or
                    title.endswith('.gov') or
                    title.endswith('.net') or
                    title.endswith('.io') or
                    title.endswith('.ai') or
                    len(title) < 10 or
                    title.lower() in ['source', 'website', 'page', 'article']
                )
            filter_condition = default_filter

        # Filter citations
        to_scrape = [c for c in citations if filter_condition(c)]

        if not to_scrape:
            if self.verbose:
                print("✅ No citations need title scraping")
            return 0, 0

        print(f"\n🌐 Scraping titles for {len(to_scrape)} citations...")

        success_count = 0
        fail_count = 0

        for i, citation in enumerate(to_scrape, 1):
            url = citation.get('url')
            if not url:
                fail_count += 1
                continue

            if self.verbose:
                print(f"\n[{i}/{len(to_scrape)}] {citation['id']}")
                print(f"   Old title: '{citation.get('title', 'N/A')}'")

            # Scrape title
            new_title = self.scrape_title(url)

            if new_title:
                citation['title'] = new_title
                success_count += 1
                if self.verbose:
                    print(f"   ✅ New title: '{new_title}'")
            else:
                fail_count += 1
                if self.verbose:
                    print(f"   ❌ Failed to scrape title")

            # Rate limiting
            if i < len(to_scrape):
                time.sleep(self.rate_limit_delay)

        return success_count, fail_count


def scrape_citation_database_titles(
    database_path: str,
    output_path: Optional[str] = None,
    filter_condition: Optional[callable] = None,
    verbose: bool = False
) -> Dict:
    """
    Scrape titles for citations in a citation database JSON file.

    Args:
        database_path: Path to citation_database.json
        output_path: Path to save updated database (None = overwrite original)
        filter_condition: Optional function to filter which citations to scrape
        verbose: Print detailed information

    Returns:
        Statistics dictionary
    """
    import json
    from pathlib import Path

    db_path = Path(database_path)

    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {database_path}")

    # Load database
    with open(db_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    citations = data.get('citations', [])

    # Scrape titles
    scraper = TitleScraper(verbose=verbose)
    success_count, fail_count = scraper.scrape_citations(citations, filter_condition)

    # Update database
    data['citations'] = citations
    if 'metadata' in data:
        data['metadata']['title_scraping_applied'] = True
        data['metadata']['titles_updated'] = success_count

    # Save
    if output_path is None:
        output_path = db_path

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    stats = {
        'total_citations': len(citations),
        'scraped_count': success_count + fail_count,
        'successful': success_count,
        'failed': fail_count
    }

    if verbose:
        print(f"\n💾 Saved updated database to: {output_path}")

    return stats


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Scrape titles for Gemini Grounded citations')
    parser.add_argument('database', help='Path to citation_database.json')
    parser.add_argument('-o', '--output', help='Output path (default: overwrite original)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--all', action='store_true', help='Scrape all citations (not just Gemini)')

    args = parser.parse_args()

    filter_fn = None if args.all else None  # Use default filter

    stats = scrape_citation_database_titles(
        args.database,
        output_path=args.output,
        filter_condition=filter_fn,
        verbose=args.verbose
    )

    print(f"\n📊 Summary:")
    print(f"   Total citations: {stats['total_citations']}")
    print(f"   Scraped: {stats['scraped_count']}")
    print(f"   Successful: {stats['successful']}")
    print(f"   Failed: {stats['failed']}")
