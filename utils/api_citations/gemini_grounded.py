#!/usr/bin/env python3
"""
ABOUTME: Gemini API client with Google Search grounding for source discovery
ABOUTME: Uses Google Search tool via REST API to find and validate real web sources with citations
"""

import os
import re
import json
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    requests = None

from .base import BaseAPIClient


class GeminiGroundedClient(BaseAPIClient):
    """
    Gemini API client with Google Search grounding.

    Uses Gemini 2.5 Pro with Google Search tool via REST API to discover real sources
    with grounded citations. Validates URLs and extracts metadata.

    Features:
    - Google Search grounding for real-time source discovery (via REST API)
    - Deep research capability with high token limits
    - URL validation (HTTP 200 checks)
    - Redirect unwrapping to final destinations
    - Domain filtering (competitors, forbidden hosts)
    - Grounding citation extraction

    Requirements:
    - requests
    - GOOGLE_API_KEY environment variable
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 120,  # Longer timeout for deep research
        max_retries: int = 3,
        forbidden_domains: Optional[List[str]] = None,
        validate_urls: bool = True
    ):
        """
        Initialize Gemini Grounded client.

        Args:
            api_key: Google AI API key (defaults to GOOGLE_API_KEY env var)
            timeout: Request timeout in seconds (120s for deep research)
            max_retries: Number of retry attempts
            forbidden_domains: List of domains to filter out
            validate_urls: Whether to validate URLs return HTTP 200
        """
        super().__init__(
            api_key=api_key or os.getenv('GOOGLE_API_KEY'),
            base_url='https://generativelanguage.googleapis.com/v1beta/models',
            timeout=timeout,
            max_retries=max_retries
        )

        if not requests:
            raise ImportError(
                "requests not installed. Run: pip install requests"
            )

        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found. Set via environment variable or constructor."
            )

        # Use Gemini 2.5 Flash for deep research (matching gtm-os-v2 pattern)
        self.model_name = 'gemini-2.5-flash'

        self.forbidden_domains = forbidden_domains or []
        self.validate_urls = validate_urls

        # Session for both API calls and URL validation
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                      'image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
        })

    def search_paper(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search for a source using Gemini with Google Search grounding via REST API.

        Args:
            query: Search query (topic, title, keywords)

        Returns:
            Paper/source metadata dict with keys:
                - title: str
                - url: str (validated, unwrapped)
                - authors: Optional[str]
                - date: Optional[str]
                - snippet: Optional[str]
            Returns None if no valid source found.
        """
        try:
            # Construct grounded search prompt
            prompt = self._build_search_prompt(query)

            # Generate with Google Search grounding via REST API
            response_data = self._generate_content_with_grounding(prompt)

            if not response_data:
                return None

            # Extract grounding citations from response
            sources = self._extract_grounding_citations(response_data)

            if not sources:
                return None

            # Validate and unwrap URLs
            valid_sources = self._validate_sources(sources)

            if not valid_sources:
                return None

            # Return first valid source
            return valid_sources[0]

        except Exception as e:
            print(f"Gemini grounded search error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _generate_content_with_grounding(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Generate content using Gemini REST API with Google Search grounding.

        Args:
            prompt: User prompt for generation

        Returns:
            API response data dict, or None if error
        """
        try:
            # Build request body (matching gtm-os-v2 pattern)
            body = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,  # Low temp for factual accuracy
                    "maxOutputTokens": 8192,  # High limit for deep research
                },
                "tools": [
                    {"googleSearch": {}},  # Enable Google Search grounding
                ]
            }

            # Make REST API call
            url = f"{self.base_url}/{self.model_name}:generateContent?key={self.api_key}"

            response = self.session.post(
                url,
                json=body,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )

            if not response.ok:
                error_text = response.text[:500]
                print(f"Gemini API error {response.status_code}: {error_text}")
                return None

            data = response.json()

            # Check for valid response
            if not data.get('candidates'):
                print(f"No candidates in response: {data}")
                return None

            return data

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _build_search_prompt(self, query: str) -> str:
        """Build search prompt for Gemini."""
        return f"""Find a credible web source about: {query}

Requirements:
- Must be from a reputable source (academic, news, official documentation)
- Must be publicly accessible (no paywalls)
- Prefer recent sources (last 5 years)
- Include author and publication date if available

Provide the source title, URL, and a brief snippet explaining relevance."""

    def _extract_grounding_citations(
        self,
        response_data: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Extract grounding citations from Gemini REST API response.

        Args:
            response_data: Gemini API response dict (from REST API)

        Returns:
            List of dicts with 'title', 'url', 'snippet' keys
        """
        sources = []

        try:
            # Check for candidates in response
            candidates = response_data.get('candidates', [])
            if not candidates:
                return sources

            candidate = candidates[0]

            # Extract grounding metadata (matching gtm-os-v2 pattern)
            grounding_metadata = candidate.get('groundingMetadata')

            if grounding_metadata:
                # Extract from grounding chunks
                grounding_chunks = grounding_metadata.get('groundingChunks', [])

                for chunk in grounding_chunks:
                    source = {}

                    # Extract web source details
                    web = chunk.get('web', {})
                    if web:
                        uri = web.get('uri')
                        title = web.get('title')

                        if uri:
                            source['url'] = uri
                        if title:
                            source['title'] = title

                        if source.get('url') and source.get('title'):
                            sources.append(source)

                # Also check webSearchQueries if available
                web_search_queries = grounding_metadata.get('webSearchQueries', [])
                if web_search_queries:
                    print(f"Web search queries used: {web_search_queries}")

            # Also extract from text content as fallback
            content = candidate.get('content', {})
            parts = content.get('parts', [])
            if parts:
                text = parts[0].get('text', '')
                if text:
                    sources.extend(self._extract_urls_from_text(text))

        except Exception as e:
            print(f"Error extracting grounding citations: {e}")
            import traceback
            traceback.print_exc()

        return sources

    def _extract_urls_from_text(self, text: str) -> List[Dict[str, str]]:
        """Extract URLs from response text as fallback."""
        sources = []
        url_pattern = re.compile(r'https?://[^\s\)]+')

        matches = url_pattern.findall(text)
        for url in matches:
            url = url.rstrip('.,;:')
            sources.append({
                'url': url,
                'title': 'Source',  # Generic title
            })

        return sources

    def _validate_sources(
        self,
        sources: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Validate and unwrap source URLs.

        Args:
            sources: List of source dicts with 'url' and 'title'

        Returns:
            List of validated source dicts with metadata
        """
        valid_sources = []

        for source in sources:
            url = source.get('url')
            if not url:
                continue

            # Filter forbidden domains
            if self._is_forbidden_domain(url):
                continue

            # Unwrap redirects
            final_url = self._unwrap_url(url)
            if not final_url:
                continue

            # Validate URL if enabled
            if self.validate_urls:
                if not self._validate_url(final_url):
                    continue

            # Build validated source metadata
            valid_source = {
                'title': source.get('title', 'Source'),
                'url': final_url,
                'snippet': source.get('snippet'),
                'authors': None,  # Not available from grounding
                'date': None,  # Not available from grounding
                'source_type': 'website',  # Industry sources are websites/reports
            }

            valid_sources.append(valid_source)

        return valid_sources

    def _is_forbidden_domain(self, url: str) -> bool:
        """Check if URL is from forbidden domain."""
        try:
            domain = urlparse(url).netloc.lower()
            return any(
                forbidden in domain
                for forbidden in self.forbidden_domains
            )
        except Exception:
            return False

    def _unwrap_url(self, url: str) -> Optional[str]:
        """
        Follow redirects to get final destination URL.

        Args:
            url: Initial URL

        Returns:
            Final URL after redirects, or None if error
        """
        try:
            response = self.session.head(
                url,
                allow_redirects=True,
                timeout=self.timeout
            )
            return response.url
        except Exception:
            # Try GET if HEAD fails
            try:
                response = self.session.get(
                    url,
                    allow_redirects=True,
                    timeout=self.timeout,
                    stream=True
                )
                response.close()
                return response.url
            except Exception:
                return None

    def _validate_url(self, url: str) -> bool:
        """
        Validate URL returns HTTP 200.

        Args:
            url: URL to validate

        Returns:
            True if URL returns 200, False otherwise
        """
        try:
            response = self.session.head(
                url,
                allow_redirects=True,
                timeout=self.timeout
            )

            # Some servers block HEAD, try GET
            if response.status_code == 405:
                response = self.session.get(
                    url,
                    allow_redirects=True,
                    timeout=self.timeout,
                    stream=True
                )
                response.close()

            return response.status_code == 200

        except Exception:
            return False

    def close(self) -> None:
        """Close HTTP session."""
        if hasattr(self, 'session'):
            self.session.close()
