import hashlib
import hmac
import logging

import cv2
import numpy as np

from src.vision.base import BaseDetector, ProcessingResult

logger = logging.getLogger(__name__)


class PlateDetector(BaseDetector):
    model_name = "fast-alpr"
    model_version = "2026.08.1"
    result_type = "plate"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        self._alpr = None
        self._plate_key = (self.config.get("hmac_key", "geofissura-plate-key")).encode()

    def _load_model(self) -> None:
        try:
            from fast_alpr import ALPR

            self._alpr = ALPR(
                detector_backend="yolov9-c",
                ocr_backend="fast-plate-ocr",
                device=self.config.get("device", "cpu"),
            )
            logger.info("PlateDetector loaded (fast-alpr)")
        except ImportError:
            logger.warning("fast-alpr not installed, PlateDetector using OpenCV fallback")
            self._alpr = None

    def detect(self, frame: np.ndarray) -> list[ProcessingResult]:
        self.load()
        if self._alpr is not None:
            return self._detect_alpr(frame)
        return self._detect_classical(frame)

    def _detect_alpr(self, frame: np.ndarray) -> list[ProcessingResult]:
        if self._alpr is None:
            return []
        results = self._alpr.predict(frame, conf_threshold=self.config.get("conf", 0.5))
        detections = []
        for plate in results:
            if not plate or not hasattr(plate, "text"):
                continue
            plate_text = plate.text if plate.text else ""
            plate_hash = hmac.new(self._plate_key, plate_text.encode(), hashlib.sha256).hexdigest()
            vehicle_bbox = None
            plate_bbox = None
            if hasattr(plate, "vehicle_bbox") and plate.vehicle_bbox is not None:
                vb = plate.vehicle_bbox
                vehicle_bbox = [float(vb.x1), float(vb.y1), float(vb.x2 - vb.x1), float(vb.y2 - vb.y1)]
            if hasattr(plate, "plate_bbox") and plate.plate_bbox is not None:
                pb = plate.plate_bbox
                plate_bbox = [float(pb.x1), float(pb.y1), float(pb.x2 - pb.x1), float(pb.y2 - pb.y1)]
            detections.append(ProcessingResult(
                result_type="plate",
                model_name=self.model_name,
                model_version=self.model_version,
                confidence=float(getattr(plate, "confidence", 0.0)),
                result_data={
                    "plate_hash": plate_hash,
                    "vehicle_bbox": vehicle_bbox,
                    "plate_bbox": plate_bbox,
                },
            ))
        return detections

    def _detect_classical(self, frame: np.ndarray) -> list[ProcessingResult]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(blurred, 30, 200)
        contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in sorted(contours, key=cv2.contourArea, reverse=True)[:10]:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)
                if 2.0 < aspect_ratio < 5.5 and w > 80 and h > 20:
                    plate_hash = hmac.new(
                        self._plate_key,
                        f"detected_{x}_{y}_{w}_{h}".encode(),
                        hashlib.sha256,
                    ).hexdigest()
                    detections.append(ProcessingResult(
                        result_type="plate",
                        model_name="classical-cv",
                        model_version="1.0.0",
                        confidence=0.5,
                        result_data={
                            "plate_hash": plate_hash,
                            "vehicle_bbox": None,
                            "plate_bbox": [float(x), float(y), float(w), float(h)],
                        },
                    ))
                    break
        return detections
