import os
import shutil
from datetime import UTC, datetime
from pathlib import Path

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


@router.post("/api/v1/capture")
async def manual_capture(token: str = Depends(verify_token)):
    from src.camera.capture_worker import CaptureWorker

    worker = CaptureWorker()
    try:
        result = worker.capture()
        if result is None:
            raise HTTPException(status_code=503, detail="Camera not available or capture failed")
        return result
    finally:
        worker.disconnect()


@router.get("/api/v1/capture/latest-image")
async def latest_capture_image(token: str = Depends(verify_token)):
    evidence_dir = Path(settings.local_evidence_dir)
    if not evidence_dir.exists():
        raise HTTPException(status_code=404, detail="No captures yet")

    latest_dirs = sorted(evidence_dir.glob("**/*_full.jpg"), reverse=True)
    if not latest_dirs:
        raise HTTPException(status_code=404, detail="No captures yet")

    latest = latest_dirs[0]
    import base64
    from fastapi.responses import Response

    image_bytes = latest.read_bytes()
    return Response(content=image_bytes, media_type="image/jpeg")


@router.get("/api/v1/stream/{camera_id}")
async def stream_camera(camera_id: str, token: str = Query(None), x_api_token: str = Header(None)):
    api_token = token or x_api_token
    if api_token != settings.local_api_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    from fastapi.responses import StreamingResponse
    import cv2
    import time

    db = SessionLocal()
    try:
        device = db.query(Device).filter(Device.device_id == camera_id).first()
        if not device or device.device_type != "camera":
            raise HTTPException(status_code=404, detail="Camera not found")

        config = device.connection_config or {}
        ip = config.get("ip", "")
        username = config.get("username", settings.camera_username)
        password = settings.camera_password
        channel = config.get("channel", settings.camera_channel)
        stream_type = config.get("stream_type", settings.camera_stream_type)
        stream_value = "0" if stream_type == "main" else "1"

        if not ip:
            raise HTTPException(status_code=400, detail="Camera IP not configured in device")

        rtsp_url = f"rtsp://{username}:{password}@{ip}:554/cam/realmonitor?channel={channel}&subtype={stream_value}"
    finally:
        db.close()

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 10000)

    if not cap.isOpened():
        raise HTTPException(status_code=503, detail="Cannot connect to camera")

    def generate():
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                _, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n")
                time.sleep(0.05)
        finally:
            cap.release()

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")
