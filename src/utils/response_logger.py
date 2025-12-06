"""
Response logger for saving AI chatbot responses.
Stores responses in JSON format with metadata for analysis.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from src.utils.config import Config

logger = logging.getLogger(__name__)


class ResponseLogger:
    """Logs and saves API responses for later analysis."""

    def __init__(self, log_dir: Optional[Path] = None):
        """
        Initialize the response logger.

        Args:
            log_dir: Directory to save responses (defaults to Config.PROJECT_ROOT/responses)
        """
        self.log_dir = log_dir or (Config.PROJECT_ROOT / "responses")
        self.log_dir.mkdir(exist_ok=True)
        logger.info(f"Response logger initialized. Saving to: {self.log_dir}")

    def save_response(
        self,
        question: str,
        response: Dict,
        scores: Optional[Dict] = None,
        filename: Optional[str] = None,
    ) -> Path:
        """
        Save a response to a JSON file.

        Args:
            question: The question that was asked
            response: The API response
            scores: Optional quality scores
            filename: Optional custom filename (without extension)

        Returns:
            Path to the saved file
        """
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Create safe filename from question
            safe_question = "".join(
                c for c in question[:50] if c.isalnum() or c in (" ", "-", "_")
            ).strip()
            safe_question = safe_question.replace(" ", "_")
            filename = f"{timestamp}_{safe_question}"

        filepath = self.log_dir / f"{filename}.json"

        # Prepare data to save
        data = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "response": {
                "answer": response.get("data", {}).get("answer", ""),
                "status_code": response.get("status_code"),
                "response_time": response.get("response_time"),
            },
        }

        # Add scores if provided
        if scores:
            data["quality_scores"] = scores

        # Save to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Response saved to: {filepath}")
        return filepath

    def load_response(self, filepath: Path) -> Dict:
        """
        Load a saved response from file.

        Args:
            filepath: Path to the JSON file

        Returns:
            Dictionary with response data
        """
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_responses(self, limit: Optional[int] = None) -> list:
        """
        List all saved responses.

        Args:
            limit: Optional limit on number of responses to return

        Returns:
            List of file paths, sorted by modification time (newest first)
        """
        responses = sorted(
            self.log_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True
        )

        if limit:
            responses = responses[:limit]

        return responses

    def get_summary(self) -> Dict:
        """
        Get summary of logged responses.

        Returns:
            Dictionary with summary statistics
        """
        responses = list(self.log_dir.glob("*.json"))

        total_size = sum(f.stat().st_size for f in responses)

        return {
            "total_responses": len(responses),
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "log_directory": str(self.log_dir),
        }
