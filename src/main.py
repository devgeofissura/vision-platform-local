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
from src.config.global_settings import seed_default_settings
from src.config.settings import settings
from src.storage.database import SessionLocal, create_tables
from src.storage.delivery_queue import process_delivery_queue
from src.storage.models import Device, Observation, User

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

_delivery_task: asyncio.Task | None = None
_auto_capture_task: asyncio.Task | None = None
_processing_task: asyncio.Task | None = None
_mqtt_task: asyncio.Task | None = None


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


async def _processing_loop():
    while True:
        try:
            db = SessionLocal()
            try:


                pending = (
                    db.query(Observation)
                    .filter(
                        Observation.processing_status == "pending",
                        Observation.file_path.isnot(None),
                    )
                    .order_by(Observation.captured_at.asc())
                    .limit(5)
                    .all()
                )

                for obs in pending:
                    _process_observation(db, obs)
            finally:
                db.close()
        except Exception as e:
            logger.error("Processing loop error: %s", e)
        await asyncio.sleep(10)


def _process_observation(db, obs: Observation):
    from datetime import UTC, datetime

    import cv2

    from src.storage.models import Device
    from src.storage.models import ProcessingResult as PRModel

    try:
        device = db.query(Device).filter(Device.device_id == obs.camera_id).first()
        task_type = device.task_type if device else "fissure"

        file_path = Path(obs.file_path)
        if not file_path.exists():
            logger.warning("Image file not found: %s", obs.file_path)
            obs.processing_status = "failed"
            db.commit()
            return

        obs.processing_status = "processing"
        obs.processing_started_at = datetime.now(UTC)
        db.commit()

        frame = cv2.imread(str(file_path))
        if frame is None:
            logger.warning("Cannot read image: %s", obs.file_path)
            obs.processing_status = "failed"
            db.commit()
            return

        from src.vision.pipeline import VisionPipeline

        pipeline = VisionPipeline(task_type)
        if not pipeline.enabled:
            obs.processing_status = "completed"
            obs.processing_completed_at = datetime.now(UTC)
            db.commit()
            return

        results, timings = pipeline.process_with_timings(frame)

        for r in results:
            pr = PRModel(
                observation_id=obs.observation_id,
                device_id=obs.camera_id,
                result_type=r.result_type,
                model_name=r.model_name,
                model_version=r.model_version,
                confidence=r.confidence,
                result_data=r.result_data,
                inference_ms=r.inference_ms,
                image_width=r.image_width,
                image_height=r.image_height,
            )
            db.add(pr)

        obs.processing_status = "completed"
        obs.processing_completed_at = datetime.now(UTC)
        db.commit()
        logger.info("Processed %s: %d results (%s)", obs.observation_id, len(results), timings)

    except Exception as e:
        logger.error("Processing failed for %s: %s", obs.observation_id, e)
        obs.processing_status = "failed"
        db.commit()


async def _auto_capture_loop():
    while True:
        try:
            from datetime import UTC, datetime

            from src.camera.schedule import parse_schedule, should_capture
            from src.config.global_settings import get_setting

            now = datetime.now(UTC)
            schedule_times = parse_schedule(get_setting("capture_schedule") or "")
            tz_name = get_setting("timezone") or "UTC"

            db = SessionLocal()
            try:
                devices = db.query(Device).filter(
                    Device.auto_capture_enabled.is_(True),
                    Device.is_active.is_(True),
                    Device.device_type == "camera",
                ).all()

                for device in devices:
                    if schedule_times:
                        if not should_capture(device.last_auto_capture_at, schedule_times, tz_name, now):
                            continue
                    else:
                        last = device.last_auto_capture_at
                        interval_min = device.auto_capture_interval_minutes or 60
                        if last is not None and (now - last.replace(tzinfo=UTC)).total_seconds() < interval_min * 60:
                            continue

                    device_id = device.device_id
                    try:
                        ok = await asyncio.to_thread(_capture_device_once, device_id)
                        if ok:
                            device.last_auto_capture_at = now
                            db.commit()
                            mode = "agenda" if schedule_times else "intervalo"
                            logger.info("Auto-capture %s (%s): OK", device_id, mode)
                        else:
                            logger.warning("Auto-capture %s: no frame", device_id)
                    except Exception as e:
                        logger.error("Auto-capture %s error: %s", device_id, e)
            finally:
                db.close()
        except Exception as e:
            logger.error("Auto-capture loop error: %s", e)
        await asyncio.sleep(30)


def _capture_device_once(device_id: str) -> bool:
    """Roda em thread própria (não tocar em sessions do event loop aqui)."""
    from src.camera.capture_worker import CaptureWorker

    worker = CaptureWorker(device_id=device_id)
    try:
        result = worker.capture()
    finally:
        worker.disconnect()
    return bool(result)


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
    global _delivery_task, _auto_capture_task, _processing_task, _mqtt_task
    logger.info(
        "Vision Platform Local starting | local_id=%s camera=%s",
        settings.local_id,
        settings.camera_id,
    )
    create_tables()
    _seed_admin()
    _seed_default_devices()
    seed_default_settings()
    logger.info("Database tables verified")
    _delivery_task = asyncio.create_task(_delivery_loop())
    _auto_capture_task = asyncio.create_task(_auto_capture_loop())
    _processing_task = asyncio.create_task(_processing_loop())
    _mqtt_task = asyncio.create_task(_mqtt_loop())
    yield
    for task in (_delivery_task, _auto_capture_task, _processing_task, _mqtt_task):
        task.cancel()
    logger.info("Vision Platform Local shutting down")


async def _mqtt_loop():
    """Mantém o cliente MQTT vivo; paho roda em thread própria com reconexão."""
    from src.config.global_settings import get_setting_bool
    from src.mqtt.client import MQTTClient

    client = MQTTClient()
    app.state.mqtt_client = client

    while True:
        if get_setting_bool("mqtt_enabled"):
            if not client.connected and client._client is None:
                client.start()
        else:
            if client._client is not None:
                logger.info("MQTT desabilitado nas settings; desconectando")
                client.stop()
        await asyncio.sleep(30)


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
