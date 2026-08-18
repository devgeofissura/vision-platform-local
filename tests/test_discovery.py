from __future__ import annotations

import socket
from unittest.mock import MagicMock, patch

from src.camera.discovery import (
    CameraInfo,
    OnvifDiscovery,
    StreamType,
)

GEOFISSURA_PROBE_RESPONSE = """\
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:wsa="http://www.w3.org/2005/08/addressing">
  <soap:Body>
    <ProbeMatch>
      <wsa:EndpointReference>
        <wsa:Address>urn:uuid:12345678-1234-1234-1234-123456789abc</wsa:Address>
      </wsa:EndpointReference>
      <Types>dn:NetworkVideoTransmitter</Types>
      <Scopes>onvif://www.onvif.org/type/NetworkVideoTransmitter onvif://www.onvif.org/hostname/GeoFissura_CAM_000001 onvif://www.onvif.org/MAC/54:ba:d9:d3:ed:26</Scopes>
      <XAddrs>http://192.168.1.50:8080/onvif/device_service</XAddrs>
      <Manufacturer>Intelbras</Manufacturer>
      <Model>VIPC-1230-B-G2</Model>
      <SerialNumber>DYO0011617671</SerialNumber>
      <Hostname>GeoFissura_CAM_000001</Hostname>
    </ProbeMatch>
  </soap:Body>
</soap:Envelope>"""

NON_GEOFISSURA_RESPONSE = """\
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:wsa="http://www.w3.org/2005/08/addressing">
  <soap:Body>
    <ProbeMatch>
      <wsa:EndpointReference>
        <wsa:Address>urn:uuid:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee</wsa:Address>
      </wsa:EndpointReference>
      <Types>dn:NetworkVideoTransmitter</Types>
      <Scopes>onvif://www.onvif.org/hostname/OtherCamera</Scopes>
      <XAddrs>http://192.168.1.51:8080/onvif/device_service</XAddrs>
      <Manufacturer>Hikvision</Manufacturer>
      <Model>DS-2CD2143</Model>
      <Hostname>OtherCamera</Hostname>
    </ProbeMatch>
  </soap:Body>
</soap:Envelope>"""


def _make_udp_response(data: str, ip: str) -> tuple[bytes, tuple[str, int]]:
    return data.encode("utf-8"), (ip, 3702)


class TestCameraInfo:
    def test_full_name(self):
        cam = CameraInfo(
            ip="192.168.1.50",
            hostname="GeoFissura_CAM_000001",
            mac="54:BA:D9:D3:ED:26",
            manufacturer="Intelbras",
            model="VIPC-1230-B-G2",
            serial="DYO0011617671",
            rtsp_port=554,
            onvif_port=80,
        )
        assert cam.full_name == "GeoFissura_CAM_000001"

    def test_full_name_fallback(self):
        cam = CameraInfo(
            ip="192.168.1.50",
            hostname="unknown-192.168.1.50",
            mac=None,
            manufacturer=None,
            model=None,
            serial=None,
            rtsp_port=554,
            onvif_port=80,
        )
        assert cam.full_name == "unknown-192.168.1.50"


class TestStreamType:
    def test_main_is_zero(self):
        assert StreamType.MAIN.value == "0"

    def test_sub_is_one(self):
        assert StreamType.SUB.value == "1"


class TestBuildRtspUrl:
    def setup_method(self):
        self.discovery = OnvifDiscovery()

    def test_main_stream(self):
        url = self.discovery.build_rtsp_url(
            ip="192.168.1.50",
            username="admin",
            password="Alohomor4",
            channel=1,
            stream=StreamType.MAIN,
        )
        assert url == "rtsp://admin:Alohomor4@192.168.1.50:554/cam/realmonitor?channel=1&subtype=0"

    def test_sub_stream(self):
        url = self.discovery.build_rtsp_url(
            ip="192.168.1.50",
            username="admin",
            password="Alohomor4",
            channel=1,
            stream=StreamType.SUB,
        )
        assert url == "rtsp://admin:Alohomor4@192.168.1.50:554/cam/realmonitor?channel=1&subtype=1"

    def test_empty_password(self):
        url = self.discovery.build_rtsp_url(
            ip="192.168.1.50",
            username="admin",
            password="",
        )
        assert url == "rtsp://admin@192.168.1.50:554/cam/realmonitor?channel=1&subtype=0"

    def test_custom_channel(self):
        url = self.discovery.build_rtsp_url(
            ip="192.168.1.50",
            username="admin",
            password="pass",
            channel=3,
            stream=StreamType.MAIN,
        )
        assert "channel=3" in url
        assert "subtype=0" in url


class TestFindCamera:
    def setup_method(self):
        self.discovery = OnvifDiscovery(timeout_seconds=1.0)

    @patch("src.camera.discovery.socket.socket")
    def test_find_camera_by_hostname_prefix(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.recvfrom.side_effect = [
            _make_udp_response(GEOFISSURA_PROBE_RESPONSE, "192.168.1.50"),
            socket.timeout,
        ]

        cam = self.discovery.find_camera(hostname_prefix="GeoFissura_CAM_")
        assert cam is not None
        assert cam.ip == "192.168.1.50"
        assert cam.hostname == "GeoFissura_CAM_000001"
        assert cam.mac == "54:BA:D9:D3:ED:26"
        assert cam.manufacturer == "Intelbras"
        assert cam.model == "VIPC-1230-B-G2"
        assert cam.serial == "DYO0011617671"

    @patch("src.camera.discovery.socket.socket")
    def test_find_camera_by_mac(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.recvfrom.side_effect = [
            _make_udp_response(GEOFISSURA_PROBE_RESPONSE, "192.168.1.50"),
            socket.timeout,
        ]

        cam = self.discovery.find_camera(hostname_prefix="", mac="54-ba-d9-d3-ed-26")
        assert cam is not None
        assert cam.mac == "54:BA:D9:D3:ED:26"

    @patch("src.camera.discovery.socket.socket")
    def test_no_match_returns_none(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.recvfrom.side_effect = [
            _make_udp_response(NON_GEOFISSURA_RESPONSE, "192.168.1.51"),
            socket.timeout,
        ]

        cam = self.discovery.find_camera(hostname_prefix="GeoFissura_CAM_")
        assert cam is None

    @patch("src.camera.discovery.socket.socket")
    def test_empty_network_returns_none(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.recvfrom.side_effect = socket.timeout

        cam = self.discovery.find_camera(hostname_prefix="GeoFissura_CAM_")
        assert cam is None

    @patch("src.camera.discovery.socket.socket")
    def test_multiple_cameras_returns_first_match(self, mock_socket_cls):
        second_response = GEOFISSURA_PROBE_RESPONSE.replace(
            "GeoFissura_CAM_000001", "GeoFissura_CAM_000002"
        ).replace("192.168.1.50", "192.168.1.51")
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.recvfrom.side_effect = [
            _make_udp_response(NON_GEOFISSURA_RESPONSE, "192.168.1.52"),
            _make_udp_response(second_response, "192.168.1.51"),
            socket.timeout,
        ]

        cam = self.discovery.find_camera(hostname_prefix="GeoFissura_CAM_")
        assert cam is not None
        assert cam.hostname == "GeoFissura_CAM_000002"


class TestFindCameraByIp:
    def setup_method(self):
        self.discovery = OnvifDiscovery(timeout_seconds=1.0)

    @patch("src.camera.discovery.socket.socket")
    def test_find_by_ip(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.recvfrom.side_effect = [
            _make_udp_response(GEOFISSURA_PROBE_RESPONSE, "192.168.1.50"),
            socket.timeout,
        ]

        cam = self.discovery.find_camera_by_ip("192.168.1.50")
        assert cam is not None
        assert cam.hostname == "GeoFissura_CAM_000001"

    @patch("src.camera.discovery.socket.socket")
    def test_ip_not_found(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.recvfrom.side_effect = [
            _make_udp_response(GEOFISSURA_PROBE_RESPONSE, "192.168.1.50"),
            socket.timeout,
        ]

        cam = self.discovery.find_camera_by_ip("192.168.1.99")
        assert cam is None


class TestFallbackResolve:
    def test_resolve_success(self):
        discovery = OnvifDiscovery()
        with patch("src.camera.discovery.socket.gethostbyname", return_value="192.168.1.50"):
            ip = discovery.fallback_resolve("geofissuracam01")
            assert ip == "192.168.1.50"

    def test_resolve_failure(self):
        discovery = OnvifDiscovery()
        with patch(
            "src.camera.discovery.socket.gethostbyname",
            side_effect=socket.gaierror("Name not found"),
        ):
            ip = discovery.fallback_resolve("nonexistent.local")
            assert ip is None


class TestParseProbeResponse:
    def test_parse_valid_response(self):
        discovery = OnvifDiscovery()
        data = GEOFISSURA_PROBE_RESPONSE.encode("utf-8")
        cam = discovery._parse_probe_response(data, "192.168.1.50")
        assert cam is not None
        assert cam.ip == "192.168.1.50"
        assert cam.hostname == "GeoFissura_CAM_000001"
        assert cam.manufacturer == "Intelbras"
        assert cam.model == "VIPC-1230-B-G2"
        assert cam.serial == "DYO0011617671"

    def test_parse_invalid_xml(self):
        discovery = OnvifDiscovery()
        cam = discovery._parse_probe_response(b"not xml", "192.168.1.50")
        assert cam is None


class TestSocketError:
    @patch("src.camera.discovery.socket.socket")
    def test_socket_error_returns_empty(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.sendto.side_effect = OSError("Network unreachable")

        discovery = OnvifDiscovery()
        results = discovery._send_probe()
        assert results == []
