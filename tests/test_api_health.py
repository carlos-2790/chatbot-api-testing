"""
Pruebas de salud y disponibilidad de la API.
"""

import pytest

from src.api.chatbot_client import ChatbotClient


@pytest.mark.smoke
class TestAPIHealth:
    """Prueba la disponibilidad de la API y funcionalidad básica."""

    def test_api_is_reachable(self, api_client):
        """Prueba que el endpoint de la API es accesible."""
        assert api_client.health_check(), "Falló el chequeo de salud de la API"

    def test_api_returns_200(self, api_client):
        """Prueba que la API retorna código de estado 200."""
        response = api_client.ask("test")
        assert (
            response["status_code"] == 200
        ), f"Se esperaba 200, se obtuvo {response['status_code']}"

    def test_response_time_acceptable(self, api_client):
        """Prueba que la API responde en un tiempo aceptable (<20 segundos)."""
        response = api_client.ask("test")
        assert (
            response["response_time"] < 20.0
        ), f"El tiempo de respuesta {response['response_time']:.2f}s excede el umbral de 20s"

    def test_api_handles_simple_query(self, api_client):
        """Prueba que la API puede manejar una consulta simple."""
        response = api_client.ask("What is testing?")
        assert "data" in response, "La respuesta no tiene el campo 'data'"
        assert "answer" in response["data"], "Los datos de respuesta no tienen el campo 'answer'"
        assert len(response["data"]["answer"]) > 0, "La respuesta está vacía"
