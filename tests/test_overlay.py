"""Tests for the generic live overlay (draw_detection_results)."""

import numpy as np

from src.vision.base import ProcessingResult
from src.vision.overlay import _result_label, draw_detection_results, result_color


def _frame(w: int = 640, h: int = 480) -> np.ndarray:
    return np.zeros((h, w, 3), dtype=np.uint8)


def _result(result_type: str = "fabric_defect", **data) -> ProcessingResult:
    return ProcessingResult(
        result_type=result_type,
        model_name="test",
        model_version="1.0.0",
        confidence=0.9,
        result_data=data,
    )


class TestResultLabel:
    def test_fabric_defect_label_with_severity(self):
        r = _result("fabric_defect", defect_type="hole", severity="high")
        assert _result_label(r) == "hole · high"

    def test_fabric_defect_label_without_severity(self):
        r = _result("fabric_defect", defect_type="stain")
        assert _result_label(r) == "stain"

    def test_fabric_defect_default_unknown_kind(self):
        r = _result("fabric_defect", severity="low")
        assert _result_label(r) == "defect · low"

    def test_generic_label_prefers_class_name(self):
        r = _result("ppe", bbox=[0, 0, 10, 10], class_name="helmet")
        assert _result_label(r) == "helmet"

    def test_generic_label_falls_back_to_result_type(self):
        r = _result("plate", bbox=[0, 0, 10, 10])
        label = _result_label(r)
        assert "plate" in label.replace("_", " ")

    def test_no_bbox_uses_result_type(self):
        r = _result("person")
        assert _result_label(r) == "person"


class TestResultColor:
    def test_fabric_defect_color(self):
        assert result_color(_result("fabric_defect")) == (255, 140, 0)

    def test_fissure_color(self):
        assert result_color(_result("fissure")) == (0, 255, 0)

    def test_unknown_task_default_color(self):
        assert result_color(_result("mystery")) == (0, 255, 0)


class TestDrawDetectionResults:
    def test_empty_results_returns_copy(self):
        frame = _frame()
        out = draw_detection_results(frame, [])
        assert isinstance(out, np.ndarray)
        assert out.shape == frame.shape

    def test_draws_single_box(self):
        frame = _frame()
        r = _result("fabric_defect", bbox=[20, 30, 100, 60], defect_type="hole", severity="low")
        out = draw_detection_results(frame, [r])
        # The overlay must have changed pixels in the box region (orange border).
        assert not np.array_equal(out, frame)

    def test_draws_multiple_boxes(self):
        frame = _frame()
        results = [
            _result("fabric_defect", bbox=[10, 10, 50, 40], defect_type="hole"),
            _result("fabric_defect", bbox=[200, 100, 60, 60], defect_type="stain", severity="high"),
        ]
        out = draw_detection_results(frame, results)
        assert not np.array_equal(out, frame)

    def test_ignores_result_without_bbox(self):
        frame = _frame()
        r = _result("fabric_defect", defect_type="hole")
        out = draw_detection_results(frame, [r])
        assert np.array_equal(out, frame)

    def test_ignores_malformed_bbox(self):
        frame = _frame()
        r = _result("fabric_defect", bbox=[0, 0])
        out = draw_detection_results(frame, [r])
        assert np.array_equal(out, frame)

    def test_clips_bbox_to_frame(self):
        # A box extending outside the frame must not crash and must stay inside.
        frame = _frame(w=100, h=100)
        r = _result("fissure", bbox=[90, 90, 400, 400])
        out = draw_detection_results(frame, [r])
        assert out.shape == frame.shape

    def test_zero_size_bbox_ignored(self):
        frame = _frame()
        r = _result("fabric_defect", bbox=[10, 10, 0, 0])
        out = draw_detection_results(frame, [r])
        assert np.array_equal(out, frame)
