import logging

import numpy as np

from src.vision.base import BaseDetector, ProcessingResult

logger = logging.getLogger(__name__)

_COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv",
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush",
]


class PersonDetector(BaseDetector):
    model_name = "yolo11n"
    model_version = "2026.08.1"
    result_type = "person"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        self._model = None
        self._onnx = None

    def _load_model(self) -> None:
        try:
            from ultralytics import YOLO

            model_path = self.config.get("model_path", "yolo11n.pt")
            self._model = YOLO(model_path)
            logger.info("PersonDetector loaded: %s", model_path)
            return
        except ImportError:
            pass
        from src.vision.onnx_backend import OnnxYoloDetector

        onnx_path = self.config.get(
            "onnx_model_path", "models/yolo11n.onnx"
        )
        detector = OnnxYoloDetector(
            onnx_path,
            conf=self.config.get("conf", 0.4),
            class_names=_COCO_CLASSES,
        )
        if detector.is_available:
            self._onnx = detector
            logger.info("PersonDetector loaded (ONNX): %s", onnx_path)
        else:
            logger.warning(
                "PersonDetector sem ultralytics e sem %s; desabilitado", onnx_path
            )

    def detect(self, frame: np.ndarray) -> list[ProcessingResult]:
        self.load()
        if self._model is not None:
            return self._detect_ultralytics(frame)
        if self._onnx is not None:
            return self._detect_onnx(frame)
        return []

    def _detect_onnx(self, frame: np.ndarray) -> list[ProcessingResult]:
        detections = []
        for det in self._onnx.detect(frame, class_filter={0}):
            detections.append(ProcessingResult(
                result_type="person",
                model_name=self.model_name,
                model_version=self.model_version,
                confidence=det["confidence"],
                result_data={
                    "bbox": det["bbox"],
                    "person_id": None,
                    "reid_embedding": None,
                },
            ))
        return detections

    def _detect_ultralytics(self, frame: np.ndarray) -> list[ProcessingResult]:
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
