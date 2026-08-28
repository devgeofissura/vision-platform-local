"""Tests for fabric inspection metrics: pixel->cm calibration, defect
dimension measurement, roll meterage estimation and the 4-Point System
(ASTM D5430) scoring."""

import pytest

from src.vision.base import ProcessingResult
from src.vision.fabric_metrics import (
    FabricCalibrator,
    RollMeterageEstimator,
    measure_defects,
    points_per_100m2,
    score_defect,
    total_points,
)


def _fake_detection(defect_type="stain", bbox=(0, 0, 40, 20), conf=0.8):
    return ProcessingResult(
        result_type="fabric_defect",
        model_name="test",
        model_version="1.0.0",
        confidence=conf,
        result_data={"defect_type": defect_type, "bbox": list(bbox)},
    )


# ── score_defect — 4-Point thresholds ──

class TestScoreDefect:
    def test_up_to_75mm_1_point(self):
        assert score_defect("stain", 75.0) == 1
        assert score_defect("stain", 10.0) == 1

    def test_75_to_150mm_2_points(self):
        assert score_defect("stain", 76.0) == 2
        assert score_defect("stain", 150.0) == 2

    def test_150_to_230mm_3_points(self):
        assert score_defect("stain", 151.0) == 3
        assert score_defect("stain", 230.0) == 3

    def test_over_230mm_4_points(self):
        assert score_defect("stain", 231.0) == 4
        assert score_defect("stain", 500.0) == 4

    def test_hole_always_4_points_regardless_of_size(self):
        assert score_defect("hole", 1.0) == 4
        assert score_defect("hole", 500.0) == 4

    def test_tear_always_4_points(self):
        assert score_defect("tear", 1.0) == 4

    def test_never_exceeds_4(self):
        assert score_defect("stain", 1e9) == 4


# ── FabricCalibrator ──

class TestFabricCalibrator:
    def test_not_calibrated_without_width(self):
        c = FabricCalibrator(fabric_width_cm=0.0, fabric_width_px=100.0)
        assert c.calibrated is False

    def test_not_calibrated_without_px(self):
        c = FabricCalibrator(fabric_width_cm=150.0, fabric_width_px=0.0)
        assert c.calibrated is False

    def test_calibrated(self):
        c = FabricCalibrator(fabric_width_cm=150.0, fabric_width_px=750.0)
        assert c.calibrated is True
        assert c.px_per_cm() == 5.0

    def test_px_to_cm(self):
        c = FabricCalibrator(fabric_width_cm=150.0, fabric_width_px=750.0)
        assert c.px_to_cm(250.0) == pytest.approx(50.0)

    def test_area_px_to_cm2(self):
        c = FabricCalibrator(fabric_width_cm=150.0, fabric_width_px=750.0)
        assert c.area_px_to_cm2(100.0) == pytest.approx(4.0)

    def test_uncalibrated_passthrough(self):
        c = FabricCalibrator(fabric_width_cm=0.0, fabric_width_px=0.0)
        assert c.px_to_cm(50.0) == 50.0
        assert c.area_px_to_cm2(25.0) == 25.0


# ── measure_defects ──

class TestMeasureDefects:
    def test_measures_length_width_and_area(self):
        det = _fake_detection("stain", (0, 0, 100, 50))
        c = FabricCalibrator(fabric_width_cm=150.0, fabric_width_px=750.0)
        measured = measure_defects([det], c, frame_width_px=750)
        assert len(measured) == 1
        m = measured[0]
        assert m.length_cm == pytest.approx(20.0)   # 100px / 5
        assert m.width_cm == pytest.approx(10.0)    # 50px / 5
        assert m.area_cm2 == pytest.approx(200.0)   # 5000px2 / 25
        assert m.defect_type == "stain"

    def test_scores_hole_as_4_points(self):
        det = _fake_detection("hole", (0, 0, 10, 10))
        c = FabricCalibrator(fabric_width_cm=150.0, fabric_width_px=750.0)
        measured = measure_defects([det], c, frame_width_px=750)
        assert measured[0].points == 4
        assert measured[0].severity == "high"

    def test_scores_short_stain_as_1_point(self):
        det = _fake_detection("stain", (0, 0, 10, 10))  # 2cm = 20mm
        c = FabricCalibrator(fabric_width_cm=150.0, fabric_width_px=750.0)
        measured = measure_defects([det], c, frame_width_px=750)
        assert measured[0].points == 1
        assert measured[0].severity == "low"

    def test_skips_detection_without_bbox(self):
        det = ProcessingResult(
            result_type="fabric_defect", model_name="m", model_version="1",
            confidence=0.5, result_data={"defect_type": "stain"},
        )
        c = FabricCalibrator(fabric_width_cm=150.0, fabric_width_px=750.0)
        assert measure_defects([det], c, frame_width_px=750) == []

    def test_uncalibrated_runs_in_pixels(self):
        det = _fake_detection("stain", (0, 0, 100, 50))
        c = FabricCalibrator(fabric_width_cm=0.0, fabric_width_px=0.0)
        measured = measure_defects([det], c, frame_width_px=0)
        assert len(measured) == 1
        assert measured[0].length_cm == pytest.approx(100.0)
        assert measured[0].points > 0


# ── total_points / points_per_100m2 ──

class TestScoring:
    def test_total_points_sums(self):
        c = FabricCalibrator(fabric_width_cm=150.0, fabric_width_px=750.0)
        dets = [
            _fake_detection("hole", (0, 0, 10, 10)),      # 4
            _fake_detection("stain", (0, 0, 25, 10)),     # 1 (2cm len)
            _fake_detection("stain", (0, 0, 600, 10)),    # 4 (>230mm)
        ]
        measured = measure_defects(dets, c, frame_width_px=750)
        assert total_points(measured) == pytest.approx(9.0)

    def test_points_per_100m2_formula(self):
        # Example from Joźwiak: 28 points, 100m inspected, fabric width 1500mm (150cm)
        # points/100m2 = 28*100000/(100*1500) = 18.67
        assert points_per_100m2(28.0, 100.0, 150.0) == pytest.approx(18.67, abs=0.01)

    def test_points_per_100m2_invalid_inputs(self):
        assert points_per_100m2(10.0, 0.0, 150.0) == 0.0
        assert points_per_100m2(10.0, 100.0, 0.0) == 0.0


# ── RollMeterageEstimator ──

class TestRollMeterageEstimator:
    def test_feed_rate_accumulates_meters(self):
        est = RollMeterageEstimator(feed_rate_m_min=60.0)  # 1 m/s
        est.advance(elapsed_seconds=10.0)
        assert est.estimate_meters() == pytest.approx(10.0)
        assert est.frames_seen == 1

    def test_fallback_meter_per_frame(self):
        est = RollMeterageEstimator(feed_rate_m_min=0.0, meter_per_frame=0.05)
        est.advance()
        est.advance()
        assert est.estimate_meters() == pytest.approx(0.1)

    def test_feed_rate_ignores_zero_elapsed(self):
        est = RollMeterageEstimator(feed_rate_m_min=60.0)
        est.advance(elapsed_seconds=0.0)
        assert est.estimate_meters() == pytest.approx(0.0)

    def test_reset(self):
        est = RollMeterageEstimator(feed_rate_m_min=60.0)
        est.advance(elapsed_seconds=5.0)
        est.reset()
        assert est.estimate_meters() == 0.0
        assert est.frames_seen == 0
