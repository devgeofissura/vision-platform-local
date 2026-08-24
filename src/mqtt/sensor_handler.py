"""Processamento de mensagens MQTT de sensores.

Payloads aceitos (JSON):
    Forma explícita:
        {"type": "temperature", "value": 25.5, "unit": "°C", "ts": 1690000000}
    Forma multi-métrica (qualquer chave numérica vira uma leitura):
        {"temperature": 25.5, "humidity": 61.2}
"""
import json
import logging
from datetime import UTC, datetime
from typing import Any

from src.config.global_settings import get_setting
from src.storage.models import SensorReading

logger = logging.getLogger(__name__)

DEFAULT_UNITS = {
    "temperature": "°C",
    "humidity": "%",
    "pressure": "hPa",
    "co2": "ppm",
    "lux": "lx",
    "pm25": "µg/m³",
    "pm10": "µg/m³",
    "voc": "ppb",
    "distance": "cm",
    "vibration": "mm/s",
    "battery": "%",
}


def extract_device_id(topic: str) -> str | None:
    """Extrai o device_id de '{prefix}{device_id}/sensors'."""
    prefix = get_setting("mqtt_topic_prefix") or "geofissura/"
    if not topic.startswith(prefix):
        return None
    remainder = topic[len(prefix):]
    parts = remainder.split("/")
    if not parts or not parts[0]:
        return None
    return parts[0]


def _parse_timestamp(raw: Any) -> datetime | None:
    if raw is None:
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    if value > 1e12:
        value /= 1000.0
    try:
        return datetime.fromtimestamp(value, tz=UTC).replace(tzinfo=None)
    except (OverflowError, OSError, ValueError):
        return None


def parse_payload(payload: bytes | str | dict) -> list[dict[str, Any]]:
    """Converte um payload JSON em lista de leituras normalizadas."""
    if isinstance(payload, dict):
        data = payload
    else:
        try:
            data = json.loads(payload if isinstance(payload, str) else payload.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            logger.warning("MQTT payload não é JSON válido: %r", payload[:120])
            return []

    if not isinstance(data, dict):
        logger.warning("MQTT payload JSON não é objeto: %r", payload[:120] if not isinstance(payload, dict) else data)
        return []

    ts = _parse_timestamp(data.get("ts") or data.get("timestamp"))

    if "type" in data and "value" in data:
        readings = [{
            "reading_type": str(data["type"])[:32],
            "value_float": float(v) if isinstance(v := data["value"], (int, float)) else None,
            "value_text": None if isinstance(v, (int, float)) else str(v),
            "unit": data.get("unit"),
            "recorded_at": ts,
        }]
    else:
        readings = []
        for key, value in data.items():
            if key in ("ts", "timestamp", "device_id"):
                continue
            if isinstance(value, bool):
                readings.append({
                    "reading_type": str(key)[:32],
                    "value_float": 1.0 if value else 0.0,
                    "value_text": None,
                    "unit": DEFAULT_UNITS.get(key),
                    "recorded_at": ts,
                })
            elif isinstance(value, (int, float)):
                readings.append({
                    "reading_type": str(key)[:32],
                    "value_float": float(value),
                    "value_text": None,
                    "unit": DEFAULT_UNITS.get(key),
                    "recorded_at": ts,
                })
            elif isinstance(value, str):
                readings.append({
                    "reading_type": str(key)[:32],
                    "value_float": None,
                    "value_text": value,
                    "unit": None,
                    "recorded_at": ts,
                })

    for reading in readings:
        if reading["unit"] is None:
            reading["unit"] = DEFAULT_UNITS.get(reading["reading_type"])
    return readings


class SensorHandler:
    """Recebe mensagens MQTT e persiste SensorReadings."""

    def __init__(self, session_factory=None):
        self._session_factory = session_factory

    def handle(self, topic: str, payload: bytes | str) -> int:
        """Processa uma mensagem; retorna quantidade de leituras salvas."""
        device_id = extract_device_id(topic)
        if device_id is None:
            logger.warning("Tópico MQTT fora do padrão, ignorado: %s", topic)
            return 0

        parsed = parse_payload(payload)
        if not parsed:
            return 0

        factory = self._session_factory
        raw_text = payload.decode("utf-8", errors="replace") if isinstance(payload, bytes) else payload
        saved = 0
        db = None
        try:
            db = factory() if factory else _default_session()
            for item in parsed:
                recorded_at = item.pop("recorded_at") or datetime.now(UTC).replace(tzinfo=None)
                db.add(SensorReading(
                    device_id=device_id,
                    topic=topic,
                    raw_payload=raw_text,
                    recorded_at=recorded_at,
                    **item,
                ))
                saved += 1
            db.commit()
        except Exception:
            if db is not None:
                db.rollback()
            logger.exception("Falha ao salvar leituras do tópico %s", topic)
            return 0
        finally:
            if factory is None and db is not None:
                db.close()
        logger.info("SensorHandler: %d leitura(s) salva(s) de %s", saved, topic)
        return saved


def _default_session():
    from src.storage.database import SessionLocal

    return SessionLocal()
