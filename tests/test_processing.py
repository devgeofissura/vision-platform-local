from datetime import UTC, datetime

from src.auth.password import hash_password
from src.storage.models import Device, Observation, ProcessingResult, User, ZoneConfig
from tests.conftest import TestSession


def _create_admin():
    db = TestSession()
    if not db.query(User).filter(User.username == "admin").first():
        db.add(User(username="admin", password_hash=hash_password("admin"), role="admin"))
        db.commit()
    db.close()


def _login(client):
    _create_admin()
    client.post("/login", data={"username": "admin", "password": "admin"})


def _create_device(**kwargs):
    db = TestSession()
    defaults = {
        "device_id": "cam_test_001",
        "name": "Test Camera",
        "device_type": "camera",
        "task_type": "fissure",
        "connection_type": "rtsp",
        "connection_config": {"ip": "192.168.0.1", "username": "admin", "password": ""},
        "capture_interval_ms": 60000,
        "is_active": True,
    }
    defaults.update(kwargs)
    d = Device(**defaults)
    db.add(d)
    db.commit()
    db.refresh(d)
    db.close()
    return d


def _create_observation(**kwargs):
    db = TestSession()
    defaults = {
        "observation_id": "obs_test_001",
        "camera_id": "cam_test_001",
        "local_id": "LOCAL-001",
        "captured_at": datetime.now(UTC),
        "file_path": "/tmp/test.jpg",
        "sha256": "abc123",
        "width": 1920,
        "height": 1080,
        "quality_score": 0.9,
        "delivery_status": "pending",
        "processing_status": "none",
    }
    defaults.update(kwargs)
    obs = Observation(**defaults)
    db.add(obs)
    db.commit()
    db.refresh(obs)
    db.close()
    return obs


def _create_processing_result(**kwargs):
    db = TestSession()
    defaults = {
        "observation_id": "obs_test_001",
        "device_id": "cam_test_001",
        "result_type": "fissure",
        "model_name": "yolo11n-seg",
        "model_version": "1.0.0",
        "confidence": 0.85,
        "result_data": {"bbox": [10, 20, 30, 40], "severity": "medium"},
        "inference_ms": 50,
        "image_width": 1920,
        "image_height": 1080,
    }
    defaults.update(kwargs)
    pr = ProcessingResult(**defaults)
    db.add(pr)
    db.commit()
    db.refresh(pr)
    db.close()
    return pr


def _create_zone(**kwargs):
    db = TestSession()
    defaults = {
        "device_id": "cam_test_001",
        "zone_name": "Test Zone",
        "zone_type": "ppe_enforcement",
        "polygon_vertices": [[0.1, 0.1], [0.9, 0.1], [0.9, 0.9], [0.1, 0.9]],
        "zone_config": {"required_ppe": ["helmet", "vest"]},
        "is_active": True,
    }
    defaults.update(kwargs)
    zone = ZoneConfig(**defaults)
    db.add(zone)
    db.commit()
    db.refresh(zone)
    db.close()
    return zone


class TestProcessingDashboard:
    def test_processing_page_renders(self, client):
        _login(client)
        resp = client.get("/dashboard/processing")
        assert resp.status_code == 200
        assert "Processamento" in resp.text

    def test_processing_page_shows_stats(self, client):
        _login(client)
        _create_observation(processing_status="completed")
        resp = client.get("/dashboard/processing")
        assert "Concluído" in resp.text

    def test_processing_page_filter_pending(self, client):
        _login(client)
        _create_observation(observation_id="obs_001", processing_status="pending")
        _create_observation(observation_id="obs_002", processing_status="completed")
        resp = client.get("/dashboard/processing?status=pending")
        assert resp.status_code == 200

    def test_processing_detail_renders(self, client):
        _login(client)
        _create_observation()
        resp = client.get("/dashboard/processing/obs_test_001")
        assert resp.status_code == 200
        assert "obs_test_001" in resp.text

    def test_processing_detail_with_results(self, client):
        _login(client)
        _create_observation()
        _create_processing_result()
        resp = client.get("/dashboard/processing/obs_test_001")
        assert resp.status_code == 200
        assert "fissure" in resp.text

    def test_processing_detail_redirect_on_missing(self, client):
        _login(client)
        resp = client.get("/dashboard/processing/nonexistent", follow_redirects=False)
        assert resp.status_code == 302


class TestZonesDashboard:
    def test_zones_page_renders(self, client):
        _login(client)
        resp = client.get("/dashboard/zones")
        assert resp.status_code == 200
        assert "Zonas" in resp.text

    def test_zones_page_shows_zones(self, client):
        _login(client)
        _create_zone()
        resp = client.get("/dashboard/zones")
        assert "Test Zone" in resp.text

    def test_zones_page_shows_empty(self, client):
        _login(client)
        resp = client.get("/dashboard/zones")
        assert "Nenhuma zona configurada" in resp.text

    def test_zone_create(self, client):
        _login(client)
        _create_device()
        resp = client.post("/dashboard/zones", data={
            "zone_name": "New Zone",
            "zone_type": "counting_line",
            "device_id": "cam_test_001",
            "polygon_vertices": "[[0,0],[1,0],[1,1],[0,1]]",
            "zone_config": "{}",
        }, follow_redirects=False)
        assert resp.status_code == 302

    def test_zone_delete(self, client):
        _login(client)
        zone = _create_zone()
        resp = client.delete(f"/dashboard/zones/{zone.id}")
        assert resp.status_code == 200


class TestProcessingAPI:
    def test_processing_status(self, client):
        _create_observation(processing_status="completed")
        resp = client.get("/api/v1/processing/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["completed"] == 1

    def test_list_processing_results_empty(self, client):
        resp = client.get("/api/v1/processing/results")
        assert resp.status_code == 200
        assert resp.json()["results"] == []

    def test_list_processing_results_with_data(self, client):
        _create_processing_result()
        resp = client.get("/api/v1/processing/results")
        assert resp.status_code == 200
        results = resp.json()["results"]
        assert len(results) == 1
        assert results[0]["result_type"] == "fissure"

    def test_list_processing_results_filter_type(self, client):
        _create_processing_result(result_type="fissure")
        _create_processing_result(observation_id="obs_002", result_type="plate")
        resp = client.get("/api/v1/processing/results?result_type=fissure")
        results = resp.json()["results"]
        assert len(results) == 1

    def test_list_processing_results_filter_obs(self, client):
        _create_processing_result(observation_id="obs_A")
        _create_processing_result(observation_id="obs_B")
        resp = client.get("/api/v1/processing/results?observation_id=obs_A")
        results = resp.json()["results"]
        assert len(results) == 1


class TestZonesAPI:
    def test_list_zones_empty(self, client):
        resp = client.get("/api/v1/zones")
        assert resp.status_code == 200
        assert resp.json()["zones"] == []

    def test_list_zones_with_data(self, client):
        _create_zone()
        resp = client.get("/api/v1/zones")
        zones = resp.json()["zones"]
        assert len(zones) == 1
        assert zones[0]["zone_name"] == "Test Zone"

    def test_create_zone_api(self, client):
        _create_device()
        resp = client.post(
            "/api/v1/zones",
            json={
                "device_id": "cam_test_001",
                "zone_name": "API Zone",
                "zone_type": "ppe_enforcement",
                "polygon_vertices": [[0, 0], [1, 0], [1, 1], [0, 1]],
                "zone_config": {"required_ppe": ["helmet"]},
            },
            headers={"X-Api-Token": "test-token"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "created"

    def test_create_zone_unauthorized(self, client):
        resp = client.post(
            "/api/v1/zones",
            json={
                "device_id": "cam_test_001",
                "zone_name": "API Zone",
                "zone_type": "ppe_enforcement",
                "polygon_vertices": [[0, 0], [1, 0], [1, 1], [0, 1]],
                "zone_config": {},
            },
            headers={"X-Api-Token": "wrong-token"},
        )
        assert resp.status_code == 401

    def test_delete_zone_api(self, client):
        zone = _create_zone()
        resp = client.delete(
            f"/api/v1/zones/{zone.id}",
            headers={"X-Api-Token": "test-token"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "deleted"

    def test_delete_zone_not_found(self, client):
        resp = client.delete(
            "/api/v1/zones/9999",
            headers={"X-Api-Token": "test-token"},
        )
        assert resp.status_code == 404

    def test_list_zones_filter_device(self, client):
        _create_zone(device_id="cam_A", zone_name="Zone A")
        _create_zone(device_id="cam_B", zone_name="Zone B")
        resp = client.get("/api/v1/zones?device_id=cam_A")
        zones = resp.json()["zones"]
        assert len(zones) == 1
        assert zones[0]["device_id"] == "cam_A"
