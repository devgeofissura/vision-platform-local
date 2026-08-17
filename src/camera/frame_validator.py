import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class FrameValidator:
    def __init__(
        self,
        min_width: int = 640,
        min_height: int = 480,
        min_brightness: float = 0.05,
        max_brightness: float = 0.95,
        min_sharpness: float = 50.0,
    ):
        self.min_width = min_width
        self.min_height = min_height
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness
        self.min_sharpness = min_sharpness

    def validate(self, frame: np.ndarray, prev_frame: np.ndarray | None = None) -> dict:
        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        brightness = float(np.mean(gray)) / 255.0
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        frozen = False
        if prev_frame is not None:
            diff = cv2.absdiff(frame, prev_frame)
            frozen = float(np.mean(diff)) < 1.0

        is_black = brightness < 0.01
        saturated = brightness > self.max_brightness
        low_resolution = w < self.min_width or h < self.min_height
        low_brightness = brightness < self.min_brightness
        low_sharpness = laplacian_var < self.min_sharpness

        issues = []
        if is_black:
            issues.append("image_is_black")
        if frozen:
            issues.append("frozen_frame")
        if low_resolution:
            issues.append("low_resolution")
        if low_brightness:
            issues.append("low_brightness")
        if saturated:
            issues.append("saturated")
        if low_sharpness:
            issues.append("low_sharpness")

        score = 1.0
        if is_black:
            score = 0.0
        else:
            if frozen:
                score -= 0.3
            if low_brightness:
                score -= 0.2
            if saturated:
                score -= 0.2
            if low_sharpness:
                score -= 0.2
            if low_resolution:
                score -= 0.1
            score = max(0.0, score)

        return {
            "score": round(score, 3),
            "brightness": round(brightness, 3),
            "sharpness": round(float(laplacian_var), 3),
            "frozen_frame": frozen,
            "is_black": is_black,
            "saturated": saturated,
            "low_resolution": low_resolution,
            "issues": issues,
            "width": w,
            "height": h,
        }
