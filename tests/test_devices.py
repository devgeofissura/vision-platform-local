import json

from src.auth.password import hash_password
from src.storage.models import Device, User
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
        "device_id": "test_dev_001",
        "name": "Test Device",
        "device_type": "camera",
        "task_type": "fissure",
        "connection_type": "rtsp",
        "connection_config": {"rtsp_url": "rtsp://test"},
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


# ── Page rendering ──

class TestDevicesPage:
    def test_devices_page_renders(self, client):
        _login(client)
        resp = client.get("/dashboard/devices")
        assert resp.status_code == 200
        assert "Devices" in resp.text

    def test_devices_page_shows_empty(self, client):
        _login(client)
        resp = client.get("/dashboard/devices")
        assert "Nenhum device configurado" in resp.text

    def test_devices_page_shows_device(self, client):
        _login(client)
        _create_device(device_id="cam_001", name="Camera 01")
        resp = client.get("/dashboard/devices")
        assert "cam_001" in resp.text
        assert "Camera 01" in resp.text

    def test_devices_page_requires_auth(self, client):
        resp = client.get("/dashboard/devices", follow_redirects=False)
        assert resp.status_code == 302
        assert resp.headers["location"] == "/login"


# ── Create ──

class TestDeviceCreate:
    def test_create_device(self, client):
        _login(client)
        resp = client.post("/dashboard/devices", data={
            "device_id": "sensor_001",
            "name": "Sensor de Fissura",
            "device_type": "sensor",
            "task_type": "fissure",
            "connection_type": "mqtt",
            "connection_config": json.dumps({"broker": "mqtt://localhost"}),
            "capture_interval_ms": "30000",
        }, follow_redirects=False)
        assert resp.status_code == 200

        db = TestSession()
        d = db.query(Device).filter(Device.device_id == "sensor_001").first()
        assert d is not None
        assert d.name == "Sensor de Fissura"
        assert d.device_type == "sensor"
        assert d.task_type == "fissure"
        assert d.connection_type == "mqtt"
        assert d.capture_interval_ms == 30000
        assert d.is_active is True
        db.close()

    def test_create_device_upserts_existing(self, client):
        _login(client)
        _create_device(device_id="cam_001", name="Old Name")
        resp = client.post("/dashboard/devices", data={
            "device_id": "cam_001",
            "name": "New Name",
            "device_type": "camera",
            "task_type": "ppe",
            "connection_type": "rtsp",
            "capture_interval_ms": "15000",
        })
        assert resp.status_code == 200

        db = TestSession()
        d = db.query(Device).filter(Device.device_id == "cam_001").first()
        assert d.name == "New Name"
        assert d.task_type == "ppe"
        db.close()

    def test_create_all_task_types(self, client):
        _login(client)
        for task in ["fissure", "ppe", "fabric_quality", "structural"]:
            resp = client.post("/dashboard/devices", data={
                "device_id": f"dev_{task}",
                "name": f"Device {task}",
                "device_type": "camera",
                "task_type": task,
                "connection_type": "rtsp",
                "capture_interval_ms": "60000",
            })
            assert resp.status_code == 200

        db = TestSession()
        assert db.query(Device).count() == 4
        db.close()


# ── Update ──

class TestDeviceUpdate:
    def test_update_device(self, client):
        _login(client)
        d = _create_device(device_id="cam_001", name="Old")
        resp = client.put(f"/dashboard/devices/{d.id}", data={
            "device_id": "cam_001",
            "name": "Updated",
            "device_type": "sensor",
            "task_type": "ppe",
            "connection_type": "mqtt",
            "capture_interval_ms": "5000",
        })
        assert resp.status_code == 200

        db = TestSession()
        updated = db.query(Device).filter(Device.id == d.id).first()
        assert updated.name == "Updated"
        assert updated.device_type == "sensor"
        assert updated.task_type == "ppe"
        assert updated.capture_interval_ms == 5000
        db.close()

    def test_update_nonexistent_returns_redirect(self, client):
        _login(client)
        resp = client.put("/dashboard/devices/9999", data={
            "device_id": "x",
            "name": "x",
            "device_type": "camera",
            "task_type": "fissure",
            "connection_type": "rtsp",
            "capture_interval_ms": "60000",
        }, follow_redirects=False)
        assert resp.status_code == 302


# ── Delete ──

class TestDeviceDelete:
    def test_delete_device(self, client):
        _login(client)
        d = _create_device(device_id="cam_del")
        resp = client.delete(f"/dashboard/devices/{d.id}")
        assert resp.status_code == 200

        db = TestSession()
        assert db.query(Device).filter(Device.id == d.id).first() is None
        db.close()

    def test_delete_nonexistent_returns_empty(self, client):
        _login(client)
        resp = client.delete("/dashboard/devices/9999")
        assert resp.status_code == 200


# ── Task types ──

class TestTaskTypes:
    def test_all_task_types_in_template(self, client):
        _login(client)
        _create_device(task_type="fissure")
        _create_device(device_id="dev2", task_type="ppe")
        _create_device(device_id="dev3", task_type="fabric_quality")
        _create_device(device_id="dev4", task_type="structural")
        resp = client.get("/dashboard/devices")
        assert "fissure" in resp.text
        assert "ppe" in resp.text
        assert "fabric_quality" in resp.text
        assert "structural" in resp.text
