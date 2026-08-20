import logging

import numpy as np

from src.vision.base import BaseDetector, ProcessingResult

logger = logging.getLogger(__name__)


class PersonDetector(BaseDetector):
    model_name = "yolo11n"
    model_version = "2026.08.1"
    result_type = "person"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        self._model = None

    def _load_model(self) -> None:
        try:
            from ultralytics import YOLO

            model_path = self.config.get("model_path", "yolo11n.pt")
            self._model = YOLO(model_path)
            logger.info("PersonDetector loaded: %s", model_path)
        except ImportError:
            logger.warning("ultralytics not installed, PersonDetector disabled")
            self._model = None

    def detect(self, frame: np.ndarray) -> list[ProcessingResult]:
        self.load()
        if self._model is None:
            return []

        results = self._model(frame, verbose=False, conf=self.config.get("conf", 0.4), classes=[0])
        detections = []
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                detections.append(ProcessingResult(
                    result_type="person",
                    model_name=self.model_name,
                    model_version=self.model_version,
                    confidence=conf,
                    result_data={
                        "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                        "person_id": None,
                        "reid_embedding": None,
                    },
                ))
        return detections

    def detect_with_tracking(self, frame: np.ndarray) -> list[ProcessingResult]:
        self.load()
        if self._model is None:
            return []

        results = self._model.track(
            frame,
            verbose=False,
            conf=self.config.get("conf", 0.4),
            classes=[0],
            tracker="bytetrack.yaml",
            persist=True,
        )
        detections = []
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                track_id = int(box.id[0]) if box.id is not None else None
                detections.append(ProcessingResult(
                    result_type="person",
                    model_name=self.model_name,
                    model_version=self.model_version,
                    confidence=conf,
                    result_data={
                        "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                        "person_id": f"track_{track_id}" if track_id is not None else None,
                        "track_id": track_id,
                        "reid_embedding": None,
                    },
                ))
        return detections
