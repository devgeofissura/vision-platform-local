import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.dashboard_routes import router as dashboard_router
from src.api.routes import router
from src.auth.password import hash_password
from src.auth.router import router as auth_router
from src.config.settings import settings
from src.storage.database import SessionLocal, create_tables
from src.storage.delivery_queue import process_delivery_queue
from src.storage.models import Device, User

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

_delivery_task: asyncio.Task | None = None
_auto_capture_task: asyncio.Task | None = None


async def _delivery_loop():
    interval_s = max(settings.central_delivery_interval_ms / 1000, 30)
    while True:
        try:
            result = process_delivery_queue()
            if result["delivered"] > 0:
                logger.info("Delivery flush: %s", result)
        except Exception as e:
            logger.error("Delivery loop error: %s", e)
        await asyncio.sleep(interval_s)


async def _auto_capture_loop():
    while True:
        try:
            db = SessionLocal()
            try:
                from datetime import UTC, datetime

                from src.camera.capture_worker import CaptureWorker

                now = datetime.now(UTC)
                devices = db.query(Device).filter(
                    Device.auto_capture_enabled.is_(True),
                    Device.is_active.is_(True),
                    Device.device_type == "camera",
                ).all()

                for device in devices:
                    last = device.last_auto_capture_at
                    interval_min = device.auto_capture_interval_minutes or 60
                    if last is None or (now - last.replace(tzinfo=UTC)).total_seconds() >= interval_min * 60:
                        try:
                            worker = CaptureWorker(device_id=device.device_id)
                            result = worker.capture()
                            worker.disconnect()
                            if result:
                                device.last_auto_capture_at = now
                                db.commit()
                                logger.info("Auto-capture %s: OK", device.device_id)
                            else:
                                logger.warning("Auto-capture %s: no frame", device.device_id)
                        except Exception as e:
                            logger.error("Auto-capture %s error: %s", device.device_id, e)
            finally:
                db.close()
        except Exception as e:
            logger.error("Auto-capture loop error: %s", e)
        await asyncio.sleep(60)


def _seed_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == settings.admin_username).first()
        if not existing:
            user = User(
                username=settings.admin_username,
                password_hash=hash_password(settings.admin_password),
                role="admin",
            )
            db.add(user)
            db.commit()
            logger.info("Default admin user created")
    finally:
        db.close()


def _seed_default_devices():
    db = SessionLocal()
    try:
        if settings.camera_id:
            existing = db.query(Device).filter(Device.device_id == settings.camera_id).first()
            if not existing:
                device = Device(
                    device_id=settings.camera_id,
                    name=settings.camera_name or settings.camera_id,
                    device_type="camera",
                    task_type="fissure",
                    connection_type="rtsp",
                    connection_config={
                        "ip": settings.camera_ip,
                        "hostname": settings.camera_hostname,
                        "username": settings.camera_username,
                        "channel": settings.camera_channel,
                        "stream_type": settings.camera_stream_type,
                        "transport": settings.camera_rtsp_transport,
                    },
                    capture_interval_ms=settings.camera_capture_interval_ms,
                    is_active=True,
                )
                db.add(device)
                db.commit()
                logger.info("Default camera device seeded: %s", settings.camera_id)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _delivery_task
    logger.info(
        "Vision Platform Local starting | local_id=%s camera=%s",
        settings.local_id,
        settings.camera_id,
    )
    create_tables()
    _seed_admin()
    _seed_default_devices()
    logger.info("Database tables verified")
    _delivery_task = asyncio.create_task(_delivery_loop())
    _auto_capture_task = asyncio.create_task(_auto_capture_loop())
    yield
    _delivery_task.cancel()
    _auto_capture_task.cancel()
    logger.info("Vision Platform Local shutting down")


app = FastAPI(
    title="Vision Platform Local",
    version="0.1.0",
    description="Local capture service for GeoFissura Vision Platform",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(router)

evidence_dir = Path(settings.local_evidence_dir)
evidence_dir.mkdir(parents=True, exist_ok=True)
app.mount("/evidence", StaticFiles(directory=str(evidence_dir)), name="evidence")
