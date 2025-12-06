"""
Enhanced test script with colorful emoji output and response logging.
"""

import sys

sys.path.insert(0, ".")

from src.api.chatbot_client import ChatbotClient
from src.validators.quality_scorer import QualityScorer
from src.utils.response_logger import ResponseLogger


def print_header(text, emoji="🎯"):
    """Print a colorful header."""
    print(f"\n{emoji} {'='*60}")
    print(f"{emoji} {text}")
    print(f"{emoji} {'='*60}\n")


def print_section(title, emoji="📋"):
    """Print a section title."""
    print(f"\n{emoji} {title}")
    print("-" * 60)


def print_score(label, value, weight=None, emoji="📊"):
    """Print a score with formatting."""
    weight_str = f" (weight: {weight})" if weight else ""
    print(f"{emoji} {label:20s} {value:.3f}{weight_str}")


def print_result(passes, score, threshold):
    """Print the final result with appropriate emoji."""
    print("\n" + "=" * 60)
    if passes:
        print("✅ RESULTADO: TEST PASADO 🎉")
        print(f"✅ Score: {score:.3f} >= Threshold: {threshold:.3f}")
    else:
        print("❌ RESULTADO: TEST FALLIDO 😞")
        print(f"❌ Score: {score:.3f} < Threshold: {threshold:.3f}")
    print("=" * 60)


def main():
    print_header("Chatbot API Testing Framework", "🤖")
    print("Testing API and Quality Scorer with Response Logging...")

    # Initialize components
    client = ChatbotClient()
    scorer = QualityScorer()
    logger = ResponseLogger()

    # Test question
    question = "¿Cómo escribir tests unitarios en Python?"
    print_section(f"Question: {question}", "❓")

    # Get response
    print("\n⏳ Fetching response from API...")
    response = client.ask(question)

    print(f"✅ Status Code: {response['status_code']}")
    print(f"⚡ Response Time: {response['response_time']:.2f}s")
    print(f"📝 Answer Length: {len(response['data']['answer'])} characters")

    # Calculate scores
    print_section("Calculating quality scores...", "🔍")
    scores = scorer.get_detailed_scores(response, question)

    # Display scores
    print_header("QUALITY SCORES", "📊")
    print_score(
        "Structural Score", scores["structural_score"], scores["weights"]["structural"], "🏗️"
    )
    print_score("Content Score", scores["content_score"], scores["weights"]["content"], "📝")
    print_score("Semantic Score", scores["semantic_score"], scores["weights"]["semantic"], "🧠")
    print("-" * 60)
    print_score("OVERALL SCORE", scores["overall_score"], emoji="⭐")
    print_score("Threshold", scores["threshold"], emoji="🎯")

    # Print result
    print_result(scores["passes_threshold"], scores["overall_score"], scores["threshold"])

    # Content details
    print_section("Content Details", "📋")
    details = scores["content_details"]
    print(
        f"  {'✅' if details['has_code_examples'] else '❌'} Has code examples: {details['has_code_examples']}"
    )
    print(f"  🔤 Keyword count: {details['keyword_count']}")
    print(f"  🛠️  Frameworks mentioned: {details['frameworks_mentioned']}")
    print(
        f"  {'✅' if details['has_structure'] else '❌'} Has structure: {details['has_structure']}"
    )
    print(f"  📏 Length: {details['length']} characters")

    # Save response
    print_section("Saving Response", "💾")
    filepath = logger.save_response(question, response, scores)
    print(f"✅ Response saved to: {filepath}")

    # Logger summary
    summary = logger.get_summary()
    print(f"\n📊 Total responses logged: {summary['total_responses']}")
    print(f"💽 Total storage used: {summary['total_size_mb']:.2f} MB")
    print(f"📁 Log directory: {summary['log_directory']}")

    client.close()

    # Return exit code based on threshold
    if scores["passes_threshold"]:
        print("\n🎉 All checks passed! Framework is working correctly! 🎉\n")
        return 0
    else:
        print("\n⚠️  Quality threshold not met. Check the scores above. ⚠️\n")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
