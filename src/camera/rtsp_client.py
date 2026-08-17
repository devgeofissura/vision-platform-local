import logging
import os

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class RTSPClient:
    def __init__(
        self,
        rtsp_url: str,
        transport: str = "tcp",
        connect_timeout_ms: int = 10000,
        reconnect_interval_ms: int = 5000,
    ):
        self.rtsp_url = rtsp_url
        self.transport = transport
        self.connect_timeout_ms = connect_timeout_ms
        self.reconnect_interval_ms = reconnect_interval_ms
        self._cap: cv2.VideoCapture | None = None
        self._last_frame: np.ndarray | None = None
        self._connected = False

    def connect(self) -> bool:
        try:
            self.release()

            if self.transport == "tcp":
                os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
            elif "OPENCV_FFMPEG_CAPTURE_OPTIONS" in os.environ:
                del os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"]

            self._cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            self._cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, self.connect_timeout_ms)

            if self._cap.isOpened():
                self._connected = True
                logger.info("RTSP connected: %s", self._redact_url(self.rtsp_url))
                return True

            self._connected = False
            logger.warning("RTSP connection failed: %s", self._redact_url(self.rtsp_url))
            return False
        except Exception as e:
            self._connected = False
            logger.error("RTSP connection error: %s", e)
            return False

    def capture_frame(self) -> np.ndarray | None:
        if self._cap is None or not self._cap.isOpened():
            return None
        ret, frame = self._cap.read()
        if ret and frame is not None:
            self._last_frame = frame
            return frame
        logger.warning("Failed to capture frame")
        return None

    def release(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
            self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected and self._cap is not None and self._cap.isOpened()

    @property
    def last_frame(self) -> np.ndarray | None:
        return self._last_frame

    @staticmethod
    def _redact_url(url: str) -> str:
        """Remove password from URL for logging."""
        if "@" in url:
            protocol_and_rest = url.split("@", 1)
            return protocol_and_rest[0].split("://")[0] + "://***@" + protocol_and_rest[1]
        return url
