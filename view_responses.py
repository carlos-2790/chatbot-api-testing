"""
Script to view saved responses.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, ".")

from src.utils.response_logger import ResponseLogger


def print_response(filepath: Path):
    """Print a saved response in a nice format."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n" + "=" * 70)
    print(f"📅 Timestamp: {data['timestamp']}")
    print(f"❓ Question: {data['question']}")
    print("=" * 70)

    print(f"\n📝 Answer:")
    print("-" * 70)
    print(data["response"]["answer"])
    print("-" * 70)

    print(f"\n⚡ Response Time: {data['response']['response_time']:.2f}s")
    print(f"✅ Status Code: {data['response']['status_code']}")

    if "quality_scores" in data:
        scores = data["quality_scores"]
        print(f"\n📊 Quality Scores:")
        print(f"  🏗️  Structural: {scores['structural_score']:.3f}")
        print(f"  📝 Content: {scores['content_score']:.3f}")
        print(f"  🧠 Semantic: {scores['semantic_score']:.3f}")
        print(f"  ⭐ Overall: {scores['overall_score']:.3f}")
        print(
            f"  {'✅ PASS' if scores['passes_threshold'] else '❌ FAIL'} (threshold: {scores['threshold']:.3f})"
        )

    print("=" * 70)


def main():
    print("\n🔍 Saved Responses Viewer\n")

    logger = ResponseLogger()
    responses = logger.list_responses()

    if not responses:
        print("❌ No saved responses found.")
        print(f"📁 Looking in: {logger.log_dir}")
        return

    print(f"📊 Found {len(responses)} saved response(s)\n")

    # List all responses
    for i, filepath in enumerate(responses, 1):
        timestamp = filepath.stem.split("_")[0]
        question = "_".join(filepath.stem.split("_")[2:])
        print(f"{i}. [{timestamp}] {question[:50]}...")

    # Show latest response by default
    print(f"\n{'='*70}")
    print("📄 Showing latest response:")
    print_response(responses[0])

    # Summary
    summary = logger.get_summary()
    print(f"\n💾 Storage Summary:")
    print(f"  📊 Total responses: {summary['total_responses']}")
    print(f"  💽 Total size: {summary['total_size_mb']:.2f} MB")
    print(f"  📁 Directory: {summary['log_directory']}")
    print()


if __name__ == "__main__":
    main()
