import numpy as np
import pytest

from src.vision.onnx_backend import OnnxYoloDetector, _decode_output, _letterbox, _nms


class TestLetterbox:
    def test_square_input_no_padding(self):
        img = np.zeros((640, 640, 3), dtype=np.uint8)
        out, ratio, pad_x, pad_y = _letterbox(img, 640)
        assert out.shape == (640, 640, 3)
        assert ratio == 1.0
        assert pad_x == 0
        assert pad_y == 0

    def test_wide_image_pads_vertically(self):
        img = np.zeros((480, 1920, 3), dtype=np.uint8)
        out, ratio, pad_x, pad_y = _letterbox(img, 640)
        assert out.shape == (640, 640, 3)
        assert ratio == pytest.approx(640 / 1920)
        assert pad_x == 0
        assert pad_y > 0

    def test_tall_image_pads_horizontally(self):
        img = np.zeros((1920, 480, 3), dtype=np.uint8)
        out, ratio, pad_x, pad_y = _letterbox(img, 640)
        assert out.shape == (640, 640, 3)
        assert ratio == pytest.approx(640 / 1920)
        assert pad_x > 0
        assert pad_y == 0

    def test_pad_value_is_114(self):
        img = np.zeros((50, 100, 3), dtype=np.uint8)
        out, _, _, pad_y = _letterbox(img, 320)
        assert pad_y == 80
        top_strip = out[:pad_y, :, :]
        bottom_strip = out[pad_y + 160 :, :, :]
        for strip in (top_strip, bottom_strip):
            assert int(strip.min()) == 114 and int(strip.max()) == 114


class TestDecodeOutput:
    def test_transposes_cx_n_layout(self):
        raw = np.random.rand(1, 84, 8400).astype(np.float32)
        decoded = _decode_output(raw)
        assert decoded.shape == (8400, 84)

    def test_keeps_already_decoded_layout(self):
        raw = np.random.rand(1, 8400, 84).astype(np.float32)
        decoded = _decode_output(raw)
        assert decoded.shape == (8400, 84)

    def test_accepts_2d_input(self):
        raw = np.random.rand(100, 84).astype(np.float32)
        assert _decode_output(raw).shape == (100, 84)


class _FakeNmsPreds:
    @staticmethod
    def make(cx, cy, w, h, class_id, score, n_classes=80):
        row = [cx, cy, w, h] + [0.0] * n_classes
        row[4 + class_id] = score
        return row


class TestNms:
    def test_filters_low_confidence(self):
        preds = np.array([
            _FakeNmsPreds.make(100, 100, 50, 50, 0, 0.9),
            _FakeNmsPreds.make(300, 300, 50, 50, 5, 0.1),
        ], dtype=np.float32)
        results = _nms(preds, conf_threshold=0.25, iou_threshold=0.45, class_filter=None)
        assert len(results) == 1
        assert results[0][4] == pytest.approx(0.9)

    def test_class_filter(self):
        preds = np.array([
            _FakeNmsPreds.make(100, 100, 50, 50, 0, 0.9),
            _FakeNmsPreds.make(300, 300, 50, 50, 2, 0.9),
        ], dtype=np.float32)
        results = _nms(preds, 0.25, 0.45, class_filter={0})
        assert len(results) == 1 and results[0][5] == 0

    def test_suppresses_overlap(self):
        preds = np.array([
            _FakeNmsPreds.make(100, 100, 60, 60, 0, 0.9),
            _FakeNmsPreds.make(102, 101, 60, 60, 0, 0.8),
            _FakeNmsPreds.make(400, 400, 60, 60, 0, 0.7),
        ], dtype=np.float32)
        results = _nms(preds, 0.25, 0.45, class_filter=None)
        assert len(results) == 2

    def test_empty_predictions(self):
        preds = np.zeros((0, 84), dtype=np.float32)
        assert _nms(preds, 0.25, 0.45, None) == []


class TestOnnxYoloDetector:
    def test_missing_model_not_available(self, tmp_path):
        det = OnnxYoloDetector(str(tmp_path / "nao_existe.onnx"))
        assert det.is_available is False
        frame = np.zeros((64, 64, 3), dtype=np.uint8)
        assert det.detect(frame) == []

    def test_class_name_fallback(self):
        det = OnnxYoloDetector("models/yolo11n.onnx", class_names=["person"])
        assert det.is_available is True
        assert det.class_names[0] == "person"

    def test_real_model_detects_person(self):
        import os

        import cv2

        model_path = "models/yolo11n.onnx"
        if not os.path.exists(model_path):
            pytest.skip("models/yolo11n.onnx não exportado neste ambiente")
        image_path = os.path.join(os.environ.get("TEMP", "/tmp"), "bus.jpg")
        if not os.path.exists(image_path):
            pytest.skip("imagem de teste bus.jpg indisponível")

        frame = cv2.imread(image_path)
        det = OnnxYoloDetector(model_path, conf=0.25, class_names=[
            "person", "bicycle", "car", "motorcycle", "airplane", "bus",
        ] + ["x"] * 74)
        dets = det.detect(frame, class_filter={0})
        persons = [d for d in dets if d["class_name"] == "person"]
        assert len(persons) >= 3
        for p in persons:
            x, y, w, h = p["bbox"]
            assert 0 <= x < frame.shape[1]
            assert 0 <= y < frame.shape[0]
            assert w > 0 and h > 0
            assert 0 < p["confidence"] <= 1.0
