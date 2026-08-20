
import numpy as np

from src.vision.ppe_detector import PPEDetector


class TestPPEDetector:
    def test_returns_empty_when_no_model(self):
        detector = PPEDetector()
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        results = detector.detect(frame)
        assert results == []

    def test_model_name(self):
        detector = PPEDetector()
        assert detector.model_name == "yolo11n-ppe"
        assert detector.result_type == "ppe"

    def test_check_ppe_for_person_empty(self):
        detector = PPEDetector()
        detected = detector._check_ppe_for_person([0, 0, 100, 100], [])
        assert detected == []

    def test_check_ppe_for_person_with_match(self):
        detector = PPEDetector()
        ppe_boxes = [
            {"class_id": 0, "confidence": 0.9, "bbox": [10, 10, 50, 50]},
            {"class_id": 2, "confidence": 0.8, "bbox": [20, 20, 40, 40]},
        ]
        detected = detector._check_ppe_for_person([0, 0, 100, 100], ppe_boxes)
        assert "helmet" in detected
        assert "vest" in detected

    def test_class_id_to_name(self):
        detector = PPEDetector()
        assert detector._class_id_to_name(0) == "helmet"
        assert detector._class_id_to_name(1) == "no-helmet"
        assert detector._class_id_to_name(2) == "vest"
        assert detector._class_id_to_name(99) is None
