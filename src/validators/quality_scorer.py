"""
Quality scoring system using multi-dimensional validation.
Combines structural, content, and semantic validation.
"""

import logging
from typing import Dict, Optional

from sentence_transformers import SentenceTransformer, util

from src.utils.config import Config
from src.validators.content_validator import ContentValidator
from src.validators.response_validator import ResponseValidator

logger = logging.getLogger(__name__)


class QualityScorer:
    """
    Multi-dimensional quality scorer for API responses.

    Scoring breakdown:
    - Structural validation: 20%
    - Content quality: 40%
    - Semantic relevance: 40%
    """

    # Weights for each dimension
    STRUCTURAL_WEIGHT = 0.20
    CONTENT_WEIGHT = 0.40
    SEMANTIC_WEIGHT = 0.40

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the quality scorer.

        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name or Config.SENTENCE_TRANSFORMER_MODEL
        self._model = None
        logger.info(f"QualityScorer initialized with model: {self.model_name}")

    @property
    def model(self) -> SentenceTransformer:
        """Lazy load the sentence transformer model."""
        if self._model is None:
            logger.info(f"Loading sentence transformer model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def calculate_structural_score(self, response: Dict) -> float:
        """
        Calculate structural validation score.

        Args:
            response: API response dictionary

        Returns:
            Structural score (0.0 - 1.0)
        """
        is_valid, errors = ResponseValidator.validate_response(response)

        if is_valid:
            return 1.0

        # Partial credit based on number of errors
        # Fewer errors = higher score
        max_possible_errors = 5
        error_count = len(errors)
        score = max(0.0, 1.0 - (error_count / max_possible_errors))

        logger.debug(f"Structural score: {score:.2f} ({error_count} errors)")
        return score

    def calculate_content_score(self, response: Dict) -> float:
        """
        Calculate content quality score.

        Args:
            response: API response dictionary

        Returns:
            Content score (0.0 - 1.0)
        """
        answer_text = ResponseValidator.get_answer_text(response)

        if not answer_text:
            return 0.0

        score = ContentValidator.calculate_content_score(answer_text)
        logger.debug(f"Content score: {score:.2f}")
        return score

    def calculate_semantic_score(self, response: Dict, question: str) -> float:
        """
        Calculate semantic relevance score using sentence transformers.

        Args:
            response: API response dictionary
            question: Original question asked

        Returns:
            Semantic score (0.0 - 1.0)
        """
        answer_text = ResponseValidator.get_answer_text(response)

        if not answer_text or not question:
            return 0.0

        try:
            # Encode question and answer
            question_embedding = self.model.encode(question, convert_to_tensor=True)
            answer_embedding = self.model.encode(answer_text, convert_to_tensor=True)

            # Calculate cosine similarity
            similarity = util.cos_sim(question_embedding, answer_embedding).item()

            # Normalize to 0.0 - 1.0 (cosine similarity is already -1 to 1, but typically 0 to 1)
            score = max(0.0, min(1.0, similarity))

            logger.debug(f"Semantic score: {score:.2f} (similarity: {similarity:.2f})")
            return score

        except Exception as e:
            logger.error(f"Error calculating semantic score: {str(e)}")
            return 0.0

    def calculate_overall_score(self, response: Dict, question: str) -> float:
        """
        Calculate overall quality score combining all dimensions.

        Args:
            response: API response dictionary
            question: Original question asked

        Returns:
            Overall quality score (0.0 - 1.0)
        """
        structural_score = self.calculate_structural_score(response)
        content_score = self.calculate_content_score(response)
        semantic_score = self.calculate_semantic_score(response, question)

        # Weighted average
        overall_score = (
            structural_score * self.STRUCTURAL_WEIGHT
            + content_score * self.CONTENT_WEIGHT
            + semantic_score * self.SEMANTIC_WEIGHT
        )

        logger.info(
            f"Quality scores - Structural: {structural_score:.2f}, "
            f"Content: {content_score:.2f}, Semantic: {semantic_score:.2f}, "
            f"Overall: {overall_score:.2f}"
        )

        return overall_score

    def get_detailed_scores(self, response: Dict, question: str) -> Dict:
        """
        Get detailed breakdown of all scores.

        Args:
            response: API response dictionary
            question: Original question asked

        Returns:
            Dictionary with detailed score breakdown
        """
        structural_score = self.calculate_structural_score(response)
        content_score = self.calculate_content_score(response)
        semantic_score = self.calculate_semantic_score(response, question)
        overall_score = self.calculate_overall_score(response, question)

        # Get content details
        answer_text = ResponseValidator.get_answer_text(response)
        content_details = ContentValidator.get_content_details(answer_text)

        return {
            "overall_score": overall_score,
            "structural_score": structural_score,
            "content_score": content_score,
            "semantic_score": semantic_score,
            "passes_threshold": overall_score >= Config.QUALITY_THRESHOLD,
            "threshold": Config.QUALITY_THRESHOLD,
            "content_details": content_details,
            "weights": {
                "structural": self.STRUCTURAL_WEIGHT,
                "content": self.CONTENT_WEIGHT,
                "semantic": self.SEMANTIC_WEIGHT,
            },
        }

    def validate_quality(self, response: Dict, question: str) -> bool:
        """
        Validate if response meets quality threshold.

        Args:
            response: API response dictionary
            question: Original question asked

        Returns:
            True if quality score >= threshold
        """
        score = self.calculate_overall_score(response, question)
        passes = score >= Config.QUALITY_THRESHOLD

        if not passes:
            logger.warning(f"Quality validation failed: {score:.2f} < {Config.QUALITY_THRESHOLD}")

        return passes
