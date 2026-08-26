"""Crack label geometric processor.

Detects the physical label elements (6 markers, large circle, lines AB/CD)
and computes geometric measurements for crack monitoring.
"""

import logging
import math
from dataclasses import dataclass, field

import cv2
import numpy as np

logger = logging.getLogger(__name__)

PROCESSING_VERSION = "1.0.0"


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
    large_circle: dict | None = None
    markers: list[Marker] = field(default_factory=list)
    line_AB: Line | None = None  # noqa: N815 — matches spec
    line_CD: Line | None = None  # noqa: N815 — matches spec
    intersection: Point | None = None
    distances: dict = field(default_factory=dict)
    angles: dict = field(default_factory=dict)
    crack_lines: list[dict] = field(default_factory=list)
    quality_score: float = 0.0
    processing_ms: int = 0

    def to_dict(self) -> dict:
        return {
            "label_corners": [c.to_list() for c in self.label_corners],
            "large_circle": self.large_circle,
            "markers": [m.to_list() for m in self.markers],
            "line_AB": self.line_AB.to_dict() if self.line_AB else None,
            "line_CD": self.line_CD.to_dict() if self.line_CD else None,
            "intersection": self.intersection.to_list() if self.intersection else None,
            "distances": self.distances,
            "angles": self.angles,
            "crack_lines": self.crack_lines,
            "quality_score": round(self.quality_score, 3),
            "processing_ms": self.processing_ms,
        }


class CrackLabelProcessor:
    """Detects geometric elements of a crack monitoring label."""

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def process(self, frame: np.ndarray) -> CrackAnalysis:
        import time

        start = time.perf_counter()
        analysis = CrackAnalysis()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        corners = self._detect_label_corners(blurred)
        analysis.label_corners = corners

        if len(corners) == 4:
            analysis.quality_score += 0.3

        large_circle = self._detect_large_circle(blurred, frame.shape)
        analysis.large_circle = large_circle
        if large_circle:
            analysis.quality_score += 0.2

        markers = self._detect_markers(blurred, corners, frame.shape)
        analysis.markers = markers
        if len(markers) >= 6:
            analysis.quality_score += 0.3

        sorted_markers = self._sort_markers(markers)

        lines = self._detect_diagonal_lines(blurred, large_circle, frame.shape)
        if len(lines) >= 2:
            analysis.line_AB = lines[0]
            analysis.line_CD = lines[1]
            analysis.quality_score += 0.1
            intersection = self._line_intersection(lines[0], lines[1])
            if intersection:
                analysis.intersection = intersection
                analysis.quality_score += 0.1

        analysis.distances = self._compute_distances(sorted_markers)
        analysis.angles = self._compute_angles(sorted_markers, analysis.line_AB, analysis.line_CD)

        analysis.crack_lines = self._detect_crack_lines(blurred, frame.shape)

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        analysis.processing_ms = elapsed_ms
        analysis.quality_score = min(analysis.quality_score, 1.0)

        logger.info(
            "CrackAnalysis: %d corners, %d markers, AB=%s, CD=%s, intersection=%s, %.0fms",
            len(corners),
            len(markers),
            "yes" if analysis.line_AB else "no",
            "yes" if analysis.line_CD else "no",
            "yes" if analysis.intersection else "no",
            elapsed_ms,
        )
        return analysis

    def draw_overlay(self, frame: np.ndarray, analysis: CrackAnalysis) -> np.ndarray:
        overlay = frame.copy()
        h, w = overlay.shape[:2]
        scale = max(1.0, min(w, h) / 800)

        def _pt(p: Point) -> tuple[int, int]:
            return (int(p.x), int(p.y))

        def _color(color_bgr: tuple[int, int, int]) -> tuple[int, int, int]:
            return color_bgr

        green = _color((0, 255, 0))
        yellow = _color((0, 255, 255))
        cyan = _color((255, 255, 0))
        red = _color((0, 0, 255))
        thickness = max(2, int(2 * scale))

        if len(analysis.label_corners) == 4:
            pts = np.array([[_pt(c) for c in analysis.label_corners]], dtype=np.int32)
            cv2.polylines(overlay, [pts], True, green, thickness, cv2.LINE_AA)
            for i, corner in enumerate(analysis.label_corners):
                cv2.circle(overlay, _pt(corner), int(6 * scale), green, -1, cv2.LINE_AA)
                cv2.putText(
                    overlay, f"C{i+1}",
                    (int(corner.x + 8 * scale), int(corner.y - 8 * scale)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5 * scale, green, max(1, int(scale)),
                    cv2.LINE_AA,
                )

        if analysis.large_circle:
            cx = int(analysis.large_circle["center"][0])
            cy = int(analysis.large_circle["center"][1])
            r = int(analysis.large_circle["radius"])
            cv2.circle(overlay, (cx, cy), r, cyan, thickness, cv2.LINE_AA)
            cv2.circle(overlay, (cx, cy), int(4 * scale), cyan, -1, cv2.LINE_AA)

        for marker in analysis.markers:
            c = _pt(marker.center)
            r = max(3, int(marker.radius * 0.6))
            cv2.circle(overlay, c, r, green, -1, cv2.LINE_AA)
            cv2.circle(overlay, c, int(marker.radius), green, thickness, cv2.LINE_AA)
            label_pos = (int(marker.center.x + 10 * scale), int(marker.center.y - 10 * scale))
            cv2.putText(
                overlay, marker.label, label_pos,
                cv2.FONT_HERSHEY_SIMPLEX, 0.5 * scale, green, max(1, int(scale)),
                cv2.LINE_AA,
            )

        for line in [analysis.line_AB, analysis.line_CD]:
            if line:
                cv2.line(overlay, _pt(line.p1), _pt(line.p2), green, thickness + 1, cv2.LINE_AA)
                mid_x = int((line.p1.x + line.p2.x) / 2 + 15 * scale)
                mid_y = int((line.p1.y + line.p2.y) / 2 - 10 * scale)
                label = "AB" if line == analysis.line_AB else "CD"
                cv2.putText(
                    overlay, f"{label} {line.length:.0f}px {line.angle_deg:.1f}deg",
                    (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45 * scale, green,
                    max(1, int(scale)), cv2.LINE_AA,
                )

        if analysis.intersection:
            c = _pt(analysis.intersection)
            cv2.circle(overlay, c, int(8 * scale), yellow, -1, cv2.LINE_AA)
            cv2.circle(overlay, c, int(10 * scale), yellow, thickness, cv2.LINE_AA)
            cv2.putText(
                overlay, "INTERSECT",
                (int(analysis.intersection.x + 12 * scale), int(analysis.intersection.y + 5 * scale)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45 * scale, yellow, max(1, int(scale)),
                cv2.LINE_AA,
            )

        for crack in analysis.crack_lines:
            pts = crack.get("points", [])
            if len(pts) >= 2:
                for i in range(len(pts) - 1):
                    cv2.line(
                        overlay,
                        (int(pts[i][0]), int(pts[i][1])),
                        (int(pts[i+1][0]), int(pts[i+1][1])),
                        red, thickness + 1, cv2.LINE_AA,
                    )

        self._draw_measurements_panel(overlay, analysis, scale)

        return overlay

    def _detect_label_corners(self, gray: np.ndarray) -> list[Point]:
        edges = cv2.Canny(gray, 30, 100)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=3)
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best_quad = None
        best_area = 0
        h, w = gray.shape[:2]
        img_area = h * w

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < img_area * 0.05 or area > img_area * 0.95:
                continue
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if len(approx) == 4 and area > best_area:
                best_quad = approx
                best_area = area

        if best_quad is None:
            return []

        pts = best_quad.reshape(4, 2).astype(float)
        center = pts.mean(axis=0)
        angles = np.arctan2(pts[:, 1] - center[1], pts[:, 0] - center[0])
        order = np.argsort(angles)
        ordered = pts[order]

        tl = ordered[np.argmin(ordered[:, 0] + ordered[:, 1])]
        tr = ordered[np.argmax(ordered[:, 0] - ordered[:, 1])]
        br = ordered[np.argmax(ordered[:, 0] + ordered[:, 1])]
        bl = ordered[np.argmin(ordered[:, 0] - ordered[:, 1])]

        return [Point(tl[0], tl[1]), Point(tr[0], tr[1]), Point(br[0], br[1]), Point(bl[0], bl[1])]

    def _detect_large_circle(self, gray: np.ndarray, shape: tuple) -> dict | None:
        h, w = shape[:2]
        min_r = int(min(h, w) * 0.08)
        max_r = int(min(h, w) * 0.45)

        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=min_r,
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

    def _detect_markers(
        self, gray: np.ndarray, corners: list[Point], shape: tuple
    ) -> list[Marker]:
        h, w = shape[:2]
        min_marker_r = int(min(h, w) * 0.005)
        max_marker_r = int(min(h, w) * 0.04)
        min_dist = max_marker_r * 2

        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, dp=1.5, minDist=min_dist,
            param1=50, param2=25, minRadius=min_marker_r, maxRadius=max_marker_r,
        )

        markers = []
        if circles is None:
            return markers

        for c in np.uint16(np.around(circles[0])):
            cx, cy, r = float(c[0]), float(c[1]), float(c[2])
            markers.append(Marker(
                label="",
                center=Point(cx, cy),
                radius=r,
                confidence=0.8,
            ))

        markers = self._assign_marker_labels(markers, corners)
        return markers

    def _assign_marker_labels(self, markers: list[Marker], corners: list[Point]) -> list[Marker]:
        if len(markers) < 6 or len(corners) < 4:
            for i, m in enumerate(markers):
                m.label = f"M{i+1}"
            return markers

        tl, tr, br, bl = corners
        mid_left = Point((tl.x + bl.x) / 2, (tl.y + bl.y) / 2)
        mid_right = Point((tr.x + br.x) / 2, (tr.y + br.y) / 2)

        for m in markers:
            dist_to_left = m.center.distance_to(mid_left)
            dist_to_right = m.center.distance_to(mid_right)
            m._side = "L" if dist_to_left < dist_to_right else "R"

        left_markers = sorted(
            [m for m in markers if m._side == "L"],
            key=lambda m: m.center.y,
        )
        right_markers = sorted(
            [m for m in markers if m._side == "R"],
            key=lambda m: m.center.y,
        )

        labeled = []
        for i, m in enumerate(left_markers[:3]):
            m.label = f"L{i+1}"
            labeled.append(m)
        for i, m in enumerate(right_markers[:3]):
            m.label = f"R{i+1}"
            labeled.append(m)

        return labeled

    def _detect_diagonal_lines(
        self, gray: np.ndarray, large_circle: dict | None, shape: tuple
    ) -> list[Line]:
        edges = cv2.Canny(gray, 50, 150)
        h, w = shape[:2]
        min_line_len = int(min(h, w) * 0.1)

        lines = cv2.HoughLinesP(
            edges, 1, np.pi / 180, threshold=30,
            minLineLength=min_line_len, maxLineGap=20,
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
        return Point(ix, iy)

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
        line_AB: Line | None,  # noqa: N803 — matches spec
        line_CD: Line | None,  # noqa: N803 — matches spec
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

    def _detect_crack_lines(self, gray: np.ndarray, shape: tuple) -> list[dict]:
        edges = cv2.Canny(gray, 40, 120)
        h, w = shape[:2]
        min_len = int(min(h, w) * 0.05)

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

    def _draw_measurements_panel(
        self, frame: np.ndarray, analysis: CrackAnalysis, scale: float
    ) -> None:
        h, w = frame.shape[:2]
        panel_w = int(280 * scale)
        panel_h = int(len(analysis.distances) * 22 * scale + len(analysis.angles) * 22 * scale + 60 * scale)
        panel_h = min(panel_h, h - 20)

        x0 = w - panel_w - 10
        y0 = 10

        overlay = frame.copy()
        cv2.rectangle(overlay, (x0, y0), (x0 + panel_w, y0 + panel_h), (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        y = y0 + int(20 * scale)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 0.4 * scale
        green = (0, 255, 0)

        cv2.putText(frame, "DISTANCES", (x0 + 10, y), font, fs * 1.1, green, max(1, int(scale)), cv2.LINE_AA)
        y += int(20 * scale)

        for key, val in analysis.distances.items():
            text = f"{key}: {val:.1f}px"
            cv2.putText(frame, text, (x0 + 10, y), font, fs, green, max(1, int(scale)), cv2.LINE_AA)
            y += int(18 * scale)

        y += int(8 * scale)
        cv2.putText(frame, "ANGLES", (x0 + 10, y), font, fs * 1.1, green, max(1, int(scale)), cv2.LINE_AA)
        y += int(20 * scale)

        for key, val in analysis.angles.items():
            text = f"{key}: {val:.1f}deg"
            cv2.putText(frame, text, (x0 + 10, y), font, fs, green, max(1, int(scale)), cv2.LINE_AA)
            y += int(18 * scale)
