"""Image caching utilities for performance optimization."""

import hashlib
import os
from typing import Dict, Optional, Tuple

import numpy as np
from PIL import Image


class ImageCache:
    """LRU cache for images to avoid reloading."""

    def __init__(self, max_size: int = 10):
        """Initialize cache.

        Args:
            max_size: Maximum number of images to cache
        """
        self.max_size = max_size
        self.cache: Dict[str, Tuple[np.ndarray, Image.Image]] = {}
        self.access_order: list = []

    def _get_file_hash(self, file_path: str) -> str:
        """Get hash of file for cache key.

        Args:
            file_path: Path to image file

        Returns:
            MD5 hash of file
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get(self, file_path: str) -> Optional[Tuple[np.ndarray, Image.Image]]:
        """Get cached image.

        Args:
            file_path: Path to image file

        Returns:
            Tuple of (cv2_image, pil_image) or None if not cached
        """
        if not os.path.exists(file_path):
            return None

        cache_key = f"{file_path}_{os.path.getmtime(file_path)}"

        if cache_key in self.cache:

            self.access_order.remove(cache_key)
            self.access_order.append(cache_key)
            return self.cache[cache_key]

        return None

    def put(
        self, file_path: str, cv2_image: np.ndarray, pil_image: Image.Image
    ) -> None:
        """Cache image.

        Args:
            file_path: Path to image file
            cv2_image: OpenCV image
            pil_image: PIL image
        """
        cache_key = f"{file_path}_{os.path.getmtime(file_path)}"

        if len(self.cache) >= self.max_size and cache_key not in self.cache:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]

        self.cache[cache_key] = (cv2_image.copy(), pil_image.copy())

        if cache_key in self.access_order:
            self.access_order.remove(cache_key)
        self.access_order.append(cache_key)

    def clear(self) -> None:
        """Clear cache."""
        self.cache.clear()
        self.access_order.clear()


image_cache = ImageCache()
