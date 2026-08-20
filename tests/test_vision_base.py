
import numpy as np

from src.vision.base import BaseDetector, ProcessingResult


class TestProcessingResult:
    def test_create_result(self):
        r = ProcessingResult(
            result_type="fissure",
            model_name="test-model",
            model_version="1.0.0",
            confidence=0.95,
            result_data={"bbox": [10, 20, 30, 40]},
        )
        assert r.result_type == "fissure"
        assert r.confidence == 0.95
        assert r.inference_ms == 0

    def test_to_dict(self):
        r = ProcessingResult(
            result_type="plate",
            model_name="alpr",
            model_version="1.0.0",
            confidence=0.8,
            result_data={"plate_hash": "abc123"},
            inference_ms=42,
            image_width=1920,
            image_height=1080,
        )
        d = r.to_dict()
        assert d["result_type"] == "plate"
        assert d["inference_ms"] == 42
        assert d["image_width"] == 1920
        assert d["result_data"]["plate_hash"] == "abc123"

    def test_to_dict_default_values(self):
        r = ProcessingResult(
            result_type="count",
            model_name="yolo",
            model_version="1.0.0",
            confidence=1.0,
            result_data={"count": 5},
        )
        d = r.to_dict()
        assert d["inference_ms"] == 0
        assert d["image_width"] == 0


class ConcreteDetector(BaseDetector):
    model_name = "test-detector"
    model_version = "0.0.1"
    result_type = "test"

    def detect(self, frame):
        return [ProcessingResult(
            result_type="test",
            model_name=self.model_name,
            model_version=self.model_version,
            confidence=0.5,
            result_data={"test": True},
        )]


class TestBaseDetector:
    def test_time_detect(self):
        detector = ConcreteDetector()
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        results, elapsed_ms = detector._time_detect(frame)
        assert len(results) == 1
        assert elapsed_ms >= 0
        assert results[0].inference_ms == elapsed_ms
        assert results[0].image_width == 100
        assert results[0].image_height == 100

    def test_contains_point_inside(self):
        detector = ConcreteDetector()
        polygon = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
        assert detector._contains_point(polygon, [0.5, 0.5]) is True

    def test_contains_point_outside(self):
        detector = ConcreteDetector()
        polygon = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
        assert detector._contains_point(polygon, [1.5, 0.5]) is False

    def test_contains_point_on_edge(self):
        detector = ConcreteDetector()
        polygon = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
        result = detector._contains_point(polygon, [0.0, 0.5])
        assert isinstance(result, bool)

    def test_bbox_center(self):
        detector = ConcreteDetector()
        center = detector._bbox_center([10, 20, 30, 40])
        assert center == [25.0, 40.0]

    def test_compute_iou_no_overlap(self):
        detector = ConcreteDetector()
        iou = detector._compute_iou([0, 0, 10, 10], [20, 20, 10, 10])
        assert iou == 0.0

    def test_compute_iou_full_overlap(self):
        detector = ConcreteDetector()
        iou = detector._compute_iou([0, 0, 10, 10], [0, 0, 10, 10])
        assert iou == 1.0

    def test_compute_iou_partial_overlap(self):
        detector = ConcreteDetector()
        iou = detector._compute_iou([0, 0, 10, 10], [5, 5, 10, 10])
        assert 0.0 < iou < 1.0

    def test_load_sets_loaded_flag(self):
        detector = ConcreteDetector()
        assert detector._loaded is False
        detector.load()
        assert detector._loaded is True

    def test_load_idempotent(self):
        detector = ConcreteDetector()
        detector.load()
        detector.load()
        assert detector._loaded is True
