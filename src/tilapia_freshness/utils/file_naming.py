"""File naming utilities for standardized input processing."""

import os
import random
import shutil
import string
from datetime import datetime
from pathlib import Path
from typing import Optional


def generate_random_filename(length: int = 20, extension: Optional[str] = None) -> str:
    """Generate timestamped random alphanumeric filename.

    Args:
        length: Length of random part (default 20)
        extension: File extension (with dot, e.g., '.jpg')

    Returns:
        Timestamped random filename (YYMMDDHHMMSS-{random}.ext)
    """

    timestamp = datetime.now().strftime("%y%m%d%H%M%S")

    chars = string.ascii_letters + string.digits
    random_part = "".join(random.choices(chars, k=length))

    filename = f"{timestamp}-{random_part}"

    if extension:
        return f"{filename}{extension}"
    return filename


def standardize_input_file(original_path: str, input_dir: str = "inputs") -> str:
    """Copy input file to standardized location with random name.

    Args:
        original_path: Path to original file
        input_dir: Directory for standardized inputs

    Returns:
        Path to standardized file
    """

    os.makedirs(input_dir, exist_ok=True)

    original_ext = Path(original_path).suffix.lower()

    random_filename = generate_random_filename(20, original_ext)
    standardized_path = os.path.join(input_dir, random_filename)

    shutil.copy2(original_path, standardized_path)

    return standardized_path


def cleanup_input_file(standardized_path: str) -> None:
    """Clean up standardized input file.

    Args:
        standardized_path: Path to standardized file to remove
    """
    try:
        if os.path.exists(standardized_path):
            os.remove(standardized_path)
    except OSError:
        pass  # Ignore cleanup errors


class InputFileManager:
    """Manager for standardized input files."""

    def __init__(self, input_dir: str = "inputs"):
        """Initialize file manager.

        Args:
            input_dir: Directory for standardized inputs
        """
        self.input_dir = input_dir
        self.current_standardized_path: Optional[str] = None
        self.original_path: Optional[str] = None

    def process_input_file(self, original_path: str) -> str:
        """Process input file with standardized naming.

        Args:
            original_path: Path to original file

        Returns:
            Path to standardized file
        """

        self.cleanup_current()

        self.original_path = original_path
        self.current_standardized_path = standardize_input_file(
            original_path, self.input_dir
        )

        return self.current_standardized_path

    def get_standardized_path(self) -> Optional[str]:
        """Get current standardized file path.

        Returns:
            Standardized file path or None
        """
        return self.current_standardized_path

    def get_original_path(self) -> Optional[str]:
        """Get original file path.

        Returns:
            Original file path or None
        """
        return self.original_path

    def cleanup_current(self) -> None:
        """Clean up current standardized file."""
        if self.current_standardized_path:
            cleanup_input_file(self.current_standardized_path)
            self.current_standardized_path = None
            self.original_path = None

    def cleanup_all(self) -> None:
        """Clean up all files in input directory."""
        try:
            if os.path.exists(self.input_dir):
                for filename in os.listdir(self.input_dir):
                    file_path = os.path.join(self.input_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
        except OSError:
            pass  # Ignore cleanup errors
