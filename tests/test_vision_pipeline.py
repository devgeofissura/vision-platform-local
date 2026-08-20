import numpy as np

from src.vision.pipeline import TASK_MODULE_MAP, VisionPipeline, run_pipeline


class TestVisionPipeline:
    def test_fissure_pipeline_enabled(self):
        pipeline = VisionPipeline("fissure")
        assert pipeline.enabled is True
        assert len(pipeline._modules) == 1

    def test_ppe_pipeline_enabled(self):
        pipeline = VisionPipeline("ppe")
        assert pipeline.enabled is True
        assert len(pipeline._modules) == 1

    def test_structural_pipeline_enabled(self):
        pipeline = VisionPipeline("structural")
        assert pipeline.enabled is True

    def test_plate_pipeline_enabled(self):
        pipeline = VisionPipeline("plate")
        assert pipeline.enabled is True

    def test_fabric_quality_pipeline_enabled(self):
        pipeline = VisionPipeline("fabric_quality")
        assert pipeline.enabled is True

    def test_unknown_task_disabled(self):
        pipeline = VisionPipeline("unknown_task")
        assert pipeline.enabled is False
        assert len(pipeline._modules) == 0

    def test_process_returns_list(self):
        pipeline = VisionPipeline("fissure")
        frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        results = pipeline.process(frame)
        assert isinstance(results, list)

    def test_process_with_invalid_frame(self):
        pipeline = VisionPipeline("fissure")
        results = pipeline.process("not_an_array")
        assert results == []

    def test_process_with_timings(self):
        pipeline = VisionPipeline("fissure")
        frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        results, timings = pipeline.process_with_timings(frame)
        assert isinstance(results, list)
        assert isinstance(timings, dict)

    def test_run_pipeline_function(self):
        frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        results = run_pipeline("fissure", frame)
        assert isinstance(results, list)

    def test_task_module_map_has_all_tasks(self):
        expected = {"fissure", "ppe", "fabric_quality", "structural", "plate", "person_tracking"}
        assert set(TASK_MODULE_MAP.keys()) == expected

    def test_config_passed_to_modules(self):
        pipeline = VisionPipeline("fissure", config={"conf": 0.5})
        assert pipeline.config["conf"] == 0.5
