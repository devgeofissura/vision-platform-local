from unittest.mock import patch

import pytest

from src.config.device_config import resolve_device_config
from src.storage.models import Device, SystemSettings
from tests.conftest import TestSession


@pytest.fixture(autouse=True)
def _env_layer():
    """Camada .env controlada para testes determinísticos."""
    with patch("src.config.device_config.settings") as s:
        s.camera_username = "env-user"
        s.camera_password = "env-pass"
        s.camera_ip = "10.10.10.10"
        s.camera_hostname = "env-host"
        s.camera_channel = 7
        s.camera_stream_type = "sub"
        s.camera_rtsp_transport = "udp"
        s.camera_connect_timeout_ms = 8000
        s.camera_capture_jpeg_quality = 80
        s.camera_capture_width = 1280
        s.camera_capture_height = 720
        s.camera_capture_interval_ms = 45000
        s.local_evidence_dir = "/env/evidence"
        yield


def _device(config: dict | None) -> Device:
    return Device(
        device_id="DEV-1",
        name="Dev",
        connection_config=config,
        capture_interval_ms=120000,
    )


# ── Camada 1: device.connection_config ──


class TestDeviceLayer:
    def test_device_overrides_everything(self):
        cfg = resolve_device_config(_device({
            "ip": "192.168.1.50",
            "username": "dev-user",
            "password": "dev-pass",
            "channel": 3,
            "stream_type": "main",
            "transport": "tcp",
        }))
        assert cfg["ip"] == "192.168.1.50"
        assert cfg["username"] == "dev-user"
        assert cfg["password"] == "dev-pass"
        assert cfg["channel"] == 3
        assert cfg["stream_type"] == "main"
        assert cfg["transport"] == "tcp"

    def test_device_partial_config_fills_rest_from_lower_layers(self):
        cfg = resolve_device_config(_device({"ip": "192.168.1.51"}))
        assert cfg["ip"] == "192.168.1.51"
        assert cfg["username"] == "admin"

    def test_empty_string_in_device_defers_to_lower_layer(self):
        cfg = resolve_device_config(_device({"username": "", "ip": ""}))
        assert cfg["username"] == "admin"
        assert cfg["ip"] == "10.10.10.10"

    def test_none_value_in_device_defers(self):
        cfg = resolve_device_config(_device({"password": None}))
        assert cfg["password"] == "env-pass"


# ── Camada 2: SystemSettings (DB) ──


class TestSystemSettingsLayer:
    def test_db_setting_beats_env(self):
        db = TestSession()
        db.add(SystemSettings(key="camera_default_username", value="db-user"))
        db.commit()
        db.close()
        cfg = resolve_device_config(_device({}))
        assert cfg["username"] == "db-user"

    def test_db_password_used_when_device_has_none(self):
        db = TestSession()
        db.add(SystemSettings(key="camera_default_password", value="db-pass"))
        db.commit()
        db.close()
        cfg = resolve_device_config(_device({}))
        assert cfg["password"] == "db-pass"

    def test_empty_db_value_defers_to_env(self):
        db = TestSession()
        db.add(SystemSettings(key="camera_default_password", value=""))
        db.commit()
        db.close()
        cfg = resolve_device_config(_device({}))
        assert cfg["password"] == "env-pass"

    def test_db_channel_coerced_to_int(self):
        db = TestSession()
        db.add(SystemSettings(key="camera_default_channel", value="4"))
        db.commit()
        db.close()
        cfg = resolve_device_config(_device({}))
        assert cfg["channel"] == 4
        assert isinstance(cfg["channel"], int)

    def test_db_jpeg_quality_coerced(self):
        db = TestSession()
        db.add(SystemSettings(key="capture_jpeg_quality", value="65"))
        db.commit()
        db.close()
        cfg = resolve_device_config(_device({}))
        assert cfg["jpeg_quality"] == 65


# ── Camadas 2/3: SystemSettings (DB) vence .env para chaves mapeadas ──


class TestLowerLayers:
    def test_mapped_keys_use_system_settings_defaults(self):
        """Chaves mapeadas nunca chegam ao .env: o default do DB cobre."""
        cfg = resolve_device_config(_device({}))
        assert cfg["username"] == "admin"
        assert cfg["stream_type"] == "main"
        assert cfg["transport"] == "tcp"
        assert cfg["channel"] == 1
        assert cfg["connect_timeout_ms"] == 10000
        assert cfg["jpeg_quality"] == 90
        assert cfg["capture_width"] == 1920
        assert cfg["capture_height"] == 1080
        assert cfg["evidence_dir"] == "/var/lib/vision-platform-local/evidence"

    def test_unmapped_keys_fall_through_to_env(self):
        """ip e hostname não têm setting no DB — vão direto ao .env."""
        cfg = resolve_device_config(_device({}))
        assert cfg["ip"] == "10.10.10.10"
        assert cfg["hostname"] == "env-host"

    def test_resolve_with_none_device_uses_env(self):
        cfg = resolve_device_config(None)
        assert cfg["hostname"] == "env-host"

    def test_module_defaults_for_empty_unmapped_keys(self):
        from types import SimpleNamespace

        empty_env = SimpleNamespace(
            camera_ip="", camera_hostname="", camera_channel=None,
        )
        with patch("src.config.device_config.settings", empty_env):
            cfg = resolve_device_config(_device({}))
        assert cfg["ip"] == ""
        assert cfg["hostname"] == ""

    def test_bad_int_in_device_falls_back_to_default(self):
        cfg = resolve_device_config(_device({"channel": "xyz", "connect_timeout_ms": "abc"}))
        assert cfg["channel"] == 1
        assert cfg["connect_timeout_ms"] == 10000


# ── capture_interval_ms ──


class TestCaptureIntervalMs:
    def test_connection_config_wins(self):
        cfg = resolve_device_config(_device({"capture_interval_ms": 9999}))
        assert cfg["capture_interval_ms"] == 9999

    def test_device_column_second(self):
        cfg = resolve_device_config(_device({}))
        assert cfg["capture_interval_ms"] == 120000

    def test_global_minutes_third(self):
        db = TestSession()
        db.add(SystemSettings(key="capture_interval_minutes", value="5"))
        db.commit()
        db.close()
        device = _device({})
        device.capture_interval_ms = None
        cfg = resolve_device_config(device)
        assert cfg["capture_interval_ms"] == 300000

    def test_db_default_minutes_used_before_env(self):
        from src.config.global_settings import get_setting

        device = _device({})
        device.capture_interval_ms = None
        cfg = resolve_device_config(device)
        expected = int(get_setting("capture_interval_minutes")) * 60_000
        assert cfg["capture_interval_ms"] == expected

    def test_zero_minutes_invalid_falls_through(self):
        db = TestSession()
        db.add(SystemSettings(key="capture_interval_minutes", value="0"))
        db.commit()
        db.close()
        device = _device({})
        device.capture_interval_ms = None
        cfg = resolve_device_config(device)
        assert cfg["capture_interval_ms"] == 45000


# ── Tipos e sanidade geral ──


class TestConfigShape:
    def test_all_keys_present(self):
        cfg = resolve_device_config(_device({}))
        expected = {
            "username", "password", "stream_type", "transport", "channel",
            "connect_timeout_ms", "jpeg_quality", "capture_width",
            "capture_height", "evidence_dir", "ip", "hostname",
            "capture_interval_ms",
        }
        assert set(cfg.keys()) == expected

    def test_int_keys_are_ints(self):
        cfg = resolve_device_config(_device({}))
        for key in ("channel", "connect_timeout_ms", "jpeg_quality",
                    "capture_width", "capture_height", "capture_interval_ms"):
            assert isinstance(cfg[key], int), f"{key} should be int"

    def test_str_keys_are_str(self):
        cfg = resolve_device_config(_device({}))
        for key in ("username", "password", "stream_type", "transport",
                    "evidence_dir", "ip", "hostname"):
            assert isinstance(cfg[key], str), f"{key} should be str"
