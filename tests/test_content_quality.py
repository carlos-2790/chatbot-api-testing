"""
Pruebas de validación de calidad de contenido.
"""

import pytest

from src.utils.config import Config
from src.validators.content_validator import ContentValidator
from src.validators.quality_scorer import QualityScorer
from src.validators.response_validator import ResponseValidator


@pytest.mark.quality
class TestContentQuality:
    """Prueba la calidad del contenido y el puntaje."""

    def test_response_contains_code_examples(self, sample_response):
        """Prueba que la respuesta incluya ejemplos de código."""
        answer = ResponseValidator.get_answer_text(sample_response)
        has_code = ContentValidator.contains_code_examples(answer)
        assert has_code, "La respuesta debería contener ejemplos de código"

    def test_response_mentions_testing_keywords(self, sample_response):
        """Prueba que la respuesta mencione palabras clave relacionadas con testing."""
        answer = ResponseValidator.get_answer_text(sample_response)
        keyword_count = ContentValidator.count_testing_keywords(answer)
        assert (
            keyword_count >= 3
        ), f"La respuesta debería mencionar al menos 3 palabras clave de testing, se encontraron {keyword_count}"

    def test_response_mentions_frameworks(self, sample_response):
        """Prueba que la respuesta mencione frameworks de testing."""
        answer = ResponseValidator.get_answer_text(sample_response)
        frameworks = ContentValidator.mentions_frameworks(answer)
        assert (
            len(frameworks) > 0
        ), "La respuesta debería mencionar al menos un framework de testing"

    def test_response_has_structure(self, sample_response):
        """Prueba que la respuesta tenga contenido estructurado."""
        answer = ResponseValidator.get_answer_text(sample_response)
        has_structure = ContentValidator.has_structured_content(answer)
        assert (
            has_structure
        ), "La respuesta debería tener contenido estructurado (listas, numeración)"

    def test_content_score_acceptable(self, sample_response):
        """Prueba que el puntaje de contenido sea aceptable."""
        answer = ResponseValidator.get_answer_text(sample_response)
        content_score = ContentValidator.calculate_content_score(answer)
        min_score = 0.6
        assert (
            content_score >= min_score
        ), f"El puntaje de contenido {content_score:.2f} está por debajo del mínimo {min_score}"

    def test_overall_quality_score_meets_threshold(
        self, sample_response, sample_question, quality_scorer
    ):
        """Prueba que el puntaje de calidad general cumpla con el umbral configurado."""
        overall_score = quality_scorer.calculate_overall_score(sample_response, sample_question)
        threshold = Config.QUALITY_THRESHOLD
        assert (
            overall_score >= threshold
        ), f"El puntaje de calidad {overall_score:.2f} está por debajo del umbral {threshold}"

    def test_quality_validation_passes(self, sample_response, sample_question, quality_scorer):
        """Prueba que la validación de calidad pase."""
        passes = quality_scorer.validate_quality(sample_response, sample_question)
        assert passes, "La validación de calidad debería pasar"

    def test_detailed_scores_breakdown(self, sample_response, sample_question, quality_scorer):
        """Prueba el desglose detallado de puntajes."""
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
            ), f"{score_key} {score_value:.2f} está fuera del rango [0.0, 1.0]"

        # Verify threshold is met
        assert scores[
            "passes_threshold"
        ], f"El puntaje general {scores['overall_score']:.2f} debería pasar el umbral {scores['threshold']}"
