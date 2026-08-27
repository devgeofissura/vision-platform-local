import asyncio
import json
import logging
import shutil
from datetime import UTC, datetime
from pathlib import Path

import psutil
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user
from src.config.global_settings import DEFAULT_DESCRIPTIONS, get_all_settings, set_settings
from src.config.settings import settings
from src.storage.database import get_db
from src.storage.models import (
    CONNECTION_TYPES,
    DEVICE_TYPES,
    TASK_TYPES,
    CrackInstallation,
    CrackReference,
    DeliveryLog,
    Device,
    Observation,
    ProcessingResult,
    SensorReading,
    ZoneConfig,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
logger = logging.getLogger(__name__)


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
):
    form = await request.form()
    device = db.query(Device).filter(Device.id == device_db_id).first()
    if not device:
        return RedirectResponse(url="/dashboard/devices", status_code=302)

    device.device_id = str(form.get("device_id", device.device_id))
    device.name = str(form.get("name", device.name))
    device.device_type = str(form.get("device_type", device.device_type))
    device.task_type = str(form.get("task_type", device.task_type))
    device.connection_type = str(form.get("connection_type", device.connection_type))
    device.capture_interval_ms = int(form.get("capture_interval_ms", device.capture_interval_ms))
    device.auto_capture_enabled = form.get("auto_capture_enabled") == "on"
    device.auto_capture_interval_minutes = int(
        form.get("auto_capture_interval_minutes", device.auto_capture_interval_minutes or 60)
    )
    device.is_active = form.get("is_active") == "on"
    device.updated_at = datetime.now(UTC)

    existing_config = device.connection_config or {}
    device.connection_config = {
        **existing_config,
        "ip": str(form.get("config_ip", existing_config.get("ip", ""))),
        "hostname": str(form.get("config_hostname", existing_config.get("hostname", ""))),
        "username": str(form.get("config_username", existing_config.get("username", ""))),
        "password": str(form.get("config_password", existing_config.get("password", ""))),
        "channel": int(form.get("config_channel", existing_config.get("channel", 1))),
        "stream_type": str(form.get("config_stream_type", existing_config.get("stream_type", "main"))),
        "transport": str(form.get("config_transport", existing_config.get("transport", "tcp"))),
        "manufacturer": str(form.get("config_manufacturer", existing_config.get("manufacturer", ""))),
        "model": str(form.get("config_model", existing_config.get("model", ""))),
        "jpeg_quality": int(form.get("config_jpeg_quality", existing_config.get("jpeg_quality", 90))),
        "capture_width": int(form.get("config_capture_width", existing_config.get("capture_width", 1920))),
        "capture_height": int(form.get("config_capture_height", existing_config.get("capture_height", 1080))),
    }

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


# ── Sensores ─────────────────────────────────────────────────

@router.get("/sensors", response_class=HTMLResponse)
async def sensors_page(
    request: Request,
    device_id: str | None = None,
    reading_type: str | None = None,
    db: Session = Depends(get_db),
):
    user, redirect = _require(request)
    if redirect:
        return redirect

    query = db.query(SensorReading)
    if device_id:
        query = query.filter(SensorReading.device_id == device_id)
    if reading_type:
        query = query.filter(SensorReading.reading_type == reading_type)

    readings = (
        query.order_by(SensorReading.recorded_at.desc(), SensorReading.id.desc())
        .limit(100)
        .all()
    )

    sensor_devices = [
        row[0]
        for row in db.query(SensorReading.device_id).distinct().order_by(SensorReading.device_id)
    ]
    known_types = [
        row[0]
        for row in db.query(SensorReading.reading_type).distinct().order_by(SensorReading.reading_type)
    ]

    mqtt_status = {"enabled": False, "connected": False, "message_count": 0, "last_message_at": None}
    mqtt_client = getattr(request.app.state, "mqtt_client", None)
    if mqtt_client is not None:
        mqtt_status = mqtt_client.status_dict()

    return _tmpl().TemplateResponse(request, "sensors.html", {
        "user": user,
        "page": "sensors",
        "readings": readings,
        "sensor_devices": sensor_devices,
        "known_types": known_types,
        "current_device": device_id,
        "current_type": reading_type,
        "mqtt": mqtt_status,
    })


@router.get("/sensors/refresh", response_class=HTMLResponse)
async def sensors_refresh(
    request: Request,
    device_id: str | None = None,
    reading_type: str | None = None,
    db: Session = Depends(get_db),
):
    user, redirect = _require(request)
    if redirect:
        return redirect

    query = db.query(SensorReading)
    if device_id:
        query = query.filter(SensorReading.device_id == device_id)
    if reading_type:
        query = query.filter(SensorReading.reading_type == reading_type)

    readings = (
        query.order_by(SensorReading.recorded_at.desc(), SensorReading.id.desc())
        .limit(100)
        .all()
    )

    return _tmpl().TemplateResponse(request, "_sensor_rows.html", {
        "readings": readings,
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


SETTING_FORM_KEYS = [
    # Geral
    "local_id",
    "local_name",
    "timezone",
    # Captura
    "capture_interval_minutes",
    "capture_schedule",
    "capture_evidence_dir",
    "capture_jpeg_quality",
    "capture_width",
    "capture_height",
    # Câmera padrão
    "camera_default_username",
    "camera_default_password",
    "camera_default_stream_type",
    "camera_default_channel",
    "camera_default_transport",
    "camera_connect_timeout_ms",
    # Entrega
    "delivery_interval_seconds",
    "central_api_base_url",
    "central_api_token",
    # MQTT
    "mqtt_enabled",
    "mqtt_broker_host",
    "mqtt_broker_port",
    "mqtt_username",
    "mqtt_password",
    "mqtt_topic_prefix",
    # Processamento
    "processing_enabled",
    "processing_auto_on_capture",
]


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
        "s": get_all_settings(),
        "desc": DEFAULT_DESCRIPTIONS,
    })


@router.post("/settings", response_class=HTMLResponse)
async def settings_save(request: Request):
    user, redirect = _require(request)
    if redirect:
        return redirect

    form = await request.form()
    updates = {}
    for key in SETTING_FORM_KEYS:
        if key in form:
            updates[key] = str(form[key])

    set_settings(updates)

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

    return _tmpl().TemplateResponse(request, "monitoring.html", {
        "user": user,
        "page": "monitoring",
        "cameras": cameras,
        "selected_id": selected_id,
        "camera_token": settings.local_api_token,
        "latest": latest,
        "latest_image_url": latest_image_url,
    })


@router.post("/monitoring/capture", response_class=HTMLResponse)
async def monitoring_capture(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    form = await request.form()
    camera_id = form.get("camera_id")

    from src.camera.capture_worker import CaptureWorker

    error = None
    result = None

    def _do_capture():
        w = CaptureWorker(device_id=camera_id)
        try:
            r = w.capture()
            return r, None
        except Exception as e:
            return None, str(e)
        finally:
            w.disconnect()

    result, error = await asyncio.to_thread(_do_capture)
    if result is None and error is None:
        error = "Câmera não disponível ou falha na captura"

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

    return _tmpl().TemplateResponse(request, "monitoring.html", {
        "user": user,
        "page": "monitoring",
        "cameras": cameras,
        "selected_id": camera_id,
        "camera_token": settings.local_api_token,
        "latest": latest,
        "latest_image_url": latest_image_url,
        "capture_result": result,
        "capture_error": error,
    })


@router.get("/monitoring-multi", response_class=HTMLResponse)
async def monitoring_multi_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    cameras = db.query(Device).filter(
        Device.device_type == "camera", Device.is_active
    ).order_by(Device.created_at.desc()).all()

    return _tmpl().TemplateResponse(request, "monitoring_multi.html", {
        "user": user,
        "page": "monitoring-multi",
        "cameras": cameras,
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

    selected_id = request.query_params.get("camera", cameras[0].device_id if cameras else None)

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

    def _do_capture():
        w = CaptureWorker(device_id=camera_id)
        try:
            r = w.capture()
            return r, None
        except Exception as e:
            return None, str(e)
        finally:
            w.disconnect()

    result, error = await asyncio.to_thread(_do_capture)
    if result is None and error is None:
        error = "Câmera não disponível ou falha na captura"

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

def _next_device_id(db: Session, prefix: str = "GeoFissura_CAM_") -> str:
    """Gera device_id sequencial tipo GeoFissura_CAM_000001."""
    import re

    rows = db.query(Device.device_id).filter(
        Device.device_id.like(f"{prefix}%")
    ).all()
    max_num = 0
    for (did,) in rows:
        m = re.search(r"(\d+)$", did)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return f"{prefix}{max_num + 1:06d}"


# ── Discovery ────────────────────────────────────────────────

@router.get("/discovery", response_class=HTMLResponse)
async def discovery_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    return _tmpl().TemplateResponse(request, "discovery.html", {
        "user": user,
        "page": "discovery",
        "cameras": [],
        "scanning": False,
        "next_device_id": _next_device_id(db),
        "device_types": DEVICE_TYPES,
        "task_types": TASK_TYPES,
    })


@router.post("/discovery/scan", response_class=HTMLResponse)
async def discovery_scan(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    from src.camera.discovery import OnvifDiscovery

    discovery = OnvifDiscovery(timeout_seconds=8.0)
    cameras_found = discovery._send_probe()

    return _tmpl().TemplateResponse(request, "discovery_results.html", {
        "cameras": cameras_found,
        "scan_count": len(cameras_found),
        "next_device_id": _next_device_id(db),
        "device_types": DEVICE_TYPES,
        "task_types": TASK_TYPES,
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
    device_type = str(form.get("device_type", "camera"))
    task_type = str(form.get("task_type", "fissure"))
    camera_username = str(form.get("camera_username", settings.camera_username))
    camera_password = str(form.get("camera_password", settings.camera_password))

    if device_type not in DEVICE_TYPES:
        device_type = "camera"
    if task_type not in TASK_TYPES:
        task_type = "fissure"

    device_id = _next_device_id(db)
    device_name = camera_model or camera_hostname or device_id

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

    device = Device(
        device_id=device_id,
        name=device_name,
        device_type=device_type,
        task_type=task_type,
        connection_type="rtsp",
        connection_config=device_config,
        capture_interval_ms=settings.camera_capture_interval_ms,
        is_active=True,
    )
    db.add(device)
    db.commit()

    from fastapi.responses import JSONResponse

    is_htmx = request.headers.get("HX-Request") == "true"
    if is_htmx:
        return JSONResponse(
            content={"ok": True, "device_id": device_id, "device_name": device_name},
            headers={
                "HX-Trigger": (
                    '{"discoveryDeviceAdded": {"device_id": "'
                    + device_id
                    + '", "device_name": "'
                    + device_name
                    + '"}}'
                )
            },
        )

    return RedirectResponse(
        url="/dashboard/discovery?added=" + device_id, status_code=302
    )


# ── Processing Results ──────────────────────────────────────

@router.get("/processing", response_class=HTMLResponse)
async def processing_page(
    request: Request,
    status: str | None = None,
    result_type: str | None = None,
    db: Session = Depends(get_db),
):
    user, redirect = _require(request)
    if redirect:
        return redirect

    query = db.query(Observation)
    if status:
        query = query.filter(Observation.processing_status == status)
    observations = (
        query.order_by(Observation.captured_at.desc())
        .limit(100)
        .all()
    )

    total = db.query(Observation).count()
    pending = db.query(Observation).filter(Observation.processing_status == "pending").count()
    processing = db.query(Observation).filter(Observation.processing_status == "processing").count()
    completed = db.query(Observation).filter(Observation.processing_status == "completed").count()
    failed = db.query(Observation).filter(Observation.processing_status == "failed").count()

    return _tmpl().TemplateResponse(request, "processing.html", {
        "user": user,
        "page": "processing",
        "observations": observations,
        "current_status": status,
        "result_type_filter": result_type,
        "total": total,
        "pending": pending,
        "processing": processing,
        "completed": completed,
        "failed": failed,
    })


@router.get("/processing/{observation_id}", response_class=HTMLResponse)
async def processing_detail(
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
        return RedirectResponse(url="/dashboard/processing", status_code=302)

    results = (
        db.query(ProcessingResult)
        .filter(ProcessingResult.observation_id == observation_id)
        .order_by(ProcessingResult.created_at.desc())
        .all()
    )

    latest_image_url = None
    if obs and obs.file_path:
        p = Path(obs.file_path)
        evidence_root = Path(settings.local_evidence_dir)
        try:
            rel = p.relative_to(evidence_root)
            latest_image_url = f"/evidence/{rel.as_posix()}"
        except ValueError:
            pass

    return _tmpl().TemplateResponse(request, "processing_detail.html", {
        "user": user,
        "page": "processing",
        "obs": obs,
        "results": results,
        "latest_image_url": latest_image_url,
    })


# ── Zones ──────────────────────────────────────────────────

@router.get("/zones", response_class=HTMLResponse)
async def zones_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    zones = db.query(ZoneConfig).order_by(ZoneConfig.zone_name).all()
    devices = db.query(Device).filter(
        Device.device_type == "camera", Device.is_active
    ).order_by(Device.name).all()

    return _tmpl().TemplateResponse(request, "zones.html", {
        "user": user,
        "page": "zones",
        "zones": zones,
        "devices": devices,
    })


@router.post("/zones", response_class=HTMLResponse)
async def zone_create(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    form = await request.form()
    zone_name = str(form.get("zone_name", ""))
    zone_type = str(form.get("zone_type", "ppe_enforcement"))
    device_id = str(form.get("device_id", ""))

    vertices_str = str(form.get("polygon_vertices", "[]"))
    try:
        vertices = json.loads(vertices_str)
    except (json.JSONDecodeError, TypeError):
        vertices = []

    config_str = str(form.get("zone_config", "{}"))
    try:
        config = json.loads(config_str)
    except (json.JSONDecodeError, TypeError):
        config = {}

    zone = ZoneConfig(
        device_id=device_id,
        zone_name=zone_name,
        zone_type=zone_type,
        polygon_vertices=vertices,
        zone_config=config,
        is_active=True,
    )
    db.add(zone)
    db.commit()

    return RedirectResponse(url="/dashboard/zones", status_code=302)


@router.delete("/zones/{zone_id}")
async def zone_delete(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(ZoneConfig).filter(ZoneConfig.id == zone_id).first()
    if zone:
        db.delete(zone)
        db.commit()
    return HTMLResponse("")


# ── Crack Training ──────────────────────────────────────────

@router.get("/crack", response_class=HTMLResponse)
async def crack_training_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    cameras = db.query(Device).filter(
        Device.device_type == "camera", Device.is_active
    ).order_by(Device.created_at.desc()).all()

    selected_id = request.query_params.get("camera", cameras[0].device_id if cameras else None)

    installations = db.query(CrackInstallation).filter(
        CrackInstallation.status == "active"
    ).order_by(CrackInstallation.created_at.desc()).all()

    return _tmpl().TemplateResponse(request, "crack_training.html", {
        "user": user,
        "page": "crack",
        "cameras": cameras,
        "selected_id": selected_id,
        "camera_token": settings.local_api_token,
        "installations": installations,
    })


@router.post("/crack/capture")
async def crack_capture(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return {"error": "unauthorized"}, 401

    form = await request.form()
    camera_id = form.get("camera_id")

    from src.camera.capture_worker import CaptureWorker

    def _do_capture():
        w = CaptureWorker(device_id=camera_id)
        try:
            r = w.capture()
            return r, None
        except Exception as e:
            return None, str(e)
        finally:
            w.disconnect()

    result, error = await asyncio.to_thread(_do_capture)
    if result is None and error is None:
        return {"error": "Câmera não disponível ou falha na captura"}, 500
    if error:
        return {"error": error}, 500

    latest_image_url = None
    if result and result.get("file_path"):
        p = Path(result["file_path"])
        evidence_root = Path(settings.local_evidence_dir)
        try:
            rel = p.relative_to(evidence_root)
            latest_image_url = f"/evidence/{rel.as_posix()}"
        except ValueError:
            pass

    return {
        "observation_id": result.get("observation_id", ""),
        "image_url": latest_image_url or "",
        "width": result.get("width", 0),
        "height": result.get("height", 0),
        "quality": result.get("quality", {}),
    }


@router.post("/crack/process")
async def crack_process(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return {"error": "unauthorized"}, 401

    form = await request.form()
    observation_id = form.get("observation_id")

    obs = db.query(Observation).filter(Observation.observation_id == observation_id).first()
    if not obs or not obs.file_path:
        return {"error": "observation not found"}, 404

    import base64
    import traceback

    import cv2

    from src.vision.crack_label_processor import CrackLabelProcessor

    try:
        frame = cv2.imread(obs.file_path)
        if frame is None:
            return {"error": "cannot read image"}, 400

        processor = CrackLabelProcessor()
        analysis = processor.process(frame)
        overlay_frame = processor.draw_overlay(frame, analysis)

        _, jpeg = cv2.imencode(".jpg", overlay_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        overlay_b64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")

        return {
            "analysis": analysis.to_dict(),
            "overlay_image": overlay_b64,
            "summary": f"Marcadores: {len(analysis.markers)}/6, "
                       f"Interseção: {'sim' if analysis.intersection else 'não'}, "
                       f"Qualidade: {analysis.quality_score:.2f}",
        }
    except Exception as exc:
        logger.error("crack/process error: %s\n%s", exc, traceback.format_exc())
        return {"error": str(exc)}, 500


@router.post("/crack/reference")
async def crack_save_reference(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    form = await request.form()
    installation_id = str(form.get("installation_id", ""))
    installation_name = str(form.get("name", ""))
    installation_location = str(form.get("description", ""))
    camera_id = str(form.get("camera_id", ""))
    observation_id = str(form.get("observation_id", ""))
    analysis_json = str(form.get("analysis_json", "{}"))

    import uuid

    try:
        analysis_data = json.loads(analysis_json)
    except (json.JSONDecodeError, TypeError):
        analysis_data = {}

    if not installation_id:
        installation_id = f"CRK-{uuid.uuid4().hex[:8].upper()}"

    existing = db.query(CrackInstallation).filter(
        CrackInstallation.installation_id == installation_id
    ).first()

    if existing:
        inst = existing
    else:
        inst = CrackInstallation(
            installation_id=installation_id,
            name=installation_name or f"Instalação {installation_id}",
            location=installation_location,
            camera_id=camera_id,
            status="active",
        )
        db.add(inst)

    ref_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
    ref = CrackReference(
        reference_id=ref_id,
        installation_id=installation_id,
        image_observation_id=observation_id,
        label_corners=analysis_data.get("label_corners"),
        marker_points=analysis_data.get("markers"),
        line_AB=analysis_data.get("line_AB"),
        line_CD=analysis_data.get("line_CD"),
        intersection=analysis_data.get("intersection"),
        distances=analysis_data.get("distances"),
        angles=analysis_data.get("angles"),
        quality_score=analysis_data.get("quality_score", 0),
        processing_version="1.0.0",
        is_active=True,
    )
    db.add(ref)
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        return {"error": f"Erro ao salvar referência: {exc}"}, 500

    return {"ok": True, "reference_id": ref_id, "installation_id": installation_id}


@router.get("/crack/installations", response_class=HTMLResponse)
async def crack_installations_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return redirect

    installations = db.query(CrackInstallation).order_by(
        CrackInstallation.created_at.desc()
    ).all()

    return _tmpl().TemplateResponse(request, "crack_installations.html", {
        "user": user,
        "page": "crack",
        "installations": installations,
    })


@router.post("/crack/installations", response_class=HTMLResponse)
async def crack_installation_create(request: Request, db: Session = Depends(get_db)):
    user, redirect = _require(request)
    if redirect:
        return HTMLResponse("")

    form = await request.form()
    name = str(form.get("name", "")).strip()
    location = str(form.get("location", "")).strip()
    camera_id = str(form.get("camera_id", "")).strip()

    if not name or not camera_id:
        return HTMLResponse('<tr><td colspan="7" class="text-red-400 px-4 py-2">Nome e Câmera obrigatórios</td></tr>')

    import uuid
    inst_id = f"CRK-{uuid.uuid4().hex[:8].upper()}"
    inst = CrackInstallation(
        installation_id=inst_id,
        name=name,
        location=location,
        camera_id=camera_id,
        status="active",
    )
    db.add(inst)
    db.commit()

    return HTMLResponse(f"""
        <tr id="inst-{inst.installation_id}" class="border-t border-gray-700 hover:bg-gray-750">
            <td class="px-4 py-3 font-mono text-xs text-blue-400">{inst.installation_id[:12]}...</td>
            <td class="px-4 py-3">{inst.name}</td>
            <td class="px-4 py-3 text-gray-400">{inst.location}</td>
            <td class="px-4 py-3 font-mono text-xs text-gray-400">{inst.camera_id}</td>
            <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded text-xs bg-green-900 text-green-300">{inst.status}</span>
            </td>
            <td class="px-4 py-3 text-gray-400 text-xs">-</td>
            <td class="px-4 py-3">
                <button hx-delete="/dashboard/crack/installations/{inst.installation_id}"
                        hx-confirm="Excluir instalação {inst.name}?"
                        hx-target="#inst-{inst.installation_id}"
                        hx-swap="outerHTML"
                        class="text-red-400 hover:text-red-300 text-xs">Excluir</button>
            </td>
        </tr>
    """)


@router.delete("/crack/installations/{installation_id}")
async def crack_installation_delete(installation_id: str, db: Session = Depends(get_db)):
    inst = db.query(CrackInstallation).filter(
        CrackInstallation.installation_id == installation_id
    ).first()
    if inst:
        db.delete(inst)
        db.commit()
    return HTMLResponse("")
