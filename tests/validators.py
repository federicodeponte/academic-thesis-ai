#!/usr/bin/env python3
"""
ABOUTME: Section-based validation system for academic papers
ABOUTME: Validates each paper section independently using AI agents (Skeptic, Verifier, Referee)
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Dict, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from config import get_config
from tests.test_utils import run_agent, count_words


@dataclass
class Section:
    """
    Represents a paper section for independent validation.

    Attributes:
        name: Section name (e.g., "Introduction", "Literature Review")
        content: Full text content of the section
        word_count: Number of words in the section
    """
    name: str
    content: str
    word_count: int

    @classmethod
    def from_text(cls, name: str, content: str) -> 'Section':
        """
        Create a Section from name and text content.

        Args:
            name: Section name
            content: Section text

        Returns:
            Section: New Section instance with computed word count
        """
        return cls(
            name=name,
            content=content,
            word_count=count_words(content)
        )


ValidatorType = Literal['skeptic', 'verifier', 'referee']


class SectionValidator:
    """
    Validates each section of a paper independently.

    Follows Single Responsibility Principle - handles only section-based validation.
    Extensible design allows adding new validator types easily.
    """

    def __init__(
        self,
        model: genai.GenerativeModel,
        output_dir: Path,
        use_pro_for_validation: bool = False
    ):
        """
        Initialize validator.

        Args:
            model: Configured Gemini model for validation
            output_dir: Directory to save validation outputs
            use_pro_for_validation: Whether to use Pro model for validation tasks
        """
        self.model = model
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.use_pro_for_validation = use_pro_for_validation

        # Map validator types to prompt paths
        self.validator_prompts: Dict[ValidatorType, str] = {
            'skeptic': 'prompts/04_validate/skeptic.md',
            'verifier': 'prompts/04_validate/verifier.md',
            'referee': 'prompts/04_validate/referee.md',
        }

    def validate_section(
        self,
        section: Section,
        validator: ValidatorType = 'skeptic',
        verbose: bool = True
    ) -> str:
        """
        Validate a single section using specified validator agent.

        Args:
            section: Section to validate
            validator: Type of validator to use ('skeptic', 'verifier', 'referee')
            verbose: Whether to print progress

        Returns:
            str: Validation report for the section

        Raises:
            ValueError: If validator type is invalid
        """
        if validator not in self.validator_prompts:
            raise ValueError(f"Invalid validator: {validator}. Must be one of: {list(self.validator_prompts.keys())}")

        prompt_path = self.validator_prompts[validator]

        # Create safe filename from section name
        safe_section_name = section.name.lower().replace(' ', '_').replace('/', '_')
        save_file = self.output_dir / f"{validator}_{safe_section_name}.md"

        # Create user input for validator
        user_input = (
            f"Review this {section.name} section ({section.word_count} words):\n\n"
            f"{section.content}"
        )

        # Run validator agent
        review = run_agent(
            model=self.model,
            name=f"{validator.title()} - {section.name}",
            prompt_path=prompt_path,
            user_input=user_input,
            save_to=save_file,
            verbose=verbose
        )

        return review

    def validate_all_sections(
        self,
        sections: List[Section],
        validator: ValidatorType = 'skeptic',
        verbose: bool = True
    ) -> List[str]:
        """
        Validate all sections and return list of reviews.

        Args:
            sections: List of sections to validate
            validator: Type of validator to use
            verbose: Whether to print progress

        Returns:
            List[str]: List of validation reports, one per section
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"Validating {len(sections)} sections with {validator.title()} agent")
            print(f"{'='*70}")

        reviews = []
        for i, section in enumerate(sections, 1):
            if verbose:
                print(f"\nSection {i}/{len(sections)}: {section.name}")

            review = self.validate_section(section, validator, verbose=False)
            reviews.append(review)

            if verbose:
                print(f"  ✅ {section.name} validated ({len(review):,} chars)")

        return reviews

    def create_consolidated_report(
        self,
        sections: List[Section],
        reviews: List[str],
        validator: ValidatorType = 'skeptic',
        save_to: Optional[Path] = None
    ) -> str:
        """
        Create a consolidated validation report from individual section reviews.

        Args:
            sections: List of sections that were validated
            reviews: List of validation reports (same order as sections)
            validator: Type of validator used
            save_to: Optional path to save consolidated report

        Returns:
            str: Consolidated report text

        Raises:
            ValueError: If sections and reviews lists don't match in length
        """
        if len(sections) != len(reviews):
            raise ValueError(
                f"Mismatch: {len(sections)} sections but {len(reviews)} reviews"
            )

        # Build consolidated report
        report_parts = [
            f"# Consolidated {validator.title()} Review",
            f"\n**Sections Reviewed:** {len(sections)}",
            f"**Total Words:** {sum(s.word_count for s in sections):,}",
            "\n---\n"
        ]

        for section, review in zip(sections, reviews):
            report_parts.extend([
                f"\n## {section.name}",
                f"\n**Word Count:** {section.word_count:,}",
                f"\n{review}",
                "\n---\n"
            ])

        consolidated = "\n".join(report_parts)

        # Save if path provided
        if save_to:
            save_path = Path(save_to)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(consolidated)
            print(f"\n✅ Consolidated report saved to: {save_path}")

        return consolidated


def validate_paper_sections(
    model: genai.GenerativeModel,
    sections: List[Section],
    output_dir: Path,
    validators: List[ValidatorType] = ['skeptic'],
    create_consolidated: bool = True,
    verbose: bool = True
) -> Dict[ValidatorType, List[str]]:
    """
    High-level function to validate paper sections with multiple validators.

    Args:
        model: Configured Gemini model
        sections: List of paper sections
        output_dir: Directory for outputs
        validators: List of validator types to run
        create_consolidated: Whether to create consolidated reports
        verbose: Whether to print progress

    Returns:
        Dict mapping validator type to list of reviews
    """
    config = get_config()
    validator = SectionValidator(
        model=model,
        output_dir=output_dir,
        use_pro_for_validation=config.validation.use_pro_model
    )

    all_reviews: Dict[ValidatorType, List[str]] = {}

    for val_type in validators:
        if verbose:
            print(f"\n{'='*70}")
            print(f"Running {val_type.title()} Validation")
            print(f"{'='*70}")

        reviews = validator.validate_all_sections(sections, val_type, verbose)
        all_reviews[val_type] = reviews

        if create_consolidated:
            consolidated_path = output_dir / f"{val_type}_complete_review.md"
            validator.create_consolidated_report(
                sections, reviews, val_type, consolidated_path
            )

    return all_reviews


if __name__ == '__main__':
    # Test validation system
    from tests.test_utils import setup_model

    print("Testing Section Validation System")
    print("="*70)

    # Create sample sections
    sample_sections = [
        Section.from_text(
            "Introduction",
            "This is a sample introduction section with some academic content. "
            "It discusses the background and motivation for the research."
        ),
        Section.from_text(
            "Methodology",
            "This methodology section describes the research approach and methods used. "
            "It includes details about data collection and analysis techniques."
        )
    ]

    print(f"\nCreated {len(sample_sections)} sample sections")
    for s in sample_sections:
        print(f"  - {s.name}: {s.word_count} words")

    # Setup model and validator
    try:
        model = setup_model()
        output_dir = Path('tests/outputs/validation_test')

        validator = SectionValidator(model, output_dir)
        print(f"\n✅ Validator initialized")
        print(f"   Output directory: {output_dir}")

        print("\n✅ Validation system ready")
        print("   Run with real sections to test end-to-end")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
