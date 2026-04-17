"""
Utility Helpers — Reusable functions for validation and sanitization.
"""

import logging
from typing import Tuple

logger = logging.getLogger(__name__)

# Sectors explicitly blocked (extensible list)
BLOCKED_SECTORS: set[str] = {"test", "null", "undefined", "none", "admin"}

# Minimum and maximum character limits
MIN_SECTOR_LEN = 3
MAX_SECTOR_LEN = 30


def sanitize_sector(sector: str) -> str:
    """
    Sanitize the sector input:
    - Strip leading/trailing whitespace
    - Convert to lowercase
    - Does NOT remove non-alphabetic characters (validation catches them)

    Args:
        sector: Raw sector string from request path.

    Returns:
        Sanitized sector string (whitespace stripped, lowercased).
    """
    sanitized = sector.strip().lower()
    logger.debug(f"Sanitized sector: '{sector}' → '{sanitized}'")
    return sanitized


def validate_sector(sector: str) -> Tuple[bool, str]:
    """
    Validate a sanitized sector name against business rules.

    Rules:
    1. Must be purely alphabetic (already enforced by sanitize, but double-checked).
    2. Length must be between MIN_SECTOR_LEN and MAX_SECTOR_LEN.
    3. Must not be in the BLOCKED_SECTORS list.

    Args:
        sector: Sanitized sector string.

    Returns:
        Tuple of (is_valid: bool, error_message: str).
        error_message is empty string if valid.
    """
    if not sector:
        return False, "Sector name cannot be empty."

    if not sector.isalpha():
        return False, f"Sector '{sector}' must contain only alphabetic characters."

    if len(sector) < MIN_SECTOR_LEN:
        return False, f"Sector name must be at least {MIN_SECTOR_LEN} characters long."

    if len(sector) > MAX_SECTOR_LEN:
        return False, f"Sector name must not exceed {MAX_SECTOR_LEN} characters."

    if sector in BLOCKED_SECTORS:
        return False, f"Sector '{sector}' is not a recognized market sector."

    return True, ""


def format_sector_display(sector: str) -> str:
    """
    Format a sanitized sector name for display (Title Case).

    Args:
        sector: Sanitized sector string.

    Returns:
        Title-cased sector string, e.g. 'pharma' → 'Pharma'.
    """
    return sector.title()
