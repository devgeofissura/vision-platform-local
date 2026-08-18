from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from src.camera.rtsp_client import RTSPClient


@pytest.fixture
def client():
    return RTSPClient(
        rtsp_url="rtsp://admin:pass@192.168.1.100:554/stream1",
        transport="tcp",
        connect_timeout_ms=10000,
        reconnect_interval_ms=5000,
    )


class TestRTSPClientConnect:
    @patch("src.camera.rtsp_client.cv2.VideoCapture")
    def test_connect_success(self, mock_cap_cls, client):
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap_cls.return_value = mock_cap

        result = client.connect()
        assert result is True
        assert client.is_connected is True

    @patch("src.camera.rtsp_client.cv2.VideoCapture")
    def test_connect_failure(self, mock_cap_cls, client):
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_cap_cls.return_value = mock_cap

        result = client.connect()
        assert result is False
        assert client.is_connected is False

    @patch("src.camera.rtsp_client.cv2.VideoCapture")
    def test_connect_releases_previous(self, mock_cap_cls, client):
        old_cap = MagicMock()
        old_cap.isOpened.return_value = True
        client._cap = old_cap

        new_cap = MagicMock()
        new_cap.isOpened.return_value = True
        mock_cap_cls.return_value = new_cap

        client.connect()
        old_cap.release.assert_called_once()


class TestRTSPClientCapture:
    @patch("src.camera.rtsp_client.cv2.VideoCapture")
    def test_capture_frame_success(self, mock_cap_cls, client):
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        fake_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, fake_frame)
        mock_cap_cls.return_value = mock_cap
        client.connect()

        frame = client.capture_frame()
        assert frame is not None
        assert frame.shape == (480, 640, 3)

    @patch("src.camera.rtsp_client.cv2.VideoCapture")
    def test_capture_frame_not_connected(self, mock_cap_cls, client):
        frame = client.capture_frame()
        assert frame is None

    @patch("src.camera.rtsp_client.cv2.VideoCapture")
    def test_capture_frame_read_fails(self, mock_cap_cls, client):
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (False, None)
        mock_cap_cls.return_value = mock_cap
        client.connect()

        frame = client.capture_frame()
        assert frame is None


class TestRTSPClientRelease:
    @patch("src.camera.rtsp_client.cv2.VideoCapture")
    def test_release(self, mock_cap_cls, client):
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap_cls.return_value = mock_cap
        client.connect()

        client.release()
        assert client._cap is None
        assert client.is_connected is False
        mock_cap.release.assert_called_once()


class TestRTSPClientProperties:
    @patch("src.camera.rtsp_client.cv2.VideoCapture")
    def test_last_frame(self, mock_cap_cls, client):
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        fake_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, fake_frame)
        mock_cap_cls.return_value = mock_cap
        client.connect()

        assert client.last_frame is None
        client.capture_frame()
        assert client.last_frame is not None


class TestRTSPClientRedactUrl:
    def test_redact_with_password(self):
        result = RTSPClient._redact_url("rtsp://admin:pass123@192.168.1.100:554/stream1")
        assert result == "rtsp://***@192.168.1.100:554/stream1"

    def test_redact_without_password(self):
        url = "rtsp://192.168.1.100:554/stream1"
        result = RTSPClient._redact_url(url)
        assert result == url
