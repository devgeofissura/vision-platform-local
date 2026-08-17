from fastapi.testclient import TestClient

from src.main import app

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
