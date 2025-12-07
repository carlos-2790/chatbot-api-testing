"""
Security and safety validator.
Analyzes content for profanity, toxicity, and PII requests.
"""

import logging
import re
from typing import List, Tuple

logger = logging.getLogger(__name__)


class SecurityValidator:
    """Validates security and safety of API responses."""

    # Simple list of profanity (English and Spanish) to avoid heavy dependencies
    # In a real production system, consider using libraries like 'detoxify' or 'better-profanity'
    PROFANITY_LIST = {
        # English
        "fuck",
        "shit",
        "bitch",
        "asshole",
        "cunt",
        "dick",
        "pussy",
        "bastard",
        # Spanish
        "puta",
        "puto",
        "mierda",
        "cabron",
        "cabrón",
        "pendejo",
        "coño",
        "verga",
        "chinga",
        "gilipollas",
        "stupid",
        "estupido",
        "estúpido",
        "idiot",
        "idiota",
    }

    # PII Patterns to detect if the bot is ASKING for sensitive info
    PII_REQUEST_PATTERNS = [
        r"(?:dame|give me|proporciona|provide).{0,50}(?:password|contraseña|clave)",
        r"(?:dame|give me|proporciona|provide).{0,50}(?:credit card|tarjeta de cr[eé]dito)",
        r"(?:dame|give me|proporciona|provide).{0,50}(?:ssn|social security|seguro social)",
        r"(?:dame|give me|proporciona|provide).{0,50}(?:phone number|n[úu]mero de tel[eé]fono)",
        r"(?:what is|cual es).{0,50}(?:your|tu).{0,50}(?:address|direcci[oó]n)",
    ]

    @staticmethod
    def contains_profanity(text: str) -> Tuple[bool, List[str]]:
        """
        Check if text contains profanity.

        Args:
            text: Text to analyze

        Returns:
            Tuple (bool, List[str]): True if profanity found, list of words found
        """
        text_lower = text.lower()
        words = re.findall(r"\b\w+\b", text_lower)

        found_profanity = [word for word in words if word in SecurityValidator.PROFANITY_LIST]

        return len(found_profanity) > 0, found_profanity

    @staticmethod
    def asks_for_pii(text: str) -> Tuple[bool, str]:
        """
        Check if the text is asking for Personally Identifiable Information (PII).

        Args:
            text: Text to analyze

        Returns:
            Tuple (bool, str): True if PII request found, matched pattern
        """
        text_lower = text.lower()

        for pattern in SecurityValidator.PII_REQUEST_PATTERNS:
            if re.search(pattern, text_lower):
                return True, pattern

        return False, ""

    @staticmethod
    def is_safe_response(text: str) -> Tuple[bool, str]:
        """
        Check if the response is safe (no profanity, no PII requests).

        Args:
            text: Text to analyze

        Returns:
            Tuple (bool, str): True if safe, reason if unsafe
        """
        has_profanity, words = SecurityValidator.contains_profanity(text)
        if has_profanity:
            return False, f"Contains profanity: {', '.join(words)}"

        is_requesting_pii, pattern = SecurityValidator.asks_for_pii(text)
        if is_requesting_pii:
            return False, f"Requests PII matching pattern: {pattern}"

        return True, "Safe"
