import numpy as np

from src.vision.plate_detector import PlateDetector


class TestPlateDetector:
    def test_classical_detect_on_blank(self):
        detector = PlateDetector()
        frame = np.ones((200, 200, 3), dtype=np.uint8) * 200
        results = detector._detect_classical(frame)
        assert isinstance(results, list)

    def test_classical_detect_with_rect(self):
        detector = PlateDetector()
        cv2 = __import__("cv2")
        frame = np.ones((300, 400, 3), dtype=np.uint8) * 200
        cv2.rectangle(frame, (50, 100), (250, 140), (0, 0, 0), 2)
        results = detector._detect_classical(frame)
        assert isinstance(results, list)

    def test_model_name(self):
        detector = PlateDetector()
        assert detector.model_name == "fast-alpr"
        assert detector.result_type == "plate"

    def test_hmac_key_configurable(self):
        d1 = PlateDetector(config={"hmac_key": "key1"})
        d2 = PlateDetector(config={"hmac_key": "key2"})
        assert d1._plate_key != d2._plate_key

    def test_returns_empty_when_no_model(self):
        detector = PlateDetector()
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        results = detector._detect_alpr(frame)
        assert results == []
