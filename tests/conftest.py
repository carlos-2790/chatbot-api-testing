"""
Configuración de Pytest y fixtures compartidos.
"""

import logging

import pytest

from src.api.chatbot_client import ChatbotClient
from src.validators.quality_scorer import QualityScorer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@pytest.fixture(scope="session")
def api_client():
    """Provee una instancia de ChatbotClient para toda la sesión de pruebas."""
    client = ChatbotClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def quality_scorer():
    """Provee una instancia de QualityScorer para toda la sesión de pruebas."""
    return QualityScorer()


@pytest.fixture
def sample_question():
    """Provee una pregunta de ejemplo para las pruebas."""
    return "¿Cómo escribir tests unitarios en Python?"


@pytest.fixture
def sample_response(api_client, sample_question):
    """Provee una respuesta de API de ejemplo para las pruebas."""
    return api_client.ask(sample_question)
