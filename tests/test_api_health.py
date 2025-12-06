"""
API health and availability tests.
"""
import pytest
from src.api.chatbot_client import ChatbotClient


@pytest.mark.smoke
class TestAPIHealth:
    """Test API availability and basic functionality."""
    
    def test_api_is_reachable(self, api_client):
        """Test that the API endpoint is reachable."""
        assert api_client.health_check(), "API health check failed"
    
    def test_api_returns_200(self, api_client):
        """Test that API returns 200 status code."""
        response = api_client.ask("test")
        assert response['status_code'] == 200, f"Expected 200, got {response['status_code']}"
    
    def test_response_time_acceptable(self, api_client):
        """Test that API responds within acceptable time (<5 seconds)."""
        response = api_client.ask("test")
        assert response['response_time'] < 5.0, \
            f"Response time {response['response_time']:.2f}s exceeds 5s threshold"
    
    def test_api_handles_simple_query(self, api_client):
        """Test that API can handle a simple query."""
        response = api_client.ask("What is testing?")
        assert 'data' in response, "Response missing 'data' field"
        assert 'answer' in response['data'], "Response data missing 'answer' field"
        assert len(response['data']['answer']) > 0, "Answer is empty"
