from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from src.storage.delivery_queue import process_delivery_queue
from src.storage.models import DeliveryLog, Observation
from tests.conftest import TestSession


def _create_pending_observation(obs_id="obs_e2e_001"):
    db = TestSession()
    obs = Observation(
        observation_id=obs_id,
        camera_id="CAM-001",
        local_id="LOCAL-001",
        captured_at=datetime.now(UTC),
        file_path=f"/tmp/{obs_id}.jpg",
        sha256="abc123def456",
        width=800,
        height=600,
        quality_score=0.95,
        algorithm_version="capture-0.1.0",
        delivery_status="pending",
    )
    db.add(obs)
    db.commit()
    db.close()


class TestE2EDeliveryFlow:
    @patch("src.storage.delivery_queue.httpx.post")
    def test_full_delivery_success(self, mock_post, client: TestClient):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        _create_pending_observation("obs_e2e_full")

        db = TestSession()
        result = process_delivery_queue(db=db)
        assert result["status"] == "ok"
        assert result["delivered"] == 1
        assert result["failed"] == 0
        db.close()

        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id="obs_e2e_full").first()
        assert obs.delivery_status == "delivered"
        assert obs.delivered_at is not None
        assert obs.delivery_attempts == 1
        db.close()

        db = TestSession()
        logs = db.query(DeliveryLog).filter_by(observation_id="obs_e2e_full").all()
        assert len(logs) == 1
        assert logs[0].status == "delivered"
        assert logs[0].status_code == 201
        db.close()

        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        assert payload["observation_id"] == "obs_e2e_full"
        assert payload["camera_id"] == "CAM-001"
        assert payload["local_id"] == "LOCAL-001"
        assert payload["sha256"] == "abc123def456"

    @patch("src.storage.delivery_queue.httpx.post")
    def test_delivery_retry_then_succeed(self, mock_post):
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ConnectionError("timeout")
            resp = MagicMock()
            resp.status_code = 201
            resp.raise_for_status = MagicMock()
            return resp

        mock_post.side_effect = side_effect

        _create_pending_observation("obs_retry")

        db = TestSession()
        result1 = process_delivery_queue(db=db)
        assert result1["failed"] == 1
        db.close()

        db = TestSession()
        result2 = process_delivery_queue(db=db)
        assert result2["delivered"] == 1
        db.close()

        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id="obs_retry").first()
        assert obs.delivery_status == "delivered"
        assert obs.delivery_attempts == 2
        db.close()

    @patch("src.storage.delivery_queue.httpx.post")
    def test_delivery_permanent_failure(self, mock_post):
        mock_post.side_effect = ConnectionError("always fail")

        _create_pending_observation("obs_fail")

        for _ in range(5):
            db = TestSession()
            process_delivery_queue(db=db)
            db.close()

        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id="obs_fail").first()
        assert obs.delivery_status == "failed"
        assert obs.delivery_attempts == 5
        assert obs.last_delivery_error is not None
        db.close()

    def test_delivery_idempotent_already_delivered(self):
        _create_pending_observation("obs_idem")
        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id="obs_idem").first()
        obs.delivery_status = "delivered"
        obs.delivered_at = datetime.now(UTC)
        db.commit()
        db.close()

        db = TestSession()
        result = process_delivery_queue(db=db)
        assert result["status"] == "empty"
        db.close()

    @patch("src.storage.delivery_queue.httpx.post")
    def test_multiple_observations_batch(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        for i in range(3):
            _create_pending_observation(f"obs_batch_{i}")

        db = TestSession()
        result = process_delivery_queue(db=db)
        assert result["delivered"] == 3
        assert result["failed"] == 0
        db.close()

        assert mock_post.call_count == 3

    def test_api_ack_triggers_delivered(self, client: TestClient):
        _create_pending_observation("obs_ack_flow")

        response = client.post(
            "/api/v1/observations/obs_ack_flow/ack",
            headers={"X-Api-Token": "test-token"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "acknowledged"

        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id="obs_ack_flow").first()
        assert obs.delivery_status == "acknowledged"
        assert obs.delivered_at is not None
        db.close()

    def test_health_reflects_pending_queue(self, client: TestClient):
        _create_pending_observation("obs_health_1")
        _create_pending_observation("obs_health_2")

        response = client.get("/health")
        data = response.json()
        assert data["storage"]["queue_pending"] == 2

    @patch("src.storage.delivery_queue.httpx.post")
    def test_flush_endpoint_delivers(self, mock_post, client: TestClient):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        _create_pending_observation("obs_flush_e2e")

        response = client.post(
            "/api/v1/delivery/flush",
            headers={"X-Api-Token": "test-token"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["delivered"] == 1
