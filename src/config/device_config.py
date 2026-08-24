"""Resolução de configuração de device com fallback em camadas.

Hierarquia (primeira camada com valor não vazio vence):
    1. Device.connection_config / colunas do Device
    2. SystemSettings (DB, editável pelo dashboard)
    3. Settings (.env)
    4. Constantes padrão deste módulo
"""
import logging
from typing import Any

from src.config.global_settings import get_setting
from src.config.settings import settings
from src.storage.models import Device

logger = logging.getLogger(__name__)

_STR_DEFAULTS = {
    "username": "admin",
    "password": "",
    "stream_type": "main",
    "transport": "tcp",
    "ip": "",
    "hostname": "",
    "evidence_dir": "./evidence",
}

_INT_DEFAULTS = {
    "channel": 1,
    "connect_timeout_ms": 10000,
    "jpeg_quality": 90,
    "capture_width": 1920,
    "capture_height": 1080,
    "capture_interval_ms": 60000,
}


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    return True


def _pick(raw: dict, config_key: str, setting_key: str | None, env_attr: str | None) -> Any:
    value = raw.get(config_key)
    if _has_value(value):
        return value
    if setting_key:
        value = get_setting(setting_key)
        if _has_value(value):
            return value
    if env_attr:
        value = getattr(settings, env_attr, None)
        if _has_value(value):
            return value
    return None


def _to_int(value: Any, fallback: int) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return fallback


def resolve_device_config(device: Device | None = None) -> dict[str, Any]:
    """Resolve a config final de um device aplicando a hierarquia de fallback."""
    raw = (device.connection_config or {}) if device is not None else {}

    config: dict[str, Any] = {}
    for key, (setting_key, env_attr) in _SETTING_ENV_MAP.items():
        value = _pick(raw, key, setting_key, env_attr)
        if key in _INT_KEYS:
            default = _INT_DEFAULTS[key]
            config[key] = _to_int(value, default) if _has_value(value) else default
        else:
            config[key] = str(value) if _has_value(value) else _STR_DEFAULTS[key]

    config["capture_interval_ms"] = _resolve_interval_ms(raw, device)

    logger.debug("Resolved device config (device=%s): %s", getattr(device, "device_id", None), {
        k: ("***" if k == "password" else v) for k, v in config.items()
    })
    return config


_SETTING_ENV_MAP: dict[str, tuple[str | None, str | None]] = {
    "username": ("camera_default_username", "camera_username"),
    "password": ("camera_default_password", "camera_password"),
    "stream_type": ("camera_default_stream_type", "camera_stream_type"),
    "transport": ("camera_default_transport", "camera_rtsp_transport"),
    "channel": ("camera_default_channel", "camera_channel"),
    "connect_timeout_ms": ("camera_connect_timeout_ms", "camera_connect_timeout_ms"),
    "jpeg_quality": ("capture_jpeg_quality", "camera_capture_jpeg_quality"),
    "capture_width": ("capture_width", "camera_capture_width"),
    "capture_height": ("capture_height", "camera_capture_height"),
    "evidence_dir": ("capture_evidence_dir", "local_evidence_dir"),
    "ip": (None, "camera_ip"),
    "hostname": (None, "camera_hostname"),
}

_INT_KEYS = set(_INT_DEFAULTS)


def _resolve_interval_ms(raw: dict, device: Device | None) -> int:
    value = raw.get("capture_interval_ms")
    if _has_value(value):
        return _to_int(value, _INT_DEFAULTS["capture_interval_ms"])

    if device is not None and device.capture_interval_ms:
        return int(device.capture_interval_ms)

    minutes = get_setting("capture_interval_minutes")
    if _has_value(minutes):
        parsed = _to_int(minutes, 0)
        if parsed > 0:
            return parsed * 60_000

    env_value = getattr(settings, "camera_capture_interval_ms", None)
    if _has_value(env_value):
        return _to_int(env_value, _INT_DEFAULTS["capture_interval_ms"])

    return _INT_DEFAULTS["capture_interval_ms"]
