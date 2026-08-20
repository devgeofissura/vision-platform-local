import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

import psutil
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user
from src.config.settings import settings
from src.storage.database import get_db
from src.storage.models import CONNECTION_TYPES, DEVICE_TYPES, TASK_TYPES, DeliveryLog, Device, Observation

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _tmpl():
    from fastapi.templating import Jinja2Templates
    return Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


def _require(request: Request):
    user = get_current_user(request)
    if user is None:
        return None, RedirectResponse(url="/login", status_code=302)
    return user, None


@router.get("", response_class=HTMLResponse)
async def dashboard_home(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    try:
        disk = shutil.disk_usage(settings.local_data_dir)
        free_gb = round(disk.free / (1024**3), 1)
        total_gb = round(disk.total / (1024**3), 1)
    except (FileNotFoundError, OSError):
        free_gb, total_gb = 0.0, 0.0

    queue_pending = db.query(Observation).filter(
        Observation.delivery_status.in_(["pending", "retry"])
    ).count()
    total_obs = db.query(Observation).count()
    delivered = db.query(Observation).filter(
        Observation.delivery_status == "acknowledged"
    ).count()
    failed = db.query(Observation).filter(
        Observation.delivery_status == "failed"
    ).count()

    device_count = db.query(Device).filter(Device.is_active).count()
    latest = (
        db.query(Observation)
        .order_by(Observation.captured_at.desc())
        .first()
    )

    return _tmpl().TemplateResponse(request, "dashboard.html", {
        "user": user,
        "page": "home",
        "local_id": settings.local_id,
        "device_count": device_count,
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_free": free_gb,
        "disk_total": total_gb,
        "queue_pending": queue_pending,
        "total_obs": total_obs,
        "delivered": delivered,
        "failed": failed,
        "latest": latest,
    })


# ── Device CRUD ──────────────────────────────────────────────

@router.get("/devices", response_class=HTMLResponse)
async def devices_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    devices = db.query(Device).order_by(Device.created_at.desc()).all()
    return _tmpl().TemplateResponse(request, "devices.html", {
        "user": user,
        "page": "devices",
        "devices": devices,
        "device_types": DEVICE_TYPES,
        "task_types": TASK_TYPES,
        "connection_types": CONNECTION_TYPES,
    })


@router.post("/devices", response_class=HTMLResponse)
async def device_create(
    request: Request,
    db: Session = Depends(get_db),
    device_id: str = Form(...),
    name: str = Form(...),
    device_type: str = Form("camera"),
    task_type: str = Form("fissure"),
    connection_type: str = Form("rtsp"),
    connection_config: str = Form("{}"),
    capture_interval_ms: int = Form(60000),
):
    existing = db.query(Device).filter(Device.device_id == device_id).first()
    if existing:
        existing.name = name
        existing.device_type = device_type
        existing.task_type = task_type
        existing.connection_type = connection_type
        existing.connection_config = json.loads(connection_config) if connection_config else {}
        existing.capture_interval_ms = capture_interval_ms
        existing.updated_at = datetime.now(UTC)
        db.commit()
        db.refresh(existing)
        devices = db.query(Device).order_by(Device.created_at.desc()).all()
        return _tmpl().TemplateResponse(request, "devices.html", {
            "user": None,
            "page": "devices",
            "devices": devices,
            "device_types": DEVICE_TYPES,
            "task_types": TASK_TYPES,
            "connection_types": CONNECTION_TYPES,
        })

    device = Device(
        device_id=device_id,
        name=name,
        device_type=device_type,
        task_type=task_type,
        connection_type=connection_type,
        connection_config=json.loads(connection_config) if connection_config else {},
        capture_interval_ms=capture_interval_ms,
        is_active=True,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    devices = db.query(Device).order_by(Device.created_at.desc()).all()
    return _tmpl().TemplateResponse(request, "devices.html", {
        "user": None,
        "page": "devices",
        "devices": devices,
        "device_types": DEVICE_TYPES,
        "task_types": TASK_TYPES,
        "connection_types": CONNECTION_TYPES,
    })


@router.put("/devices/{device_db_id}", response_class=HTMLResponse)
async def device_update(
    request: Request,
    device_db_id: int,
    db: Session = Depends(get_db),
    device_id: str = Form(...),
    name: str = Form(...),
    device_type: str = Form("camera"),
    task_type: str = Form("fissure"),
    connection_type: str = Form("rtsp"),
    capture_interval_ms: int = Form(60000),
):
    device = db.query(Device).filter(Device.id == device_db_id).first()
    if not device:
        return RedirectResponse(url="/dashboard/devices", status_code=302)

    device.device_id = device_id
    device.name = name
    device.device_type = device_type
    device.task_type = task_type
    device.connection_type = connection_type
    device.capture_interval_ms = capture_interval_ms
    device.updated_at = datetime.now(UTC)
    db.commit()

    devices = db.query(Device).order_by(Device.created_at.desc()).all()
    return _tmpl().TemplateResponse(request, "devices.html", {
        "user": None,
        "page": "devices",
        "devices": devices,
        "device_types": DEVICE_TYPES,
        "task_types": TASK_TYPES,
        "connection_types": CONNECTION_TYPES,
    })


@router.delete("/devices/{device_db_id}")
async def device_delete(device_db_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_db_id).first()
    if device:
        db.delete(device)
        db.commit()
    return HTMLResponse("")


# ── Observations ─────────────────────────────────────────────

@router.get("/observations", response_class=HTMLResponse)
async def observations_page(
    request: Request,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    user, redirect = _require(request)
    if redirect:
        return redirect

    query = db.query(Observation)
    if status:
        query = query.filter(Observation.delivery_status == status)

    observations = (
        query.order_by(Observation.captured_at.desc())
        .limit(100)
        .all()
    )

    return _tmpl().TemplateResponse(request, "observations.html", {
        "user": user,
        "page": "observations",
        "observations": observations,
        "current_status": status,
    })


@router.get("/observations/{observation_id}", response_class=HTMLResponse)
async def observation_detail(
    request: Request,
    observation_id: str,
    db: Session = Depends(get_db),
):
    user, redirect = _require(request)
    if redirect:
        return redirect

    obs = db.query(Observation).filter(
        Observation.observation_id == observation_id
    ).first()
    if obs is None:
        return RedirectResponse(url="/dashboard/observations", status_code=302)

    logs = (
        db.query(DeliveryLog)
        .filter(DeliveryLog.observation_id == observation_id)
        .order_by(DeliveryLog.created_at.desc())
        .all()
    )

    return _tmpl().TemplateResponse(request, "observation_detail.html", {
        "user": user,
        "page": "observations",
        "obs": obs,
        "logs": logs,
    })


# ── Queue ────────────────────────────────────────────────────

@router.get("/queue", response_class=HTMLResponse)
async def queue_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    pending = db.query(Observation).filter(
        Observation.delivery_status == "pending"
    ).count()
    retry = db.query(Observation).filter(
        Observation.delivery_status == "retry"
    ).count()
    delivered_count = db.query(Observation).filter(
        Observation.delivery_status == "acknowledged"
    ).count()
    failed = db.query(Observation).filter(
        Observation.delivery_status == "failed"
    ).count()

    recent_logs = (
        db.query(DeliveryLog)
        .order_by(DeliveryLog.created_at.desc())
        .limit(20)
        .all()
    )

    return _tmpl().TemplateResponse(request, "queue.html", {
        "user": user,
        "page": "queue",
        "pending": pending,
        "retry": retry,
        "delivered_count": delivered_count,
        "failed": failed,
        "recent_logs": recent_logs,
    })


@router.post("/queue/flush")
async def queue_flush(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect
    from src.storage.delivery_queue import process_delivery_queue
    process_delivery_queue(db=db)
    return RedirectResponse(url="/dashboard/queue", status_code=302)


# ── Settings ─────────────────────────────────────────────────

@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, saved: bool = False):
    user, redirect = _require(request)
    if redirect:
        return redirect

    return _tmpl().TemplateResponse(request, "settings.html", {
        "user": user,
        "page": "settings",
        "saved": saved,
        "local_id": settings.local_id,
        "local_name": settings.local_name,
        "timezone": settings.timezone,
        "local_api_token": settings.local_api_token,
        "data_dir": settings.local_data_dir,
        "central_api_base_url": settings.central_api_base_url,
        "central_api_token": settings.central_api_token,
        "central_delivery_interval_ms": settings.central_delivery_interval_ms,
        "camera_id": settings.camera_id,
        "camera_name": settings.camera_name,
        "camera_hostname": settings.camera_hostname,
        "camera_username": settings.camera_username,
        "camera_password": settings.camera_password,
        "camera_ip": settings.camera_ip,
        "camera_stream_type": settings.camera_stream_type,
        "camera_channel": settings.camera_channel,
        "camera_rtsp_url": settings.camera_rtsp_url,
        "camera_capture_interval_ms": settings.camera_capture_interval_ms,
        "camera_capture_width": settings.camera_capture_width,
        "camera_capture_height": settings.camera_capture_height,
        "camera_capture_jpeg_quality": settings.camera_capture_jpeg_quality,
        "camera_rtsp_transport": settings.camera_rtsp_transport,
    })


@router.post("/settings", response_class=HTMLResponse)
async def settings_save(request: Request):
    user, redirect = _require(request)
    if redirect:
        return redirect

    form = await request.form()
    updates = {}
    env_map = {
        "local_id": "LOCAL_ID",
        "local_name": "LOCAL_NAME",
        "timezone": "TIMEZONE",
        "local_data_dir": "LOCAL_DATA_DIR",
        "local_api_token": "LOCAL_API_TOKEN",
        "central_api_base_url": "CENTRAL_API_BASE_URL",
        "central_api_token": "CENTRAL_API_TOKEN",
        "central_delivery_interval_ms": "CENTRAL_DELIVERY_INTERVAL_MS",
        "camera_id": "CAMERA_ID",
        "camera_name": "CAMERA_NAME",
        "camera_hostname": "CAMERA_HOSTNAME",
        "camera_username": "CAMERA_USERNAME",
        "camera_password": "CAMERA_PASSWORD",
        "camera_ip": "CAMERA_IP",
        "camera_stream_type": "CAMERA_STREAM_TYPE",
        "camera_channel": "CAMERA_CHANNEL",
        "camera_rtsp_url": "CAMERA_RTSP_URL",
        "camera_capture_interval_ms": "CAMERA_CAPTURE_INTERVAL_MS",
        "camera_capture_width": "CAMERA_CAPTURE_WIDTH",
        "camera_capture_height": "CAMERA_CAPTURE_HEIGHT",
        "camera_capture_jpeg_quality": "CAMERA_CAPTURE_JPEG_QUALITY",
        "camera_rtsp_transport": "CAMERA_RTSP_TRANSPORT",
    }

    for form_key, env_key in env_map.items():
        if form_key in form:
            updates[env_key] = str(form[form_key])

    settings.save_to_env(updates)

    return RedirectResponse(url="/dashboard/settings?saved=1", status_code=302)


# ── API (HTMX) ──────────────────────────────────────────────

@router.get("/api/stats")
async def api_stats(db: Session = Depends(get_db)):
    queue_pending = db.query(Observation).filter(
        Observation.delivery_status.in_(["pending", "retry"])
    ).count()
    total_obs = db.query(Observation).count()
    delivered = db.query(Observation).filter(
        Observation.delivery_status == "acknowledged"
    ).count()
    failed = db.query(Observation).filter(
        Observation.delivery_status == "failed"
    ).count()
    return {
        "queue_pending": queue_pending,
        "total_obs": total_obs,
        "delivered": delivered,
        "failed": failed,
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
    }


# ── Camera ───────────────────────────────────────────────────

@router.get("/monitoring", response_class=HTMLResponse)
async def monitoring_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    cameras = db.query(Device).filter(
        Device.device_type == "camera", Device.is_active
    ).order_by(Device.created_at.desc()).all()

    selected_id = request.query_params.get("camera", cameras[0].device_id if cameras else None)

    return _tmpl().TemplateResponse(request, "monitoring.html", {
        "user": user,
        "page": "monitoring",
        "cameras": cameras,
        "selected_id": selected_id,
        "camera_token": settings.local_api_token,
    })


@router.get("/camera", response_class=HTMLResponse)
async def camera_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    cameras = db.query(Device).filter(
        Device.device_type == "camera", Device.is_active
    ).order_by(Device.created_at.desc()).all()

    selected_id = request.query_params.get("camera", settings.camera_id)

    latest = (
        db.query(Observation)
        .order_by(Observation.captured_at.desc())
        .first()
    )

    latest_image_url = None
    if latest and latest.file_path:
        p = Path(latest.file_path)
        evidence_root = Path(settings.local_evidence_dir)
        try:
            rel = p.relative_to(evidence_root)
            latest_image_url = f"/evidence/{rel.as_posix()}"
        except ValueError:
            pass

    return _tmpl().TemplateResponse(request, "camera.html", {
        "user": user,
        "page": "camera",
        "cameras": cameras,
        "selected_id": selected_id,
        "latest": latest,
        "latest_image_url": latest_image_url,
        "camera_token": settings.local_api_token,
    })


@router.post("/camera/capture", response_class=HTMLResponse)
async def camera_capture(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    form = await request.form()
    camera_id = form.get("camera_id", settings.camera_id)

    from src.camera.capture_worker import CaptureWorker

    error = None
    result = None
    worker = CaptureWorker(device_id=camera_id)
    try:
        result = worker.capture()
        if result is None:
            error = "Câmera não disponível ou falha na captura"
    except Exception as e:
        error = str(e)
    finally:
        worker.disconnect()

    cameras = db.query(Device).filter(
        Device.device_type == "camera", Device.is_active
    ).order_by(Device.created_at.desc()).all()

    latest = (
        db.query(Observation)
        .order_by(Observation.captured_at.desc())
        .first()
    )

    latest_image_url = None
    if latest and latest.file_path:
        p = Path(latest.file_path)
        evidence_root = Path(settings.local_evidence_dir)
        try:
            rel = p.relative_to(evidence_root)
            latest_image_url = f"/evidence/{rel.as_posix()}"
        except ValueError:
            pass

    return _tmpl().TemplateResponse(request, "camera.html", {
        "user": user,
        "page": "camera",
        "cameras": cameras,
        "selected_id": camera_id,
        "latest": latest,
        "latest_image_url": latest_image_url,
        "camera_token": settings.local_api_token,
        "capture_result": result,
        "capture_error": error,
    })


# ── Discovery ────────────────────────────────────────────────

@router.get("/discovery", response_class=HTMLResponse)
async def discovery_page(request: Request):
    user, redirect = _require(request)
    if redirect:
        return redirect

    return _tmpl().TemplateResponse(request, "discovery.html", {
        "user": user,
        "page": "discovery",
        "cameras": [],
        "scanning": False,
    })


@router.post("/discovery/scan", response_class=HTMLResponse)
async def discovery_scan(request: Request):
    user, redirect = _require(request)
    if redirect:
        return redirect

    from src.camera.discovery import OnvifDiscovery

    discovery = OnvifDiscovery(timeout_seconds=8.0)
    cameras_found = discovery._send_probe()

    return _tmpl().TemplateResponse(request, "discovery_results.html", {
        "cameras": cameras_found,
        "scan_count": len(cameras_found),
        "default_device_id": settings.camera_id,
        "default_username": settings.camera_username,
        "default_password": settings.camera_password,
    })


@router.post("/discovery/select", response_class=HTMLResponse)
async def discovery_select(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    form = await request.form()
    camera_ip = str(form.get("camera_ip", ""))
    camera_hostname = str(form.get("camera_hostname", ""))
    camera_manufacturer = str(form.get("camera_manufacturer", ""))
    camera_model = str(form.get("camera_model", ""))
    device_id = str(form.get("device_id", settings.camera_id))
    device_name = str(form.get("device_name", camera_model or camera_hostname or device_id))
    camera_username = str(form.get("camera_username", settings.camera_username))
    camera_password = str(form.get("camera_password", settings.camera_password))

    updates = {
        "CAMERA_IP": camera_ip,
        "CAMERA_USERNAME": camera_username,
        "CAMERA_PASSWORD": camera_password,
    }
    settings.save_to_env(updates)

    existing = db.query(Device).filter(Device.device_id == device_id).first()
    device_config = {
        "ip": camera_ip,
        "hostname": camera_hostname,
        "manufacturer": camera_manufacturer,
        "model": camera_model,
        "username": camera_username,
        "password": camera_password,
        "channel": settings.camera_channel,
        "stream_type": settings.camera_stream_type,
        "transport": settings.camera_rtsp_transport,
    }
    if existing:
        existing.name = device_name
        existing.connection_config = device_config
        existing.updated_at = datetime.now(UTC)
        db.commit()
    else:
        device = Device(
            device_id=device_id,
            name=device_name,
            device_type="camera",
            task_type="fissure",
            connection_type="rtsp",
            connection_config=device_config,
            capture_interval_ms=settings.camera_capture_interval_ms,
            is_active=True,
        )
        db.add(device)
        db.commit()

    return RedirectResponse(url="/dashboard/discovery?selected=1", status_code=302)
