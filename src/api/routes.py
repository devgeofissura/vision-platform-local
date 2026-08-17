import shutil

import psutil
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from src.config.settings import settings

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
async def health():
    try:
        disk = shutil.disk_usage(settings.local_data_dir)
        free_bytes, total_bytes = disk.free, disk.total
    except FileNotFoundError:
        free_bytes, total_bytes = 0, 0

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
            "queue_pending": 0,
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
async def list_observations(cursor: str | None = None):
    # TODO: implement cursor-based pagination from database
    return {"observations": [], "next_cursor": None}


@router.post("/api/v1/observations/{observation_id}/ack")
async def ack_observation(observation_id: str, token: str = Depends(verify_token)):
    # TODO: mark observation as delivered in database
    return {"observation_id": observation_id, "status": "acknowledged"}
