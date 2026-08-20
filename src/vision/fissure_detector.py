import logging

import cv2
import numpy as np

from src.vision.base import BaseDetector, ProcessingResult

logger = logging.getLogger(__name__)

CRACK_SEVERITY_THRESHOLDS = {
    "low": 2,
    "medium": 5,
}


class FissureDetector(BaseDetector):
    model_name = "yolo11n-seg"
    model_version = "2026.08.1"
    result_type = "fissure"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        self._model = None

    def _load_model(self) -> None:
        try:
            from ultralytics import YOLO

            model_path = self.config.get("model_path", "yolo11n-seg.pt")
            self._model = YOLO(model_path)
            logger.info("FissureDetector loaded: %s", model_path)
        except ImportError:
            logger.warning("ultralytics not installed, FissureDetector using classical fallback")
            self._model = None

    def detect(self, frame: np.ndarray) -> list[ProcessingResult]:
        self.load()
        if self._model is not None:
            return self._detect_yolo(frame)
        return self._detect_classical(frame)

    def _detect_yolo(self, frame: np.ndarray) -> list[ProcessingResult]:
        results = self._model(frame, verbose=False, conf=self.config.get("conf", 0.25))
        detections = []
        for r in results:
            if r.boxes is None:
                continue
            for i, box in enumerate(r.boxes):
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                w_px = float(x2 - x1)
                h_px = float(y2 - y1)
                severity = self._classify_severity(max(w_px, h_px))
                detections.append(ProcessingResult(
                    result_type="fissure",
                    model_name=self.model_name,
                    model_version=self.model_version,
                    confidence=conf,
                    result_data={
                        "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                        "width_px": round(w_px, 1),
                        "length_px": round(h_px, 1),
                        "area_px": round(w_px * h_px, 1),
                        "severity": severity,
                        "mask_path": None,
                    },
                ))
        return detections

    def _detect_classical(self, frame: np.ndarray) -> list[ProcessingResult]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        min_length = self.config.get("min_length_px", 30)
        for cnt in contours:
            length = cv2.arcLength(cnt, False)
            if length < min_length:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            severity = self._classify_severity(max(w, h))
            detections.append(ProcessingResult(
                result_type="fissure",
                model_name="classical-cv",
                model_version="1.0.0",
                confidence=min(length / 200, 1.0),
                result_data={
                    "bbox": [float(x), float(y), float(w), float(h)],
                    "width_px": round(float(w), 1),
                    "length_px": round(float(h), 1),
                    "area_px": round(float(area), 1),
                    "severity": severity,
                    "contour_length": round(float(length), 1),
                },
            ))
        return detections

    def _classify_severity(self, max_dim_px: float) -> str:
        if max_dim_px < CRACK_SEVERITY_THRESHOLDS["low"]:
            return "low"
        if max_dim_px < CRACK_SEVERITY_THRESHOLDS["medium"]:
            return "medium"
        return "high"
