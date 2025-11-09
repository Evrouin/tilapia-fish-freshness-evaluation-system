"""GrabCut segmentation for gill area extraction."""

from typing import Optional, Tuple

import cv2
import numpy as np

from ..config import config
from ..enums import GrabCut


class GillSegmenter:
    """GrabCut-based gill segmentation."""

    def __init__(self) -> None:
        """Initialize segmenter."""
        pass

    def segment_gill(
        self, image: np.ndarray, bbox: Tuple[int, int, int, int], iterations: Optional[int] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Segment gill area using GrabCut.

        Args:
            image: Input image
            bbox: Bounding box (x, y, w, h)
            iterations: GrabCut iterations (optional, uses config default)

        Returns:
            Tuple of (segmented_image, mask)
        """
        if iterations is None:
            iterations = config.analysis.grabcut_iterations

        x, y, w, h = bbox

        cropped = image[y : y + h, x : x + w]

        crop_h, crop_w = cropped.shape[:2]
        margin = GrabCut.MARGIN
        rect = (margin, margin, crop_w - 2 * margin, crop_h - 2 * margin)

        mask = np.zeros(cropped.shape[:2], np.uint8)
        bg_model = np.zeros((1, 65), np.float64)
        fg_model = np.zeros((1, 65), np.float64)

        cv2.grabCut(
            cropped, mask, rect, bg_model, fg_model, iterations, cv2.GC_INIT_WITH_RECT
        )

        final_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")

        segmented = cropped * final_mask[:, :, np.newaxis]

        gray_mask = cv2.cvtColor(segmented, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(gray_mask, 0, 255, cv2.THRESH_BINARY)

        b, g, r = cv2.split(segmented)
        rgba = cv2.merge([b, g, r, alpha])

        return rgba, alpha
