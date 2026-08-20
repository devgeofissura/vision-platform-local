import logging

import numpy as np

from src.vision.base import BaseDetector, ProcessingResult
from src.vision.person_detector import PersonDetector

logger = logging.getLogger(__name__)

DEFAULT_REQUIRED_PPE = ["helmet", "vest"]


class PPEDetector(BaseDetector):
    model_name = "yolo11n-ppe"
    model_version = "2026.08.1"
    result_type = "ppe"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        self._model = None
        self._person_detector = PersonDetector(config)
        self._ppe_classes = {
            "helmet": 0,
            "no-helmet": 1,
            "vest": 2,
            "no-vest": 3,
            "gloves": 4,
            "glasses": 5,
            "boots": 6,
        }

    def _load_model(self) -> None:
        try:
            from ultralytics import YOLO

            model_path = self.config.get("model_path", "yolo11n.pt")
            self._model = YOLO(model_path)
            logger.info("PPEDetector loaded: %s", model_path)
        except ImportError:
            logger.warning("ultralytics not installed, PPEDetector disabled")
            self._model = None

    def detect(self, frame: np.ndarray) -> list[ProcessingResult]:
        self.load()
        if self._model is None:
            return []

        person_results = self._person_detector.detect(frame)
        if not person_results:
            return []

        ppe_results = self._model(frame, verbose=False, conf=self.config.get("conf", 0.3))
        ppe_boxes = []
        for r in ppe_results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                ppe_boxes.append({
                    "class_id": cls_id,
                    "confidence": conf,
                    "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                })

        detections = []
        for person in person_results:
            person_bbox = person.result_data["bbox"]
            person_id = person.result_data.get("person_id") or "unknown"
            required_ppe = self.config.get("required_ppe", DEFAULT_REQUIRED_PPE)
            detected_ppe = self._check_ppe_for_person(person_bbox, ppe_boxes)
            missing = [p for p in required_ppe if p not in detected_ppe]
            compliant = len(missing) == 0

            detections.append(ProcessingResult(
                result_type="ppe",
                model_name=self.model_name,
                model_version=self.model_version,
                confidence=person.confidence,
                result_data={
                    "person_id": person_id,
                    "required": required_ppe,
                    "detected": detected_ppe,
                    "missing": missing,
                    "compliant": compliant,
                    "person_bbox": person_bbox,
                },
            ))
        return detections

    def _check_ppe_for_person(self, person_bbox: list[float], ppe_boxes: list[dict]) -> list[str]:
        detected = []
        for ppe in ppe_boxes:
            iou = self._compute_iou(person_bbox, ppe["bbox"])
            if iou > 0.1:
                class_id = ppe["class_id"]
                ppe_name = self._class_id_to_name(class_id)
                if ppe_name and ppe_name not in detected:
                    detected.append(ppe_name)
        return detected

    def _class_id_to_name(self, class_id: int) -> str | None:
        for name, cid in self._ppe_classes.items():
            if cid == class_id:
                return name
        return None
