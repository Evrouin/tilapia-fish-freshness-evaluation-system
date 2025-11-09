"""RGB color analysis for freshness evaluation."""

from typing import Any, Dict, Tuple

import numpy as np

from ..config import config
from ..enums import FreshnessLevel


class ColorAnalyzer:
    """RGB color analyzer for freshness evaluation."""

    def __init__(self) -> None:
        """Initialize analyzer."""
        self.fresh_reference = config.analysis.fresh_reference_rgb
        self.mean_median_weight = config.analysis.mean_median_weight

    def analyze_colors(
        self, segmented_image: np.ndarray, mask: np.ndarray
    ) -> Dict[str, Any]:
        """Analyze colors in segmented gill area.

        Args:
            segmented_image: Segmented gill image
            mask: Binary mask

        Returns:
            Dictionary containing color analysis results
        """

        mask_condition = mask == 255
        valid_pixels = segmented_image[mask_condition]

        if len(valid_pixels) == 0:
            return {
                "avg_rgb": (0, 0, 0),
                "pixel_count": 0,
                "freshness": FreshnessLevel.NOT_FRESH,
                "confidence": 0.0,
                "metrics": {},
            }

        avg_b = int(np.mean(valid_pixels[:, 0]))
        avg_g = int(np.mean(valid_pixels[:, 1]))
        avg_r = int(np.mean(valid_pixels[:, 2]))

        median_b = int(np.median(valid_pixels[:, 0]))
        median_g = int(np.median(valid_pixels[:, 1]))
        median_r = int(np.median(valid_pixels[:, 2]))

        weight_mean, weight_median = self.mean_median_weight
        final_r = int(weight_mean * avg_r + weight_median * median_r)
        final_g = int(weight_mean * avg_g + weight_median * median_g)
        final_b = int(weight_mean * avg_b + weight_median * median_b)

        metrics = self._calculate_metrics(final_r, final_g, final_b)

        freshness, confidence = self._classify_freshness(
            final_r, final_g, final_b, metrics
        )

        return {
            "avg_rgb": (final_r, final_g, final_b),
            "pixel_count": len(valid_pixels),
            "freshness": freshness,
            "confidence": confidence,
            "metrics": metrics,
        }

    def _calculate_metrics(self, r: int, g: int, b: int) -> Dict[str, float]:
        """Calculate color metrics.

        Args:
            r, g, b: RGB values

        Returns:
            Dictionary of color metrics
        """

        distance = np.sqrt(
            (r - self.fresh_reference[0]) ** 2
            + (g - self.fresh_reference[1]) ** 2
            + (b - self.fresh_reference[2]) ** 2
        )

        brightness = (r + g + b) / 3
        max_rgb = max(r, g, b)
        min_rgb = min(r, g, b)
        saturation = (max_rgb - min_rgb) / max(max_rgb, 1) * 100

        rg_ratio = r / max(g, 1)
        rb_ratio = r / max(b, 1)
        gb_ratio = g / max(b, 1)

        return {
            "distance": distance,
            "brightness": brightness,
            "saturation": saturation,
            "rg_ratio": rg_ratio,
            "rb_ratio": rb_ratio,
            "gb_ratio": gb_ratio,
        }

    def _classify_freshness(
        self, r: int, g: int, b: int, metrics: Dict[str, float]
    ) -> Tuple[FreshnessLevel, float]:
        """Classify freshness based on color analysis.

        Args:
            r, g, b: RGB values
            metrics: Color metrics

        Returns:
            Tuple of (freshness_level, confidence)
        """
        distance = metrics["distance"]
        brightness = metrics["brightness"]
        saturation = metrics["saturation"]
        rg_ratio = metrics["rg_ratio"]

        close_thresh = config.analysis.close_distance_threshold
        moderate_thresh = config.analysis.moderate_distance_threshold

        if distance < close_thresh:  # Very close to fresh reference
            if (
                saturation > config.analysis.min_saturation_fresh
                and brightness < config.analysis.max_brightness_fresh
            ):
                return FreshnessLevel.FRESH, 0.9
            else:
                return FreshnessLevel.NOT_FRESH, 0.7

        elif distance < moderate_thresh:  # Moderate distance
            if r > g and r > b and rg_ratio > config.analysis.min_red_dominance_ratio:
                if (
                    brightness < config.analysis.max_brightness_moderate
                    and saturation > config.analysis.min_saturation_moderate
                ):
                    return FreshnessLevel.FRESH, 0.8
                else:
                    return FreshnessLevel.NOT_FRESH, 0.6
            elif b > r and b > g:
                return FreshnessLevel.OLD, 0.7
            else:
                return FreshnessLevel.NOT_FRESH, 0.5

        else:  # Far from reference
            if (
                brightness > config.analysis.max_brightness_old
                or saturation < config.analysis.min_saturation_old
            ):
                return FreshnessLevel.OLD, 0.8
            elif b > r + config.analysis.blue_shift_threshold:
                return FreshnessLevel.OLD, 0.7
            else:
                return FreshnessLevel.NOT_FRESH, 0.6
