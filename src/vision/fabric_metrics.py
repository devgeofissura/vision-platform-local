"""Fabric inspection metrics: defect dimension measurement, roll meterage
estimation by vision, and the industrial 4-Point grading system (ASTM D5430).

The 4-Point System assigns penalty points to each defect based on its length:

    <= 75 mm ................ 1 point
    75  < length <= 150 mm .. 2 points
    150 < length <= 230 mm .. 3 points
    > 230 mm ................ 4 points

Holes always score 4 points regardless of size. A single defect never scores
more than 4 points, and no linear meter may accumulate more than 4 points.

Roll/shipment acceptability is expressed as points per 100 m^2:

    points/100m2 = (total_points * 100000) / (inspected_meters * fabric_width_mm)

Typical acceptance thresholds (per 100 m^2): worsted/woolens 24, knits 30,
linen blends 40-48. Most mills use 24 as the passing score.
"""

from __future__ import annotations

from dataclasses import dataclass

MAX_POINTS_PER_DEFECT = 4.0
MAX_POINTS_PER_LINEAR_METER = 4.0

# Defect length thresholds in millimeters (4-Point System).
POINT_THRESHOLDS_MM = (75.0, 150.0, 230.0)
POINT_VALUES = (1.0, 2.0, 3.0, 4.0)

# Defect types that always score 4 points regardless of size.
ALWAYS_MAX_DEFECT_TYPES = {"hole", "tear"}


@dataclass
class DefectMeasurement:
    """A fabric defect with real-dimension measurements and its penalty score."""

    defect_type: str
    confidence: float
    bbox_px: list[float]
    length_cm: float
    width_cm: float
    area_cm2: float
    points: float
    severity: str


@dataclass
class FabricCalibrator:
    """Convert between pixels and real centimeters using a known fabric width.

    The fabric fills ``fabric_width_px`` pixels across the frame while its
    physical width (selvedge to selvedge) is ``fabric_width_cm``. This yields
    a local pixel-per-cm ratio used to measure every defect in the frame.

    If ``fabric_width_cm`` is not known, ``calibrated`` is False and defect
    dimensions fall back to raw pixels (cm == px) so the pipeline still runs.
    """

    fabric_width_cm: float = 0.0
    fabric_width_px: float = 0.0

    @property
    def calibrated(self) -> bool:
        return self.fabric_width_cm > 0 and self.fabric_width_px > 0

    def px_per_cm(self) -> float:
        if not self.calibrated:
            return 1.0
        return self.fabric_width_px / self.fabric_width_cm

    def px_to_cm(self, px: float) -> float:
        if not self.calibrated:
            return float(px)
        ratio = self.px_per_cm()
        return float(px) / ratio if ratio else 0.0

    def area_px_to_cm2(self, area_px: float) -> float:
        if not self.calibrated:
            return float(area_px)
        ratio = self.px_per_cm()
        return float(area_px) / (ratio * ratio) if ratio else 0.0


def score_defect(defect_type: str, length_mm: float) -> float:
    """Return the 4-Point System penalty for a defect of a given length.

    ``length_mm`` is the longest dimension (lengthwise or breadthwise) of the
    defect in millimeters. Holes/tears and lengths over the top threshold score
    the maximum (4 points). Never returns more than ``MAX_POINTS_PER_DEFECT``.
    """
    if defect_type in ALWAYS_MAX_DEFECT_TYPES:
        return MAX_POINTS_PER_DEFECT

    if length_mm <= POINT_THRESHOLDS_MM[0]:
        return POINT_VALUES[0]
    if length_mm <= POINT_THRESHOLDS_MM[1]:
        return POINT_VALUES[1]
    if length_mm <= POINT_THRESHOLDS_MM[2]:
        return POINT_VALUES[2]
    return POINT_VALUES[3]


def _severity_from_points(points: float) -> str:
    if points >= 4.0:
        return "high"
    if points >= 2.0:
        return "medium"
    return "low"


def measure_defects(
    detections: list,
    calibrator: FabricCalibrator,
    frame_width_px: int = 0,
) -> list[DefectMeasurement]:
    """Measure each detection in real dimensions and score it.

    ``detections`` is a list of objects (ProcessingResult) with a
    ``result_data`` dict containing ``defect_type`` and ``bbox`` = [x, y, w, h]
    in pixels. Returns a list of :class:`DefectMeasurement`.
    """
    if frame_width_px > 0 and calibrator.fabric_width_cm > 0:
        working = FabricCalibrator(
            fabric_width_cm=calibrator.fabric_width_cm,
            fabric_width_px=float(frame_width_px),
        )
    else:
        working = calibrator

    measurements = []
    for det in detections:
        data = getattr(det, "result_data", None) or {}
        defect_type = data.get("defect_type", "stain")
        bbox = data.get("bbox")
        if not bbox or len(bbox) < 4:
            continue
        x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
        length_cm = working.px_to_cm(max(w, h))
        width_cm = working.px_to_cm(min(w, h))
        area_cm2 = working.area_px_to_cm2(float(w) * float(h))

        length_mm = length_cm * 10.0
        points = score_defect(defect_type, length_mm)
        measurements.append(DefectMeasurement(
            defect_type=defect_type,
            confidence=float(getattr(det, "confidence", 0.0) or 0.0),
            bbox_px=[float(x), float(y), float(w), float(h)],
            length_cm=round(length_cm, 2),
            width_cm=round(width_cm, 2),
            area_cm2=round(area_cm2, 2),
            points=points,
            severity=_severity_from_points(points),
        ))
    return measurements


def points_per_100m2(total_points: float, inspected_meters: float, fabric_width_cm: float) -> float:
    """Compute points per 100 square meters (ASTM D5430) for a roll/section.

    Formula: points/100m2 = (total_points * 100000) / (meters * width_mm).
    Returns 0.0 when inputs are invalid (no inspected length or width).
    """
    if inspected_meters <= 0 or fabric_width_cm <= 0:
        return 0.0
    width_mm = fabric_width_cm * 10.0
    return round((total_points * 100000.0) / (inspected_meters * width_mm), 2)


def total_points(measurements: list[DefectMeasurement]) -> float:
    """Sum the penalty points of all measured defects, per 4-Point system."""
    return round(sum(m.points for m in measurements), 2)


@dataclass
class RollMeterageEstimator:
    """Estimate the inspected fabric length in meters using vision.

    One-shot capture has no motion, so meterage estimation relies on:
      * a running count of distinct measured frames, and
      * an optional feed-rate (m/min) plus elapsed seconds.

    ``feed_rate_m_min`` (m/min) can be supplied by the user or read from the
    inspection machine. When it is 0, we fall back to an area-based estimate
    using the number of frames processed and a nominal frame width travelled
    (configured via ``meter_per_frame``).
    """

    feed_rate_m_min: float = 0.0
    meter_per_frame: float = 0.05
    inspected_meters: float = 0.0
    frames_seen: int = 0

    def advance(self, elapsed_seconds: float = 0.0) -> None:
        """Accumulate inspected length for one processing step."""
        if self.feed_rate_m_min > 0:
            self.inspected_meters += self.feed_rate_m_min * (elapsed_seconds / 60.0)
        else:
            self.inspected_meters += self.meter_per_frame
        self.frames_seen += 1

    def estimate_meters(self) -> float:
        return round(self.inspected_meters, 2)

    def reset(self) -> None:
        self.inspected_meters = 0.0
        self.frames_seen = 0
