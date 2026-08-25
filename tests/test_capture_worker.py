import json
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from src.camera.capture_worker import CaptureWorker
from src.storage.models import Device, Observation, SystemSettings
from tests.conftest import TestSession


@pytest.fixture
def worker():
    with patch("src.camera.capture_worker.settings") as mock_settings:
        mock_settings.camera_rtsp_url = "rtsp://test"
        mock_settings.camera_rtsp_transport = "tcp"
        mock_settings.camera_connect_timeout_ms = 5000
        mock_settings.camera_reconnect_interval_ms = 3000
        mock_settings.local_id = "LOCAL-001"
        mock_settings.camera_id = "CAM-001"
        mock_settings.camera_auto_discover = False
        mock_settings.local_evidence_dir = "/tmp/test_evidence"
        mock_settings.camera_capture_jpeg_quality = 95
        w = CaptureWorker()
        yield w


def _fake_frame(w=640, h=480):
    return np.random.randint(50, 200, (h, w, 3), dtype=np.uint8)


class TestCaptureWorkerConnect:
    def test_connect_delegates_to_client(self, worker):
        worker.client.connect = MagicMock(return_value=True)
        result = worker.connect()
        assert result is True

    def test_disconnect_releases(self, worker):
        worker.client.release = MagicMock()
        worker.disconnect()
        worker.client.release.assert_called_once()


class TestCaptureWorkerCapture:
    def _mock_client(self, worker, frame):
        worker.client.connect = MagicMock(return_value=True)
        worker.client._connected = True
        worker.client._cap = MagicMock()
        worker.client.capture_frame = MagicMock(return_value=frame)

    def test_capture_success(self, tmp_path):
        db = TestSession()
        db.add(SystemSettings(key="capture_evidence_dir", value=str(tmp_path)))
        db.add(SystemSettings(key="capture_jpeg_quality", value="95"))
        db.commit()
        db.close()

        frame = _fake_frame()

        with patch("src.camera.capture_worker.settings") as s:
            s.camera_rtsp_url = "rtsp://test"
            s.camera_rtsp_transport = "tcp"
            s.camera_connect_timeout_ms = 5000
            s.camera_reconnect_interval_ms = 3000
            s.local_id = "LOCAL-001"
            s.camera_id = "CAM-001"
            s.local_evidence_dir = str(tmp_path)
            s.camera_capture_jpeg_quality = 95

            worker = CaptureWorker()
            self._mock_client(worker, frame)
            worker._get_roi = MagicMock(return_value=None)

            with patch("src.camera.capture_worker.SessionLocal", TestSession):
                result = worker.capture()

        assert result is not None
        assert result["observation_id"].startswith("obs_LOCAL-001_CAM-001_")
        assert result["camera_id"] == "CAM-001"
        assert result["local_id"] == "LOCAL-001"
        assert result["width"] == 640
        assert result["height"] == 480
        assert result["algorithm_version"] == "capture-0.1.0"
        from pathlib import Path

        assert Path(result["file_path"]).exists()
        assert str(tmp_path) in result["file_path"]

    def test_capture_not_connected_fails(self, worker):
        worker.client.connect = MagicMock(return_value=False)
        worker.client._connected = False

        result = worker.capture()
        assert result is None
        assert worker._error_count == 1

    def test_capture_frame_none_fails(self, worker):
        worker.client.connect = MagicMock(return_value=True)
        worker.client._connected = True
        worker.client.capture_frame = MagicMock(return_value=None)

        result = worker.capture()
        assert result is None
        assert worker._error_count == 1


class TestCaptureWorkerResolvedConfig:
    def test_device_config_overrides_rtsp_url(self):
        db = TestSession()
        db.add(Device(
            device_id="CAM-TEST",
            name="Test Cam",
            connection_type="rtsp",
            connection_config={
                "ip": "10.0.0.99",
                "username": "camuser",
                "password": "campass",
                "channel": 2,
                "stream_type": "sub",
                "transport": "udp",
            },
        ))
        db.commit()
        db.close()

        with patch("src.camera.capture_worker.settings") as s:
            s.camera_reconnect_interval_ms = 3000
            s.camera_auto_discover = False
            worker = CaptureWorker(device_id="CAM-TEST")

        assert "10.0.0.99" in worker.client.rtsp_url
        assert "camuser:campass" in worker.client.rtsp_url
        assert "channel=2" in worker.client.rtsp_url
        assert "subtype=1" in worker.client.rtsp_url
        assert worker.client.transport == "udp"

    def test_worker_without_device_uses_global_defaults(self):
        with patch("src.camera.capture_worker.settings") as s:
            s.camera_reconnect_interval_ms = 3000
            s.camera_auto_discover = False
            worker = CaptureWorker()

        assert worker._config["channel"] == 1
        assert worker._config["stream_type"] == "main"
        assert worker._config["transport"] == "tcp"
        assert worker._config["username"] == "admin"

    def test_worker_missing_device_id_falls_back_to_defaults(self):
        with patch("src.camera.capture_worker.settings") as s:
            s.camera_reconnect_interval_ms = 3000
            s.camera_auto_discover = False
            worker = CaptureWorker(device_id="NO-SUCH-DEVICE")

        assert worker._device is None
        assert worker._config["transport"] == "tcp"


class TestCaptureWorkerSaveObservation:
    def test_save_observation(self, worker):
        data = {
            "observation_id": "obs_test_001",
            "camera_id": "CAM-001",
            "local_id": "LOCAL-001",
            "captured_at": datetime.now(UTC).isoformat(),
            "file_path": "/tmp/test.jpg",
            "sha256": "abc123",
            "width": 800,
            "height": 600,
            "quality": {"score": 0.9, "issues": ["low_sharpness"]},
            "algorithm_version": "capture-0.1.0",
        }
        with patch("src.camera.capture_worker.SessionLocal", TestSession):
            worker._save_observation(data)

        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id="obs_test_001").first()
        assert obs is not None
        assert obs.camera_id == "CAM-001"
        assert obs.quality_score == 0.9
        assert json.loads(obs.quality_issues) == ["low_sharpness"]
        assert obs.delivery_status == "pending"
        db.close()


class TestCaptureWorkerStatus:
    def test_status_initial(self, worker):
        s = worker.status
        assert s["connected"] is False
        assert s["last_capture_at"] is None
        assert s["capture_count"] == 0
        assert s["error_count"] == 0


class TestCaptureWorkerGetRoi:
    def test_get_roi_default(self, worker):
        assert worker._get_roi() is None


class TestCaptureWorkerProcessingStatus:
    def _capture(self, tmp_path, extra_settings=()):
        db = TestSession()
        db.add(SystemSettings(key="capture_evidence_dir", value=str(tmp_path)))
        db.add(SystemSettings(key="capture_jpeg_quality", value="95"))
        for k, v in extra_settings:
            db.add(SystemSettings(key=k, value=v))
        db.commit()
        db.close()

        frame = _fake_frame()
        with patch("src.camera.capture_worker.settings") as s:
            s.camera_rtsp_url = "rtsp://test"
            s.camera_rtsp_transport = "tcp"
            s.camera_connect_timeout_ms = 5000
            s.camera_reconnect_interval_ms = 3000
            s.local_id = "LOCAL-001"
            s.camera_id = "CAM-001"
            s.local_evidence_dir = str(tmp_path)
            s.camera_capture_jpeg_quality = 95

            w = CaptureWorker()
            w.client.connect = MagicMock(return_value=True)
            w.client._connected = True
            w.client._cap = MagicMock()
            w.client.capture_frame = MagicMock(return_value=frame)
            w._get_roi = MagicMock(return_value=None)

            with patch("src.camera.capture_worker.SessionLocal", TestSession):
                return w.capture()

    def test_processing_enabled_saves_pending(self, tmp_path):
        result = self._capture(
            tmp_path, [("processing_enabled", "true")]
        )
        assert result is not None
        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id=result["observation_id"]).first()
        assert obs.processing_status == "pending"
        db.close()

    def test_processing_disabled_saves_none(self, tmp_path):
        result = self._capture(tmp_path)
        assert result is not None
        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id=result["observation_id"]).first()
        assert obs.processing_status == "none"
        db.close()

    def test_auto_on_capture_disabled_saves_none(self, tmp_path):
        result = self._capture(
            tmp_path,
            [("processing_enabled", "true"), ("processing_auto_on_capture", "false")],
        )
        assert result is not None
        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id=result["observation_id"]).first()
        assert obs.processing_status == "none"
        db.close()
