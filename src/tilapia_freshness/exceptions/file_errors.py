"""File-related exceptions."""

from .base import TilapiaFreshnessError


class FileNotFoundError(TilapiaFreshnessError):
    """Exception raised when required file is not found."""

    pass


class InvalidFileFormatError(TilapiaFreshnessError):
    """Exception raised for invalid file format."""

    pass
