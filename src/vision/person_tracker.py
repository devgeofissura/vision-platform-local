"""Person centroid tracker with IO + overlap matching (pure OpenCV/NumPy).

Works without ultralytics — suitable for the ONNX fallback path.
Tracks people across frames and draws bounding boxes with a distinct
color per track, plus a running count overlay.
"""

import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)

TRACKER_VERSION = "0.1.0"

# 12 distinct BGR colors so multiple people never share a color.
COLOR_PALETTE = [
    (0, 255, 0),      # green
    (255, 0, 0),      # blue
    (0, 0, 255),      # red
    (255, 255, 0),    # cyan
    (0, 255, 255),    # yellow
    (255, 0, 255),    # magenta
    (128, 255, 0),    # aqua green
    (255, 128, 0),    # orange
    (0, 128, 255),    # light blue
    (255, 0, 128),    # pink
    (128, 0, 255),    # purple
    (0, 255, 128),    # mint
]


class CentroidTracker:
    """Simple centroid-based tracker that matches detections across frames.

    Matching uses a combination of centroid Euclidean distance and bbox
    overlap (IoU) so tracks survive when a person partially occludes.
    """

    def __init__(
        self,
        max_disappeared: int = 6,
        max_distance: float = 150.0,
        min_iou: float = 0.1,
        min_hits: int = 2,
    ):
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
        self.min_iou = min_iou
        self.min_hits = min_hits
        self._next_id = 1
        self.objects: dict[int, dict] = {}
        self.disappeared: dict[int, int] = {}
        self.colors: dict[int, tuple[int, int, int]] = {}
        self.hit_streak: dict[int, int] = {}

    def _new_color(self) -> tuple[int, int, int]:
        idx = (self._next_id - 1) % len(COLOR_PALETTE)
        return COLOR_PALETTE[idx]

    def _register(self, bbox: list, confidence: float) -> int:
        track_id = self._next_id
        self._next_id += 1
        cx, cy = self._centroid(bbox)
        self.objects[track_id] = {
            "centroid": (float(cx), float(cy)),
            "bbox": [float(v) for v in bbox],
            "confidence": float(confidence),
        }
        self.disappeared[track_id] = 0
        self.colors[track_id] = self._new_color()
        # A brand new track starts unconfirmed, so a single spurious
        # detection (e.g. a false positive while the subject is moving
        # fast) cannot inflate the person count with a ghost ID. As in
        # SORT's `min_hits`, it only becomes visible after it has been
        # detected consistently for `min_hits` consecutive frames.
        self.hit_streak[track_id] = 1
        return track_id

    @staticmethod
    def _centroid(bbox: list) -> tuple[float, float]:
        x, y, w, h = bbox[:4]
        return float(x + w / 2), float(y + h / 2)

    def update(self, detections: list[dict]) -> dict[int, dict]:
        """Update tracker state with new detections.

        Args:
            detections: list of dicts with keys:
                        - bbox: [x1, y1, width, height]
                        - confidence: float

        Returns:
            dict of {track_id: {"centroid", "bbox", "confidence", "color"}}
        """
        # Empty detections -> mark all as disappeared.
        if not detections:
            for track_id in list(self.disappeared):
                self.disappeared[track_id] += 1
                if self.disappeared[track_id] > self.max_disappeared:
                    self._deregister(track_id)
            return self._snapshot()

        # Existing tracks centroids.
        track_ids = list(self.objects.keys())
        track_centroids = np.array(
            [self.objects[tid]["centroid"] for tid in track_ids],
            dtype=np.float32,
        ) if track_ids else np.zeros((0, 2), dtype=np.float32)

        # New detections centroids.
        det_centroids = np.array(
            [self._centroid(d["bbox"]) for d in detections],
            dtype=np.float32,
        )

        matched_track_ids = set()
        matched_det_indices = set()

        if track_centroids.shape[0] > 0 and det_centroids.shape[0] > 0:
            # Distance + IoU scoring.
            dists = self._compute_distances(track_centroids, det_centroids)
            ious = self._compute_ious(self.objects, detections)

            used_tracks = set()
            used_dets = set()
            # Prefer the pair with the STRONGEST IoU (dominant cue), as in
            # SORT. Because detections are sparse (~2s apart) on edge, a full
            # body box still overlaps the previous one even when the centroid
            # has moved significantly; matching on overlap first keeps the
            # identity stable where a centroid-only match would switch IDs.
            # Distance is used as a tie-breaker only.
            for _ in range(min(len(track_ids), len(detections))):
                best_iou = -1.0
                best_min_dist = np.inf
                best_track = -1
                best_det = -1
                for i, tid in enumerate(track_ids):
                    if i in used_tracks:
                        continue
                    for j in range(len(detections)):
                        if j in used_dets:
                            continue
                        iou = float(ious[i, j])
                        d = float(dists[i, j])
                        # Select by highest IoU first; break ties by distance.
                        if iou > best_iou + 1e-9 or (
                            abs(iou - best_iou) <= 1e-9 and d < best_min_dist
                        ):
                            best_iou = iou
                            best_min_dist = d
                            best_track = i
                            best_det = j

                if best_track == -1 or best_det == -1:
                    break

                tid = track_ids[best_track]
                iou = float(ious[best_track, best_det])
                within_dist = best_min_dist <= self.max_distance
                within_iou = iou >= self.min_iou

                # Match if within distance OR overlapping enough.
                if within_dist or within_iou:
                    matched_track_ids.add(tid)
                    matched_det_indices.add(best_det)
                    used_tracks.add(best_track)
                    used_dets.add(best_det)
                    self.objects[tid] = {
                        "centroid": tuple(det_centroids[best_det]),
                        "bbox": [float(v) for v in detections[best_det]["bbox"]],
                        "confidence": float(detections[best_det].get("confidence", 1.0)),
                    }
                    self.disappeared[tid] = 0
                    self.hit_streak[tid] = self.hit_streak.get(tid, 0) + 1
                else:
                    break

        # Deregister unmatched tracks (they disappeared this frame).
        for tid in track_ids:
            if tid not in matched_track_ids:
                self.disappeared[tid] += 1
                if self.disappeared[tid] > self.max_disappeared:
                    self._deregister(tid)

        # Register unmatched new detections.
        for j, det in enumerate(detections):
            if j not in matched_det_indices:
                self._register(det["bbox"], det.get("confidence", 1.0))

        return self._snapshot()

    def _deregister(self, track_id: int) -> None:
        self.objects.pop(track_id, None)
        self.disappeared.pop(track_id, None)
        self.colors.pop(track_id, None)
        self.hit_streak.pop(track_id, None)

    def _compute_distances(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        # a: (N,2), b: (M,2) -> (N,M)
        return np.linalg.norm(a[:, None, :] - b[None, :, :], axis=2)

    def _compute_ious(self, objects: dict, detections: list[dict]) -> np.ndarray:
        track_bboxes = np.array(
            [objects[tid]["bbox"] for tid in objects],
            dtype=np.float32,
        ) if objects else np.zeros((0, 4), dtype=np.float32)
        det_bboxes = np.array(
            [d["bbox"] for d in detections],
            dtype=np.float32,
        )
        n_track = track_bboxes.shape[0]
        n_det = det_bboxes.shape[0]
        ious = np.zeros((n_track, n_det), dtype=np.float32)
        if n_track == 0 or n_det == 0:
            return ious
        for i in range(n_track):
            for j in range(n_det):
                ious[i, j] = self._iou(track_bboxes[i], det_bboxes[j])
        return ious

    @staticmethod
    def _iou(a: np.ndarray, b: np.ndarray) -> float:
        x1 = max(float(a[0]), float(b[0]))
        y1 = max(float(a[1]), float(b[1]))
        x2 = min(float(a[0] + a[2]), float(b[0] + b[2]))
        y2 = min(float(a[1] + a[3]), float(b[1] + b[3]))
        if x2 <= x1 or y2 <= y1:
            return 0.0
        inter = (x2 - x1) * (y2 - y1)
        union = float(a[2] * a[3]) + float(b[2] * b[3]) - inter
        return inter / union if union > 0 else 0.0

    def _snapshot(self) -> dict[int, dict]:
        return {
            tid: {
                "centroid": self.objects[tid]["centroid"],
                "bbox": self.objects[tid]["bbox"],
                "confidence": self.objects[tid]["confidence"],
                "color": self.colors.get(tid, COLOR_PALETTE[0]),
            }
            for tid in self.objects
            if self.hit_streak.get(tid, 0) >= self.min_hits
        }

    def draw(self, frame: np.ndarray, tracked: dict[int, dict]) -> np.ndarray:
        """Draw bounding boxes, labels and a person-count overlay.

        Args:
            frame: BGR image to draw on.
            tracked: dict from update().

        Returns:
            Frame with overlays drawn.
        """
        overlay = frame.copy()
        h, w = overlay.shape[:2]

        for track_id, info in tracked.items():
            x, y, bw, bh = [int(v) for v in info["bbox"]]
            color = tuple(int(c) for c in info["color"])
            conf = info["confidence"]

            x = max(0, x)
            y = max(0, y)
            bw = min(bw, w - x)
            bh = min(bh, h - y)

            cv2.rectangle(overlay, (x, y), (x + bw, y + bh), color, 2, cv2.LINE_AA)

            label = f"P{track_id} {conf:.0%}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(
                overlay,
                (x, y - th - 6),
                (x + tw + 8, y),
                color,
                -1,
            )
            cv2.putText(
                overlay, label, (x + 4, y - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA,
            )

        count = len(tracked)

        # Bottom count bar.
        bar_w = 220
        bar_h = 44
        bx = (w - bar_w) // 2
        by = h - bar_h - 12
        cv2.rectangle(
            overlay, (bx, by), (bx + bar_w, by + bar_h),
            (30, 30, 30), -1,
        )
        cv2.addWeighted(
            overlay[by:by + bar_h, bx:bx + bar_w], 0.3,
            overlay[by:by + bar_h, bx:bx + bar_w], 0.7, 0,
            overlay[by:by + bar_h, bx:bx + bar_w],
        )
        cv2.putText(
            overlay, f"PESSOAS: {count}",
            (bx + 12, by + 28),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA,
        )

        return overlay
