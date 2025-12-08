"""
Cliente HTTP para interactuar con la API del chatbot.
Incluye lógica de reintento, manejo de tiempos de espera y métricas de rendimiento.
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
    """Cliente para realizar peticiones a la API del chatbot."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Inicializa el cliente del chatbot.

        Args:
            base_url: URL base para la API (por defecto usa Config.API_URL)
            timeout: Tiempo de espera de la petición en segundos (por defecto usa Config.API_TIMEOUT)
        """
        self.base_url = base_url or Config.API_URL
        self.timeout = timeout or Config.API_TIMEOUT
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Crea una sesión de requests con lógica de reintento."""
        session = requests.Session()

        # Configurar estrategia de reintento
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
        Envía una pregunta a la API del chatbot.

        Args:
            question: La pregunta a realizar

        Returns:
            Dict conteniendo la respuesta de la API con metadatos adicionales

        Raises:
            requests.RequestException: Si la petición falla
        """
        start_time = time.time()

        try:
            logger.info(f"Enviando pregunta a la API: {question[:50]}...")

            # Realizar la petición POST enviando JSON
            payload = {"question": question}
            response = self.session.post(self.base_url, json=payload, timeout=self.timeout)

            # Lanzar excepción para códigos de estado erróneos
            response.raise_for_status()

            # Verificar respuesta vacía
            if not response.content or not response.text.strip():
                raise ValueError("Respuesta vacía recibida de la API")

            # Calcular tiempo de respuesta
            response_time = time.time() - start_time

            # Analizar respuesta JSON
            try:
                data = response.json()
            except ValueError as e:
                raise ValueError(f"Respuesta JSON inválida: {response.text[:200]}...") from e

            # Añadir metadatos
            result = {
                "data": data,
                "response_time": response_time,
                "status_code": response.status_code,
                "question": question,
            }

            logger.info(f"Respuesta recibida en {response_time:.2f}s")
            return result

        except requests.exceptions.Timeout:
            logger.error(f"La petición expiró después de {self.timeout}s")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"La petición falló: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"Fallo al analizar la respuesta JSON: {str(e)}")
            raise

    def health_check(self) -> bool:
        """
        Verifica si la API está disponible.

        Returns:
            True si la API está saludable, False en caso contrario
        """
        try:
            response = self.ask("test")
            return response["status_code"] == 200
        except Exception as e:
            logger.error(f"Verificación de salud falló: {str(e)}")
            return False

    def close(self):
        """Cierra la sesión."""
        self.session.close()

    def __enter__(self):
        """Entrada del administrador de contexto."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Salida del administrador de contexto."""
        self.close()
