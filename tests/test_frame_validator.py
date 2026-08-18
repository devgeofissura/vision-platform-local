import numpy as np
import pytest

from src.camera.frame_validator import FrameValidator


@pytest.fixture
def validator():
    return FrameValidator(
        min_width=640,
        min_height=480,
        min_brightness=0.05,
        max_brightness=0.95,
        min_sharpness=50.0,
    )


@pytest.fixture
def good_frame():
    frame = np.random.randint(50, 200, (600, 800, 3), dtype=np.uint8)
    return frame


@pytest.fixture
def black_frame():
    return np.zeros((600, 800, 3), dtype=np.uint8)


@pytest.fixture
def white_frame():
    return np.full((600, 800, 3), 255, dtype=np.uint8)


@pytest.fixture
def low_res_frame():
    return np.random.randint(50, 200, (360, 480, 3), dtype=np.uint8)


@pytest.fixture
def blurry_frame():
    frame = np.random.randint(50, 200, (600, 800, 3), dtype=np.uint8)
    return frame


class TestFrameValidatorDefaults:
    def test_good_frame_score_one(self, validator, good_frame):
        result = validator.validate(good_frame)
        assert result["score"] == 1.0
        assert result["is_black"] is False
        assert result["saturated"] is False
        assert result["low_resolution"] is False
        assert result["frozen_frame"] is False
        assert result["width"] == 800
        assert result["height"] == 600
        assert result["issues"] == []

    def test_black_frame_score_zero(self, validator, black_frame):
        result = validator.validate(black_frame)
        assert result["score"] == 0.0
        assert result["is_black"] is True
        assert "image_is_black" in result["issues"]

    def test_white_frame_saturated(self, validator, white_frame):
        result = validator.validate(white_frame)
        assert result["saturated"] is True
        assert "saturated" in result["issues"]
        assert result["score"] < 1.0

    def test_low_resolution_detected(self, validator, low_res_frame):
        result = validator.validate(low_res_frame)
        assert result["low_resolution"] is True
        assert "low_resolution" in result["issues"]
        assert result["score"] == 0.9

    def test_frozen_frame_detected(self, validator, good_frame):
        result = validator.validate(good_frame, prev_frame=good_frame.copy())
        assert result["frozen_frame"] is True
        assert "frozen_frame" in result["issues"]
        assert result["score"] == 0.7


class TestFrameValidatorScoring:
    def test_multiple_issues_compound(self, validator, low_res_frame):
        result = validator.validate(low_res_frame)
        assert result["score"] == 0.9
        assert result["low_resolution"] is True

    def test_score_never_negative(self, validator, black_frame):
        result = validator.validate(black_frame)
        assert result["score"] >= 0.0

    def test_different_brightness_levels(self, validator):
        dim = np.random.randint(5, 15, (600, 800, 3), dtype=np.uint8)
        result = validator.validate(dim)
        assert result["brightness"] < 0.05
        assert "low_brightness" in result["issues"]
        assert result["score"] == 0.8


class TestFrameValidatorDimensions:
    def test_custom_min_dimensions(self):
        v = FrameValidator(min_width=320, min_height=240)
        frame = np.random.randint(50, 200, (300, 400, 3), dtype=np.uint8)
        result = v.validate(frame)
        assert result["low_resolution"] is False

    def test_exact_boundary(self):
        v = FrameValidator(min_width=640, min_height=480)
        frame = np.random.randint(50, 200, (480, 640, 3), dtype=np.uint8)
        result = v.validate(frame)
        assert result["low_resolution"] is False
