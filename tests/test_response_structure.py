"""
Pruebas de validación de estructura de respuesta.
"""

import pytest

from src.validators.response_validator import ResponseValidator


@pytest.mark.regression
class TestResponseStructure:
    """Prueba la estructura de la respuesta y la validación del esquema."""

    def test_response_has_data_field(self, sample_response):
        """Prueba que la respuesta contenga el campo 'data'."""
        assert "data" in sample_response, "La respuesta no tiene el campo 'data'"

    def test_response_has_answer_field(self, sample_response):
        """Prueba que los datos de respuesta contengan el campo 'answer'."""
        assert (
            "answer" in sample_response["data"]
        ), "Los datos de respuesta no tienen el campo 'answer'"

    def test_answer_is_string(self, sample_response):
        """Prueba que el campo 'answer' sea una cadena de texto."""
        answer = sample_response["data"]["answer"]
        assert isinstance(
            answer, str
        ), f"La respuesta debe ser texto, se obtuvo {type(answer).__name__}"

    def test_answer_not_empty(self, sample_response):
        """Prueba que la respuesta no esté vacía."""
        answer = sample_response["data"]["answer"]
        assert len(answer.strip()) > 0, "La respuesta está vacía"

    def test_response_has_metadata(self, sample_response):
        """Prueba que la respuesta incluya campos de metadatos."""
        assert "status_code" in sample_response, "La respuesta no tiene 'status_code'"
        assert "response_time" in sample_response, "La respuesta no tiene 'response_time'"
        assert "question" in sample_response, "La respuesta no tiene 'question'"

    def test_response_validation_passes(self, sample_response):
        """Prueba que la respuesta pase la validación completa."""
        is_valid, errors = ResponseValidator.validate_response(sample_response)
        assert is_valid, f"Falló la validación de respuesta: {', '.join(errors)}"

    def test_answer_minimum_length(self, sample_response):
        """Prueba que la respuesta cumpla con la longitud mínima."""
        answer = sample_response["data"]["answer"]
        min_length = 100
        assert (
            len(answer) >= min_length
        ), f"La longitud de la respuesta {len(answer)} está por debajo del mínimo {min_length}"
