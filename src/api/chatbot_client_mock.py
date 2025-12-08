"""
Cliente de ChatBot con soporte para modo mock/simulación.
Útil para testing cuando la API no está completamente configurada.
"""

import logging
import os
from typing import Dict, Any, Optional
from src.api.chatbot_client import ChatbotClient as BaseClient

logger = logging.getLogger(__name__)


class ChatbotClientWithMock(BaseClient):
    """Cliente que extiende ChatbotClient con capacidad de mock"""

    def __init__(
        self, 
        base_url: Optional[str] = None, 
        timeout: Optional[int] = None,
        use_mock: bool = False,
        mock_delay: float = 0.5
    ):
        """
        Inicializa el cliente con opción de mock.
        
        Args:
            base_url: URL de la API
            timeout: Timeout en segundos
            use_mock: Si True, usa respuestas simuladas
            mock_delay: Delay simulado en segundos
        """
        super().__init__(base_url, timeout)
        self.use_mock = use_mock or os.getenv("USE_MOCK", "false").lower() == "true"
        self.mock_delay = mock_delay

    def ask(self, question: str, debug: bool = False) -> Dict[str, Any]:
        """
        Realiza una pregunta. Si use_mock=True, retorna respuesta simulada.
        
        Args:
            question: La pregunta a realizar
            debug: Mostrar información de debug
            
        Returns:
            Respuesta de la API o respuesta simulada
        """
        if self.use_mock:
            return self._get_mock_response(question, debug)
        
        return super().ask(question, debug)

    def _get_mock_response(self, question: str, debug: bool = False) -> Dict[str, Any]:
        """Retorna una respuesta simulada para testing"""
        import time
        
        start_time = time.time()
        if self.mock_delay > 0:
            time.sleep(self.mock_delay)
        response_time = time.time() - start_time

        # Respuestas simuladas basadas en la pregunta
        mock_data = {
            "answer": f"This is a mock response for the question: '{question}'. "
                     "In a real scenario, this would be the LLM's response about QA automation.",
            "best_practices": [
                "Use automation for regression testing",
                "Implement CI/CD pipelines",
                "Write maintainable test code",
                "Follow the pyramid testing strategy",
                "Use meaningful assertions",
                "Test behavior, not implementation",
                "Keep tests independent"
            ],
            "recommended_frameworks": [
                "pytest (Python)",
                "unittest (Python)",
                "Selenium (Browser automation)",
                "Cypress (Browser automation)",
                "Robot Framework",
                "TestNG (Java)",
                "JUnit (Java)"
            ]
        }

        result = {
            "data": mock_data,
            "response_time": response_time,
            "status_code": 200,
            "question": question,
            "is_mock": True
        }

        if debug:
            logger.info(f"DEBUG (MOCK) - Question: {question}")
            logger.info(f"DEBUG (MOCK) - Response Time: {response_time:.2f}s")
            logger.info(f"DEBUG (MOCK) - Returning mock data")

        return result


# Exportar para uso conveniente
def get_client(use_mock: bool = False) -> ChatbotClientWithMock:
    """Factory function para crear cliente"""
    return ChatbotClientWithMock(use_mock=use_mock)
