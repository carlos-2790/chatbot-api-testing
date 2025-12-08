#!/usr/bin/env python
"""
Script para verificar y diagnosticar la API de Magic Loops
"""

import json
import sys

from src.api.chatbot_client import ChatbotClient
from src.utils.config import Config


def test_magic_loop():
    """Prueba la conexión con Magic Loops y muestra información detallada"""

    print("=" * 80)
    print("VERIFICACIÓN DE MAGIC LOOPS API")
    print("=" * 80)

    print(f"\nURL de la API: {Config.API_URL}")
    print(f"Timeout: {Config.API_TIMEOUT}s")
    print(f"Reintentos: {Config.REQUEST_RETRY_COUNT}")

    # Crear cliente
    client = ChatbotClient()

    # Preguntas de prueba
    test_questions = [
        "What is testing?",
        "What are the best practices for QA automation?",
        "Recommend me QA testing frameworks",
    ]

    for question in test_questions:
        print("\n" + "=" * 80)
        print(f"PREGUNTA: {question}")
        print("=" * 80)

        try:
            response = client.ask(question, debug=True)

            print(f"\n✓ Respuesta exitosa en {response['response_time']:.2f}s")
            print(f"Status Code: {response['status_code']}")
            print(f"\nDatos recibidos:")
            print(json.dumps(response["data"], indent=2, ensure_ascii=False))

        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")
            import traceback

            traceback.print_exc()

    client.close()
    print("\n" + "=" * 80)
    print("FIN DE LA VERIFICACIÓN")
    print("=" * 80)


if __name__ == "__main__":
    test_magic_loop()
