import logging
from typing import Any

from sqlalchemy.orm import Session

from src.storage.database import SessionLocal
from src.storage.models import SystemSettings

logger = logging.getLogger(__name__)

_DEFAULT_SPECS: dict[str, tuple[str, str]] = {
    # Geral
    "local_id": ("sl000001", "Identificador único deste local"),
    "local_name": ("Orange Pi 001", "Nome amigável do local"),
    "timezone": ("America/Sao_Paulo", "Fuso horário"),
    # Captura global
    "capture_interval_minutes": ("60", "Intervalo padrão de captura em minutos"),
    "capture_schedule": ("07:00,12:00,23:00", "Horários diários de captura HH:MM (vírgula; vazio = intervalo)"),
    "capture_evidence_dir": ("/var/lib/vision-platform-local/evidence", "Diretório de evidências"),
    "capture_jpeg_quality": ("90", "Qualidade JPEG padrão (1-100)"),
    "capture_width": ("1920", "Largura padrão da captura"),
    "capture_height": ("1080", "Altura padrão da captura"),
    # Câmera padrão
    "camera_default_username": ("admin", "Usuário padrão das câmeras"),
    "camera_default_password": ("", "Senha padrão das câmeras"),
    "camera_default_stream_type": ("main", "Stream padrão (main ou sub)"),
    "camera_default_channel": ("1", "Canal padrão"),
    "camera_default_transport": ("tcp", "Transporte RTSP padrão"),
    "camera_connect_timeout_ms": ("10000", "Timeout de conexão RTSP (ms)"),
    # Entrega (central)
    "delivery_interval_seconds": ("60", "Intervalo de entrega à central (s)"),
    "central_api_base_url": ("", "URL da API central"),
    "central_api_token": ("", "Token de autenticação da central"),
    # MQTT
    "mqtt_broker_host": ("localhost", "Host do broker MQTT"),
    "mqtt_broker_port": ("1883", "Porta do broker MQTT"),
    "mqtt_username": ("", "Usuário MQTT"),
    "mqtt_password": ("", "Senha MQTT"),
    "mqtt_topic_prefix": ("geofissura/", "Prefixo dos tópicos MQTT"),
    "mqtt_enabled": ("false", "Habilitar cliente MQTT"),
    # Processamento
    "processing_enabled": ("false", "Habilitar processamento de visão"),
    "processing_auto_on_capture": ("true", "Processar automaticamente ao capturar"),
    # Inspeção de tecido
    "fabric_width_cm": ("150", "Largura do tecido (cm, ourela a ourela) para medição de defeitos"),
    "fabric_feed_rate_m_min": ("20", "Velocidade de inspeção do tecido (m/min) para estimar metragem"),
    "fabric_pass_meters": ("100", "Comprimento de lote (metros) para pontuação por 100 m²"),
    "fabric_point_threshold": ("24", "Limite de aceitação (pontos por 100 m², ASTM D5430)"),
}

DEFAULT_SETTINGS: dict[str, str] = {k: spec[0] for k, spec in _DEFAULT_SPECS.items()}
DEFAULT_DESCRIPTIONS: dict[str, str] = {k: spec[1] for k, spec in _DEFAULT_SPECS.items()}

_cache: dict[str, str] = {}


def clear_cache() -> None:
    _cache.clear()


def get_setting(key: str, default: str | None = None, db: Session | None = None) -> str | None:
    if key in _cache:
        return _cache[key]

    own_db = db is None
    if own_db:
        db = SessionLocal()
    try:
        row = db.query(SystemSettings).filter(SystemSettings.key == key).first()
    finally:
        if own_db:
            db.close()

    if row is not None:
        _cache[key] = row.value
        return row.value
    if key in DEFAULT_SETTINGS:
        return DEFAULT_SETTINGS[key]
    return default


def get_setting_int(key: str, default: int = 0, db: Session | None = None) -> int:
    raw = get_setting(key, db=db)
    if raw is None:
        return default
    try:
        return int(raw)
    except (ValueError, TypeError):
        return default


def get_setting_float(key: str, default: float = 0.0, db: Session | None = None) -> float:
    raw = get_setting(key, db=db)
    if raw is None:
        return default
    try:
        return float(raw)
    except (ValueError, TypeError):
        return default


def get_setting_bool(key: str, default: bool = False, db: Session | None = None) -> bool:
    raw = get_setting(key, db=db)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in ("true", "1", "yes", "on")


def set_setting(key: str, value: Any, description: str | None = None, db: Session | None = None) -> None:
    text_value = "" if value is None else str(value)
    own_db = db is None
    if own_db:
        db = SessionLocal()
    try:
        row = db.query(SystemSettings).filter(SystemSettings.key == key).first()
        if row is None:
            row = SystemSettings(
                key=key,
                value=text_value,
                description=description or DEFAULT_DESCRIPTIONS.get(key),
            )
            db.add(row)
        else:
            row.value = text_value
            if description:
                row.description = description
        db.commit()
    finally:
        if own_db:
            db.close()
    _cache[key] = text_value


def set_settings(updates: dict[str, Any], db: Session | None = None) -> None:
    own_db = db is None
    if own_db:
        db = SessionLocal()
    try:
        for key, value in updates.items():
            set_setting(key, value, db=db)
    finally:
        if own_db:
            db.close()


def get_all_settings(db: Session | None = None) -> dict[str, str]:
    own_db = db is None
    if own_db:
        db = SessionLocal()
    try:
        rows = db.query(SystemSettings).all()
    finally:
        if own_db:
            db.close()
    result = dict(DEFAULT_SETTINGS)
    result.update({row.key: row.value for row in rows})
    return result


def seed_default_settings(db: Session | None = None) -> int:
    own_db = db is None
    if own_db:
        db = SessionLocal()
    inserted = 0
    try:
        existing = {row.key for row in db.query(SystemSettings.key).all()}
        for key, (value, description) in _DEFAULT_SPECS.items():
            if key in existing:
                continue
            db.add(SystemSettings(key=key, value=value, description=description))
            inserted += 1
        if inserted:
            db.commit()
            logger.info("Seeded %d default settings", inserted)
    finally:
        if own_db:
            db.close()
    clear_cache()
    return inserted
