"""Person centroid tracker with Kalman prediction + multi-stage matching.

Pure OpenCV/NumPy (works without ultralytics, suitable for the ONNX
fallback path). Tracks people across frames and draws distinct-color boxes
plus a running count. Built on lessons from SORT, Deep-SORT and PineSORT:

- Constant-velocity Kalman filter per track predicts the next centroid/box
  so identity survives motion between sparse detections (the ID-switching fix
  for ~2s-apart inference on the Orange Pi).
- Multi-stage association (high IoU -> mid IoU -> low IoU -> distance) so
  fast-moving or partially-occluded subjects keep one ID (PineSORT pattern).
- Lightweight appearance (HSV histogram in the box) is used *only* when a
  track is currently lost (disappeared > 0), to re-associate it cheaply
  without the cost of a per-frame re-ID encoder (womprat/Deep-SORT hybrid).
"""

import logging
import time

import cv2
import numpy as np

logger = logging.getLogger(__name__)

TRACKER_VERSION = "0.2.0"

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

# IoU thresholds for the staged association (high -> mid -> low). A lower
# threshold keeps matching when the box moved a lot between sparse frames.
_ASSOCIATION_IOU_STAGES = [0.30, 0.15, 0.05]

# Squares of the process-noised velocity (px/frame^2). Tuned so predicted
# boxes do not run away while a track coasts for a few seconds.
_KF_DT_DEFAULT = 1.0
_KF_POS_PROCESS = 1e-2
_KF_VEL_PROCESS = 1e-1
_KF_MEAS_NOISE = 1e-1

# State order: [cx, cy, w, h, vx, vy, vw, vh]
_KF_MEAS = 4
_KF_STATE = 8


def _kf_h() -> np.ndarray:
    h_mat = np.zeros((_KF_MEAS, _KF_STATE), dtype=np.float32)
    for idx in range(_KF_MEAS):
        h_mat[idx, idx] = 1.0
    return h_mat


def _kf_f(dt: float) -> np.ndarray:
    f_mat = np.eye(_KF_STATE, dtype=np.float32)
    # position += velocity * dt
    for idx in range(_KF_MEAS):
        f_mat[idx, idx + _KF_MEAS] = dt
    return f_mat


class _KalmanBox:
    """Minimal constant-velocity Kalman filter over (cx, cy, w, h)."""

    __slots__ = ("x", "P", "H", "last_dt")

    def __init__(self, bbox):
        cx, cy, w, h = _cx_cy_wh(bbox)
        w = max(w, 1.0)
        h = max(h, 1.0)
        self.x = np.array(
            [cx, cy, w, h, 0.0, 0.0, 0.0, 0.0], dtype=np.float32)
        self.P = np.eye(_KF_STATE, dtype=np.float32) * 10.0
        self.P[_KF_MEAS:, _KF_MEAS:] *= 100.0  # uncertainty on velocity
        self.H = _kf_h()
        self.last_dt = _KF_DT_DEFAULT

    def predict(self, dt: float) -> None:
        dt = max(dt, 1e-3)
        f_mat = _kf_f(dt)
        self.x = f_mat @ self.x
        q_mat = np.eye(_KF_STATE, dtype=np.float32)
        for i in range(_KF_MEAS):
            q_mat[i, i] = _KF_POS_PROCESS
        for i in range(_KF_MEAS, _KF_STATE):
            q_mat[i, i] = _KF_VEL_PROCESS * (dt * dt)
        self.P = f_mat @ self.P @ f_mat.T + q_mat
        self.last_dt = dt

    def correct(self, bbox) -> None:
        z = np.array(_cx_cy_wh(bbox), dtype=np.float32)
        r_mat = np.eye(_KF_MEAS, dtype=np.float32) * _KF_MEAS_NOISE
        hp = self.H @ self.P
        s_mat = hp @ self.H.T + r_mat
        k_mat = self.P @ self.H.T @ np.linalg.inv(s_mat)
        y = z - self.H @ self.x
        self.x = self.x + k_mat @ y
        ident = np.eye(_KF_STATE, dtype=np.float32)
        self.P = (ident - k_mat @ self.H) @ self.P

    def bbox(self) -> list:
        cx, cy, w, h = self.x[0], self.x[1], self.x[2], self.x[3]
        return [float(cx - w / 2), float(cy - h / 2), float(w), float(h)]

    @property
    def centroid(self) -> tuple:
        return float(self.x[0]), float(self.x[1])


def _cx_cy_wh(bbox) -> tuple:
    x, y, w, h = bbox[:4]
    return float(x + w / 2), float(y + h / 2), float(w), float(h)


def _clip_bbox(bbox, w, h) -> list:
    x, y, bw, bh = bbox[:4]
    x = max(0.0, float(x))
    y = max(0.0, float(y))
    bw = min(max(1.0, float(bw)), w - x)
    bh = min(max(1.0, float(bh)), h - y)
    return [x, y, bw, bh]


class CentroidTracker:
    """Centroid tracker with a Kalman model and staged association.

    Matching runs in stages from strong (IoU) to weak (centroid distance)
    cues so tracks survive motion, occlusion and missed detections without
    switching IDs. A lightweight visual template is consulted only to rescue
    tracks that are currently lost.
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
        self._kf: dict[int, _KalmanBox] = {}
        self._templates: dict[int, np.ndarray] = {}
        self._last_time: float | None = None

    def _new_color(self) -> tuple[int, int, int]:
        idx = (self._next_id - 1) % len(COLOR_PALETTE)
        return COLOR_PALETTE[idx]

    def _register(self, bbox: list, confidence: float, frame=None) -> int:
        track_id = self._next_id
        self._next_id += 1
        kf = _KalmanBox(bbox)
        self._kf[track_id] = kf
        self.objects[track_id] = {
            "centroid": kf.centroid,
            "bbox": kf.bbox(),
            "confidence": float(confidence),
        }
        self.disappeared[track_id] = 0
        self.colors[track_id] = self._new_color()
        if frame is not None:
            self._templates[track_id] = _template(frame, bbox)
        self.hit_streak[track_id] = 1
        return track_id

    @staticmethod
    def _centroid(bbox: list) -> tuple[float, float]:
        return _cx_cy_wh(bbox)[:2]

    def predict(self, dt: float | None = None) -> None:
        """Advance every track one Kalman step (no new measurements).

        Called by the streaming loop on every displayed frame so boxes coast
        with their velocity between the sparse detector runs.
        """
        now = time.monotonic()
        span = _KF_DT_DEFAULT
        if dt is not None:
            span = max(float(dt), 1e-3)
        elif self._last_time is not None:
            span = max(now - self._last_time, 1e-3)
        self._last_time = now

        for tid in list(self.objects):
            kf = self._kf.get(tid)
            if kf is None:
                continue
            kf.predict(span)
            self.objects[tid]["centroid"] = kf.centroid
            self.objects[tid]["bbox"] = kf.bbox()

    def update(
        self,
        detections: list[dict],
        frame: np.ndarray | None = None,
    ) -> dict[int, dict]:
        """Update tracker state with new detections.

        Args:
            detections: list of dicts with keys:
                        - bbox: [x1, y1, width, height]
                        - confidence: float
            frame: optional BGR frame (native coords) used to build/compare
                   lightweight appearance templates for lost-track rescue.

        Returns:
            dict of {track_id: {"centroid", "bbox", "confidence", "color"}}
        """
        if detections:
            self.predict()

        active_ids = [tid for tid in self.objects
                      if self.disappeared.get(tid, 0) == 0]
        lost_ids = [tid for tid in self.objects
                    if self.disappeared.get(tid, 0) > 0]

        # Each matched track maps to the detection index that corrected its
        # Kalman filter.
        matched_track_ids: set[int] = set()
        matched_det_indices: set[int] = set()

        det_boxes = [list(d["bbox"][:4]) for d in detections]

        # Stage 1-3: geometric matching of ACTIVE tracks via staged IoU.
        # Stronger overlap thresholds are tried first (PineSORT pattern) so a
        # clear, high-IoU match is locked before weaker cues get a chance.
        track_to_det: dict[int, int] = {}
        if active_ids:
            used_tracks: set[int] = set()
            used_dets: set[int] = set()
            for stage_iou in _ASSOCIATION_IOU_STAGES:
                threshold = stage_iou
                rem_tracks = [tid for tid in active_ids if tid not in used_tracks]
                rem_dets = [j for j in range(len(det_boxes)) if j not in used_dets]
                if not rem_tracks or not rem_dets:
                    continue
                ious = self._compute_ious_boxes(
                    [self.objects[tid]["bbox"] for tid in rem_tracks],
                    [det_boxes[j] for j in rem_dets],
                )
                order = np.dstack(
                    np.unravel_index(np.argsort(-ious.ravel(), kind="stable"),
                                     ious.shape)
                )[0]
                for ii, jj in order:
                    if ious[ii, jj] < threshold:
                        continue
                    tid = rem_tracks[ii]
                    det_j = rem_dets[jj]
                    used_tracks.add(tid)
                    used_dets.add(det_j)
                    matched_track_ids.add(tid)
                    matched_det_indices.add(det_j)
                    track_to_det[tid] = det_j

            # Stage 4: centroid-distance fallback for leftover active pairs.
            rem_tracks = [tid for tid in active_ids if tid not in used_tracks]
            rem_dets = [j for j in range(len(det_boxes)) if j not in used_dets]
            if rem_tracks and rem_dets and self.max_distance > 0:
                centroids_t = np.array(
                    [self.objects[tid]["centroid"] for tid in rem_tracks],
                    dtype=np.float32,
                )
                centroids_d = np.array(
                    [self._centroid(det_boxes[j]) for j in rem_dets],
                    dtype=np.float32,
                )
                dists = np.linalg.norm(
                    centroids_t[:, None, :] - centroids_d[None, :, :], axis=2
                )
                order = np.dstack(
                    np.unravel_index(np.argsort(dists.ravel(), kind="stable"),
                                     dists.shape)
                )[0]
                for ii, jj in order:
                    if dists[ii, jj] > self.max_distance:
                        continue
                    tid = rem_tracks[ii]
                    det_j = rem_dets[jj]
                    used_tracks.add(tid)
                    used_dets.add(det_j)
                    matched_track_ids.add(tid)
                    matched_det_indices.add(det_j)
                    track_to_det[tid] = det_j

        # Stage 5: appearance rescue for LOST tracks (no geometric match).
        if lost_ids and frame is not None:
            available_dets = [j for j in range(len(det_boxes))
                              if j not in matched_det_indices]
            for tid in lost_ids:
                if tid in matched_track_ids:
                    continue
                if self._templates.get(tid) is None:
                    continue
                best_sim = -1.0
                best_j = -1
                for j in available_dets:
                    sim = _template_sim(
                        self._templates[tid],
                        _template(frame, det_boxes[j]),
                    )
                    if sim > best_sim:
                        best_sim = sim
                        best_j = j
                if best_j >= 0 and best_sim >= 0.6:
                    matched_track_ids.add(tid)
                    matched_det_indices.add(best_j)
                    track_to_det[tid] = best_j
                    available_dets.remove(best_j)

        # Correct Kalman with the matched measurement.
        for tid in matched_track_ids:
            j = track_to_det[tid]
            kf = self._kf.get(tid)
            if kf is not None:
                kf.correct(det_boxes[j])
                self.objects[tid] = {
                    "centroid": kf.centroid,
                    "bbox": kf.bbox(),
                    "confidence": float(detections[j].get("confidence", 1.0)),
                }
            else:
                self.objects[tid] = {
                    "centroid": self._centroid(det_boxes[j]),
                    "bbox": det_boxes[j],
                    "confidence": float(detections[j].get("confidence", 1.0)),
                }
            self.disappeared[tid] = 0
            self.hit_streak[tid] = self.hit_streak.get(tid, 0) + 1
            # Refresh the appearance template with the freshest look.
            if frame is not None:
                self._templates[tid] = _template(frame, det_boxes[j])

        # Deregister / coast unmatched tracks.
        for tid in list(self.objects):
            if tid not in matched_track_ids:
                self.disappeared[tid] += 1
                if self.disappeared[tid] > self.max_disappeared:
                    self._deregister(tid)

        # Register unmatched new detections.
        for j, det in enumerate(detections):
            if j not in matched_det_indices:
                self._register(det["bbox"], det.get("confidence", 1.0), frame)

        return self._snapshot()

    def _compute_ious_boxes(self, boxes_a: list, boxes_b: list) -> np.ndarray:
        a = np.array(boxes_a, dtype=np.float32).reshape(-1, 4)
        b = np.array(boxes_b, dtype=np.float32).reshape(-1, 4)
        n, m = a.shape[0], b.shape[0]
        ious = np.zeros((n, m), dtype=np.float32)
        for i in range(n):
            for j in range(m):
                ious[i, j] = self._iou(a[i], b[j])
        return ious

    def _compute_ious(self, objects: dict, detections: list[dict]) -> np.ndarray:
        return self._compute_ious_boxes(
            [objects[tid]["bbox"] for tid in objects],
            [d["bbox"] for d in detections],
        )

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

    def _deregister(self, track_id: int) -> None:
        self.objects.pop(track_id, None)
        self.disappeared.pop(track_id, None)
        self.colors.pop(track_id, None)
        self.hit_streak.pop(track_id, None)
        self._kf.pop(track_id, None)
        self._templates.pop(track_id, None)

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

    def snapshot(self) -> dict[int, dict]:
        """Public accessor for the current visible (confirmed) tracks.

        Used by the detection thread to publish smooth, coasted state to the
        streaming loop between sparse detections.
        """
        return self._snapshot()

    def draw(self, frame: np.ndarray, tracked: dict[int, dict]) -> np.ndarray:
        """Draw bounding boxes, labels and a person-count overlay."""
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


def _template(frame: np.ndarray, bbox) -> np.ndarray:
    """HSV color histogram (normalized) inside the box — a cheap appearance
    descriptor robust to small scale changes and motion."""
    h, w = frame.shape[:2]
    x, y, bw, bh = _clip_bbox(bbox, w, h)
    patch = frame[int(y):int(y + bh), int(x):int(x + bw)]
    if patch.size == 0:
        return np.zeros((16,), dtype=np.float32)
    try:
        hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)
    except cv2.error:
        return np.zeros((16,), dtype=np.float32)
    hist = cv2.calcHist([hsv], [0, 1], None, [8, 8], [0, 180, 0, 256])
    cv2.normalize(hist, hist, norm_type=cv2.NORM_L1)
    return hist.astype(np.float32).ravel()


def _template_sim(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape or a.size == 0:
        return -1.0
    return float(np.sum(np.minimum(a, b)))
