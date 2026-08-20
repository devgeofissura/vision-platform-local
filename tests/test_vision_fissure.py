import numpy as np

from src.vision.fissure_detector import FissureDetector


class TestFissureDetectorClassical:
    def test_detect_returns_list(self):
        detector = FissureDetector()
        frame = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        results = detector.detect(frame)
        assert isinstance(results, list)

    def test_classify_severity_low(self):
        detector = FissureDetector()
        assert detector._classify_severity(1) == "low"
        assert detector._classify_severity(0) == "low"

    def test_classify_severity_medium(self):
        detector = FissureDetector()
        assert detector._classify_severity(3) == "medium"

    def test_classify_severity_high(self):
        detector = FissureDetector()
        assert detector._classify_severity(10) == "high"

    def test_classical_detect_on_blank_frame(self):
        detector = FissureDetector()
        frame = np.ones((200, 200, 3), dtype=np.uint8) * 128
        results = detector._detect_classical(frame)
        assert isinstance(results, list)

    def test_classical_detect_on_frame_with_line(self):
        detector = FissureDetector()
        frame = np.ones((200, 200, 3), dtype=np.uint8) * 200
        cv2 = __import__("cv2")
        cv2.line(frame, (10, 50), (150, 50), (10, 10, 10), 2)
        results = detector._detect_classical(frame)
        assert isinstance(results, list)

    def test_model_name(self):
        detector = FissureDetector()
        assert detector.model_name == "yolo11n-seg"
        assert detector.result_type == "fissure"

    def test_min_length_config(self):
        detector = FissureDetector(config={"min_length_px": 100})
        assert detector.config["min_length_px"] == 100
