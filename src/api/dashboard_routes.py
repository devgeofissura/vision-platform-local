import shutil
from pathlib import Path

import psutil
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user
from src.config.settings import settings
from src.storage.database import get_db
from src.storage.models import DeliveryLog, Observation

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

    latest = (
        db.query(Observation)
        .order_by(Observation.captured_at.desc())
        .first()
    )

    return _tmpl().TemplateResponse(request, "dashboard.html", {
        "user": user,
        "page": "home",
        "local_id": settings.local_id,
        "camera_id": settings.camera_id,
        "camera_name": settings.camera_name,
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


@router.get("/cameras", response_class=HTMLResponse)
async def cameras_page(request: Request):
    user, redirect = _require(request)
    if redirect:
        return redirect

    return _tmpl().TemplateResponse(request, "cameras.html", {
        "user": user,
        "page": "cameras",
        "camera_id": settings.camera_id,
        "camera_name": settings.camera_name,
        "camera_hostname": settings.camera_hostname,
        "camera_username": settings.camera_username,
        "camera_stream_type": settings.camera_stream_type,
        "camera_channel": settings.camera_channel,
        "camera_auto_discover": settings.camera_auto_discover,
        "camera_interval_s": settings.capture_interval_s,
    })


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
        "capture_interval_s": settings.capture_interval_s,
        "data_dir": settings.local_data_dir,
    })


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


@router.post("/queue/flush")
async def queue_flush(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect
    from src.storage.delivery_queue import process_delivery_queue
    result = process_delivery_queue(db=db)
    return RedirectResponse(url="/dashboard/queue", status_code=302)
