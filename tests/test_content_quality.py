"""
Content quality validation tests.
"""

import pytest

from src.utils.config import Config
from src.validators.content_validator import ContentValidator
from src.validators.quality_scorer import QualityScorer
from src.validators.response_validator import ResponseValidator


@pytest.mark.quality
class TestContentQuality:
    """Test content quality and scoring."""

    def test_response_contains_code_examples(self, sample_response):
        """Test that response includes code examples."""
        answer = ResponseValidator.get_answer_text(sample_response)
        has_code = ContentValidator.contains_code_examples(answer)
        assert has_code, "Response should contain code examples"

    def test_response_mentions_testing_keywords(self, sample_response):
        """Test that response mentions testing-related keywords."""
        answer = ResponseValidator.get_answer_text(sample_response)
        keyword_count = ContentValidator.count_testing_keywords(answer)
        assert (
            keyword_count >= 3
        ), f"Response should mention at least 3 testing keywords, found {keyword_count}"

    def test_response_mentions_frameworks(self, sample_response):
        """Test that response mentions testing frameworks."""
        answer = ResponseValidator.get_answer_text(sample_response)
        frameworks = ContentValidator.mentions_frameworks(answer)
        assert len(frameworks) > 0, "Response should mention at least one testing framework"

    def test_response_has_structure(self, sample_response):
        """Test that response has structured content."""
        answer = ResponseValidator.get_answer_text(sample_response)
        has_structure = ContentValidator.has_structured_content(answer)
        assert has_structure, "Response should have structured content (lists, numbering)"

    def test_content_score_acceptable(self, sample_response):
        """Test that content score is acceptable."""
        answer = ResponseValidator.get_answer_text(sample_response)
        content_score = ContentValidator.calculate_content_score(answer)
        min_score = 0.6
        assert (
            content_score >= min_score
        ), f"Content score {content_score:.2f} is below minimum {min_score}"

    def test_overall_quality_score_meets_threshold(
        self, sample_response, sample_question, quality_scorer
    ):
        """Test that overall quality score meets the configured threshold."""
        overall_score = quality_scorer.calculate_overall_score(sample_response, sample_question)
        threshold = Config.QUALITY_THRESHOLD
        assert (
            overall_score >= threshold
        ), f"Quality score {overall_score:.2f} is below threshold {threshold}"

    def test_quality_validation_passes(self, sample_response, sample_question, quality_scorer):
        """Test that quality validation passes."""
        passes = quality_scorer.validate_quality(sample_response, sample_question)
        assert passes, "Quality validation should pass"

    def test_detailed_scores_breakdown(self, sample_response, sample_question, quality_scorer):
        """Test detailed score breakdown."""
        scores = quality_scorer.get_detailed_scores(sample_response, sample_question)

        # Verify all score components are present
        assert "overall_score" in scores
        assert "structural_score" in scores
        assert "content_score" in scores
        assert "semantic_score" in scores
        assert "passes_threshold" in scores

        # Verify scores are in valid range
        for score_key in ["overall_score", "structural_score", "content_score", "semantic_score"]:
            score_value = scores[score_key]
            assert (
                0.0 <= score_value <= 1.0
            ), f"{score_key} {score_value:.2f} is out of range [0.0, 1.0]"

        # Verify threshold is met
        assert scores[
            "passes_threshold"
        ], f"Overall score {scores['overall_score']:.2f} should pass threshold {scores['threshold']}"
