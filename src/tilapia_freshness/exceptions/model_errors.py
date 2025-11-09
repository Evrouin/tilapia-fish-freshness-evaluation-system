"""Model-related exceptions."""

from .base import TilapiaFreshnessError


class ModelLoadError(TilapiaFreshnessError):
    """Exception raised when model fails to load."""

    pass


class DetectionError(TilapiaFreshnessError):
    """Exception raised during object detection."""

    pass


class SegmentationError(TilapiaFreshnessError):
    """Exception raised during image segmentation."""

    pass
