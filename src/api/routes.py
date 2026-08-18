import shutil
from datetime import UTC, datetime

import psutil
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.storage.database import get_db
from src.storage.delivery_queue import process_delivery_queue
from src.storage.models import Observation

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    local_id: str
    service: str
    camera: dict
    storage: dict
    version: str


class ObservationAck(BaseModel):
    observation_id: str


def verify_token(x_api_token: str = Header(...)):
    if x_api_token != settings.local_api_token:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/health", response_model=HealthResponse)
async def health(db: Session = Depends(get_db)):
    try:
        disk = shutil.disk_usage(settings.local_data_dir)
        free_bytes, total_bytes = disk.free, disk.total
    except FileNotFoundError:
        free_bytes, total_bytes = 0, 0

    queue_pending = db.query(Observation).filter(
        Observation.delivery_status.in_(["pending", "retry"])
    ).count()

    return HealthResponse(
        status="ok",
        local_id=settings.local_id,
        service="vision-platform-local",
        camera={
            "camera_id": settings.camera_id,
            "status": "unknown",
            "last_frame_at": None,
        },
        storage={
            "free_bytes": free_bytes,
            "total_bytes": total_bytes,
            "queue_pending": queue_pending,
        },
        version="0.1.0",
    )


@router.get("/api/v1/status")
async def status():
    return {
        "local_id": settings.local_id,
        "local_name": settings.local_name,
        "uptime_seconds": 0,
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
    }


@router.get("/api/v1/cameras")
async def list_cameras():
    return {
        "cameras": [
            {
                "camera_id": settings.camera_id,
                "name": settings.camera_name,
                "status": "unknown",
            }
        ]
    }


@router.get("/api/v1/observations")
async def list_observations(
    cursor: str | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Observation)

    if cursor:
        cursor_obs = db.query(Observation).filter(Observation.observation_id == cursor).first()
        if cursor_obs:
            query = query.filter(Observation.captured_at > cursor_obs.captured_at)

    if status_filter:
        query = query.filter(Observation.delivery_status == status_filter)

    observations = (
        query.order_by(Observation.captured_at.desc())
        .limit(limit + 1)
        .all()
    )

    has_next = len(observations) > limit
    items = observations[:limit]

    next_cursor = items[-1].observation_id if has_next and items else None

    return {
        "observations": [
            {
                "observation_id": obs.observation_id,
                "camera_id": obs.camera_id,
                "local_id": obs.local_id,
                "captured_at": obs.captured_at.isoformat(),
                "sha256": obs.sha256,
                "width": obs.width,
                "height": obs.height,
                "quality_score": obs.quality_score,
                "delivery_status": obs.delivery_status,
                "delivery_attempts": obs.delivery_attempts,
                "created_at": obs.created_at.isoformat(),
            }
            for obs in items
        ],
        "next_cursor": next_cursor,
    }


@router.post("/api/v1/observations/{observation_id}/ack")
async def ack_observation(
    observation_id: str,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    obs = db.query(Observation).filter(Observation.observation_id == observation_id).first()
    if obs is None:
        raise HTTPException(status_code=404, detail="Observation not found")

    obs.delivery_status = "acknowledged"
    obs.delivered_at = datetime.now(UTC)
    obs.updated_at = datetime.now(UTC)
    db.commit()

    return {"observation_id": observation_id, "status": "acknowledged"}


@router.post("/api/v1/delivery/flush")
async def flush_delivery(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    result = process_delivery_queue(db=db)
    return result
