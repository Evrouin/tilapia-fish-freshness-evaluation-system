"""Tests for color analyzer."""

import numpy as np

from tilapia_freshness.enums import FreshnessLevel
from tilapia_freshness.models.analyzer import ColorAnalyzer


class TestColorAnalyzer:
    """Test cases for ColorAnalyzer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = ColorAnalyzer()

    def test_analyzer_initialization(self):
        """Test analyzer initializes correctly."""
        assert self.analyzer is not None
        assert hasattr(self.analyzer, "fresh_reference")

    def test_analyze_colors_empty_mask(self):
        """Test analysis with empty mask."""
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        mask = np.zeros((100, 100), dtype=np.uint8)

        result = self.analyzer.analyze_colors(image, mask)

        assert result["avg_rgb"] == (0, 0, 0)
        assert result["pixel_count"] == 0
        assert result["freshness"] == FreshnessLevel.NOT_FRESH

    def test_analyze_colors_valid_input(self):
        """Test analysis with valid input."""
        # Create test image with red pixels
        image = np.full((100, 100, 3), [50, 20, 15], dtype=np.uint8)
        mask = np.full((100, 100), 255, dtype=np.uint8)

        result = self.analyzer.analyze_colors(image, mask)

        assert result["pixel_count"] > 0
        assert isinstance(result["freshness"], FreshnessLevel)
        assert "confidence" in result
        assert "metrics" in result
