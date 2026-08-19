import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

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
                        "rtsp_url": settings.camera_rtsp_url,
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
    yield
    _delivery_task.cancel()
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
