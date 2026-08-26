"""Tests for the crack label processor pipeline (VP-008 hierarchical)."""

import cv2
import numpy as np
import pytest

from src.vision.crack_label_processor import (
    CrackAnalysis,
    CrackLabelProcessor,
    Line,
    Marker,
    Point,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_blank_image(w: int = 1920, h: int = 1080, color: tuple = (30, 30, 30)) -> np.ndarray:
    return np.full((h, w, 3), color, dtype=np.uint8)


def _make_label_image(
    w: int = 1920, h: int = 1080,
    label_color: tuple = (240, 240, 240),
    bg_color: tuple = (30, 30, 30),
    label_rect: tuple | None = None,
) -> np.ndarray:
    """Create an image with a white rectangle (label) on dark background."""
    img = np.full((h, w, 3), bg_color, dtype=np.uint8)
    if label_rect is None:
        x1, y1, x2, y2 = int(w * 0.2), int(h * 0.15), int(w * 0.8), int(h * 0.85)
    else:
        x1, y1, x2, y2 = label_rect
    cv2.rectangle(img, (x1, y1), (x2, y2), label_color, -1)
    return img


def _make_label_with_markers(
    w: int = 1920, h: int = 1080,
) -> np.ndarray:
    """Create an image with label + 6 marker circles + large circle."""
    img = _make_label_image(w, h)
    label_x1, label_y1 = int(w * 0.2), int(h * 0.15)
    label_x2, label_y2 = int(w * 0.8), int(h * 0.85)

    cx = (label_x1 + label_x2) // 2
    cy = (label_y1 + label_y2) // 2

    large_r = int(min(label_x2 - label_x1, label_y2 - label_y1) * 0.3)
    cv2.circle(img, (cx, cy), large_r, (180, 180, 180), 3)

    marker_positions = [
        (label_x1 + 50, label_y1 + 60),
        (label_x1 + 50, cy),
        (label_x1 + 50, label_y2 - 60),
        (label_x2 - 50, label_y1 + 60),
        (label_x2 - 50, cy),
        (label_x2 - 50, label_y2 - 60),
    ]
    for mx, my in marker_positions:
        cv2.circle(img, (mx, my), 20, (50, 50, 50), -1)

    return img


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class TestPoint:
    def test_to_list(self):
        p = Point(10.5, 20.3)
        assert p.to_list() == [10.5, 20.3]

    def test_distance_to(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        assert p1.distance_to(p2) == pytest.approx(5.0)

    def test_distance_zero(self):
        p = Point(5, 5)
        assert p.distance_to(p) == 0.0


class TestLine:
    def test_angle_deg_horizontal(self):
        line = Line(Point(0, 0), Point(100, 0))
        assert line.angle_deg == pytest.approx(0.0, abs=0.1)

    def test_angle_deg_vertical(self):
        line = Line(Point(0, 0), Point(0, 100))
        assert line.angle_deg == pytest.approx(90.0, abs=0.1)

    def test_length(self):
        line = Line(Point(0, 0), Point(3, 4))
        assert line.length == pytest.approx(5.0)

    def test_to_dict(self):
        line = Line(Point(0, 0), Point(10, 0))
        d = line.to_dict()
        assert d["p1"] == [0, 0]
        assert d["p2"] == [10, 0]
        assert d["length"] == pytest.approx(10.0)
        assert d["angle_deg"] == pytest.approx(0.0, abs=0.1)


class TestMarker:
    def test_to_dict(self):
        m = Marker("L1", Point(100, 200), 15.0, 0.9)
        d = m.to_dict()
        assert d["label"] == "L1"
        assert d["center"] == [100, 200]
        assert d["radius"] == 15.0
        assert d["confidence"] == 0.9


class TestCrackAnalysis:
    def test_to_dict_defaults(self):
        a = CrackAnalysis()
        d = a.to_dict()
        assert d["label_detected"] is False
        assert d["label_status"] == "NOT_PROCESSED"
        assert d["label_corners"] == []
        assert d["markers"] == []
        assert d["quality_score"] == 0.0

    def test_to_dict_with_data(self):
        a = CrackAnalysis()
        a.label_detected = True
        a.label_status = "OK"
        a.markers = [Marker("L1", Point(10, 20), 5.0, 0.8)]
        a.distances = {"distance_L1_L2": 100.0}
        d = a.to_dict()
        assert d["label_detected"] is True
        assert len(d["markers"]) == 1
        assert d["distances"]["distance_L1_L2"] == 100.0


# ---------------------------------------------------------------------------
# Image quality
# ---------------------------------------------------------------------------

class TestImageQuality:
    def test_empty_image(self):
        proc = CrackLabelProcessor()
        result = proc._check_image_quality(np.array([]))
        assert result == "EMPTY_IMAGE"

    def test_too_small(self):
        proc = CrackLabelProcessor()
        img = np.full((50, 50, 3), 0, dtype=np.uint8)
        result = proc._check_image_quality(img)
        assert result == "IMAGE_TOO_SMALL"

    def test_valid_image(self):
        proc = CrackLabelProcessor()
        img = _make_blank_image()
        result = proc._check_image_quality(img)
        assert result == "OK"


# ---------------------------------------------------------------------------
# Label detection
# ---------------------------------------------------------------------------

class TestLabelDetection:
    def test_no_label_in_dark_image(self):
        proc = CrackLabelProcessor()
        img = _make_blank_image(color=(30, 30, 30))
        corners, meta = proc._detect_label(img)
        assert len(corners) == 0

    def test_label_found_in_synthetic_image(self):
        proc = CrackLabelProcessor()
        img = _make_label_image()
        corners, meta = proc._detect_label(img)
        assert len(corners) == 4
        assert meta["area"] > 0

    def test_label_large_enough(self):
        proc = CrackLabelProcessor()
        img = _make_label_image(
            label_rect=(200, 150, 1700, 950),
        )
        corners, meta = proc._detect_label(img)
        assert len(corners) == 4
        assert meta["area_ratio"] > 0.1


# ---------------------------------------------------------------------------
# Corner ordering
# ---------------------------------------------------------------------------

class TestOrderCorners:
    def test_already_ordered(self):
        proc = CrackLabelProcessor()
        pts = np.array([[0, 0], [100, 0], [100, 100], [0, 100]], dtype=np.float32)
        ordered = proc._order_corners(pts)
        assert ordered is not None
        assert ordered.shape == (4, 2)

    def test_shuffled_order(self):
        proc = CrackLabelProcessor()
        pts = np.array([[100, 100], [0, 0], [100, 0], [0, 100]], dtype=np.float32)
        ordered = proc._order_corners(pts)
        assert ordered is not None
        tl = ordered[0]
        br = ordered[2]
        assert tl[0] < br[0]
        assert tl[1] < br[1]

    def test_degenerate_points(self):
        proc = CrackLabelProcessor()
        pts = np.array([[0, 0], [1, 1], [2, 2], [3, 3]], dtype=np.float32)
        result = proc._order_corners(pts)
        assert result is None

    def test_too_few_points(self):
        proc = CrackLabelProcessor()
        pts = np.array([[0, 0], [100, 0], [100, 100]], dtype=np.float32)
        result = proc._order_corners(pts)
        assert result is None


# ---------------------------------------------------------------------------
# ROI validation
# ---------------------------------------------------------------------------

class TestROIValidation:
    def test_valid_roi(self):
        proc = CrackLabelProcessor()
        corners = [Point(100, 100), Point(500, 100), Point(500, 400), Point(100, 400)]
        assert proc._validate_roi(corners) == "OK"

    def test_no_corners(self):
        proc = CrackLabelProcessor()
        assert proc._validate_roi([]) == "NO_CORNERS"

    def test_too_small_roi(self):
        proc = CrackLabelProcessor()
        corners = [Point(10, 10), Point(12, 10), Point(12, 12), Point(10, 12)]
        assert proc._validate_roi(corners) == "ROI_TOO_SMALL"

    def test_invalid_aspect_ratio(self):
        proc = CrackLabelProcessor()
        corners = [Point(0, 0), Point(1000, 0), Point(1000, 10), Point(0, 10)]
        assert proc._validate_roi(corners) == "INVALID_ASPECT_RATIO"


# ---------------------------------------------------------------------------
# Homography
# ---------------------------------------------------------------------------

class TestHomography:
    def test_identity_rectification(self):
        proc = CrackLabelProcessor()
        img = _make_label_image(
            label_rect=(0, 0, 1599, 999),
        )
        corners = [Point(0, 0), Point(1599, 0), Point(1599, 999), Point(0, 999)]
        rectified, canonical = proc._rectify_label(img, corners)
        assert rectified.shape == (1000, 1600, 3)
        assert len(canonical) == 4

    def test_perspective_rectification(self):
        proc = CrackLabelProcessor()
        img = _make_blank_image()
        corners = [
            Point(200, 150),
            Point(1700, 130),
            Point(1720, 950),
            Point(180, 970),
        ]
        rectified, canonical = proc._rectify_label(img, corners)
        assert rectified.shape == (1000, 1600, 3)


# ---------------------------------------------------------------------------
# Pipeline — without label
# ---------------------------------------------------------------------------

class TestPipelineNoLabel:
    def test_process_without_label(self):
        proc = CrackLabelProcessor()
        img = _make_blank_image()
        analysis = proc.process(img)
        assert analysis.label_detected is False
        assert analysis.label_status == "LABEL_NOT_FOUND"
        assert analysis.markers == []
        assert analysis.line_AB is None
        assert analysis.processing_ms >= 0

    def test_quality_score_zero_without_label(self):
        proc = CrackLabelProcessor()
        img = _make_blank_image()
        analysis = proc.process(img)
        assert analysis.quality_score == 0.0


# ---------------------------------------------------------------------------
# Pipeline — with label
# ---------------------------------------------------------------------------

class TestPipelineWithLabel:
    def test_process_with_label(self):
        proc = CrackLabelProcessor()
        img = _make_label_image()
        analysis = proc.process(img)
        assert analysis.label_detected is True
        assert analysis.label_status == "OK"
        assert analysis.rectified_width == 1600
        assert analysis.rectified_height == 1000

    def test_process_returns_dict(self):
        proc = CrackLabelProcessor()
        img = _make_label_image()
        analysis = proc.process(img)
        d = analysis.to_dict()
        assert "label_detected" in d
        assert "label_status" in d
        assert "rectified_width" in d
        assert "rectified_height" in d


# ---------------------------------------------------------------------------
# Internal detection — on normalized image
# ---------------------------------------------------------------------------

class TestInternalDetection:
    def test_no_markers_in_dark_normalized(self):
        proc = CrackLabelProcessor()
        dark = np.zeros((1000, 1600), dtype=np.uint8)
        markers, circle, line_ab, line_cd, cracks, inter = proc._detect_internal_elements(dark)
        assert markers == []
        assert circle is None
        assert line_ab is None
        assert line_cd is None

    def test_marker_labeling_left_right(self):
        proc = CrackLabelProcessor()
        markers = [
            Marker("", Point(300, 200), 20, 0.8),
            Marker("", Point(300, 500), 20, 0.8),
            Marker("", Point(300, 800), 20, 0.8),
            Marker("", Point(1300, 200), 20, 0.8),
            Marker("", Point(1300, 500), 20, 0.8),
            Marker("", Point(1300, 800), 20, 0.8),
        ]
        labeled = proc._assign_marker_labels_normalized(markers)
        labels = {m.label for m in labeled}
        assert "L1" in labels
        assert "L2" in labels
        assert "L3" in labels
        assert "R1" in labels
        assert "R2" in labels
        assert "R3" in labels

    def test_marker_labeling_fewer_than_6(self):
        proc = CrackLabelProcessor()
        markers = [
            Marker("", Point(300, 200), 20, 0.8),
            Marker("", Point(1300, 500), 20, 0.8),
        ]
        labeled = proc._assign_marker_labels_normalized(markers)
        assert labeled[0].label == "L1"
        assert labeled[1].label == "R1"


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------

class TestMeasurements:
    def test_distances(self):
        proc = CrackLabelProcessor()
        markers = {
            "L1": Marker("L1", Point(100, 100), 10, 0.8),
            "L2": Marker("L2", Point(100, 300), 10, 0.8),
            "R1": Marker("R1", Point(500, 100), 10, 0.8),
        }
        dists = proc._compute_distances(markers)
        assert "distance_L1_L2" in dists
        assert dists["distance_L1_L2"] == pytest.approx(200.0, abs=1)
        assert "distance_L1_R1" in dists
        assert dists["distance_L1_R1"] == pytest.approx(400.0, abs=1)

    def test_angles(self):
        proc = CrackLabelProcessor()
        markers = {
            "L1": Marker("L1", Point(100, 100), 10, 0.8),
            "L2": Marker("L2", Point(100, 300), 10, 0.8),
        }
        line_ab = Line(Point(0, 0), Point(100, 100))
        line_cd = Line(Point(100, 0), Point(0, 100))
        angles = proc._compute_angles(markers, line_ab, line_cd)
        assert "angle_AB_CD" in angles
        assert angles["angle_AB_CD"] == pytest.approx(90.0, abs=1)

    def test_line_intersection(self):
        proc = CrackLabelProcessor()
        line_a = Line(Point(0, 0), Point(100, 100))
        line_b = Line(Point(100, 0), Point(0, 100))
        pt = proc._line_intersection(line_a, line_b)
        assert pt is not None
        assert pt.x == pytest.approx(50.0, abs=0.1)
        assert pt.y == pytest.approx(50.0, abs=0.1)

    def test_line_intersection_parallel(self):
        proc = CrackLabelProcessor()
        line_a = Line(Point(0, 0), Point(100, 0))
        line_b = Line(Point(0, 10), Point(100, 10))
        pt = proc._line_intersection(line_a, line_b)
        assert pt is None


# ---------------------------------------------------------------------------
# Overlay
# ---------------------------------------------------------------------------

class TestOverlay:
    def test_draw_overlay_without_label(self):
        proc = CrackLabelProcessor()
        img = _make_blank_image()
        analysis = proc.process(img)
        overlay = proc.draw_overlay(img, analysis)
        assert overlay.shape == img.shape

    def test_draw_overlay_with_label(self):
        proc = CrackLabelProcessor()
        img = _make_label_image()
        analysis = proc.process(img)
        overlay = proc.draw_overlay(img, analysis)
        assert overlay.shape[0] > img.shape[0]


# ---------------------------------------------------------------------------
# Empty / edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_none_image(self):
        proc = CrackLabelProcessor()
        analysis = proc.process(np.array([]))
        assert analysis.label_status == "EMPTY_IMAGE"

    def test_single_pixel_image(self):
        proc = CrackLabelProcessor()
        tiny = np.full((1, 1, 3), 128, dtype=np.uint8)
        analysis = proc.process(tiny)
        assert analysis.label_status == "IMAGE_TOO_SMALL"
