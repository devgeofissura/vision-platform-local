"""Live overlay drawing for detection results (typed bounding boxes).

Works on top of the generic ``ProcessingResult`` list produced by the
``VisionPipeline``, so any task type (fabric, fissure, ppe, plate, ...) can
share one streaming overlay instead of each detector drawing its own.
"""

import cv2
import numpy as np

_TASK_COLORS: dict[str, tuple[int, int, int]] = {
    "fabric_defect": (255, 140, 0),   # orange
    "fissure": (0, 255, 0),           # green
    "ppe": (0, 200, 255),             # yellow
    "plate": (255, 0, 0),             # blue
    "person": (0, 165, 255),          # orange-ish for person fallback
}

_DEFAULT_COLOR = (0, 255, 0)


def _defect_label(data: dict) -> str:
    """Human label for a fabric defect box: 'hole · high'."""
    kind = data.get("defect_type", "defect")
    sev = data.get("severity")
    if sev:
        return f"{kind} · {sev}"
    return str(kind)


def _result_label(result) -> str:
    """Best-effort short label for a detection result."""
    data = result.result_data or {}
    if result.result_type == "fabric_defect":
        return _defect_label(data)
    bbox = data.get("bbox")
    if bbox and len(bbox) >= 4:
        label = data.get("label") or data.get("class_name") or result.result_type
    else:
        label = result.result_type
    return str(label).replace("_", " ")


def result_color(result) -> tuple[int, int, int]:
    base = _TASK_COLORS.get(result.result_type, _DEFAULT_COLOR)
    return tuple(int(c) for c in base)


def draw_detection_results(frame: np.ndarray, results: list) -> np.ndarray:
    """Draw typed bounding boxes onto a copy of ``frame`` and return it.

    Bboxes inside ``result.result_data["bbox"]`` are [x, y, w, h] in the same
    coordinate space as ``frame`` (caller scales them to the output size
    before calling). Draws a filled header label with the type/severity and a
    small count bar at the bottom.
    """
    overlay = frame.copy()
    h, w = overlay.shape[:2]

    count = 0
    for result in results:
        data = result.result_data or {}
        bbox = data.get("bbox")
        if not bbox or len(bbox) < 4:
            continue
        x = max(0, int(bbox[0]))
        y = max(0, int(bbox[1]))
        bw = int(bbox[2])
        bh = int(bbox[3])
        bw = min(bw, w - x)
        bh = min(bh, h - y)
        if bw <= 0 or bh <= 0:
            continue

        color = result_color(result)
        count += 1
        cv2.rectangle(overlay, (x, y), (x + bw, y + bh), color, 2, cv2.LINE_AA)

        label = _result_label(result)
        conf = result.confidence if result.confidence is not None else 0.0
        text = f"{label} {conf:.0%}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        try:
            head_y = y - th - 6
            bg_y = head_y if head_y >= 0 else y
            y0 = y - 4 if head_y >= 0 else y + th + 6
            cv2.rectangle(
                overlay, (x, bg_y), (x + tw + 8, bg_y + th + 6), color, -1,
            )
            cv2.putText(
                overlay, text, (x + 4, y0),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA,
            )
        except Exception:
            pass

    if count > 0:
        bar_w = 240
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
            overlay, f"DETECCOES: {count}",
            (bx + 12, by + 28),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA,
        )

    return overlay
