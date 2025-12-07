"""
HTTP client for interacting with the chatbot API.
Includes retry logic, timeout handling, and performance metrics.
"""

import logging
import time
from typing import Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.utils.config import Config

logger = logging.getLogger(__name__)


class ChatbotClient:
    """Client for making requests to the chatbot API."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the chatbot client.

        Args:
            base_url: Base URL for the API (defaults to Config.API_URL)
            timeout: Request timeout in seconds (defaults to Config.API_TIMEOUT)
        """
        self.base_url = base_url or Config.API_URL
        self.timeout = timeout or Config.API_TIMEOUT
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=Config.REQUEST_RETRY_COUNT,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def ask(self, question: str) -> Dict:
        """
        Send a question to the chatbot API.

        Args:
            question: The question to ask

        Returns:
            Dict containing the API response with additional metadata

        Raises:
            requests.RequestException: If the request fails
        """
        start_time = time.time()

        try:
            logger.info(f"Sending question to API: {question[:50]}...")

            # Make the request
            response = self.session.get(
                self.base_url, params={"input": question}, timeout=self.timeout
            )

            # Raise exception for bad status codes
            response.raise_for_status()

            # Check for empty response
            if not response.content or not response.text.strip():
                raise ValueError("Empty response received from API")

            # Calculate response time
            response_time = time.time() - start_time

            # Parse JSON response
            try:
                data = response.json()
            except ValueError as e:
                raise ValueError(f"Invalid JSON response: {response.text[:200]}...") from e

            # Add metadata
            result = {
                "data": data,
                "response_time": response_time,
                "status_code": response.status_code,
                "question": question,
            }

            logger.info(f"Received response in {response_time:.2f}s")
            return result

        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {self.timeout}s")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            raise

    def health_check(self) -> bool:
        """
        Check if the API is available.

        Returns:
            True if API is healthy, False otherwise
        """
        try:
            response = self.ask("test")
            return response["status_code"] == 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
