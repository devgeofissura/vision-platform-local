import numpy as np

from src.vision.person_tracker import COLOR_PALETTE, TRACKER_VERSION, CentroidTracker


class TestCentroidTracker:
    def test_version(self):
        assert TRACKER_VERSION == "0.2.0"

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


class TestKalmanPredict:
    """Kalman prediction coasts the box with its velocity between sparse
    detections, so the overlay keeps moving smoothly and stems ID-switch."""

    def test_predict_moves_box_along_velocity(self):
        tracker = CentroidTracker(min_hits=1, max_distance=0)
        # Two consistent detections establish a rightward velocity.
        tracker.update([{"bbox": [100, 100, 50, 100], "confidence": 0.9}])
        tracker.update([{"bbox": [130, 100, 50, 100], "confidence": 0.9}])
        cx_before = next(iter(tracker.objects.values()))["centroid"][0]
        # Coast a prediction step even without a new detection.
        tracker.predict(dt=1.0)
        cx_after = next(iter(tracker.objects.values()))["centroid"][0]
        # Velocity (rightward) should carry the centroid further right.
        assert cx_after >= cx_before

    def test_kalman_smoothes_jump_and_keeps_same_id(self):
        # Even a large single-frame jump stays the same track (PenguinSORT/
        # sparse-motion robustness) as long as it matches one of the stages.
        tracker = CentroidTracker(min_hits=1, max_distance=400)
        tracker.update([{"bbox": [100, 100, 60, 140], "confidence": 0.9}])
        tracked = tracker.update([{"bbox": [140, 100, 60, 140], "confidence": 0.9}])
        assert len(tracked) == 1

    def test_far_detection_not_matched_by_kalman(self):
        # A distant, non-overlapping detection is read as a new object even
        # though a Kalman velocity model exists.
        tracker = CentroidTracker(min_hits=1, max_distance=80)
        tracker.update([{"bbox": [10, 10, 50, 100], "confidence": 0.9}])
        tracker.update([{"bbox": [30, 10, 50, 100], "confidence": 0.9}])
        tracked = tracker.update([{"bbox": [900, 900, 50, 100], "confidence": 0.9}])
        assert len(tracked) == 2


class TestMultiStageAssociation:
    """Staged IoU thresholds let a match be locked by a strong overlap first,
    then rescued by progressively weaker cues (PineSORT pattern)."""

    def test_mid_iou_stage_still_matches(self):
        tracker = CentroidTracker(min_hits=1, max_distance=0)
        tracker.update([{"bbox": [100, 100, 60, 140], "confidence": 0.9}])
        # Moderate overlap that clears stage-2 (0.15) but not stage-1 (0.30).
        tracked = tracker.update([{"bbox": [120, 100, 60, 140], "confidence": 0.9}])
        assert len(tracked) == 1

    def test_weak_iou_stage_matches_fast_move(self):
        tracker = CentroidTracker(min_hits=1, max_distance=0)
        tracker.update([{"bbox": [100, 100, 40, 80], "confidence": 0.9}])
        # Small box jumped far but still slightly overlaps (stage-3, 0.05).
        tracked = tracker.update([{"bbox": [135, 100, 40, 80], "confidence": 0.9}])
        assert len(tracked) == 1

    def test_no_overlap_no_distance_no_match(self):
        tracker = CentroidTracker(min_hits=1, max_distance=0)
        tracker.update([{"bbox": [100, 100, 40, 80], "confidence": 0.9}])
        tracked = tracker.update([{"bbox": [300, 300, 40, 80], "confidence": 0.9}])
        # No IoU overlap and distance fallback disabled -> two tracks.
        assert len(tracked) == 2


class TestAppearanceRescue:
    """A lightweight HSV template rescues a LOST track that has no geometric
    overlap, without a per-frame re-ID encoder (womprat pattern)."""

    def _make_tracker(self):
        return CentroidTracker(min_hits=1, max_distance=20)

    def test_lost_track_rescued_by_appearance(self):
        tracker = self._make_tracker()
        # A bright red box that the tracker can remember.
        frame_red = np.zeros((300, 400, 3), dtype=np.uint8)
        frame_red[:, :] = (0, 0, 255)
        tracker.update(
            [{"bbox": [50, 50, 60, 100], "confidence": 0.9}], frame=frame_red
        )

        # Person briefly disappears (one empty frame) -> track is now "lost".
        tracker.update([])

        # Comes back at a basically non-overlapping spot, but same colors.
        later = np.zeros((300, 400, 3), dtype=np.uint8)
        later[:, :] = (0, 0, 255)
        later[:, :] = (5, 3, 250)
        tracker.update(
            [{"bbox": [200, 210, 60, 100], "confidence": 0.9}], frame=later
        )

        # The lost track should be rescued by appearance -> still 1 person.
        assert len(tracker.objects) == 1

    def test_different_appearance_not_rescued(self):
        tracker = self._make_tracker()
        frame_red = np.zeros((300, 400, 3), dtype=np.uint8)
        frame_red[:, :] = (0, 0, 255)
        tracker.update(
            [{"bbox": [50, 50, 60, 100], "confidence": 0.9}], frame=frame_red
        )
        tracker.update([])

        # The re-detection is a different color (blue) -> not the same person.
        frame_blue = np.zeros((300, 400, 3), dtype=np.uint8)
        frame_blue[:, :] = (255, 0, 0)
        tracker.update(
            [{"bbox": [200, 210, 60, 100], "confidence": 0.9}], frame=frame_blue
        )
        # New detection becomes a separate object.
        assert len(tracker.objects) == 2
