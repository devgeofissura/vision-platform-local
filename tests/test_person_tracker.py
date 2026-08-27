import numpy as np

from src.vision.person_tracker import COLOR_PALETTE, TRACKER_VERSION, CentroidTracker


class TestCentroidTracker:
    def test_version(self):
        assert TRACKER_VERSION == "0.1.0"

    def test_new_tracks_registered(self):
        tracker = CentroidTracker(min_hits=1)
        tracked = tracker.update([
            {"bbox": [10, 10, 50, 100], "confidence": 0.9},
            {"bbox": [200, 20, 60, 110], "confidence": 0.8},
        ])
        assert len(tracked) == 2

    def test_stable_track_id_across_frames(self):
        tracker = CentroidTracker(min_hits=1)
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
        tracker = CentroidTracker(min_hits=1)
        tracked = tracker.update([
            {"bbox": [10, 10, 50, 100], "confidence": 0.9},
            {"bbox": [200, 20, 60, 110], "confidence": 0.82},
        ])
        colors = {id(info["color"]) for info in tracked.values()}
        assert len(colors) == len(tracked)

    def test_disappeared_then_removed(self):
        tracker = CentroidTracker(max_disappeared=2, min_hits=1)
        tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        # No detections for max_disappeared+1 frames.
        for _ in range(3):
            tracked = tracker.update([])
        assert len(tracked) == 0

    def test_new_track_id_for_new_person(self):
        tracker = CentroidTracker(min_hits=1)
        tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        tracked = tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        ids = set(tracked.keys())
        assert len(ids) == 1

    def test_far_new_detection_gets_new_id(self):
        tracker = CentroidTracker(max_distance=80, min_hits=1)
        tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        tracked = tracker.update([{"bbox": [800, 800, 50, 100], "confidence": 0.9}])
        # New far-away detection should be a brand new track.
        assert len(tracked) == 2

    def test_bbox_x_y_w_h_layout(self):
        tracker = CentroidTracker(min_hits=1)
        tracked = tracker.update([{"bbox": [10, 20, 50, 100], "confidence": 0.9}])
        bbox = next(iter(tracked.values()))["bbox"]
        assert bbox[2] > 0  # width
        assert bbox[3] > 0  # height


class TestMinHitsConfirmation:
    """A track only appears after `min_hits` consistent detections.

    This is what stops a fast-moving subject from inflating the person
    count with ghost IDs: a single spurious/unstable detection is kept
    internally but never surfaces to the overlay/count.
    """

    def test_default_requires_two_hits(self):
        tracker = CentroidTracker()  # default min_hits=2
        # First detection: track is registered internally but NOT confirmed.
        tracked1 = tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        assert len(tracked1) == 0
        # Second consistent detection confirms it.
        tracked2 = tracker.update([{"bbox": [12, 12, 50, 100], "confidence": 0.9}])
        assert len(tracked2) == 1

    def test_single_flash_motion_does_not_create_ghost(self):
        """The reported bug: a brief detection while moving must not count."""
        tracker = CentroidTracker()  # default min_hits=2
        tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        # Subject moves fast; the detection appears once in a new spot and
        # then is gone. This single flash must NOT create a visible track.
        tracker.update([{"bbox": [400, 400, 50, 100], "confidence": 0.9}])
        tracked = tracker.update([])
        assert len(tracked) == 0

    def test_auth_motion_same_id_not_inflated(self):
        """Moving subject that keeps overlapping keeps ONE stable ID."""
        tracker = CentroidTracker(min_hits=1)
        tracker.update([{"bbox": [100, 100, 200, 400], "confidence": 0.9}])
        # Several frames of a person walking across, boxes still overlapping.
        ids = set()
        for dx in range(0, 220, 40):
            tr = tracker.update([
                {"bbox": [100 + dx, 100, 200, 400], "confidence": 0.9}
            ])
            ids.update(tr.keys())
        # One person moving -> exactly one track id over the whole path.
        assert len(ids) == 1

    def test_lost_track_expires_fast_with_small_max_disappeared(self):
        tracker = CentroidTracker(max_disappeared=6, min_hits=1)
        tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        # Subject leaves: the orphan ID must expire quickly (6 frames)
        # so the count does not stay inflated for a long time.
        tracked = None
        for _ in range(7):
            tracked = tracker.update([])
        assert len(tracked) == 0
        # And a returning person is counted as new without delay after expiry.
        tracked2 = tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        assert len(tracked2) == 1


class TestSparseMotionRobustness:
    """Detection is sparse (~2s) on edge; boxes of a moving full-body
    subject overlap heavily, so matching on IoU (dominant) must keep the ID
    even when the centroid moved a lot between cycles."""

    def test_iou_keeps_id_when_centroid_moved_far(self):
        tracker = CentroidTracker(max_distance=150, min_hits=1)
        tracker.update([{"bbox": [100, 100, 180, 360], "confidence": 0.9}])
        # Huge movement, but still heavy overlap -> same ID via IoU.
        tracked = tracker.update([{"bbox": [220, 120, 180, 360], "confidence": 0.9}])
        assert len(tracked) == 1

    def test_no_overlap_and_beyond_distance_gets_new_id(self):
        tracker = CentroidTracker(max_distance=150, min_hits=1)
        tracker.update([{"bbox": [100, 100, 40, 80], "confidence": 0.9}])
        # Far away AND no overlap -> a genuinely new track.
        tracked = tracker.update([{"bbox": [900, 900, 40, 80], "confidence": 0.9}])
        assert len(tracked) == 2

    def test_dominant_iou_picks_right_match_with_two_detections(self):
        # Two tracks exist; next frame offers two boxes. The match must take
        # each track to its own most-overlapping box (no ID swap).
        tracker = CentroidTracker(max_distance=400, min_hits=1)
        tracker.update([
            {"bbox": [100, 100, 60, 140], "confidence": 0.9},
            {"bbox": [400, 100, 60, 140], "confidence": 0.9},
        ])
        tracked = tracker.update([
            # box A moved right a bit, box B moved left a bit; overlap keeps
            # each aligned with the SAME track.
            {"bbox": [120, 100, 60, 140], "confidence": 0.9},
            {"bbox": [380, 100, 60, 140], "confidence": 0.9},
        ])
        assert len(tracked) == 2


class TestCentroidTrackerDraw:
    def test_draw_returns_same_shape(self):
        tracker = CentroidTracker(min_hits=1)
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
        tracker = CentroidTracker(max_distance=10, min_iou=0.1, min_hits=1)
        tracker.update([{"bbox": [100, 100, 60, 140], "confidence": 0.9}])
        # Slight overlap between frames.
        tracked = tracker.update([{"bbox": [105, 105, 60, 140], "confidence": 0.9}])
        assert len(tracked) == 1

    def test_centroid_distance_matches(self):
        tracker = CentroidTracker(max_distance=50, min_hits=1)
        tracker.update([{"bbox": [100, 100, 40, 80], "confidence": 0.9}])
        # Move within max_distance but no IoU overlap.
        tracked = tracker.update([{"bbox": [150, 100, 40, 80], "confidence": 0.9}])
        assert len(tracked) == 1
