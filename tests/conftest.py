"""
Pytest configuration and shared fixtures.
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
    """Provide a ChatbotClient instance for the entire test session."""
    client = ChatbotClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def quality_scorer():
    """Provide a QualityScorer instance for the entire test session."""
    return QualityScorer()


@pytest.fixture
def sample_question():
    """Provide a sample question for testing."""
    return "¿Cómo escribir tests unitarios en Python?"


@pytest.fixture
def sample_response(api_client, sample_question):
    """Provide a sample API response for testing."""
    return api_client.ask(sample_question)
