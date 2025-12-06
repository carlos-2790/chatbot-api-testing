"""
Response structure validator.
Validates JSON schema and data types.
"""

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


class ResponseValidator:
    """Validates API response structure and schema."""

    @staticmethod
    def validate_json_structure(response: Dict) -> Tuple[bool, List[str]]:
        """
        Validate that response has expected JSON structure.

        Args:
            response: API response dictionary

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check if 'data' key exists
        if "data" not in response:
            errors.append("Missing 'data' key in response")
            return False, errors

        data = response["data"]

        # Check if 'answer' field exists
        if "answer" not in data:
            errors.append("Missing 'answer' field in response data")

        # Check if answer is a string
        if "answer" in data and not isinstance(data["answer"], str):
            errors.append(f"'answer' field must be string, got {type(data['answer']).__name__}")

        # Check if answer is not empty
        if "answer" in data and isinstance(data["answer"], str) and not data["answer"].strip():
            errors.append("'answer' field is empty")

        is_valid = len(errors) == 0
        return is_valid, errors

    @staticmethod
    def validate_metadata(response: Dict) -> Tuple[bool, List[str]]:
        """
        Validate response metadata (status_code, response_time, etc.).

        Args:
            response: API response dictionary

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check status code
        if "status_code" not in response:
            errors.append("Missing 'status_code' in response")
        elif response["status_code"] != 200:
            errors.append(f"Expected status_code 200, got {response['status_code']}")

        # Check response time exists
        if "response_time" not in response:
            errors.append("Missing 'response_time' in response")
        elif not isinstance(response["response_time"], (int, float)):
            errors.append(
                f"'response_time' must be numeric, got {type(response['response_time']).__name__}"
            )

        is_valid = len(errors) == 0
        return is_valid, errors

    @staticmethod
    def validate_response(response: Dict) -> Tuple[bool, List[str]]:
        """
        Perform complete response validation.

        Args:
            response: API response dictionary

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        all_errors = []

        # Validate structure
        struct_valid, struct_errors = ResponseValidator.validate_json_structure(response)
        all_errors.extend(struct_errors)

        # Validate metadata
        meta_valid, meta_errors = ResponseValidator.validate_metadata(response)
        all_errors.extend(meta_errors)

        is_valid = len(all_errors) == 0

        if not is_valid:
            logger.warning(f"Response validation failed: {', '.join(all_errors)}")

        return is_valid, all_errors

    @staticmethod
    def get_answer_text(response: Dict) -> str:
        """
        Safely extract answer text from response.

        Args:
            response: API response dictionary

        Returns:
            Answer text or empty string if not found
        """
        try:
            return response.get("data", {}).get("answer", "")
        except (AttributeError, TypeError):
            return ""
