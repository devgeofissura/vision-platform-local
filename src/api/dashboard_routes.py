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
async def settings_page(request: Request):
    user, redirect = _require(request)
    if redirect:
        return redirect

    return _tmpl().TemplateResponse(request, "settings.html", {
        "user": user,
        "page": "settings",
        "local_id": settings.local_id,
        "local_name": settings.local_name,
        "local_api_token": settings.local_api_token,
        "central_api_base_url": settings.central_api_base_url,
        "central_api_token": settings.central_api_token,
        "central_delivery_interval_ms": settings.central_delivery_interval_ms,
        "data_dir": settings.local_data_dir,
    })


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
