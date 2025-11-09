"""Tests for file naming utilities."""

import os
import tempfile

from tilapia_freshness.utils.file_naming import (
    InputFileManager,
    generate_random_filename,
)


class TestFileNaming:
    """Test cases for file naming utilities."""

    def test_generate_random_filename(self):
        """Test random filename generation."""
        filename = generate_random_filename(20, ".jpg")

        # Check format: YYMMDDHHMMSS-{20chars}.jpg
        assert filename.endswith(".jpg")
        assert len(filename) == 12 + 1 + 20 + 4  # timestamp + dash + random + ext
        assert "-" in filename

    def test_generate_random_filename_no_extension(self):
        """Test random filename without extension."""
        filename = generate_random_filename(20)

        assert len(filename) == 12 + 1 + 20  # timestamp + dash + random
        assert "-" in filename

    def test_input_file_manager(self):
        """Test InputFileManager functionality."""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name

        try:
            manager = InputFileManager()
            standardized_path = manager.process_input_file(tmp_path)

            assert os.path.exists(standardized_path)
            assert standardized_path != tmp_path
            assert standardized_path.endswith(".jpg")

            manager.cleanup_current()
            assert not os.path.exists(standardized_path)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
