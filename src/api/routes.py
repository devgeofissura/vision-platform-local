import logging
import os
import shutil
from datetime import UTC, datetime
from pathlib import Path

import psutil
from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.storage.database import SessionLocal, get_db
from src.storage.delivery_queue import process_delivery_queue
from src.storage.models import Device, Observation, ProcessingResult, SensorReading, ZoneConfig

logger = logging.getLogger(__name__)

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


@router.get("/api/v1/settings")
async def get_settings_api():
    from src.config.global_settings import DEFAULT_DESCRIPTIONS, get_all_settings

    all_values = get_all_settings()
    return {
        "settings": {
            key: {"value": all_values.get(key, ""), "description": DEFAULT_DESCRIPTIONS.get(key, "")}
            for key in sorted(all_values)
        },
        "count": len(all_values),
    }


@router.post("/api/v1/settings")
async def update_settings_api(payload: dict):
    from src.config.global_settings import (
        DEFAULT_SETTINGS,
        clear_cache,
        set_settings,
    )

    if not isinstance(payload, dict) or not payload:
        raise HTTPException(status_code=400, detail="body must be a non-empty JSON object")

    unknown = [k for k in payload if k not in DEFAULT_SETTINGS]
    if unknown:
        raise HTTPException(
            status_code=400,
            detail=f"unknown settings keys: {', '.join(sorted(unknown))}",
        )

    set_settings({k: v for k, v in payload.items()})
    clear_cache()

    return {"updated": len(payload), "keys": sorted(payload.keys())}


@router.get("/api/v1/sensors/readings")
async def list_sensor_readings(
    device_id: str | None = Query(None),
    reading_type: str | None = Query(None),
    since_id: int | None = Query(None, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(SensorReading)

    if device_id:
        query = query.filter(SensorReading.device_id == device_id)
    if reading_type:
        query = query.filter(SensorReading.reading_type == reading_type)
    if since_id is not None:
        query = query.filter(SensorReading.id > since_id)

    readings = (
        query.order_by(SensorReading.recorded_at.desc(), SensorReading.id.desc())
        .limit(limit + 1)
        .all()
    )

    has_next = len(readings) > limit
    items = readings[:limit]
    next_since_id = items[-1].id if has_next and items else None

    return {
        "readings": [r.to_dict() for r in items],
        "next_since_id": next_since_id,
        "count": len(items),
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
    from fastapi.responses import Response

    image_bytes = latest.read_bytes()
    return Response(content=image_bytes, media_type="image/jpeg")


@router.get("/api/v1/debug/camera/{camera_id}")
async def debug_camera(camera_id: str, x_api_token: str = Header(None)):
    if x_api_token != settings.local_api_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    import cv2

    db = SessionLocal()
    try:
        device = db.query(Device).filter(Device.device_id == camera_id).first()
        if not device:
            return {"status": "error", "detail": f"Device '{camera_id}' not found in DB"}

        config = device.connection_config or {}
        ip = config.get("ip", "")
        username = config.get("username", "")
        password = config.get("password", "")
        channel = config.get("channel", 1)
        stream_type = config.get("stream_type", "main")
        stream_value = "0" if stream_type == "main" else "1"

        if not ip:
            return {"status": "error", "detail": "No IP in device connection_config", "config": config}

        rtsp_url = f"rtsp://{username}:{password}@{ip}:554/cam/realmonitor?channel={channel}&subtype={stream_value}"
        redacted = f"rtsp://{username}:***@{ip}:554/cam/realmonitor?channel={channel}&subtype={stream_value}"
    finally:
        db.close()

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 10000)

    if not cap.isOpened():
        return {"status": "error", "detail": "Cannot open RTSP stream", "url": redacted}

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        return {"status": "error", "detail": "Cannot read frame", "url": redacted}

    return {
        "status": "ok",
        "url": redacted,
        "width": frame.shape[1],
        "height": frame.shape[0],
    }


def _open_camera_stream(camera_id: str, decoding_res: tuple[int, int] | None = None):
    """Validate token+device, build RTSP URL, open VideoCapture.

    If `decoding_res` (width, height) is given, the FFmpeg decoder is asked
    to decode directly at that size (CAP_PROP_FRAME_WIDTH/HEIGHT), which
    reduces real decode cost — the main bottleneck on the Orange Pi — not
    just the output resize. A defensive cv2.resize is also applied when the
    decoder ignores the property.

    Raises HTTPException on error; returns an opened cv2.VideoCapture.
    """
    import cv2

    db = SessionLocal()
    try:
        device = db.query(Device).filter(Device.device_id == camera_id).first()
        if not device or device.device_type != "camera":
            raise HTTPException(status_code=404, detail="Camera not found")

        config = device.connection_config or {}
        ip = config.get("ip", "")
        username = config.get("username", settings.camera_username)
        password = config.get("password", settings.camera_password)
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

    if decoding_res is not None:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, decoding_res[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, decoding_res[1])

    if not cap.isOpened():
        raise HTTPException(status_code=503, detail="Cannot connect to camera")
    return cap


_STREAM_RESOLUTIONS = {
    "1080p": (1920, 1080),
    "720p": (1280, 720),
    "540p": (960, 540),
    "360p": (640, 360),
}


def _parse_resolution(res: str) -> tuple[int, int]:
    """Map a resolution label (1080p/720p/540p/360p or WxH) to (width, height).

    Raises HTTPException(400) on unknown/negative values.
    """
    res = (res or "").strip().lower()
    if res in _STREAM_RESOLUTIONS:
        return _STREAM_RESOLUTIONS[res]

    # Arbitrary WxH, e.g. "720x540" or "640x480".
    if "x" in res:
        parts = res.split("x")
        if len(parts) == 2:
            try:
                w = int(parts[0])
                h = int(parts[1])
            except ValueError:
                w = h = 0
            if 0 < w <= 7680 and 0 < h <= 4320:
                return w, h

    raise HTTPException(
        status_code=400,
        detail=f"Invalid resolution '{res}'. Use one of "
        f"{list(_STREAM_RESOLUTIONS)} or a WxH like 720x540.",
    )


@router.get("/api/v1/stream/{camera_id}")
async def stream_camera(camera_id: str, token: str = Query(None), x_api_token: str = Header(None)):
    api_token = token or x_api_token
    if api_token != settings.local_api_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    import time

    import cv2
    from fastapi.responses import StreamingResponse

    cap = _open_camera_stream(camera_id)

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


@router.get("/api/v1/stream/{camera_id}/tracked")
async def stream_camera_tracked(
    camera_id: str,
    res: str = Query("1080p"),
    det_fps: float = Query(0.5),
    token: str = Query(None),
    x_api_token: str = Header(None),
):
    """Live MJPEG stream with real-time person detection + tracking overlay.

    Each person is enclosed in a colored bounding box (distinct color per
    track) and a running count is drawn at the bottom of the frame.

    Detection runs on a background thread; the streaming loop consumes RTSP
    frames in order (fast-forwarding over the backlog accumulated during
    inference) and draws the latest tracking result onto them, so the video
    stays fluid instead of stalling on each slow inference.

    The `res` query param selects the output resolution: 1080p, 720p,
    540p, 360p or 720x540 (any WxH). Lower resolutions reduce decode/encode
    cost for a higher streaming frame rate.

    The `det_fps` query param caps the ONNX inference rate (default 0.5 =>
    one detection every 2s). Because inference is the heavy CPU consumer on
    edge, throttling it frees processor time for fluid streaming; tracking
    still interpolates between detections.
    """
    api_token = token or x_api_token
    if api_token != settings.local_api_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    import threading
    import time

    import cv2
    from fastapi.responses import StreamingResponse

    from src.vision.person_detector import PersonDetector
    from src.vision.person_tracker import CentroidTracker

    out_w, out_h = _parse_resolution(res)
    det_interval = 1.0 / max(det_fps, 0.05) if det_fps > 0 else float("inf")

    # The camera saturates when two RTSP connections (display + detection)
    # are open at once, so we use a SINGLE VideoCapture for the stream and
    # share the latest decoded frame with the detection thread. Because
    # cv2.VideoCapture (FFmpeg) is not thread-safe, only `generate()` touches
    # the cap; the detection thread only reads a protected snapshot.
    #
    # IMPORTANT: the Pi's OpenCV/FFmpeg build IGNORES CAP_PROP_FRAME_WIDTH/
    # HEIGHT and always returns the full native frame (1080p). We detect and
    # draw on that NATIVE frame (so small/distant people stay detectable) and
    # downscale only at the very end to the output resolution. Detection and
    # drawing share the native coordinate space, so boxes stay aligned.
    display_cap = _open_camera_stream(camera_id)

    detector = PersonDetector({"conf": 0.4})
    tracker = CentroidTracker(max_disappeared=12, max_distance=150.0, min_iou=0.1)

    # Latest tracking state (bboxes+colors per track) published by the
    # detection thread; consumed by the streaming loop to draw the overlay.
    # Bboxes are in NATIVE-frame coordinates.
    latest_tracked: dict = {}
    latest_lock = threading.Lock()

    # Snapshot of the most recent native frame published by `generate()` and
    # consumed by the detection thread.
    frame_lock = threading.Lock()
    latest_frame: object = None

    stop_event = threading.Event()

    def detection_loop():
        last = 0.0
        try:
            while not stop_event.is_set():
                # Throttle inference to det_interval to spare CPU for the
                # streaming loop on the resource-limited Orange Pi.
                now = time.monotonic()
                if now - last < det_interval:
                    time.sleep(0.05)
                    continue
                last = now

                with frame_lock:
                    snap = latest_frame
                    det_frame = None if snap is None else snap.copy()

                if det_frame is None:
                    logger.warning("DBG detect: latest_frame is None, skipping")
                    time.sleep(0.1)
                    continue

                logger.warning("DBG detect: frame shape=%s", det_frame.shape)

                detections = []
                try:
                    for result in detector.detect(det_frame):
                        bbox = result.result_data.get("bbox")
                        if bbox:
                            # Keep bbox in native-frame coordinates; the
                            # streaming loop scales it to the output size.
                            detections.append({
                                "bbox": list(bbox[:4]),
                                "confidence": result.confidence,
                            })
                except Exception as e:
                    logger.error("tracked detect error: %s", e)
                    time.sleep(0.2)
                    continue

                tracked = tracker.update(detections)
                logger.warning("DBG detect: ndet=%d ntracks=%d", len(detections), len(tracked))
                with latest_lock:
                    latest_tracked.clear()
                    latest_tracked.update(tracked)
        except Exception as e:
            logger.error("tracked detection thread ended: %s", e)

    thr = threading.Thread(target=detection_loop, daemon=True)
    thr.start()

    def generate():
        nonlocal latest_frame
        try:
            while True:
                # Fast-forward: drop the frames queued during the last
                # inference so playback stays current, then grab one frame.
                ok = display_cap.grab()
                if not ok:
                    break
                ret, frame = display_cap.retrieve()
                if not ret or frame is None:
                    break

                native_h, native_w = frame.shape[:2]
                # Publish the NATIVE frame for detection (full res keeps small
                # or distant people detectable regardless of display size).
                with frame_lock:
                    latest_frame = frame

                # Scale bboxes from native coords to display coords, then draw
                # on the display-size frame (cheap resize, done after overlay
                # position is computed).
                sx = out_w / native_w if native_w else 1.0
                sy = out_h / native_h if native_h else 1.0

                with latest_lock:
                    tracked = {
                        tid: dict(info)
                        for tid, info in latest_tracked.items()
                    }
                if tracked:
                    logger.warning("DBG draw: tracked nao vazio, tid=%s bbox=%s",
                                   list(tracked.keys()),
                                   [info.get("bbox") for info in tracked.values()])
                for info in tracked.values():
                    bbox = info.get("bbox")
                    if bbox and len(bbox) >= 4:
                        info["bbox"] = [bbox[0] * sx, bbox[1] * sy,
                                        bbox[2] * sx, bbox[3] * sy]

                if (out_w, out_h) != (frame.shape[1], frame.shape[0]):
                    frame = cv2.resize(
                        frame, (out_w, out_h), interpolation=cv2.INTER_AREA
                    )

                processed = tracker.draw(frame, tracked)

                _, jpeg = cv2.imencode(".jpg", processed, [cv2.IMWRITE_JPEG_QUALITY, 80])
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n")
                time.sleep(0.03)
        finally:
            stop_event.set()
            thr.join(timeout=2.0)
            display_cap.release()

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")


@router.get("/api/v1/processing/results")
async def list_processing_results(
    observation_id: str | None = Query(None),
    result_type: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(ProcessingResult)
    if observation_id:
        query = query.filter(ProcessingResult.observation_id == observation_id)
    if result_type:
        query = query.filter(ProcessingResult.result_type == result_type)
    results = query.order_by(ProcessingResult.created_at.desc()).limit(limit).all()
    return {
        "results": [
            {
                "id": r.id,
                "observation_id": r.observation_id,
                "device_id": r.device_id,
                "result_type": r.result_type,
                "model_name": r.model_name,
                "model_version": r.model_version,
                "confidence": r.confidence,
                "result_data": r.result_data,
                "inference_ms": r.inference_ms,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in results
        ]
    }


@router.get("/api/v1/processing/status")
async def processing_status(db: Session = Depends(get_db)):
    total = db.query(Observation).count()
    pending = db.query(Observation).filter(Observation.processing_status == "pending").count()
    processing = db.query(Observation).filter(Observation.processing_status == "processing").count()
    completed = db.query(Observation).filter(Observation.processing_status == "completed").count()
    failed = db.query(Observation).filter(Observation.processing_status == "failed").count()
    return {
        "total": total,
        "pending": pending,
        "processing": processing,
        "completed": completed,
        "failed": failed,
    }


@router.get("/api/v1/zones")
async def list_zones(
    device_id: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(ZoneConfig)
    if device_id:
        query = query.filter(ZoneConfig.device_id == device_id)
    zones = query.filter(ZoneConfig.is_active.is_(True)).order_by(ZoneConfig.zone_name).all()
    return {
        "zones": [
            {
                "id": z.id,
                "device_id": z.device_id,
                "zone_name": z.zone_name,
                "zone_type": z.zone_type,
                "polygon_vertices": z.polygon_vertices,
                "zone_config": z.zone_config,
                "is_active": z.is_active,
            }
            for z in zones
        ]
    }


@router.post("/api/v1/zones")
async def create_zone(
    device_id: str = Body(...),
    zone_name: str = Body(...),
    zone_type: str = Body(...),
    polygon_vertices: list = Body(...),
    zone_config: dict = Body(default={}),
    token: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    zone = ZoneConfig(
        device_id=device_id,
        zone_name=zone_name,
        zone_type=zone_type,
        polygon_vertices=polygon_vertices,
        zone_config=zone_config,
        is_active=True,
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return {"id": zone.id, "zone_name": zone.zone_name, "status": "created"}


@router.delete("/api/v1/zones/{zone_id}")
async def delete_zone(
    zone_id: int,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    zone = db.query(ZoneConfig).filter(ZoneConfig.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    db.delete(zone)
    db.commit()
    return {"status": "deleted"}
