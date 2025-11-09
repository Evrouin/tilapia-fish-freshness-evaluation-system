"""Application configuration settings."""

import os
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class ModelConfig:
    """YOLO model configuration."""

    config_path: str = "data/yolov3_tilapia.cfg"
    weights_path: str = "data/yolov3_tilapia.weights"
    names_path: str = "data/obj.names"
    confidence_threshold: float = 0.5
    nms_threshold: float = 0.5
    input_size: Tuple[int, int] = (416, 416)


@dataclass
class AnalysisConfig:
    """Color analysis configuration."""

    fresh_reference_rgb: Tuple[int, int, int] = (32, 19, 17)
    mean_median_weight: Tuple[float, float] = (0.7, 0.3)
    grabcut_iterations: int = 5

    close_distance_threshold: float = 60.0
    moderate_distance_threshold: float = 100.0

    min_saturation_fresh: float = 15.0
    max_brightness_fresh: float = 80.0
    min_red_dominance_ratio: float = 1.2
    max_brightness_moderate: float = 100.0
    min_saturation_moderate: float = 10.0
    max_brightness_old: float = 120.0
    min_saturation_old: float = 5.0
    blue_shift_threshold: int = 20


@dataclass
class GUIConfig:
    """GUI configuration."""

    window_title: str = "Tilapia Freshness Evaluator"
    window_size: str = "1366x768"
    canvas_size: Tuple[int, int] = (1320, 420)
    font_family: str = "Helvetica"
    font_size: int = 18
    button_font: str = "ariel 15 bold"


@dataclass
class PathConfig:
    """File path configuration."""

    output_dir: str = "outputs"
    log_dir: str = "outputs"

    main_log_file: str = "tilapia_freshness.log"
    analysis_log_file: str = "analysis_results.log"


@dataclass
class AppConfig:
    """Main application configuration."""

    model: ModelConfig = field(default_factory=ModelConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    gui: GUIConfig = field(default_factory=GUIConfig)
    paths: PathConfig = field(default_factory=PathConfig)

    def __post_init__(self) -> None:
        """Ensure output directories exist."""
        os.makedirs(self.paths.output_dir, exist_ok=True)
        os.makedirs(self.paths.log_dir, exist_ok=True)


config = AppConfig()
