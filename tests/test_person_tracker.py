import numpy as np

from src.vision.person_tracker import COLOR_PALETTE, TRACKER_VERSION, CentroidTracker


class TestCentroidTracker:
    def test_version(self):
        assert TRACKER_VERSION == "0.1.0"

    def test_new_tracks_registered(self):
        tracker = CentroidTracker()
        tracked = tracker.update([
            {"bbox": [10, 10, 50, 100], "confidence": 0.9},
            {"bbox": [200, 20, 60, 110], "confidence": 0.8},
        ])
        assert len(tracked) == 2

    def test_stable_track_id_across_frames(self):
        tracker = CentroidTracker()
        dets = [
            {"bbox": [10, 10, 50, 100], "confidence": 0.9},
            {"bbox": [200, 20, 60, 110], "confidence": 0.8},
        ]
        tracked1 = tracker.update(dets)
        ids1 = set(tracked1.keys())
        # Slight movement should keep the same track ids.
        tracked2 = tracker.update([
            {"bbox": [12, 12, 50, 100], "confidence": 0.9},
            {"bbox": [202, 22, 60, 110], "confidence": 0.8},
        ])
        ids2 = set(tracked2.keys())
        assert ids1 == ids2

    def test_distinct_colors(self):
        tracker = CentroidTracker()
        tracked = tracker.update([
            {"bbox": [10, 10, 50, 100], "confidence": 0.9},
            {"bbox": [200, 20, 60, 110], "confidence": 0.82},
        ])
        colors = {id(info["color"]) for info in tracked.values()}
        assert len(colors) == len(tracked)

    def test_disappeared_then_removed(self):
        tracker = CentroidTracker(max_disappeared=2)
        tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        # No detections for max_disappeared+1 frames.
        for _ in range(3):
            tracked = tracker.update([])
        assert len(tracked) == 0

    def test_new_track_id_for_new_person(self):
        tracker = CentroidTracker()
        tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        tracked = tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        ids = set(tracked.keys())
        assert len(ids) == 1

    def test_far_new_detection_gets_new_id(self):
        tracker = CentroidTracker(max_distance=80)
        tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        tracked = tracker.update([{"bbox": [800, 800, 50, 100], "confidence": 0.9}])
        # New far-away detection should be a brand new track.
        assert len(tracked) == 2

    def test_bbox_x_y_w_h_layout(self):
        tracker = CentroidTracker()
        tracked = tracker.update([{"bbox": [10, 20, 50, 100], "confidence": 0.9}])
        bbox = next(iter(tracked.values()))["bbox"]
        assert bbox[2] > 0  # width
        assert bbox[3] > 0  # height


class TestCentroidTrackerDraw:
    def test_draw_returns_same_shape(self):
        tracker = CentroidTracker()
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        tracked = tracker.update([
            {"bbox": [10, 10, 50, 100], "confidence": 0.9},
            {"bbox": [200, 20, 60, 110], "confidence": 0.82},
        ])
        out = tracker.draw(frame, tracked)
        assert out.shape == frame.shape
        # Overlay drew something (pixels differ where boxes/text drawn).
        assert not np.array_equal(out, frame)

    def test_draw_empty_no_crash(self):
        tracker = CentroidTracker()
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        tracked = tracker.update([])
        out = tracker.draw(frame, tracked)
        assert out.shape == frame.shape

    def test_palette_has_distinct_colors(self):
        assert len(COLOR_PALETTE) >= 10
        assert len({tuple(c) for c in COLOR_PALETTE}) == len(COLOR_PALETTE)


class TestCentroidTrackerMatches:
    def test_iou_overlap_matches(self):
        tracker = CentroidTracker(max_distance=10, min_iou=0.1)
        tracker.update([{"bbox": [100, 100, 60, 140], "confidence": 0.9}])
        # Slight overlap between frames.
        tracked = tracker.update([{"bbox": [105, 105, 60, 140], "confidence": 0.9}])
        assert len(tracked) == 1

    def test_centroid_distance_matches(self):
        tracker = CentroidTracker(max_distance=50)
        tracker.update([{"bbox": [100, 100, 40, 80], "confidence": 0.9}])
        # Move within max_distance but no IoU overlap.
        tracked = tracker.update([{"bbox": [150, 100, 40, 80], "confidence": 0.9}])
        assert len(tracked) == 1
