from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.storage.database import Base

DEVICE_TYPES = ["camera", "sensor", "other"]
TASK_TYPES = ["fissure", "ppe", "fabric_quality", "structural"]
CONNECTION_TYPES = ["rtsp", "mqtt", "http", "serial"]


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

    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    delivery_logs = relationship("DeliveryLog", back_populates="observation", cascade="all, delete-orphan")


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
