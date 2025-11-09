"""Main GUI window for tilapia freshness evaluation."""

import os
import tkinter as tk
from tkinter import GROOVE, RIDGE, Button, Canvas, Label, filedialog, messagebox
from typing import Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageTk

from ..config import config
from ..exceptions import (
    AnalysisError,
    DetectionError,
    InvalidImageError,
    ModelLoadError,
    NoGillsDetectedError,
)
from ..models.analyzer import ColorAnalyzer
from ..models.detector import YOLODetector
from ..models.segmentation import GillSegmenter
from ..utils.cache import image_cache
from ..utils.file_naming import InputFileManager
from ..utils.logger import app_logger, get_logger, log_error
from ..utils.progress import run_with_progress
from ..utils.resources import get_icon_path


class MainWindow:
    """Main application window."""

    def __init__(self) -> None:
        """Initialize main window."""
        self.logger = get_logger("gui.main_window")
        self.logger.info("Initializing Tilapia Freshness Evaluator")

        self.root = tk.Tk()
        self.root.title(config.gui.window_title)
        self.root.geometry(config.gui.window_size)

        self._set_icon()

        self.detector: Optional[YOLODetector] = None
        self.segmenter = GillSegmenter()
        self.analyzer = ColorAnalyzer()
        self.input_file_manager = InputFileManager()

        self.original_image_path: Optional[str] = None
        self.current_image_path: Optional[str] = None
        self.current_image: Optional[Image.Image] = None
        self.detection_bbox: Optional[Tuple[int, int, int, int]] = None

        self.detection_result_image: Optional[np.ndarray] = None
        self.segmented_image: Optional[np.ndarray] = None
        self.mask_image: Optional[np.ndarray] = None

        self._initialize_models()
        self._setup_gui()

    def _set_icon(self) -> None:
        """Set application icon."""
        try:
            icon_path = get_icon_path()
            if icon_path:
                icon_image = Image.open(icon_path)
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, icon_photo)

                self.root._icon_photo = icon_photo  # type: ignore
                self.logger.info("Application icon loaded successfully")
            else:
                self.logger.warning("Application icon not found")
        except Exception as e:
            self.logger.error(f"Could not set application icon: {e}")

    def _initialize_models(self) -> None:
        """Initialize ML models with lazy loading."""
        try:
            self.logger.info("Initializing YOLO detector")

            self.detector = YOLODetector()
            self.logger.info("YOLO detector initialized")
        except (ModelLoadError, FileNotFoundError) as e:
            self.logger.error(f"Failed to initialize YOLO detector: {e}")
            messagebox.showerror(
                "Model Error", f"Failed to initialize YOLO detector: {e}"
            )

    def _setup_gui(self) -> None:
        """Setup GUI components."""

        self.canvas = Canvas(self.root, width=1320, height=420, relief=RIDGE, bd=2)
        self.canvas.place(x=15, y=10)

        self.freshness_label = Label(
            self.root, text="<<FRESHNESS ANALYSIS>>", font=("Helvetica", 18)
        )
        self.freshness_label.place(x=60, y=480)

        self.rgb_label = Label(
            self.root, text="<<AVERAGE COLOR RGB>>", font=("Helvetica", 18)
        )
        self.rgb_label.place(x=60, y=520)

        self.select_button = Button(
            self.root,
            text="Select Image",
            font="ariel 15 bold",
            relief=GROOVE,
            command=self.select_image,
        )
        self.select_button.place(x=60, y=570)

        self.analyze_button = Button(
            self.root,
            text="Start Analysis",
            width=12,
            font="ariel 15 bold",
            relief=GROOVE,
            command=self.analyze_freshness,
        )
        self.analyze_button.place(x=240, y=570)

    def select_image(self) -> None:
        """Handle image selection."""
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select Fish Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")],
        )

        if not file_path:
            return

        self.original_image_path = file_path
        self.current_image_path = self.input_file_manager.process_input_file(file_path)

        self.logger.info(f"Image selected: {os.path.basename(self.current_image_path)}")

        self.freshness_label.config(
            text="<<FRESHNESS ANALYSIS>>", font=("Helvetica", 18)
        )
        self.rgb_label.config(text="<<AVERAGE COLOR RGB>>", font=("Helvetica", 18))

        self._detect_gills()

    def _detect_gills(self) -> None:
        """Detect gills in selected image with caching and progress."""
        if not self.current_image_path or not self.detector:
            return

        def detection_operation() -> bool:
            assert self.current_image_path is not None, "No image selected"

            cached_images = image_cache.get(self.current_image_path)
            if cached_images:
                self.logger.info("Using cached image")
                image, _ = cached_images
            else:

                image = cv2.imread(self.current_image_path)
                if image is None:
                    raise InvalidImageError(
                        "Failed to load image", self.current_image_path
                    )

                pil_image = Image.open(self.current_image_path)
                image_cache.put(self.current_image_path, image, pil_image)
                self.logger.info("Image loaded and cached")

            if self.detector is None:
                self.detector = YOLODetector()

            b_boxes, confidences, class_ids, indices = self.detector.detect(image)

            if not indices:
                raise NoGillsDetectedError("No gills detected in image")

            result_image = self.detector.draw_detections(
                image, b_boxes, class_ids, indices
            )

            self.detection_result_image = result_image.copy()

            self.detection_bbox = tuple(b_boxes[indices[0]])

            return True

        try:
            result = run_with_progress(
                self.root,
                detection_operation,
                "Detecting Gills",
                "Analyzing image for gill detection...",
            )

            if result:
                if self.detection_result_image is not None:
                    self._display_image_from_array(self.detection_result_image)
                self.logger.info("Gill detection completed successfully")

        except (DetectionError, InvalidImageError, NoGillsDetectedError) as e:
            self.logger.error(f"Detection failed: {e}")
            messagebox.showerror("Detection Error", str(e))
        except Exception as e:
            self.logger.error(f"Unexpected error during detection: {e}")
            log_error("Gill detection failed", e, "gui.main_window")
            messagebox.showerror("Error", f"Detection failed: {e}")

    def analyze_freshness(self) -> None:
        """Analyze freshness of detected gills."""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        try:

            def analysis_operation() -> dict:
                assert self.current_image_path is not None, "No image selected"

                cached_images = image_cache.get(self.current_image_path)
                if cached_images:
                    image, _ = cached_images
                else:
                    image = cv2.imread(self.current_image_path)
                    if image is None:
                        raise InvalidImageError(
                            "Failed to load image", self.current_image_path
                        )

                if not self.detection_bbox:
                    raise AnalysisError("No detection coordinates available")

                bbox = self.detection_bbox

                segmented_image, mask = self.segmenter.segment_gill(image, bbox)

                self.segmented_image = segmented_image.copy()
                self.mask_image = mask.copy()

                analysis_result = self.analyzer.analyze_colors(
                    segmented_image[:, :, :3], mask
                )

                return analysis_result

            result = run_with_progress(
                self.root,
                analysis_operation,
                "Analyzing Freshness",
                "Performing segmentation and color analysis...",
            )

            if result:

                self._display_analysis_results(result)

                self._log_results(result)

                if self.segmented_image is not None:
                    self._display_image_from_array(self.segmented_image)

                self.logger.info("Freshness analysis completed successfully")

                self._save_results_to_files()

        except (AnalysisError, InvalidImageError) as e:
            self.logger.error(f"Analysis failed: {e}")
            messagebox.showerror("Analysis Error", str(e))
        except Exception as e:
            self.logger.error(f"Unexpected error during analysis: {e}")
            log_error("Freshness analysis failed", e, "gui.main_window")
            messagebox.showerror("Error", f"Analysis failed: {e}")

    def _display_image(self, image_path: str) -> None:
        """Display image on canvas from file path."""
        try:
            img = Image.open(image_path)
            img.thumbnail((600, 600))
            photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(660, 210, image=photo)
            self.canvas._image = photo  # type: ignore
        except Exception as e:
            self.logger.error(f"Failed to display image: {e}")
            log_error("Image display failed", e, "gui.main_window")

    def _display_image_from_array(self, image_array: np.ndarray) -> None:
        """Display image on canvas from numpy array."""
        try:

            if len(image_array.shape) == 3 and image_array.shape[2] == 3:
                image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            elif len(image_array.shape) == 3 and image_array.shape[2] == 4:
                image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGRA2RGBA)
            else:
                image_rgb = image_array

            img = Image.fromarray(image_rgb)
            img.thumbnail((600, 600))
            photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(660, 210, image=photo)
            self.canvas._image = photo  # type: ignore
        except Exception as e:
            self.logger.error(f"Failed to display image from array: {e}")
            log_error("Image array display failed", e, "gui.main_window")

    def _save_results_to_files(self) -> None:
        """Save processed images to files (for export/backup)."""
        try:
            if self.detection_result_image is not None:
                cv2.imwrite("outputs/prediction.jpg", self.detection_result_image)

            if self.segmented_image is not None:
                cv2.imwrite("outputs/segmented.png", self.segmented_image)

            if self.mask_image is not None:
                cv2.imwrite("outputs/mask.png", self.mask_image)

            if self.detection_bbox is not None and self.current_image_path:
                original_image = cv2.imread(self.current_image_path)
                if original_image is not None:
                    x, y, w, h = self.detection_bbox
                    cropped = original_image[y : y + h, x : x + w]
                    cv2.imwrite("outputs/grabcut.png", cropped)

            self.logger.info("Results saved to output files")
        except Exception as e:
            self.logger.error(f"Failed to save results to files: {e}")
            log_error("File save failed", e, "gui.main_window")

    def _display_analysis_results(self, result: dict) -> None:
        """Display analysis results on GUI."""
        freshness = result["freshness"].value
        r, g, b = result["avg_rgb"]

        freshness_text = f"FRESHNESS ANALYSIS: {freshness}"
        rgb_text = f"AVERAGE COLOR RGB: {r} {g} {b}"

        self.freshness_label.config(text=freshness_text, font=("Helvetica", 18))
        self.rgb_label.config(text=rgb_text, font=("Helvetica", 18))

        metrics = result["metrics"]
        details = f"{freshness_text}\n{rgb_text}\n"
        details += f"Confidence: {result['confidence']:.1%}\n"
        details += f"Distance: {metrics.get('distance', 0):.1f}\n"
        details += f"Brightness: {metrics.get('brightness', 0):.1f}\n"
        details += f"Saturation: {metrics.get('saturation', 0):.1f}%"

        messagebox.showinfo("Analysis Results", details)

    def _log_results(self, result: dict) -> None:
        """Log analysis results using structured logging."""
        try:
            if not self.current_image_path or not self.original_image_path:
                return

            app_logger.log_analysis_result(
                image_path=self.original_image_path,
                freshness=result["freshness"].value,
                rgb=result["avg_rgb"],
                confidence=result["confidence"],
                metrics=result["metrics"],
            )

            self.logger.info(
                f"Analysis completed for {os.path.basename(self.original_image_path)}"
            )

        except Exception as e:
            self.logger.error(f"Failed to log results: {e}")

    def run(self) -> None:
        """Start the application."""
        try:

            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            self.root.mainloop()
        finally:

            self._cleanup()

    def _on_closing(self) -> None:
        """Handle application closing."""
        self._cleanup()
        self.root.destroy()

    def _cleanup(self) -> None:
        """Clean up resources."""
        try:
            self.input_file_manager.cleanup_current()
            self.logger.info("Application cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def main() -> None:
    """Main entry point for the application."""
    logger = get_logger("main")

    try:
        logger.info("Starting Tilapia Freshness Evaluator")
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        log_error("Application startup failed", e, "main")
        import sys

        sys.exit(1)
