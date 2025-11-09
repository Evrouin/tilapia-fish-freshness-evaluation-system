"""Analysis-related exceptions."""

from .base import TilapiaFreshnessError


class AnalysisError(TilapiaFreshnessError):
    """Exception raised during color analysis."""

    pass


class InvalidImageError(TilapiaFreshnessError):
    """Exception raised for invalid image data."""

    pass


class NoGillsDetectedError(TilapiaFreshnessError):
    """Exception raised when no gills are detected in image."""

    pass
