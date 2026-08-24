from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.storage.database import Base

DEVICE_TYPES = ["camera", "sensor", "other"]
TASK_TYPES = ["fissure", "ppe", "fabric_quality", "structural"]
CONNECTION_TYPES = ["rtsp", "onvif", "http", "mqtt", "serial"]
RESULT_TYPES = ["fissure", "person", "ppe", "plate", "count", "fabric_defect"]
PROCESSING_STATUSES = ["none", "pending", "processing", "completed", "failed"]


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    device_type = Column(String(32), nullable=False, default="camera")
    task_type = Column(String(32), nullable=False, default="fissure")
    connection_type = Column(String(32), nullable=False, default="rtsp")
    connection_config = Column(JSON, nullable=True, default=dict)
    capture_interval_ms = Column(Integer, nullable=False, default=60000)
    auto_capture_enabled = Column(Boolean, nullable=False, default=False)
    auto_capture_interval_minutes = Column(Integer, nullable=False, default=60)
    last_auto_capture_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "device_id": self.device_id,
            "name": self.name,
            "device_type": self.device_type,
            "task_type": self.task_type,
            "connection_type": self.connection_type,
            "connection_config": self.connection_config or {},
            "capture_interval_ms": self.capture_interval_ms,
            "auto_capture_enabled": self.auto_capture_enabled,
            "auto_capture_interval_minutes": self.auto_capture_interval_minutes,
            "last_auto_capture_at": self.last_auto_capture_at.isoformat() if self.last_auto_capture_at else None,
            "is_active": self.is_active,
        }


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    observation_id = Column(String(128), unique=True, nullable=False, index=True)
    camera_id = Column(String(64), nullable=False, index=True)
    local_id = Column(String(64), nullable=False, index=True)
    captured_at = Column(DateTime, nullable=False, index=True)
    file_path = Column(Text, nullable=False)
    sha256 = Column(String(64), nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    quality_score = Column(Float, nullable=True)
    quality_issues = Column(Text, nullable=True)
    algorithm_version = Column(String(32), nullable=True)

    delivery_status = Column(String(32), nullable=False, default="pending", index=True)
    delivery_attempts = Column(Integer, nullable=False, default=0)
    last_delivery_at = Column(DateTime, nullable=True)
    last_delivery_error = Column(Text, nullable=True)
    delivered_at = Column(DateTime, nullable=True)

    processing_status = Column(String(32), nullable=False, default="none")
    processing_started_at = Column(DateTime, nullable=True)
    processing_completed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    delivery_logs = relationship("DeliveryLog", back_populates="observation", cascade="all, delete-orphan")
    processing_results = relationship("ProcessingResult", back_populates="observation", cascade="all, delete-orphan")


class DeliveryLog(Base):
    __tablename__ = "delivery_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    observation_id = Column(String(128), ForeignKey("observations.observation_id"), nullable=False, index=True)
    attempt = Column(Integer, nullable=False)
    status = Column(String(32), nullable=False)
    status_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    observation = relationship("Observation", back_populates="delivery_logs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(32), nullable=False, default="admin")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))


class ProcessingResult(Base):
    __tablename__ = "processing_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    observation_id = Column(String(128), ForeignKey("observations.observation_id"), nullable=False, index=True)
    device_id = Column(String(64), nullable=False, index=True)

    result_type = Column(String(32), nullable=False, index=True)
    model_name = Column(String(64), nullable=False)
    model_version = Column(String(32), nullable=False)
    confidence = Column(Float, nullable=False)

    result_data = Column(JSON, nullable=False)

    inference_ms = Column(Integer, nullable=True)
    image_width = Column(Integer, nullable=True)
    image_height = Column(Integer, nullable=True)

    delivered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    observation = relationship("Observation", back_populates="processing_results")


class TrackingSession(Base):
    __tablename__ = "tracking_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(128), unique=True, nullable=False, index=True)
    device_id = Column(String(64), nullable=False, index=True)
    entity_type = Column(String(32), nullable=False)
    entity_id = Column(String(64), nullable=True, index=True)

    first_seen_at = Column(DateTime, nullable=False)
    last_seen_at = Column(DateTime, nullable=False)
    frame_count = Column(Integer, nullable=False, default=1)

    avg_bbox_width = Column(Float, nullable=True)
    avg_bbox_height = Column(Float, nullable=True)
    path_centroids = Column(JSON, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class ZoneConfig(Base):
    __tablename__ = "zone_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(64), nullable=False, index=True)
    zone_name = Column(String(64), nullable=False)
    zone_type = Column(String(32), nullable=False)

    polygon_vertices = Column(JSON, nullable=False)
    zone_config = Column(JSON, nullable=False, default=dict)

    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))


class SystemSettings(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(64), nullable=False, index=True)
    topic = Column(String(256), nullable=True)
    reading_type = Column(String(32), nullable=False, index=True)
    value_float = Column(Float, nullable=True)
    value_text = Column(Text, nullable=True)
    unit = Column(String(16), nullable=True)
    raw_payload = Column(Text, nullable=True)
    recorded_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "device_id": self.device_id,
            "topic": self.topic,
            "reading_type": self.reading_type,
            "value_float": self.value_float,
            "value_text": self.value_text,
            "unit": self.unit,
            "raw_payload": self.raw_payload,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
