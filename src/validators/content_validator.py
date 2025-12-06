"""
Content quality validator.
Analyzes content for testing-related keywords, code examples, and structure.
"""

import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class ContentValidator:
    """Validates content quality of API responses."""

    # Testing-related keywords
    TESTING_KEYWORDS = {
        "test",
        "testing",
        "assert",
        "mock",
        "unittest",
        "pytest",
        "tdd",
        "bdd",
        "integration",
        "unit",
        "e2e",
        "end-to-end",
        "automated",
        "automation",
        "coverage",
        "fixture",
        "suite",
        "case",
        "scenario",
        "stub",
        "spy",
        "continuous integration",
        "ci/cd",
        "regression",
        "smoke",
    }

    # Common testing frameworks
    TESTING_FRAMEWORKS = {
        "pytest",
        "unittest",
        "jest",
        "mocha",
        "jasmine",
        "junit",
        "testng",
        "selenium",
        "cypress",
        "playwright",
        "robot framework",
        "cucumber",
        "rspec",
        "minitest",
        "nose",
        "doctest",
    }

    @staticmethod
    def contains_code_examples(text: str) -> bool:
        """
        Check if text contains code examples.

        Args:
            text: Text to analyze

        Returns:
            True if code examples are found
        """
        # Look for code blocks (triple backticks or indented code)
        code_block_pattern = r"```[\s\S]*?```|`[^`]+`"
        has_code_blocks = bool(re.search(code_block_pattern, text))

        # Look for common code patterns
        code_patterns = [
            r"def\s+\w+\s*\(",  # Python function
            r"class\s+\w+",  # Class definition
            r"import\s+\w+",  # Import statement
            r"from\s+\w+\s+import",  # From import
            r"self\.\w+",  # self references
            r"assert\w*\s*\(",  # Assert statements
            r"@\w+",  # Decorators
        ]

        has_code_patterns = any(re.search(pattern, text) for pattern in code_patterns)

        return has_code_blocks or has_code_patterns

    @staticmethod
    def count_testing_keywords(text: str) -> int:
        """
        Count occurrences of testing-related keywords.

        Args:
            text: Text to analyze

        Returns:
            Number of testing keywords found
        """
        text_lower = text.lower()
        count = sum(1 for keyword in ContentValidator.TESTING_KEYWORDS if keyword in text_lower)
        return count

    @staticmethod
    def mentions_frameworks(text: str) -> List[str]:
        """
        Find testing frameworks mentioned in text.

        Args:
            text: Text to analyze

        Returns:
            List of frameworks mentioned
        """
        text_lower = text.lower()
        mentioned = [fw for fw in ContentValidator.TESTING_FRAMEWORKS if fw in text_lower]
        return mentioned

    @staticmethod
    def has_structured_content(text: str) -> bool:
        """
        Check if content has structured formatting (lists, numbering).

        Args:
            text: Text to analyze

        Returns:
            True if structured content is found
        """
        # Look for numbered lists (1), 2), etc.)
        numbered_pattern = r"\d+\)"
        has_numbered = bool(re.search(numbered_pattern, text))

        # Look for bullet points or dashes
        bullet_pattern = r"^\s*[-*•]\s+"
        has_bullets = bool(re.search(bullet_pattern, text, re.MULTILINE))

        # Look for newlines indicating list structure
        has_multiple_paragraphs = text.count("\n\n") >= 2

        return has_numbered or has_bullets or has_multiple_paragraphs

    @staticmethod
    def calculate_content_score(text: str) -> float:
        """
        Calculate content quality score (0.0 - 1.0).

        Args:
            text: Text to analyze

        Returns:
            Content quality score
        """
        score = 0.0
        max_score = 5.0

        # 1. Has code examples (1.0 point)
        if ContentValidator.contains_code_examples(text):
            score += 1.0

        # 2. Testing keywords (up to 1.0 point)
        keyword_count = ContentValidator.count_testing_keywords(text)
        score += min(keyword_count / 5.0, 1.0)  # Max 1.0 for 5+ keywords

        # 3. Mentions frameworks (1.0 point)
        frameworks = ContentValidator.mentions_frameworks(text)
        if frameworks:
            score += 1.0

        # 4. Has structured content (1.0 point)
        if ContentValidator.has_structured_content(text):
            score += 1.0

        # 5. Minimum length check (1.0 point)
        if len(text) >= 200:
            score += 1.0

        # Normalize to 0.0 - 1.0
        normalized_score = score / max_score

        logger.debug(
            f"Content score: {normalized_score:.2f} (keywords: {keyword_count}, "
            f"frameworks: {len(frameworks)}, code: {ContentValidator.contains_code_examples(text)})"
        )

        return normalized_score

    @staticmethod
    def get_content_details(text: str) -> Dict:
        """
        Get detailed content analysis.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with content analysis details
        """
        return {
            "has_code_examples": ContentValidator.contains_code_examples(text),
            "keyword_count": ContentValidator.count_testing_keywords(text),
            "frameworks_mentioned": ContentValidator.mentions_frameworks(text),
            "has_structure": ContentValidator.has_structured_content(text),
            "length": len(text),
            "content_score": ContentValidator.calculate_content_score(text),
        }
