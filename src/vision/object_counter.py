import logging

import numpy as np

from src.vision.base import BaseDetector, ProcessingResult

logger = logging.getLogger(__name__)


class ObjectCounter(BaseDetector):
    model_name = "yolo11n"
    model_version = "2026.08.1"
    result_type = "count"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        self._model = None

    def _load_model(self) -> None:
        try:
            from ultralytics import YOLO

            model_path = self.config.get("model_path", "yolo11n.pt")
            self._model = YOLO(model_path)
            logger.info("ObjectCounter loaded: %s", model_path)
        except ImportError:
            logger.warning("ultralytics not installed, ObjectCounter disabled")
            self._model = None

    def detect(self, frame: np.ndarray) -> list[ProcessingResult]:
        self.load()
        if self._model is None:
            return []

        results = self._model.track(
            frame,
            verbose=False,
            conf=self.config.get("conf", 0.4),
            tracker="bytetrack.yaml",
            persist=True,
        )

        class_counts: dict[str, int] = {}
        all_bboxes: dict[str, list] = {}

        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = self._model.names.get(cls_id, f"class_{cls_id}")
                class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
                if cls_name not in all_bboxes:
                    all_bboxes[cls_name] = []
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                all_bboxes[cls_name].append([float(x1), float(y1), float(x2 - x1), float(y2 - y1)])

        detections = []
        for cls_name, count in class_counts.items():
            detections.append(ProcessingResult(
                result_type="count",
                model_name=self.model_name,
                model_version=self.model_version,
                confidence=1.0,
                result_data={
                    "class": cls_name,
                    "count": count,
                    "zone": self.config.get("zone_name", "default"),
                    "bboxes": all_bboxes.get(cls_name, []),
                },
            ))

        if self.config.get("zones"):
            for zone in self.config["zones"]:
                zone_counts = self._count_in_zone(frame, zone)
                if zone_counts:
                    detections.append(ProcessingResult(
                        result_type="count",
                        model_name=self.model_name,
                        model_version=self.model_version,
                        confidence=1.0,
                        result_data={
                            "class": "all",
                            "count": sum(zone_counts.values()),
                            "zone": zone.get("name", "unnamed"),
                            "classwise": zone_counts,
                        },
                    ))
        return detections

    def _count_in_zone(self, frame: np.ndarray, zone: dict) -> dict[str, int]:
        polygon = zone.get("polygon_vertices", [])
        if not polygon:
            return {}

        results = self._model.track(
            frame,
            verbose=False,
            conf=self.config.get("conf", 0.4),
            tracker="bytetrack.yaml",
            persist=True,
        )

        zone_counts: dict[str, int] = {}
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = self._model.names.get(cls_id, f"class_{cls_id}")
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                center = [float((x1 + x2) / 2), float((y1 + y2) / 2)]
                if self._contains_point(polygon, center):
                    zone_counts[cls_name] = zone_counts.get(cls_name, 0) + 1
        return zone_counts
