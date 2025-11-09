"""Base exception classes."""

from typing import Optional


class TilapiaFreshnessError(Exception):
    """Base exception for tilapia freshness evaluation system."""

    def __init__(self, message: str, details: Optional[str] = None):
        """Initialize exception.

        Args:
            message: Error message
            details: Additional error details
        """
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation of error."""
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message
