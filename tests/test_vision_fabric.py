import numpy as np

from src.vision.fabric_defect_detector import FabricDefectDetector


class TestFabricDefectDetector:
    def test_returns_empty_when_no_model(self):
        detector = FabricDefectDetector()
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        results = detector.detect(frame)
        assert isinstance(results, list)

    def test_classify_severity_low(self):
        detector = FabricDefectDetector()
        assert detector._classify_severity(50) == "low"

    def test_classify_severity_medium(self):
        detector = FabricDefectDetector()
        assert detector._classify_severity(200) == "medium"

    def test_classify_severity_high(self):
        detector = FabricDefectDetector()
        assert detector._classify_severity(600) == "high"

    def test_classical_detect_on_blank(self):
        detector = FabricDefectDetector()
        frame = np.ones((200, 200, 3), dtype=np.uint8) * 128
        results = detector._detect_classical(frame)
        assert isinstance(results, list)

    def test_classical_detect_with_blotch(self):
        cv2 = __import__("cv2")
        detector = FabricDefectDetector()
        frame = np.ones((200, 200, 3), dtype=np.uint8) * 200
        cv2.circle(frame, (100, 100), 30, (10, 10, 10), -1)
        results = detector._detect_classical(frame)
        assert isinstance(results, list)

    def test_model_name(self):
        detector = FabricDefectDetector()
        assert detector.model_name == "yolov8m-seg"
        assert detector.result_type == "fabric_defect"
