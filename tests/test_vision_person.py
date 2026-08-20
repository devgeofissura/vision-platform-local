import numpy as np

from src.vision.person_detector import PersonDetector


class TestPersonDetector:
    def test_returns_empty_when_no_model(self):
        detector = PersonDetector()
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        results = detector.detect(frame)
        assert results == []

    def test_model_name(self):
        detector = PersonDetector()
        assert detector.model_name == "yolo11n"
        assert detector.result_type == "person"

    def test_import_error_graceful(self):
        detector = PersonDetector()
        detector._model = None
        detector._loaded = True
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        results = detector.detect(frame)
        assert results == []
