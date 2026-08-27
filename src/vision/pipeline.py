import logging

from src.vision.base import BaseDetector, ProcessingResult
from src.vision.fabric_defect_detector import FabricDefectDetector
from src.vision.fissure_detector import FissureDetector
from src.vision.object_counter import ObjectCounter
from src.vision.person_detector import PersonDetector
from src.vision.plate_detector import PlateDetector
from src.vision.ppe_detector import PPEDetector

logger = logging.getLogger(__name__)

TASK_MODULE_MAP = {
    "fissure": [FissureDetector],
    "ppe": [PPEDetector],
    "fabric_quality": [FabricDefectDetector],
    "structural": [ObjectCounter],
    "plate": [PlateDetector],
    "person_tracking": [PersonDetector],
}


class VisionPipeline:
    def __init__(self, task_type: str, config: dict | None = None):
        self.task_type = task_type
        self.config = config or {}
        self._modules = self._build_modules()

    def _build_modules(self) -> list[BaseDetector]:
        module_classes = TASK_MODULE_MAP.get(self.task_type, [])
        return [cls(self.config) for cls in module_classes]

    @property
    def enabled(self) -> bool:
        return len(self._modules) > 0

    def process(self, frame) -> list[ProcessingResult]:
        import numpy as np

        if not isinstance(frame, np.ndarray):
            logger.warning("Frame is not a numpy array, skipping processing")
            return []

        all_results = []
        for module in self._modules:
            try:
                results = module.detect(frame)
                all_results.extend(results)
            except Exception as e:
                logger.error("Module %s failed: %s", module.model_name, e)
        return all_results

    def process_with_timings(self, frame) -> tuple[list[ProcessingResult], dict]:
        import time

        import numpy as np

        if not isinstance(frame, np.ndarray):
            return [], {}

        all_results = []
        timings = {}
        for module in self._modules:
            start = time.perf_counter()
            try:
                results = module.detect(frame)
                all_results.extend(results)
            except Exception as e:
                logger.error("Module %s failed: %s", module.model_name, e)
            elapsed = (time.perf_counter() - start) * 1000
            timings[module.model_name] = round(elapsed, 1)
        return all_results, timings


def run_pipeline(task_type: str, frame, config: dict | None = None) -> list[ProcessingResult]:
    pipeline = VisionPipeline(task_type, config)
    return pipeline.process(frame)
