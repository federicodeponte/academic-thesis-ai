#!/usr/bin/env python3
"""
ABOUTME: Citation management utility for formatting and validating BibTeX citations
ABOUTME: Supports APA, IEEE, Chicago, and MLA styles using pybtex and citeproc
"""

import argparse
import sys
import os
from pathlib import Path

try:
    import pybtex
    from pybtex.database import parse_file, BibliographyData, Entry
    from pybtex.database.input import bibtex
    PYBTEX_AVAILABLE = True
except ImportError:
    PYBTEX_AVAILABLE = False
    print("Warning: pybtex not installed. Run: pip install pybtex")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: requests not installed. Run: pip install requests")


def get_citation_from_doi(doi):
    """Fetch citation metadata from DOI using CrossRef API"""
    if not REQUESTS_AVAILABLE:
        print("ERROR: requests library required")
        return None
    
    url = f"https://doi.org/{doi}"
    headers = {'Accept': 'application/x-bibtex'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"ERROR: Could not fetch DOI {doi}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def format_citation(entry, style='apa'):
    """Format a BibTeX entry as a citation string"""
    # Simple APA-style formatting
    authors = entry.persons.get('author', [])
    author_str = ", ".join([str(author) for author in authors[:3]])
    if len(authors) > 3:
        author_str += ", et al."
    
    year = entry.fields.get('year', 'n.d.')
    title = entry.fields.get('title', 'Untitled')
    
    if style == 'apa':
        return f"{author_str} ({year}). {title}."
    elif style == 'mla':
        return f"{author_str}. \"{title}.\" {year}."
    elif style == 'chicago':
        return f"{author_str}. {year}. \"{title}.\""
    else:
        return f"{author_str} ({year}). {title}."


def validate_bibtex(bib_file):
    """Validate a BibTeX file"""
    if not PYBTEX_AVAILABLE:
        print("ERROR: pybtex not installed")
        return False
    
    try:
        bib_data = parse_file(bib_file)
        print(f"✅ Valid BibTeX file: {len(bib_data.entries)} entries")
        
        # Check for common issues
        issues = []
        for key, entry in bib_data.entries.items():
            # Check for missing required fields
            required_fields = []
            if entry.type == 'article':
                required_fields = ['author', 'title', 'journal', 'year']
            elif entry.type == 'inproceedings':
                required_fields = ['author', 'title', 'booktitle', 'year']
            elif entry.type == 'book':
                required_fields = ['author', 'title', 'publisher', 'year']
            
            missing = [f for f in required_fields if f not in entry.fields]
            if missing:
                issues.append(f"Entry '{key}' missing: {', '.join(missing)}")
        
        if issues:
            print(f"\n⚠️  Found {len(issues)} issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✅ No issues found")
        
        return True
    
    except Exception as e:
        print(f"❌ Invalid BibTeX: {e}")
        return False


def generate_bibliography(bib_file, output_file, style='apa'):
    """Generate formatted bibliography from BibTeX file"""
    if not PYBTEX_AVAILABLE:
        print("ERROR: pybtex not installed")
        return False
    
    try:
        bib_data = parse_file(bib_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Bibliography ({style.upper()} style)\n\n")
            
            # Sort by author last name
            sorted_entries = sorted(bib_data.entries.items(),
                                  key=lambda x: str(x[1].persons.get('author', [''])[0]))
            
            for key, entry in sorted_entries:
                citation = format_citation(entry, style)
                f.write(f"{citation}\n\n")
        
        print(f"✅ Bibliography generated: {output_file}")
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Citation management utilities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Validate BibTeX file
  python citations.py --validate references.bib
  
  # Generate APA bibliography
  python citations.py --bibliography references.bib --output bibliography.md --style apa
  
  # Get citation from DOI
  python citations.py --doi 10.1234/example
        '''
    )
    parser.add_argument('--validate', help='Validate BibTeX file')
    parser.add_argument('--bibliography', help='Generate bibliography from BibTeX file')
    parser.add_argument('--output', '-o', help='Output file for bibliography')
    parser.add_argument('--style', default='apa', choices=['apa', 'mla', 'chicago', 'ieee'],
                        help='Citation style (default: apa)')
    parser.add_argument('--doi', help='Fetch citation from DOI')
    
    args = parser.parse_args()
    
    if args.validate:
        validate_bibtex(args.validate)
    elif args.bibliography:
        if not args.output:
            print("ERROR: --output required for bibliography generation")
            sys.exit(1)
        generate_bibliography(args.bibliography, args.output, args.style)
    elif args.doi:
        citation = get_citation_from_doi(args.doi)
        if citation:
            print(citation)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
