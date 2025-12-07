"""
Pruebas basadas en escenarios con diferentes preguntas.
"""

import json
from pathlib import Path

import pytest

from src.utils.config import Config
from src.validators.quality_scorer import QualityScorer

# Load test questions
test_data_path = Config.DATA_DIR / "test_questions.json"
with open(test_data_path, "r", encoding="utf-8") as f:
    test_questions_data = json.load(f)

# Extract questions for parametrization
test_questions = [item["question"] for item in test_questions_data]


@pytest.mark.regression
@pytest.mark.parametrize("question", test_questions)
class TestScenarios:
    """Prueba varios escenarios de preguntas."""

    def test_question_gets_valid_response(self, api_client, question):
        """Prueba que cada pregunta obtenga una respuesta válida."""
        response = api_client.ask(question)
        assert response["status_code"] == 200, f"Error al obtener respuesta válida para: {question}"
        assert "answer" in response["data"], f"No hay respuesta para: {question}"

    def test_question_meets_quality_threshold(self, api_client, question, quality_scorer):
        """Prueba que la respuesta de cada pregunta cumpla con el umbral de calidad."""
        response = api_client.ask(question)
        overall_score = quality_scorer.calculate_overall_score(response, question)
        threshold = Config.QUALITY_THRESHOLD

        assert (
            overall_score >= threshold
        ), f"La pregunta '{question}' falló el control de calidad: {overall_score:.2f} < {threshold}"

    def test_question_response_time(self, api_client, question):
        """Prueba que cada pregunta responda en un tiempo aceptable."""
        response = api_client.ask(question)
        max_time = 20.0
        assert (
            response["response_time"] < max_time
        ), f"La pregunta '{question}' tardó demasiado: {response['response_time']:.2f}s > {max_time}s"


@pytest.mark.quality
class TestSpecificScenarios:
    """Prueba escenarios específicos importantes."""

    def test_python_unittest_question(self, api_client, quality_scorer):
        """Prueba preguntas sobre unit testing en Python."""
        question = "¿Cómo escribir tests unitarios en Python?"
        response = api_client.ask(question)

        scores = quality_scorer.get_detailed_scores(response, question)

        # Should mention pytest or unittest
        answer = response["data"]["answer"].lower()
        assert (
            "pytest" in answer or "unittest" in answer
        ), "La respuesta debería mencionar pytest o unittest"

        # Should pass quality threshold
        assert scores[
            "passes_threshold"
        ], f"El puntaje de calidad {scores['overall_score']:.2f} está por debajo del umbral"

    def test_mocking_question(self, api_client, quality_scorer):
        """Prueba preguntas sobre mocking."""
        question = "¿Qué es mocking y cuándo usarlo?"
        response = api_client.ask(question)

        answer = response["data"]["answer"].lower()

        # Should mention mock-related concepts
        mock_keywords = ["mock", "stub", "fake", "dependency"]
        mentions_mocking = any(keyword in answer for keyword in mock_keywords)
        assert mentions_mocking, "La respuesta debería mencionar conceptos de mocking"

        # Should pass quality threshold
        passes = quality_scorer.validate_quality(response, question)
        assert passes, "La pregunta sobre mocking debería pasar la validación de calidad"

    def test_tdd_question(self, api_client, quality_scorer):
        """Prueba preguntas sobre TDD."""
        question = "¿Qué es TDD y cómo implementarlo?"
        response = api_client.ask(question)

        answer = response["data"]["answer"].lower()

        # Should mention TDD concepts
        tdd_keywords = ["tdd", "test-driven", "red", "green", "refactor"]
        mentions_tdd = any(keyword in answer for keyword in tdd_keywords)
        assert mentions_tdd, "La respuesta debería mencionar conceptos de TDD"

        # Should pass quality threshold
        scores = quality_scorer.get_detailed_scores(response, question)
        assert scores[
            "passes_threshold"
        ], f"El puntaje de calidad de la pregunta TDD {scores['overall_score']:.2f} está por debajo del umbral"
