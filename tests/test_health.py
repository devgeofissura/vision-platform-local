from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.storage.database import Base, get_db

TEST_DB_URL = "sqlite:///test_local.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=test_engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def patch_delivery_session():
    with patch("src.storage.delivery_queue.SessionLocal", TestSession), \
         patch("src.camera.capture_worker.SessionLocal", TestSession):
        yield


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "vision-platform-local"
    assert "camera" in data
    assert "storage" in data
    assert data["version"] == "0.1.0"


def test_status_endpoint():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["local_id"] == "LOCAL-001"


def test_cameras_endpoint():
    response = client.get("/api/v1/cameras")
    assert response.status_code == 200
    data = response.json()
    assert len(data["cameras"]) == 1
    assert data["cameras"][0]["camera_id"] == "CAM-001"


def test_list_observations_empty():
    response = client.get("/api/v1/observations")
    assert response.status_code == 200
    data = response.json()
    assert data["observations"] == []
    assert data["next_cursor"] is None


def test_ack_observation_not_found():
    response = client.post(
        "/api/v1/observations/obs_nonexistent/ack",
        headers={"X-Api-Token": "change-me"},
    )
    assert response.status_code == 404


def test_ack_observation_unauthorized():
    response = client.post("/api/v1/observations/obs_test/ack")
    assert response.status_code == 422


def test_flush_delivery():
    response = client.post(
        "/api/v1/delivery/flush",
        headers={"X-Api-Token": "change-me"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "empty"
