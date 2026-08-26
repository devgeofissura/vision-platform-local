"""Crack label geometric processor — VP-008 hierarchical pipeline.

Mandatory stage order (spec §107):
  Full Image → Label Detection (ONLY detector on full image)
    → ROI Extraction → ROI Validation → Homography
      → Normalized Image → Internal Detection (markers, lines, circle, crack)
        → Measurements → Reference → Comparison

If label is not found → LABEL_NOT_FOUND. No fallback to global search.
"""

import logging
import math
import time
from dataclasses import dataclass, field

import cv2
import numpy as np

logger = logging.getLogger(__name__)

PROCESSING_VERSION = "2.0.0"

NORMALIZED_WIDTH = 1600
NORMALIZED_HEIGHT = 1000

LABEL_MIN_AREA_RATIO = 0.03
LABEL_MAX_AREA_RATIO = 0.95
LABEL_MIN_ASPECT_RATIO = 0.3
LABEL_MAX_ASPECT_RATIO = 3.0


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Point:
    x: float
    y: float

    def to_list(self) -> list[float]:
        return [round(self.x, 2), round(self.y, 2)]

    def distance_to(self, other: "Point") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


@dataclass
class Line:
    p1: Point
    p2: Point

    @property
    def angle_deg(self) -> float:
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        return round(math.degrees(math.atan2(dy, dx)), 2)

    @property
    def length(self) -> float:
        return self.p1.distance_to(self.p2)

    def to_dict(self) -> dict:
        return {
            "p1": self.p1.to_list(),
            "p2": self.p2.to_list(),
            "length": round(self.length, 2),
            "angle_deg": self.angle_deg,
        }


@dataclass
class Marker:
    label: str
    center: Point
    radius: float
    confidence: float

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "center": self.center.to_list(),
            "radius": round(self.radius, 2),
            "confidence": round(self.confidence, 3),
        }


@dataclass
class CrackAnalysis:
    label_corners: list[Point] = field(default_factory=list)
    label_detected: bool = False
    label_status: str = "NOT_PROCESSED"
    large_circle: dict | None = None
    markers: list[Marker] = field(default_factory=list)
    line_AB: Line | None = None  # noqa: N815
    line_CD: Line | None = None  # noqa: N815
    intersection: Point | None = None
    distances: dict = field(default_factory=dict)
    angles: dict = field(default_factory=dict)
    crack_lines: list[dict] = field(default_factory=list)
    quality_score: float = 0.0
    processing_ms: int = 0
    rectified_width: int = 0
    rectified_height: int = 0

    def to_dict(self) -> dict:
        return {
            "label_detected": self.label_detected,
            "label_status": self.label_status,
            "label_corners": [c.to_list() for c in self.label_corners],
            "large_circle": self.large_circle,
            "markers": [m.to_dict() for m in self.markers],
            "line_AB": self.line_AB.to_dict() if self.line_AB else None,
            "line_CD": self.line_CD.to_dict() if self.line_CD else None,
            "intersection": self.intersection.to_list() if self.intersection else None,
            "distances": self.distances,
            "angles": self.angles,
            "crack_lines": self.crack_lines,
            "quality_score": round(self.quality_score, 3),
            "processing_ms": self.processing_ms,
            "rectified_width": self.rectified_width,
            "rectified_height": self.rectified_height,
        }


# ---------------------------------------------------------------------------
# Processor — hierarchical pipeline
# ---------------------------------------------------------------------------

class CrackLabelProcessor:
    """Detects geometric elements of a crack monitoring label.

    Pipeline stages:
        STAGE 2: Label detection (full image)
        STAGE 3: ROI extraction
        STAGE 4: ROI validation
        STAGE 5: Perspective rectification
        STAGE 7: Internal element detection (normalized image only)
    """

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    # -----------------------------------------------------------------------
    # STAGE 0: Image quality
    # -----------------------------------------------------------------------

    def _check_image_quality(self, frame: np.ndarray) -> str:
        if frame is None or frame.size == 0:
            return "EMPTY_IMAGE"
        h, w = frame.shape[:2]
        if h < 100 or w < 100:
            return "IMAGE_TOO_SMALL"
        return "OK"

    # -----------------------------------------------------------------------
    # STAGE 2: Label detection — ONLY detector on full image
    # -----------------------------------------------------------------------

    def _detect_label(self, frame: np.ndarray) -> tuple[list[Point], dict]:
        """Detect white rectangular label on full image.

        Returns:
            (corners, metadata) — 4 ordered corners or empty list.
        """
        h, w = frame.shape[:2]
        img_area = h * w
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best_quad = None
        best_area = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < img_area * LABEL_MIN_AREA_RATIO or area > img_area * LABEL_MAX_AREA_RATIO:
                continue
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if len(approx) != 4:
                continue
            if area > best_area:
                pts = approx.reshape(4, 2).astype(np.float32)
                corners = self._order_corners(pts)
                if corners is not None:
                    best_quad = corners
                    best_area = area

        if best_quad is None:
            return [], {"reason": "no_quadrilateral_found"}

        corners = [Point(float(c[0]), float(c[1])) for c in best_quad]

        return corners, {
            "area": float(best_area),
            "area_ratio": float(best_area / img_area),
            "aspect_ratio": self._compute_aspect_ratio(corners),
        }

    def _order_corners(self, pts: np.ndarray) -> np.ndarray | None:
        """Order 4 points as TL, TR, BR, BL for homography.

        Returns None if points are degenerate (collinear).
        """
        if pts.shape != (4, 2):
            return None

        s = pts.sum(axis=1)
        d = np.diff(pts, axis=1).flatten()

        tl = pts[np.argmin(s)]
        br = pts[np.argmax(s)]
        tr = pts[np.argmin(d)]
        bl = pts[np.argmax(d)]

        ordered = np.array([tl, tr, br, bl], dtype=np.float32)

        area = cv2.contourArea(ordered)
        if area < 100:
            return None

        return ordered

    def _compute_aspect_ratio(self, corners: list[Point]) -> float:
        if len(corners) < 4:
            return 0.0
        w_top = corners[0].distance_to(corners[1])
        w_bot = corners[3].distance_to(corners[2])
        h_left = corners[0].distance_to(corners[3])
        h_right = corners[1].distance_to(corners[2])
        avg_w = (w_top + w_bot) / 2
        avg_h = (h_left + h_right) / 2
        if avg_h < 1:
            return 0.0
        return round(avg_w / avg_h, 3)

    # -----------------------------------------------------------------------
    # STAGE 4: ROI validation
    # -----------------------------------------------------------------------

    def _validate_roi(self, corners: list[Point]) -> str:
        """Validate that corners form a plausible label ROI.

        Returns "OK" or error status string.
        """
        if len(corners) != 4:
            return "NO_CORNERS"

        pts = np.array([[c.x, c.y] for c in corners], dtype=np.float32)
        area = cv2.contourArea(pts)
        if area < 500:
            return "ROI_TOO_SMALL"

        ar = self._compute_aspect_ratio(corners)
        if ar < LABEL_MIN_ASPECT_RATIO or ar > LABEL_MAX_ASPECT_RATIO:
            return "INVALID_ASPECT_RATIO"

        return "OK"

    # -----------------------------------------------------------------------
    # STAGE 5: Perspective rectification
    # -----------------------------------------------------------------------

    def _rectify_label(
        self, frame: np.ndarray, corners: list[Point]
    ) -> tuple[np.ndarray, list[Point]]:
        """Apply homography to get normalized frontal view of label.

        Returns:
            (rectified_image, canonical_corners) — the warped image and
            the 4 canonical corner positions in normalized space.
        """
        src = np.array(
            [[c.x, c.y] for c in corners], dtype=np.float32
        )

        dst = np.array([
            [0, 0],
            [NORMALIZED_WIDTH - 1, 0],
            [NORMALIZED_WIDTH - 1, NORMALIZED_HEIGHT - 1],
            [0, NORMALIZED_HEIGHT - 1],
        ], dtype=np.float32)

        mat = cv2.getPerspectiveTransform(src, dst)
        rectified = cv2.warpPerspective(
            frame, mat, (NORMALIZED_WIDTH, NORMALIZED_HEIGHT),
            flags=cv2.INTER_LINEAR,
        )

        canonical = [
            Point(0, 0),
            Point(NORMALIZED_WIDTH - 1, 0),
            Point(NORMALIZED_WIDTH - 1, NORMALIZED_HEIGHT - 1),
            Point(0, NORMALIZED_HEIGHT - 1),
        ]

        return rectified, canonical

    # -----------------------------------------------------------------------
    # STAGE 7: Internal element detection — NORMALIZED IMAGE ONLY
    # -----------------------------------------------------------------------

    def _detect_internal_elements(
        self, normalized_gray: np.ndarray
    ) -> tuple[list[Marker], dict | None, Line | None, Line | None, list[dict], Point | None]:
        """Run all internal detectors on the normalized (1600x1000) image.

        Parameters are calibrated for NORMALIZED_WIDTH x NORMALIZED_HEIGHT.
        No fallback to full image is allowed (spec §67).
        """
        blurred = cv2.GaussianBlur(normalized_gray, (7, 7), 0)

        large_circle = self._detect_large_circle_normalized(blurred)

        markers = self._detect_markers_normalized(blurred, large_circle)

        lines = self._detect_diagonal_lines_normalized(blurred)
        line_ab = lines[0] if len(lines) >= 1 else None
        line_cd = lines[1] if len(lines) >= 2 else None

        intersection = None
        if line_ab and line_cd:
            intersection = self._line_intersection(line_ab, line_cd)

        crack_lines = self._detect_crack_lines_normalized(blurred)

        return markers, large_circle, line_ab, line_cd, crack_lines, intersection

    def _detect_large_circle_normalized(self, gray: np.ndarray) -> dict | None:
        """Detect large reference circle on normalized 1600x1000 image."""
        min_r = 120
        max_r = 450

        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=200,
            param1=80, param2=40, minRadius=min_r, maxRadius=max_r,
        )
        if circles is None:
            return None

        circles = np.uint16(np.around(circles[0]))
        best = max(circles, key=lambda c: c[2])
        return {
            "center": [float(best[0]), float(best[1])],
            "radius": float(best[2]),
        }

    def _detect_markers_normalized(self, gray: np.ndarray, large_circle: dict | None) -> list[Marker]:
        """Detect 6 small marker circles on normalized 1600x1000 image."""
        min_r = 15
        max_r = 60
        min_dist = max_r * 2

        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, dp=1.5, minDist=min_dist,
            param1=50, param2=25, minRadius=min_r, maxRadius=max_r,
        )

        markers = []
        if circles is None:
            return markers

        for c in np.uint16(np.around(circles[0])):
            cx, cy, r = float(c[0]), float(c[1]), float(c[2])

            if large_circle:
                dist_to_center = math.hypot(
                    cx - large_circle["center"][0],
                    cy - large_circle["center"][1],
                )
                if dist_to_center < large_circle["radius"] * 0.3:
                    continue

            markers.append(Marker(
                label="",
                center=Point(cx, cy),
                radius=r,
                confidence=0.8,
            ))

        markers = self._assign_marker_labels_normalized(markers)
        return markers

    def _assign_marker_labels_normalized(self, markers: list[Marker]) -> list[Marker]:
        """Assign L1-L3 / R1-R3 labels based on normalized coordinates.

        In normalized space (1600x1000):
            Left half = L side (x < 800)
            Right half = R side (x >= 800)
            Top = lower y, Bottom = higher y
        """
        if len(markers) < 2:
            for i, m in enumerate(markers):
                m.label = f"M{i+1}"
            return markers

        mid_x = NORMALIZED_WIDTH / 2

        left_markers = sorted(
            [m for m in markers if m.center.x < mid_x],
            key=lambda m: m.center.y,
        )
        right_markers = sorted(
            [m for m in markers if m.center.x >= mid_x],
            key=lambda m: m.center.y,
        )

        labeled = []
        for i, m in enumerate(left_markers[:3]):
            m.label = f"L{i+1}"
            labeled.append(m)
        for i, m in enumerate(right_markers[:3]):
            m.label = f"R{i+1}"
            labeled.append(m)

        remaining = [
            m for m in markers
            if m not in labeled
        ]
        for i, m in enumerate(remaining[:6 - len(labeled)]):
            m.label = f"X{i+1}"
            labeled.append(m)

        return labeled

    def _detect_diagonal_lines_normalized(self, gray: np.ndarray) -> list[Line]:
        """Detect diagonal lines AB and CD on normalized 1600x1000 image."""
        edges = cv2.Canny(gray, 50, 150)
        min_line_len = 200

        lines = cv2.HoughLinesP(
            edges, 1, np.pi / 180, threshold=30,
            minLineLength=min_line_len, maxLineGap=30,
        )
        if lines is None:
            return []

        segments = []
        for line in lines:
            flat = line.ravel()
            x1, y1, x2, y2 = int(flat[0]), int(flat[1]), int(flat[2]), int(flat[3])
            angle = abs(math.degrees(math.atan2(y2 - y1, x2 - x1)))
            length = math.hypot(x2 - x1, y2 - y1)
            if 15 < angle < 165 and length > min_line_len:
                segments.append(Line(Point(x1, y1), Point(x2, y2)))

        if len(segments) < 2:
            return []

        segments.sort(key=lambda s: s.length, reverse=True)
        selected = [segments[0]]
        for seg in segments[1:]:
            angle_diff = abs(seg.angle_deg - selected[0].angle_deg)
            if angle_diff > 20 or angle_diff < -20:
                selected.append(seg)
                if len(selected) >= 2:
                    break

        return selected[:2]

    def _line_intersection(self, line_a: Line, line_b: Line) -> Point | None:
        x1, y1 = line_a.p1.x, line_a.p1.y
        x2, y2 = line_a.p2.x, line_a.p2.y
        x3, y3 = line_b.p1.x, line_b.p1.y
        x4, y4 = line_b.p2.x, line_b.p2.y

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-10:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)

        if 0 <= ix <= NORMALIZED_WIDTH and 0 <= iy <= NORMALIZED_HEIGHT:
            return Point(ix, iy)
        return None

    def _detect_crack_lines_normalized(self, gray: np.ndarray) -> list[dict]:
        """Detect crack line segments on normalized 1600x1000 image."""
        edges = cv2.Canny(gray, 40, 120)
        min_len = 80

        lines = cv2.HoughLinesP(
            edges, 1, np.pi / 180, threshold=15,
            minLineLength=min_len, maxLineGap=15,
        )
        if lines is None:
            return []

        crack_lines = []
        for line in lines[:10]:
            flat = line.ravel()
            x1, y1, x2, y2 = int(flat[0]), int(flat[1]), int(flat[2]), int(flat[3])
            length = math.hypot(x2 - x1, y2 - y1)
            angle = abs(math.degrees(math.atan2(y2 - y1, x2 - x1)))
            crack_lines.append({
                "points": [[int(x1), int(y1)], [int(x2), int(y2)]],
                "length": round(float(length), 2),
                "angle_deg": round(float(angle), 2),
            })

        return crack_lines

    # -----------------------------------------------------------------------
    # Measurements (on normalized coordinates)
    # -----------------------------------------------------------------------

    def _sort_markers(self, markers: list[Marker]) -> dict[str, Marker]:
        result = {}
        for m in markers:
            if m.label:
                result[m.label] = m
        return result

    def _compute_distances(self, sorted_markers: dict[str, Marker]) -> dict:
        distances = {}
        for side in ["L", "R"]:
            for i in range(1, 3):
                k1 = f"{side}{i}"
                k2 = f"{side}{i+1}"
                if k1 in sorted_markers and k2 in sorted_markers:
                    d = sorted_markers[k1].center.distance_to(sorted_markers[k2].center)
                    distances[f"distance_{k1}_{k2}"] = round(d, 2)

        for i in range(1, 4):
            lk = f"L{i}"
            rk = f"R{i}"
            if lk in sorted_markers and rk in sorted_markers:
                d = sorted_markers[lk].center.distance_to(sorted_markers[rk].center)
                distances[f"distance_{lk}_{rk}"] = round(d, 2)

        return distances

    def _compute_angles(
        self,
        sorted_markers: dict[str, Marker],
        line_AB: Line | None,  # noqa: N803
        line_CD: Line | None,  # noqa: N803
    ) -> dict:
        angles = {}

        if line_AB and line_CD:
            a1 = math.radians(line_AB.angle_deg)
            a2 = math.radians(line_CD.angle_deg)
            diff = abs(math.degrees(a1 - a2))
            if diff > 180:
                diff = 360 - diff
            angles["angle_AB_CD"] = round(diff, 2)

        for side in ["L", "R"]:
            for i in range(1, 3):
                k1 = f"{side}{i}"
                k2 = f"{side}{i+1}"
                if k1 in sorted_markers and k2 in sorted_markers:
                    p1 = sorted_markers[k1].center
                    p2 = sorted_markers[k2].center
                    angle = math.degrees(math.atan2(p2.y - p1.y, p2.x - p1.x))
                    angles[f"orientation_{k1}_{k2}"] = round(angle, 2)

        return angles

    # -----------------------------------------------------------------------
    # Main pipeline
    # -----------------------------------------------------------------------

    def process(self, frame: np.ndarray) -> CrackAnalysis:
        """Run the full hierarchical pipeline.

        Stage order (spec §107):
            Image Quality → Label Detection → ROI Validation
            → Homography → Internal Detection → Measurements
        """
        start = time.perf_counter()
        analysis = CrackAnalysis()

        quality = self._check_image_quality(frame)
        if quality != "OK":
            analysis.label_status = quality
            analysis.processing_ms = int((time.perf_counter() - start) * 1000)
            return analysis

        corners, label_meta = self._detect_label(frame)
        analysis.label_corners = corners

        if len(corners) == 4:
            analysis.label_detected = True
            analysis.quality_score += 0.3
        else:
            analysis.label_status = "LABEL_NOT_FOUND"
            analysis.processing_ms = int((time.perf_counter() - start) * 1000)
            logger.warning("Label not found: %s", label_meta.get("reason", "unknown"))
            return analysis

        roi_status = self._validate_roi(corners)
        if roi_status != "OK":
            analysis.label_status = roi_status
            analysis.processing_ms = int((time.perf_counter() - start) * 1000)
            logger.warning("ROI validation failed: %s", roi_status)
            return analysis

        rectified, canonical = self._rectify_label(frame, corners)
        analysis.rectified_width = rectified.shape[1]
        analysis.rectified_height = rectified.shape[0]
        analysis.label_corners = corners
        analysis.label_status = "OK"
        analysis.quality_score += 0.2

        rectified_gray = cv2.cvtColor(rectified, cv2.COLOR_BGR2GRAY)

        (
            markers,
            large_circle,
            line_ab,
            line_cd,
            crack_lines,
            intersection,
        ) = self._detect_internal_elements(rectified_gray)

        analysis.markers = markers
        analysis.large_circle = large_circle
        analysis.crack_lines = crack_lines

        if len(markers) >= 6:
            analysis.quality_score += 0.3

        if large_circle:
            analysis.quality_score += 0.1

        sorted_markers = self._sort_markers(markers)

        if line_ab and line_cd:
            analysis.line_AB = line_ab
            analysis.line_CD = line_cd
            analysis.quality_score += 0.1
            if intersection:
                analysis.intersection = intersection
                analysis.quality_score += 0.1

        analysis.distances = self._compute_distances(sorted_markers)
        analysis.angles = self._compute_angles(sorted_markers, analysis.line_AB, analysis.line_CD)

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        analysis.processing_ms = elapsed_ms
        analysis.quality_score = min(analysis.quality_score, 1.0)

        logger.info(
            "CrackAnalysis v%s: label=%s, status=%s, %d markers, "
            "AB=%s, CD=%s, intersection=%s, %d crack_lines, %.0fms",
            PROCESSING_VERSION,
            "yes" if analysis.label_detected else "no",
            analysis.label_status,
            len(markers),
            "yes" if analysis.line_AB else "no",
            "yes" if analysis.line_CD else "no",
            "yes" if analysis.intersection else "no",
            len(crack_lines),
            elapsed_ms,
        )
        return analysis

    # -----------------------------------------------------------------------
    # Overlay — dual view: original with ROI + normalized with detections
    # -----------------------------------------------------------------------

    def draw_overlay(self, frame: np.ndarray, analysis: CrackAnalysis) -> np.ndarray:
        """Draw analysis overlay as dual panel.

        Left: original image with ROI rectangle and corners.
        Right: normalized image with internal detections.
        """
        if not analysis.label_detected or analysis.label_status != "OK":
            return self._draw_no_label_overlay(frame, analysis)

        rectified_bgr = self._rectify_label(frame, analysis.label_corners)[0]

        h_orig, w_orig = frame.shape[:2]
        h_norm, w_norm = rectified_bgr.shape[:2]

        panel_w = max(w_orig, w_norm)
        panel_h = h_orig + h_norm + 40
        canvas = np.zeros((panel_h, panel_w, 3), dtype=np.uint8)
        canvas[:] = (40, 40, 40)

        canvas[:h_orig, :w_orig] = frame.copy()
        canvas[h_orig + 40:h_orig + 40 + h_norm, :w_norm] = rectified_bgr

        self._draw_label_roi(canvas, analysis, w_orig, h_orig)
        self._draw_normalized_detections(canvas, analysis, h_orig + 40, w_norm, h_norm)

        self._draw_measurements_panel(canvas, analysis)

        cv2.putText(
            canvas, "ORIGINAL + ROI", (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2, cv2.LINE_AA,
        )
        cv2.putText(
            canvas, "NORMALIZED (1600x1000)", (10, h_orig + 65),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2, cv2.LINE_AA,
        )

        return canvas

    def _draw_no_label_overlay(self, frame: np.ndarray, analysis: CrackAnalysis) -> np.ndarray:
        overlay = frame.copy()
        h, w = overlay.shape[:2]

        cv2.rectangle(overlay, (0, 0), (w, 60), (20, 20, 80), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        cv2.putText(
            frame, f"Label: {analysis.label_status}",
            (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 100, 255), 2, cv2.LINE_AA,
        )
        cv2.putText(
            frame, f"Quality: {analysis.quality_score:.2f}",
            (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2, cv2.LINE_AA,
        )

        return frame

    def _draw_label_roi(self, canvas: np.ndarray, analysis: CrackAnalysis, w: int, h: int) -> None:
        if len(analysis.label_corners) != 4:
            return

        green = (0, 255, 0)
        thickness = 3

        pts = np.array(
            [[int(c.x), int(c.y)] for c in analysis.label_corners],
            dtype=np.int32,
        )
        cv2.polylines(canvas, [pts], True, green, thickness, cv2.LINE_AA)

        for i, corner in enumerate(analysis.label_corners):
            cv2.circle(canvas, (int(corner.x), int(corner.y)), 8, green, -1, cv2.LINE_AA)
            cv2.putText(
                canvas, f"C{i+1}",
                (int(corner.x + 12), int(corner.y - 12)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, green, 2, cv2.LINE_AA,
            )

    def _draw_normalized_detections(
        self, canvas: np.ndarray, analysis: CrackAnalysis,
        y_offset: int, w: int, h: int,
    ) -> None:
        green = (0, 255, 0)
        yellow = (0, 255, 255)
        cyan = (255, 255, 0)
        red = (0, 0, 255)
        thickness = 2

        if analysis.large_circle:
            cx = int(analysis.large_circle["center"][0])
            cy = int(analysis.large_circle["center"][1]) + y_offset
            r = int(analysis.large_circle["radius"])
            cv2.circle(canvas, (cx, cy), r, cyan, thickness, cv2.LINE_AA)
            cv2.circle(canvas, (cx, cy), 5, cyan, -1, cv2.LINE_AA)

        for marker in analysis.markers:
            cx = int(marker.center.x)
            cy = int(marker.center.y) + y_offset
            r = max(3, int(marker.radius * 0.6))
            cv2.circle(canvas, (cx, cy), r, green, -1, cv2.LINE_AA)
            cv2.circle(canvas, (cx, cy), int(marker.radius), green, thickness, cv2.LINE_AA)
            cv2.putText(
                canvas, marker.label,
                (cx + 12, cy - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, green, 2, cv2.LINE_AA,
            )

        for line in [analysis.line_AB, analysis.line_CD]:
            if line:
                p1 = (int(line.p1.x), int(line.p1.y) + y_offset)
                p2 = (int(line.p2.x), int(line.p2.y) + y_offset)
                cv2.line(canvas, p1, p2, green, thickness + 1, cv2.LINE_AA)
                mid_x = int((line.p1.x + line.p2.x) / 2 + 15)
                mid_y = int((line.p1.y + line.p2.y) / 2 - 10) + y_offset
                label = "AB" if line == analysis.line_AB else "CD"
                cv2.putText(
                    canvas, f"{label} {line.length:.0f}px {line.angle_deg:.1f}deg",
                    (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, green,
                    1, cv2.LINE_AA,
                )

        if analysis.intersection:
            ix = int(analysis.intersection.x)
            iy = int(analysis.intersection.y) + y_offset
            cv2.circle(canvas, (ix, iy), 10, yellow, -1, cv2.LINE_AA)
            cv2.circle(canvas, (ix, iy), 13, yellow, thickness, cv2.LINE_AA)
            cv2.putText(
                canvas, "INTERSECT",
                (ix + 15, iy + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, yellow, 2, cv2.LINE_AA,
            )

        for crack in analysis.crack_lines:
            pts = crack.get("points", [])
            if len(pts) >= 2:
                for i in range(len(pts) - 1):
                    p1 = (int(pts[i][0]), int(pts[i][1]) + y_offset)
                    p2 = (int(pts[i+1][0]), int(pts[i+1][1]) + y_offset)
                    cv2.line(canvas, p1, p2, red, thickness + 1, cv2.LINE_AA)

    def _draw_measurements_panel(self, canvas: np.ndarray, analysis: CrackAnalysis) -> None:
        h, w = canvas.shape[:2]
        panel_w = 300
        n_dist = len(analysis.distances)
        n_angles = len(analysis.angles)
        panel_h = min(n_dist * 22 + n_angles * 22 + 80, h - 20)

        x0 = w - panel_w - 10
        y0 = 10

        overlay_region = canvas[y0:y0 + panel_h, x0:x0 + panel_w].copy()
        cv2.rectangle(canvas, (x0, y0), (x0 + panel_w, y0 + panel_h), (30, 30, 30), -1)
        canvas[y0:y0 + panel_h, x0:x0 + panel_w] = cv2.addWeighted(
            overlay_region, 0.3,
            canvas[y0:y0 + panel_h, x0:x0 + panel_w], 0.7, 0,
        )

        y = y0 + 25
        font = cv2.FONT_HERSHEY_SIMPLEX
        green = (0, 255, 0)

        cv2.putText(canvas, "DISTANCES", (x0 + 10, y), font, 0.55, green, 2, cv2.LINE_AA)
        y += 25

        for key, val in analysis.distances.items():
            cv2.putText(canvas, f"{key}: {val:.1f}px", (x0 + 10, y), font, 0.42, green, 1, cv2.LINE_AA)
            y += 20

        y += 10
        cv2.putText(canvas, "ANGLES", (x0 + 10, y), font, 0.55, green, 2, cv2.LINE_AA)
        y += 25

        for key, val in analysis.angles.items():
            cv2.putText(canvas, f"{key}: {val:.1f}deg", (x0 + 10, y), font, 0.42, green, 1, cv2.LINE_AA)
            y += 20
