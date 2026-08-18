from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

from src.storage.delivery_queue import (
    deliver_observation,
    get_pending_observations,
    process_delivery_queue,
)
from src.storage.models import Observation
from tests.conftest import TestSession


def _create_observation(db, obs_id, status="pending", attempts=0):
    obs = Observation(
        observation_id=obs_id,
        camera_id="CAM-001",
        local_id="LOCAL-001",
        captured_at=datetime.now(UTC),
        file_path=f"/tmp/{obs_id}.jpg",
        sha256="abc123",
        width=800,
        height=600,
        quality_score=0.95,
        algorithm_version="capture-0.1.0",
        delivery_status=status,
        delivery_attempts=attempts,
    )
    db.add(obs)
    db.commit()
    return obs


class TestGetPendingObservations:
    def test_empty(self):
        db = TestSession()
        result = get_pending_observations(db)
        assert result == []
        db.close()

    def test_pending(self):
        db = TestSession()
        _create_observation(db, "obs1", status="pending")
        _create_observation(db, "obs2", status="delivered")
        _create_observation(db, "obs3", status="retry")

        result = get_pending_observations(db)
        assert len(result) == 2
        assert {r.observation_id for r in result} == {"obs1", "obs3"}
        db.close()

    def test_limit(self):
        db = TestSession()
        for i in range(5):
            _create_observation(db, f"obs{i}", status="pending")

        result = get_pending_observations(db, limit=2)
        assert len(result) == 2
        db.close()


class TestDeliverObservation:
    @patch("src.storage.delivery_queue.httpx.post")
    def test_deliver_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        db = TestSession()
        _create_observation(db, "obs_ok", status="pending")
        result = deliver_observation("obs_ok", db=db)

        assert result is True
        obs = db.query(Observation).filter_by(observation_id="obs_ok").first()
        assert obs.delivery_status == "delivered"
        assert obs.delivered_at is not None
        db.close()

    @patch("src.storage.delivery_queue.httpx.post")
    def test_deliver_retry_on_failure(self, mock_post):
        mock_post.side_effect = Exception("connection refused")

        db = TestSession()
        _create_observation(db, "obs_fail", status="pending")
        result = deliver_observation("obs_fail", db=db)

        assert result is False
        obs = db.query(Observation).filter_by(observation_id="obs_fail").first()
        assert obs.delivery_status == "retry"
        assert obs.delivery_attempts == 1
        db.close()

    @patch("src.storage.delivery_queue.httpx.post")
    def test_deliver_failed_after_max_retries(self, mock_post):
        mock_post.side_effect = Exception("always fail")

        db = TestSession()
        _create_observation(db, "obs_max", status="retry", attempts=4)
        result = deliver_observation("obs_max", db=db)

        assert result is False
        obs = db.query(Observation).filter_by(observation_id="obs_max").first()
        assert obs.delivery_status == "failed"
        assert obs.delivery_attempts == 5
        db.close()

    def test_deliver_not_found(self):
        db = TestSession()
        result = deliver_observation("obs_nonexistent", db=db)
        assert result is False
        db.close()

    def test_deliver_already_delivered(self):
        db = TestSession()
        _create_observation(db, "obs_delivered", status="delivered")
        result = deliver_observation("obs_delivered", db=db)
        assert result is True
        db.close()

    @patch("src.storage.delivery_queue.httpx.post")
    def test_deliver_creates_delivery_log(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        db = TestSession()
        _create_observation(db, "obs_log", status="pending")
        deliver_observation("obs_log", db=db)

        from src.storage.models import DeliveryLog

        logs = db.query(DeliveryLog).filter_by(observation_id="obs_log").all()
        assert len(logs) == 1
        assert logs[0].status == "delivered"
        db.close()


class TestProcessDeliveryQueue:
    @patch("src.storage.delivery_queue.deliver_observation")
    def test_empty_queue(self, mock_deliver):
        db = TestSession()
        result = process_delivery_queue(db=db)
        assert result["status"] == "empty"
        assert result["delivered"] == 0
        mock_deliver.assert_not_called()
        db.close()

    @patch("src.storage.delivery_queue.deliver_observation")
    def test_process_delivers_all(self, mock_deliver):
        mock_deliver.return_value = True

        db = TestSession()
        for i in range(3):
            _create_observation(db, f"obs{i}")

        result = process_delivery_queue(db=db)
        assert result["status"] == "ok"
        assert result["delivered"] == 3
        assert result["failed"] == 0
        db.close()

    @patch("src.storage.delivery_queue.deliver_observation")
    def test_process_mix_success_and_failure(self, mock_deliver):
        def side_effect(obs_id, db=None):
            return obs_id != "obs1"

        mock_deliver.side_effect = side_effect

        db = TestSession()
        for i in range(3):
            _create_observation(db, f"obs{i}")

        result = process_delivery_queue(db=db)
        assert result["status"] == "ok"
        assert result["delivered"] == 2
        assert result["failed"] == 1
        db.close()
