import logging
from datetime import UTC, datetime

import httpx
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.storage.database import SessionLocal
from src.storage.models import DeliveryLog, Observation

logger = logging.getLogger(__name__)

MAX_RETRIES = 5
RETRY_DELAYS_S = [5, 15, 60, 300, 900]


def deliver_observation(observation_id: str, central_url: str | None = None, db: Session | None = None) -> bool:
    own_session = db is None
    if own_session:
        db = SessionLocal()

    url = (central_url or settings.central_api_base_url).rstrip("/")
    token = settings.central_api_token

    try:
        obs = db.query(Observation).filter(Observation.observation_id == observation_id).first()
        if obs is None:
            logger.warning("Observation not found for delivery: %s", observation_id)
            return False

        if obs.delivery_status == "delivered":
            return True

        payload = {
            "observation_id": obs.observation_id,
            "camera_id": obs.camera_id,
            "local_id": obs.local_id,
            "captured_at": obs.captured_at.isoformat(),
            "sha256": obs.sha256,
            "width": obs.width,
            "height": obs.height,
            "quality_score": obs.quality_score,
            "algorithm_version": obs.algorithm_version,
        }

        attempt = obs.delivery_attempts + 1
        try:
            resp = httpx.post(
                f"{url}/api/v1/observations",
                json=payload,
                headers={"X-Api-Token": token},
                timeout=15,
            )
            resp.raise_for_status()

            obs.delivery_status = "delivered"
            obs.delivery_attempts = attempt
            obs.last_delivery_at = datetime.now(UTC)
            obs.delivered_at = datetime.now(UTC)
            obs.updated_at = datetime.now(UTC)

            db.add(DeliveryLog(
                observation_id=observation_id,
                attempt=attempt,
                status="delivered",
                status_code=resp.status_code,
            ))
            db.commit()
            logger.info("Delivered observation %s (attempt %d)", observation_id, attempt)
            return True

        except Exception as e:
            obs.delivery_status = "retry" if attempt < MAX_RETRIES else "failed"
            obs.delivery_attempts = attempt
            obs.last_delivery_at = datetime.now(UTC)
            obs.last_delivery_error = str(e)[:500]
            obs.updated_at = datetime.now(UTC)

            db.add(DeliveryLog(
                observation_id=observation_id,
                attempt=attempt,
                status="failed",
                error_message=str(e)[:500],
            ))
            db.commit()
            logger.warning("Delivery failed for %s (attempt %d): %s", observation_id, attempt, e)
            return False

    finally:
        if own_session:
            db.close()


def get_pending_observations(db: Session, limit: int = 10) -> list[Observation]:
    return (
        db.query(Observation)
        .filter(Observation.delivery_status.in_(["pending", "retry"]))
        .order_by(Observation.captured_at.asc())
        .limit(limit)
        .all()
    )


def process_delivery_queue(db: Session | None = None) -> dict:
    own_session = db is None
    if own_session:
        db = SessionLocal()

    try:
        pending = get_pending_observations(db)
        if not pending:
            return {"status": "empty", "delivered": 0, "failed": 0}

        delivered = 0
        failed = 0
        for obs in pending:
            success = deliver_observation(obs.observation_id, db=db)
            if success:
                delivered += 1
            else:
                failed += 1

        return {"status": "ok", "delivered": delivered, "failed": failed}
    finally:
        if own_session:
            db.close()
