"""YOLOv3 object detection for tilapia gill identification."""

from typing import List, Optional, Tuple

import cv2
import numpy as np

from ..config import config
from ..enums import YOLOv3
from ..exceptions import DetectionError, FileNotFoundError, ModelLoadError


class YOLODetector:
    """YOLOv3 detector for tilapia gill identification with lazy loading."""

    def __init__(
        self, config_path: Optional[str] = None, weights_path: Optional[str] = None, names_path: Optional[str] = None
    ) -> None:
        """Initialize YOLO detector with lazy loading.

        Args:
            config_path: Path to YOLO config file (optional, uses config default)
            weights_path: Path to YOLO weights file (optional, uses config default)
            names_path: Path to class names file (optional, uses config default)
        """
        self.config_path = config_path or config.model.config_path
        self.weights_path = weights_path or config.model.weights_path
        self.names_path = names_path or config.model.names_path

        self.net: Optional[cv2.dnn.Net] = None
        self.classes: List[str] = []
        self.output_layers: List[str] = []
        self._model_loaded = False

    def _ensure_model_loaded(self) -> None:
        """Ensure model is loaded (lazy loading)."""
        if not self._model_loaded:
            self._load_model()
            self._model_loaded = True

    def _load_model(self) -> None:
        """Load YOLO model and configuration."""
        try:
            import os

            if not os.path.exists(self.config_path):
                raise FileNotFoundError("YOLO config file not found", self.config_path)
            if not os.path.exists(self.weights_path):
                raise FileNotFoundError(
                    "YOLO weights file not found", self.weights_path
                )
            if not os.path.exists(self.names_path):
                raise FileNotFoundError("Class names file not found", self.names_path)

            self.net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

            with open(self.names_path, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]

            layers = self.net.getLayerNames()
            unconnected_out_layers = self.net.getUnconnectedOutLayers()
            if len(unconnected_out_layers.shape) == 1:
                self.output_layers = [layers[i - 1] for i in unconnected_out_layers]
            else:
                self.output_layers = [layers[i[0] - 1] for i in unconnected_out_layers]

        except Exception as e:
            if isinstance(e, (FileNotFoundError,)):
                raise e
            raise ModelLoadError("Failed to load YOLO model", str(e))

    def detect(
        self, image: np.ndarray, conf_thresh: Optional[float] = None, nms_thresh: Optional[float] = None
    ) -> Tuple[List, List, List, List]:
        """Detect objects in image.

        Args:
            image: Input image
            conf_thresh: Confidence threshold (optional, uses config default)
            nms_thresh: NMS threshold (optional, uses config default)

        Returns:
            Tuple of (bounding_boxes, confidences, class_ids, indices)
        """

        self._ensure_model_loaded()
        assert self.net is not None, "Model should be loaded"

        if conf_thresh is None:
            conf_thresh = config.model.confidence_threshold
        if nms_thresh is None:
            nms_thresh = config.model.nms_threshold

        try:
            height, width = image.shape[:2]

            input_size = config.model.input_size
            blob = cv2.dnn.blobFromImage(
                image, YOLOv3.SCALE_FACTOR, input_size, swapRB=True, crop=False
            )
            self.net.setInput(blob)
            layer_outputs = self.net.forward(self.output_layers)

            class_ids, confidences, b_boxes = [], [], []
            for output in layer_outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    if confidence > conf_thresh:
                        center_x, center_y, w, h = (
                            detection[0:4] * np.array([width, height, width, height])
                        ).astype("int")

                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        b_boxes.append([x, y, int(w), int(h)])
                        confidences.append(float(confidence))
                        class_ids.append(int(class_id))

            if b_boxes:
                nms_result = cv2.dnn.NMSBoxes(
                    b_boxes, confidences, conf_thresh, nms_thresh
                )
                if len(nms_result) > 0:
                    indices = np.array(nms_result).flatten().tolist()
                else:
                    indices = []
            else:
                indices = []

            return b_boxes, confidences, class_ids, indices

        except Exception as e:
            raise DetectionError("Failed to detect objects in image", str(e))

    def draw_detections(
        self, image: np.ndarray, b_boxes: List, class_ids: List, indices: List
    ) -> np.ndarray:
        """Draw detection results on image.

        Args:
            image: Input image
            b_boxes: Bounding boxes
            class_ids: Class IDs
            indices: Valid detection indices

        Returns:
            Image with drawn detections
        """

        self._ensure_model_loaded()

        colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

        for index in indices:
            x, y, w, h = b_boxes[index]
            class_id = class_ids[index]
            color = colors[class_id] if class_id < len(colors) else colors[0]

            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                image,
                self.classes[class_id],
                (x + 5, y + 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                1,
                color,
                2,
            )

        return image
