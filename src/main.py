import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes import router
from src.config.settings import settings
from src.storage.database import create_tables
from src.storage.delivery_queue import process_delivery_queue

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _delivery_task
    logger.info(
        "Vision Platform Local starting | local_id=%s camera=%s",
        settings.local_id,
        settings.camera_id,
    )
    create_tables()
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

app.include_router(router)
