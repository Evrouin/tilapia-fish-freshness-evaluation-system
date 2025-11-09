"""Industry-standard logging configuration."""

import logging
import os
from datetime import datetime
from typing import Optional

from ..enums import Log


class AppLogger:
    """Application logger with industry-standard formatting."""

    def __init__(self, name: str = "tilapia_freshness", log_dir: str = "outputs"):
        """Initialize logger.

        Args:
            name: Logger name
            log_dir: Directory for log files
        """
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self._setup_logger()

    def _setup_logger(self) -> None:
        """Setup logger with handlers and formatters."""
        if self.logger.handlers:
            return  # Already configured

        self.logger.setLevel(logging.INFO)

        os.makedirs(self.log_dir, exist_ok=True)

        detailed_formatter = logging.Formatter(
            Log.DETAILED_FORMAT, datefmt=Log.DATE_FORMAT
        )

        simple_formatter = logging.Formatter(Log.SIMPLE_FORMAT, datefmt=Log.DATE_FORMAT)

        log_file = os.path.join(self.log_dir, f"{self.name}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)

        analysis_file = os.path.join(self.log_dir, "analysis_results.log")
        analysis_handler = logging.FileHandler(analysis_file)
        analysis_handler.setLevel(logging.INFO)
        analysis_handler.setFormatter(simple_formatter)

        class AnalysisFilter(logging.Filter):
            def filter(self, record: logging.LogRecord) -> bool:
                return record.name == f"{self.name}.analysis"

        analysis_handler.addFilter(AnalysisFilter())

        error_file = os.path.join(self.log_dir, "errors.log")
        error_handler = logging.FileHandler(error_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(error_handler)

        analysis_logger = logging.getLogger(f"{self.name}.analysis")
        analysis_logger.setLevel(logging.INFO)
        analysis_logger.propagate = False  # Don't propagate to parent

        analysis_logger.addHandler(analysis_handler)
        analysis_logger.addHandler(file_handler)  # Also log to main file

    def get_logger(self, module_name: Optional[str] = None) -> logging.Logger:
        """Get logger for specific module.

        Args:
            module_name: Optional module name to append

        Returns:
            Logger instance
        """
        if module_name:
            return logging.getLogger(f"{self.name}.{module_name}")
        return self.logger

    def log_error(
        self, message: str, exception: Optional[Exception] = None, module: Optional[str] = None
    ) -> None:
        """Log error with structured format.

        Args:
            message: Error message
            exception: Optional exception object
            module: Optional module name
        """
        error_logger = self.get_logger("error")

        if exception:
            error_msg = f"{message}: {str(exception)}"
            if hasattr(exception, "__traceback__"):
                import traceback

                error_msg += f"\nTraceback: {traceback.format_exc()}"
        else:
            error_msg = message

        if module:
            error_msg = f"[{module}] {error_msg}"

        error_logger.error(error_msg)

    def log_analysis_result(
        self,
        image_path: str,
        freshness: str,
        rgb: tuple,
        confidence: float,
        metrics: dict,
    ) -> None:
        """Log analysis result in structured format.

        Args:
            image_path: Path to analyzed image
            freshness: Freshness classification
            rgb: RGB values tuple
            confidence: Classification confidence
            metrics: Analysis metrics
        """
        analysis_logger = self.get_logger("analysis")

        result_data = {
            "timestamp": datetime.now().isoformat(),
            "image": os.path.basename(image_path),
            "freshness": freshness,
            "rgb": f"R:{rgb[0]} G:{rgb[1]} B:{rgb[2]}",
            "confidence": f"{confidence:.2%}",
            "distance": f"{metrics.get('distance', 0):.2f}",
            "brightness": f"{metrics.get('brightness', 0):.1f}",
            "saturation": f"{metrics.get('saturation', 0):.1f}%",
        }

        log_message = " | ".join([f"{k}:{v}" for k, v in result_data.items()])
        analysis_logger.info(log_message)
        """Log analysis result in structured format.

        Args:
            image_path: Path to analyzed image
            freshness: Freshness classification
            rgb: RGB values tuple
            confidence: Classification confidence
            metrics: Analysis metrics
        """
        analysis_logger = self.get_logger("analysis")

        result_data = {
            "timestamp": datetime.now().isoformat(),
            "image": os.path.basename(image_path),
            "freshness": freshness,
            "rgb": f"R:{rgb[0]} G:{rgb[1]} B:{rgb[2]}",
            "confidence": f"{confidence:.2%}",
            "distance": f"{metrics.get('distance', 0):.2f}",
            "brightness": f"{metrics.get('brightness', 0):.1f}",
            "saturation": f"{metrics.get('saturation', 0):.1f}%",
        }

        log_message = " | ".join([f"{k}:{v}" for k, v in result_data.items()])
        analysis_logger.info(log_message)


def log_error(message: str, exception: Optional[Exception] = None, module: Optional[str] = None) -> None:
    """Global error logging function.

    Args:
        message: Error message
        exception: Optional exception object
        module: Optional module name
    """
    app_logger.log_error(message, exception, module)


app_logger = AppLogger()


def get_logger(module_name: str) -> logging.Logger:
    """Get logger for module.

    Args:
        module_name: Module name

    Returns:
        Logger instance
    """
    return app_logger.get_logger(module_name)
