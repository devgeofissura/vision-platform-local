import logging

import cv2
import numpy as np

from src.vision.base import BaseDetector, ProcessingResult

logger = logging.getLogger(__name__)

DEFECT_CLASSES = {
    0: "hole",
    1: "stain",
    2: "line",
    3: "knot",
}

DEFECT_SEVERITY_THRESHOLDS = {
    "low": 100,
    "medium": 500,
}


class FabricDefectDetector(BaseDetector):
    model_name = "yolov8m-seg"
    model_version = "2026.08.1"
    result_type = "fabric_defect"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        self._model = None

    def _load_model(self) -> None:
        try:
            from ultralytics import YOLO

            model_path = self.config.get("model_path", "yolov8m-seg.pt")
            self._model = YOLO(model_path)
            logger.info("FabricDefectDetector loaded: %s", model_path)
        except ImportError:
            logger.warning("ultralytics not installed, FabricDefectDetector using classical fallback")
            self._model = None

    def detect(self, frame: np.ndarray) -> list[ProcessingResult]:
        self.load()
        if self._model is not None:
            return self._detect_yolo(frame)
        return self._detect_classical(frame)

    def _detect_yolo(self, frame: np.ndarray) -> list[ProcessingResult]:
        results = self._model(frame, verbose=False, conf=self.config.get("conf", 0.3))
        detections = []
        for r in results:
            if r.boxes is None:
                continue
            for i, box in enumerate(r.boxes):
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                w, h = float(x2 - x1), float(y2 - y1)
                area = w * h
                defect_type = DEFECT_CLASSES.get(cls_id, f"defect_{cls_id}")
                severity = self._classify_severity(area)
                mask_path = None
                if r.masks is not None and i < len(r.masks):
                    mask_data = r.masks[i].data[0].cpu().numpy()
                    mask_resized = cv2.resize(mask_data, (int(w), int(h)))
                    binary_mask = (mask_resized > 0.5).astype(np.uint8) * 255
                    mask_area = int(np.sum(binary_mask > 0))
                    severity = self._classify_severity(float(mask_area))
                detections.append(ProcessingResult(
                    result_type="fabric_defect",
                    model_name=self.model_name,
                    model_version=self.model_version,
                    confidence=conf,
                    result_data={
                        "defect_type": defect_type,
                        "severity": severity,
                        "bbox": [float(x1), float(y1), w, h],
                        "area_px": round(area, 1),
                        "mask_path": mask_path,
                    },
                ))
        return detections

    def _detect_classical(self, frame: np.ndarray) -> list[ProcessingResult]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 50:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            aspect = w / float(h) if h > 0 else 1.0
            if aspect > 8:
                defect_type = "line"
            elif area > 2000:
                defect_type = "hole"
            else:
                defect_type = "stain"
            severity = self._classify_severity(float(area))
            detections.append(ProcessingResult(
                result_type="fabric_defect",
                model_name="classical-cv",
                model_version="1.0.0",
                confidence=min(area / 5000, 1.0),
                result_data={
                    "defect_type": defect_type,
                    "severity": severity,
                    "bbox": [float(x), float(y), float(w), float(h)],
                    "area_px": round(float(area), 1),
                    "mask_path": None,
                },
            ))
        return detections

    def _classify_severity(self, area_px: float) -> str:
        if area_px < DEFECT_SEVERITY_THRESHOLDS["low"]:
            return "low"
        if area_px < DEFECT_SEVERITY_THRESHOLDS["medium"]:
            return "medium"
        return "high"
