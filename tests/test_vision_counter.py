
import numpy as np

from src.vision.object_counter import ObjectCounter


class TestObjectCounter:
    def test_returns_empty_when_no_model(self):
        counter = ObjectCounter()
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        results = counter.detect(frame)
        assert results == []

    def test_model_name(self):
        counter = ObjectCounter()
        assert counter.model_name == "yolo11n"
        assert counter.result_type == "count"

    def test_zone_config(self):
        counter = ObjectCounter(config={"zone_name": "entrance"})
        assert counter.config["zone_name"] == "entrance"
