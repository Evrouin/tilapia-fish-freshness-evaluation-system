"""Enums and constants for tilapia freshness evaluation."""

from enum import Enum
from typing import Tuple


class FreshnessLevel(Enum):
    """Freshness classification levels."""

    FRESH = "Fresh"
    NOT_FRESH = "Not Fresh"
    OLD = "Old"


class ColorAnalysis:
    """Constants for color analysis and freshness classification."""

    FRESH_REFERENCE_RGB: Tuple[int, int, int] = (32, 19, 17)
    MEAN_MEDIAN_WEIGHTS: Tuple[float, float] = (0.7, 0.3)

    CLOSE_DISTANCE_THRESHOLD: float = 60.0
    MODERATE_DISTANCE_THRESHOLD: float = 100.0

    MIN_SATURATION_FRESH: float = 15.0
    MAX_BRIGHTNESS_FRESH: float = 80.0
    MIN_RED_DOMINANCE_RATIO: float = 1.2

    MAX_BRIGHTNESS_MODERATE: float = 100.0
    MIN_SATURATION_MODERATE: float = 10.0

    MAX_BRIGHTNESS_OLD: float = 120.0
    MIN_SATURATION_OLD: float = 5.0
    BLUE_SHIFT_THRESHOLD: int = 20


class YOLOv3:
    """Constants for YOLO object detection."""

    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.5
    DEFAULT_NMS_THRESHOLD: float = 0.5
    DEFAULT_INPUT_SIZE: Tuple[int, int] = (416, 416)
    SCALE_FACTOR: float = 0.00392


class GrabCut:
    """Constants for GrabCut segmentation."""

    DEFAULT_ITERATIONS: int = 5
    MARGIN: int = 1


class GUI:
    """Constants for GUI configuration."""

    DEFAULT_WINDOW_SIZE: str = "1366x768"
    DEFAULT_CANVAS_SIZE: Tuple[int, int] = (1320, 420)
    DEFAULT_FONT_FAMILY: str = "Helvetica"
    DEFAULT_FONT_SIZE: int = 18
    DEFAULT_BUTTON_FONT: str = "ariel 15 bold"


class File:
    """Constants for file handling."""

    SUPPORTED_IMAGE_EXTENSIONS: Tuple[str, ...] = (".jpg", ".jpeg", ".png", ".bmp")


class Log:
    """Constants for logging configuration."""

    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DETAILED_FORMAT: str = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(funcName)s:%(lineno)d - %(message)s"
    )
    SIMPLE_FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"
