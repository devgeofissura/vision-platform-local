import hashlib
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

import cv2
import numpy as np

from src.camera.frame_validator import FrameValidator
from src.camera.rtsp_client import RTSPClient
from src.config.settings import settings
from src.storage.database import SessionLocal
from src.storage.models import Observation

logger = logging.getLogger(__name__)


class CaptureWorker:
    def __init__(self):
        self.client = RTSPClient(
            rtsp_url=settings.camera_rtsp_url,
            transport=settings.camera_rtsp_transport,
            connect_timeout_ms=settings.camera_connect_timeout_ms,
            reconnect_interval_ms=settings.camera_reconnect_interval_ms,
        )
        self.validator = FrameValidator()
        self._prev_frame: np.ndarray | None = None
        self._last_capture_at: datetime | None = None
        self._capture_count: int = 0
        self._error_count: int = 0

    def capture(self) -> dict | None:
        if not self.client.is_connected:
            self.client.connect()

        if not self.client.is_connected:
            self._error_count += 1
            return None

        frame = self.client.capture_frame()
        if frame is None:
            self._error_count += 1
            return None

        validation = self.validator.validate(frame, self._prev_frame)
        self._prev_frame = frame.copy()

        now = datetime.now(UTC)
        observation_id = f"obs_{settings.local_id}_{settings.camera_id}_{now.strftime('%Y%m%dT%H%M%SZ')}"

        evidence_dir = Path(settings.local_evidence_dir) / now.strftime("%Y/%m/%d")
        evidence_dir.mkdir(parents=True, exist_ok=True)

        full_path = evidence_dir / f"{observation_id}_full.jpg"
        cv2.imwrite(str(full_path), frame, [cv2.IMWRITE_JPEG_QUALITY, settings.camera_capture_jpeg_quality])

        roi_path = evidence_dir / f"{observation_id}_roi.jpg"
        roi_config = self._get_roi()
        if roi_config:
            x, y, w, h = roi_config["x"], roi_config["y"], roi_config["width"], roi_config["height"]
            roi_frame = frame[y : y + h, x : x + w]
            cv2.imwrite(str(roi_path), roi_frame, [cv2.IMWRITE_JPEG_QUALITY, settings.camera_capture_jpeg_quality])

        sha256 = hashlib.sha256(full_path.read_bytes()).hexdigest()

        self._last_capture_at = now
        self._capture_count += 1

        result = {
            "observation_id": observation_id,
            "camera_id": settings.camera_id,
            "local_id": settings.local_id,
            "captured_at": now.isoformat(),
            "file_path": str(full_path),
            "sha256": sha256,
            "width": frame.shape[1],
            "height": frame.shape[0],
            "quality": validation,
            "algorithm_version": "capture-0.1.0",
        }

        self._save_observation(result)
        return result

    def _save_observation(self, data: dict) -> None:
        db = SessionLocal()
        try:
            record = Observation(
                observation_id=data["observation_id"],
                camera_id=data["camera_id"],
                local_id=data["local_id"],
                captured_at=datetime.fromisoformat(data["captured_at"]),
                file_path=data["file_path"],
                sha256=data["sha256"],
                width=data["width"],
                height=data["height"],
                quality_score=data["quality"]["score"],
                quality_issues=json.dumps(data["quality"]["issues"]),
                algorithm_version=data["algorithm_version"],
                delivery_status="pending",
            )
            db.add(record)
            db.commit()
            logger.info("Saved observation %s to database", data["observation_id"])
        except Exception as e:
            db.rollback()
            logger.error("Failed to save observation %s: %s", data["observation_id"], e)
        finally:
            db.close()

    @staticmethod
    def _get_roi() -> dict | None:
        return None

    def connect(self) -> bool:
        return self.client.connect()

    def disconnect(self) -> None:
        self.client.release()

    @property
    def status(self) -> dict:
        return {
            "connected": self.client.is_connected,
            "last_capture_at": self._last_capture_at.isoformat() if self._last_capture_at else None,
            "capture_count": self._capture_count,
            "error_count": self._error_count,
        }
