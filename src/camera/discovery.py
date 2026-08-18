from __future__ import annotations

import logging
import socket
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

WS_DISCOVERY_ADDRESS = "239.255.255.250"
WS_DISCOVERY_PORT = 3702
ONVIF_DEVICE_NAMESPACE = "http://www.onvif.org/ver10/device/wsdl"
INTELBRAS_RTSP_PORT = 554
DEFAULT_ONVIF_PORT = 80

WS_DISCOVERY_SOAP = """\
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:wsa="http://www.w3.org/2005/08/addressing"
    xmlns:dn="http://www.onvif.org/ver10/network/wsdl">
  <soap:Header>
    <wsa:Action>http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action>
    <wsa:MessageID>uuid:{message_id}</wsa:MessageID>
    <wsa:ReplyTo>
      <wsa:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa:Address>
    </wsa:ReplyTo>
    <wsa:To>urn:schemas-xmlsoap-org:ws:2005:04:discovery</wsa:To>
  </soap:Header>
  <soap:Body>
    <dn:Probe/>
  </soap:Body>
</soap:Envelope>"""


class StreamType(Enum):
    MAIN = "0"  # Stream Principal — resolucao maxima
    SUB = "1"   # Stream Extra — resolucao reduzida


@dataclass
class CameraInfo:
    ip: str
    hostname: str
    mac: str | None
    manufacturer: str | None
    model: str | None
    serial: str | None
    rtsp_port: int
    onvif_port: int

    @property
    def full_name(self) -> str:
        return self.hostname or f"camera-{self.ip}"


class OnvifDiscovery:
    def __init__(
        self,
        timeout_seconds: float = 5.0,
        onvif_port: int = DEFAULT_ONVIF_PORT,
    ):
        self.timeout_seconds = timeout_seconds
        self.onvif_port = onvif_port

    def find_camera(
        self,
        hostname_prefix: str = "GeoFissura_CAM_",
        mac: str | None = None,
    ) -> CameraInfo | None:
        probes = self._send_probe()
        for probe in probes:
            if self._matches_filter(probe, hostname_prefix, mac):
                logger.info(
                    "Camera found: %s (ip=%s, mac=%s)",
                    probe.hostname,
                    probe.ip,
                    probe.mac,
                )
                return probe
        logger.warning(
            "No camera found matching prefix=%s mac=%s after %d responses",
            hostname_prefix,
            mac,
            len(probes),
        )
        return None

    def find_camera_by_ip(self, ip: str) -> CameraInfo | None:
        probes = self._send_probe()
        for probe in probes:
            if probe.ip == ip:
                return probe
        return None

    def build_rtsp_url(
        self,
        ip: str,
        username: str = "admin",
        password: str = "",
        channel: int = 1,
        stream: StreamType = StreamType.MAIN,
        rtsp_port: int = INTELBRAS_RTSP_PORT,
    ) -> str:
        auth = f"{username}:{password}" if password else username
        return (
            f"rtsp://{auth}@{ip}:{rtsp_port}"
            f"/cam/realmonitor?channel={channel}&subtype={stream.value}"
        )

    def _send_probe(self) -> list[CameraInfo]:
        import uuid

        message_id = str(uuid.uuid4())
        payload = WS_DISCOVERY_SOAP.format(message_id=message_id).encode("utf-8")

        results: list[CameraInfo] = []
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(self.timeout_seconds)
            sock.sendto(
                payload,
                (WS_DISCOVERY_ADDRESS, WS_DISCOVERY_PORT),
            )

            while True:
                try:
                    data, addr = sock.recvfrom(65535)
                    ip = addr[0]
                    camera = self._parse_probe_response(data, ip)
                    if camera:
                        results.append(camera)
                except TimeoutError:
                    break
        except OSError as e:
            logger.error("WS-Discovery socket error: %s", e)
        finally:
            try:
                sock.close()
            except Exception:
                pass

        logger.info("WS-Discovery received %d probe responses", len(results))
        return results

    def _parse_probe_response(self, data: bytes, source_ip: str) -> CameraInfo | None:
        try:
            root = ET.fromstring(data)
            scopes = self._extract_scopes(root)
            hostname = self._extract_hostname(root)
            manufacturer = self._extract_manufacturer(root)
            model_name = self._extract_model(root)
            serial = self._extract_serial(root)
            mac = self._extract_mac(scopes)

            if not hostname:
                hostname = self._reverse_dns(source_ip)

            return CameraInfo(
                ip=source_ip,
                hostname=hostname or f"unknown-{source_ip}",
                mac=mac,
                manufacturer=manufacturer,
                model=model_name,
                serial=serial,
                rtsp_port=INTELBRAS_RTSP_PORT,
                onvif_port=self.onvif_port,
            )
        except ET.ParseError as e:
            logger.debug("Failed to parse probe response from %s: %s", source_ip, e)
            return None

    def _matches_filter(
        self,
        camera: CameraInfo,
        hostname_prefix: str,
        mac: str | None,
    ) -> bool:
        if hostname_prefix and not camera.hostname.upper().startswith(hostname_prefix.upper()):
            return False
        if mac and (not camera.mac or camera.mac.upper().replace("-", ":") != mac.upper().replace("-", ":")):
            return False
        return True

    @staticmethod
    def _extract_scopes(root: ET.Element) -> str:
        for probe_match in root.iter():
            if "ProbeMatch" in probe_match.tag:
                for scope in probe_match.iter():
                    if "Scope" in scope.tag and scope.text:
                        return scope.text
        return ""

    @staticmethod
    def _extract_hostname(root: ET.Element) -> str | None:
        for elem in root.iter():
            tag_lower = elem.tag.lower() if isinstance(elem.tag, str) else ""
            if "hostname" in tag_lower and elem.text:
                return elem.text.strip()
        return None

    @staticmethod
    def _extract_manufacturer(root: ET.Element) -> str | None:
        for elem in root.iter():
            tag_lower = elem.tag.lower() if isinstance(elem.tag, str) else ""
            if "manufacturer" in tag_lower and elem.text:
                return elem.text.strip()
        return None

    @staticmethod
    def _extract_model(root: ET.Element) -> str | None:
        for elem in root.iter():
            tag_lower = elem.tag.lower() if isinstance(elem.tag, str) else ""
            if "model" in tag_lower and elem.text:
                return elem.text.strip()
        return None

    @staticmethod
    def _extract_serial(root: ET.Element) -> str | None:
        for elem in root.iter():
            tag_lower = elem.tag.lower() if isinstance(elem.tag, str) else ""
            if "serialnumber" in tag_lower.replace("-", "") and elem.text:
                return elem.text.strip()
        return None

    @staticmethod
    def _extract_mac(scopes: str) -> str | None:
        import re
        match = re.search(r"MAC/([0-9a-fA-F:.-]+)", scopes)
        if match:
            mac = match.group(1).replace("-", ":")
            if len(mac) == 17 and mac.count(":") == 5:
                return mac.upper()
        return None

    @staticmethod
    def _reverse_dns(ip: str) -> str | None:
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except (socket.herror, socket.gaierror, OSError):
            return None

    def fallback_resolve(self, hostname: str) -> str | None:
        try:
            ip = socket.gethostbyname(hostname)
            logger.info("DNS resolved %s -> %s", hostname, ip)
            return ip
        except (socket.gaierror, OSError) as e:
            logger.warning("DNS resolution failed for %s: %s", hostname, e)
            return None
