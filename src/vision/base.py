import logging
import time
from abc import ABC, abstractmethod

import numpy as np

logger = logging.getLogger(__name__)


class ProcessingResult:
    def __init__(
        self,
        result_type: str,
        model_name: str,
        model_version: str,
        confidence: float,
        result_data: dict,
        inference_ms: int = 0,
        image_width: int = 0,
        image_height: int = 0,
    ):
        self.result_type = result_type
        self.model_name = model_name
        self.model_version = model_version
        self.confidence = confidence
        self.result_data = result_data
        self.inference_ms = inference_ms
        self.image_width = image_width
        self.image_height = image_height

    def to_dict(self) -> dict:
        return {
            "result_type": self.result_type,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "confidence": self.confidence,
            "result_data": self.result_data,
            "inference_ms": self.inference_ms,
            "image_width": self.image_width,
            "image_height": self.image_height,
        }


class BaseDetector(ABC):
    model_name: str = "base"
    model_version: str = "0.0.1"
    result_type: str = "unknown"

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self._loaded = False

    @abstractmethod
    def detect(self, frame: np.ndarray) -> list[ProcessingResult]:
        pass

    def _time_detect(self, frame: np.ndarray) -> tuple[list[ProcessingResult], int]:
        start = time.perf_counter()
        results = self.detect(frame)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        for r in results:
            r.inference_ms = elapsed_ms
            r.image_width = frame.shape[1]
            r.image_height = frame.shape[0]
        return results, elapsed_ms

    def load(self) -> None:
        if not self._loaded:
            self._load_model()
            self._loaded = True

    def _load_model(self) -> None:
        pass

    def _contains_point(self, polygon: list[list[float]], point: list[float]) -> bool:
        x, y = point
        n = len(polygon)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside

    def _bbox_center(self, bbox: list[float]) -> list[float]:
        x, y, w, h = bbox
        return [x + w / 2, y + h / 2]

    def _compute_iou(self, box_a: list[float], box_b: list[float]) -> float:
        ax, ay, aw, ah = box_a
        bx, by, bw, bh = box_b
        x1 = max(ax, bx)
        y1 = max(ay, by)
        x2 = min(ax + aw, bx + bw)
        y2 = min(ay + ah, by + bh)
        if x2 <= x1 or y2 <= y1:
            return 0.0
        intersection = (x2 - x1) * (y2 - y1)
        union = aw * ah + bw * bh - intersection
        return intersection / union if union > 0 else 0.0
