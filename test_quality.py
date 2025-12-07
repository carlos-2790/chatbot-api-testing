"""
Script de prueba mejorado con emojis coloridos y registro de respuestas.
"""

import sys

sys.path.insert(0, ".")

from src.api.chatbot_client import ChatbotClient
from src.utils.response_logger import ResponseLogger
from src.validators.quality_scorer import QualityScorer


def print_header(text, emoji="🎯"):
    """Imprime un encabezado colorido."""
    print(f"\n{emoji} {'='*60}")
    print(f"{emoji} {text}")
    print(f"{emoji} {'='*60}\n")


def print_section(title, emoji="📋"):
    """Imprime el título de una sección."""
    print(f"\n{emoji} {title}")
    print("-" * 60)


def print_score(label, value, weight=None, emoji="📊"):
    """Imprime un puntaje con formato."""
    weight_str = f" (weight: {weight})" if weight else ""
    print(f"{emoji} {label:20s} {value:.3f}{weight_str}")


def print_result(passes, score, threshold):
    """Imprime el resultado final con el emoji apropiado."""
    print("\n" + "=" * 60)
    if passes:
        print("✅ RESULTADO: TEST PASADO 🎉")
        print(f"✅ Score: {score:.3f} >= Threshold: {threshold:.3f}")
    else:
        print("❌ RESULTADO: TEST FALLIDO 😞")
        print(f"❌ Score: {score:.3f} < Threshold: {threshold:.3f}")
    print("=" * 60)


def main():
    print_header("Framework de Pruebas de API de Chatbot", "🤖")
    print("Probando API y Puntaje de Calidad con Registro de Respuestas...")

    # Initialize components
    client = ChatbotClient()
    scorer = QualityScorer()
    logger = ResponseLogger()

    # Test question
    question = "¿Cómo escribir tests unitarios en Python?"
    print_section(f"Pregunta: {question}", "❓")

    # Get response
    print("\n⏳ Obteniendo respuesta de la API...")
    response = client.ask(question)

    print(f"✅ Código de Estado: {response['status_code']}")
    print(f"⚡ Tiempo de Respuesta: {response['response_time']:.2f}s")
    print(f"📝 Longitud de Respuesta: {len(response['data']['answer'])} caracteres")

    # Calculate scores
    print_section("Calculando puntajes de calidad...", "🔍")
    scores = scorer.get_detailed_scores(response, question)

    # Display scores
    print_header("PUNTAJES DE CALIDAD", "📊")
    print_score(
        "Puntaje Estructural", scores["structural_score"], scores["weights"]["structural"], "🏗️"
    )
    print_score("Puntaje de Contenido", scores["content_score"], scores["weights"]["content"], "📝")
    print_score("Puntaje Semántico", scores["semantic_score"], scores["weights"]["semantic"], "🧠")
    print("-" * 60)
    print_score("PUNTAJE GENERAL", scores["overall_score"], emoji="⭐")
    print_score("Umbral", scores["threshold"], emoji="🎯")

    # Print result
    print_result(scores["passes_threshold"], scores["overall_score"], scores["threshold"])

    # Content details
    print_section("Detalles del Contenido", "📋")
    details = scores["content_details"]
    print(
        f"  {'✅' if details['has_code_examples'] else '❌'} Tiene ejemplos de código: {details['has_code_examples']}"
    )
    print(f"  🔤 Recuento de palabras clave: {details['keyword_count']}")
    print(f"  🛠️  Frameworks mencionados: {details['frameworks_mentioned']}")
    print(
        f"  {'✅' if details['has_structure'] else '❌'} Tiene estructura: {details['has_structure']}"
    )
    print(f"  📏 Longitud: {details['length']} caracteres")

    # Save response
    print_section("Guardando Respuesta", "💾")
    filepath = logger.save_response(question, response, scores)
    print(f"✅ Respuesta guardada en: {filepath}")

    # Logger summary
    summary = logger.get_summary()
    print(f"\n📊 Total respuestas registradas: {summary['total_responses']}")
    print(f"💽 Almacenamiento total usado: {summary['total_size_mb']:.2f} MB")
    print(f"📁 Directorio de registros: {summary['log_directory']}")

    client.close()

    # Return exit code based on threshold
    if scores["passes_threshold"]:
        print(
            "\n🎉 ¡Todos los chequeos pasaron! ¡El framework está funcionando correctamente! 🎉\n"
        )
        return 0
    else:
        print("\n⚠️  El umbral de calidad no se cumplió. Revisa los puntajes arriba. ⚠️\n")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
