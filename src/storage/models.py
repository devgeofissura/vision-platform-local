from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.storage.database import Base


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
