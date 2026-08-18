from datetime import UTC, datetime

from fastapi.testclient import TestClient

from src.storage.models import Observation
from tests.conftest import TestSession


def _seed_observation(obs_id="obs_test_001", status="pending"):
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
        delivery_status=status,
    )
    db.add(obs)
    db.commit()
    db.close()


class TestHealthEndpoint:
    def test_health_ok(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "vision-platform-local"
        assert "camera" in data
        assert "storage" in data
        assert data["version"] == "0.1.0"

    def test_health_has_storage_stats(self, client: TestClient):
        response = client.get("/health")
        storage = response.json()["storage"]
        assert "queue_pending" in storage
        assert "free_bytes" in storage


class TestStatusEndpoint:
    def test_status(self, client: TestClient):
        response = client.get("/api/v1/status")
        assert response.status_code == 200
        data = response.json()
        assert data["local_id"] == "LOCAL-001"


class TestCamerasEndpoint:
    def test_cameras(self, client: TestClient):
        response = client.get("/api/v1/cameras")
        assert response.status_code == 200
        data = response.json()
        assert len(data["cameras"]) == 1
        assert data["cameras"][0]["camera_id"] == "GeoFissura_CAM_000001"


class TestListObservations:
    def test_empty(self, client: TestClient):
        response = client.get("/api/v1/observations")
        assert response.status_code == 200
        data = response.json()
        assert data["observations"] == []
        assert data["next_cursor"] is None

    def test_with_observations(self, client: TestClient):
        _seed_observation("obs1", "pending")
        _seed_observation("obs2", "delivered")

        response = client.get("/api/v1/observations")
        assert response.status_code == 200
        data = response.json()
        assert len(data["observations"]) == 2

    def test_cursor_pagination(self, client: TestClient):
        for i in range(5):
            _seed_observation(f"obs{i}", "pending")

        resp1 = client.get("/api/v1/observations?limit=2")
        data1 = resp1.json()
        assert len(data1["observations"]) == 2
        assert data1["next_cursor"] is not None

        resp2 = client.get(f"/api/v1/observations?limit=2&cursor={data1['next_cursor']}")
        data2 = resp2.json()
        assert len(data2["observations"]) <= 3


class TestAckObservation:
    def test_ack_success(self, client: TestClient):
        _seed_observation("obs_ack", "pending")

        response = client.post(
            "/api/v1/observations/obs_ack/ack",
            headers={"X-Api-Token": "change-me"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "acknowledged"

        db = TestSession()
        obs = db.query(Observation).filter_by(observation_id="obs_ack").first()
        assert obs.delivery_status == "acknowledged"
        assert obs.delivered_at is not None
        db.close()

    def test_ack_not_found(self, client: TestClient):
        response = client.post(
            "/api/v1/observations/obs_nonexistent/ack",
            headers={"X-Api-Token": "change-me"},
        )
        assert response.status_code == 404

    def test_ack_unauthorized(self, client: TestClient):
        response = client.post("/api/v1/observations/obs_test/ack")
        assert response.status_code == 422


class TestFlushDelivery:
    def test_flush_empty(self, client: TestClient):
        response = client.post(
            "/api/v1/delivery/flush",
            headers={"X-Api-Token": "change-me"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "empty"

    def test_flush_delivers_pending(self, client: TestClient):
        from unittest.mock import patch as _patch

        _seed_observation("obs_flush", "pending")

        with _patch("src.storage.delivery_queue.deliver_observation", return_value=True):
            response = client.post(
                "/api/v1/delivery/flush",
                headers={"X-Api-Token": "change-me"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["delivered"] >= 1
