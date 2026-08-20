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


# ── Camera config per-device ──

class TestDeviceCameraConfig:
    def test_update_saves_camera_config(self, client):
        _login(client)
        d = _create_device(device_id="cam_cfg")
        resp = client.put(f"/dashboard/devices/{d.id}", data={
            "device_id": "cam_cfg",
            "name": "Camera Config",
            "device_type": "camera",
            "task_type": "fissure",
            "connection_type": "rtsp",
            "capture_interval_ms": "5000",
            "is_active": "on",
            "config_ip": "192.168.0.183",
            "config_hostname": "geofissuracam01",
            "config_username": "geofissura",
            "config_password": "secret123",
            "config_channel": "1",
            "config_stream_type": "main",
            "config_transport": "tcp",
            "config_manufacturer": "Intelbras",
            "config_model": "VIPC-1230",
            "config_jpeg_quality": "95",
            "config_capture_width": "1920",
            "config_capture_height": "1080",
        })
        assert resp.status_code == 200

        db = TestSession()
        updated = db.query(Device).filter(Device.id == d.id).first()
        cfg = updated.connection_config
        assert cfg["ip"] == "192.168.0.183"
        assert cfg["hostname"] == "geofissuracam01"
        assert cfg["username"] == "geofissura"
        assert cfg["password"] == "secret123"
        assert cfg["channel"] == 1
        assert cfg["stream_type"] == "main"
        assert cfg["transport"] == "tcp"
        assert cfg["manufacturer"] == "Intelbras"
        assert cfg["model"] == "VIPC-1230"
        assert cfg["jpeg_quality"] == 95
        assert cfg["capture_width"] == 1920
        assert cfg["capture_height"] == 1080
        assert updated.is_active is True
        db.close()

    def test_update_preserves_existing_config_keys(self, client):
        _login(client)
        d = _create_device(
            device_id="cam_keep",
            connection_config={"ip": "10.0.0.1", "extra_key": "keep_me"},
        )
        resp = client.put(f"/dashboard/devices/{d.id}", data={
            "device_id": "cam_keep",
            "name": "Keep Config",
            "device_type": "camera",
            "task_type": "fissure",
            "connection_type": "rtsp",
            "capture_interval_ms": "60000",
            "config_ip": "192.168.0.200",
        })
        assert resp.status_code == 200

        db = TestSession()
        updated = db.query(Device).filter(Device.id == d.id).first()
        assert updated.connection_config["ip"] == "192.168.0.200"
        assert updated.connection_config["extra_key"] == "keep_me"
        db.close()

    def test_update_is_active_checkbox_off(self, client):
        _login(client)
        d = _create_device(device_id="cam_active", is_active=True)
        resp = client.put(f"/dashboard/devices/{d.id}", data={
            "device_id": "cam_active",
            "name": "Deactivate",
            "device_type": "camera",
            "task_type": "fissure",
            "connection_type": "rtsp",
            "capture_interval_ms": "60000",
        })
        assert resp.status_code == 200

        db = TestSession()
        updated = db.query(Device).filter(Device.id == d.id).first()
        assert updated.is_active is False
        db.close()

    def test_to_dict_includes_all_fields(self, client):
        _login(client)
        d = _create_device(
            device_id="cam_dict",
            name="Dict Test",
            connection_config={"ip": "1.2.3.4"},
        )
        result = d.to_dict()
        assert result["device_id"] == "cam_dict"
        assert result["name"] == "Dict Test"
        assert result["connection_config"] == {"ip": "1.2.3.4"}
        assert result["is_active"] is True
        assert "id" in result

    def test_to_dict_returns_empty_config_when_none(self):
        d = Device(device_id="x", name="X", connection_config=None)
        assert d.to_dict()["connection_config"] == {}


# ── Auto-capture fields ──

class TestAutoCapture:
    def test_update_saves_auto_capture_enabled(self, client):
        _login(client)
        d = _create_device(device_id="cam_auto")
        resp = client.put(f"/dashboard/devices/{d.id}", data={
            "device_id": "cam_auto",
            "name": "Auto Capture",
            "device_type": "camera",
            "task_type": "fissure",
            "connection_type": "rtsp",
            "capture_interval_ms": "60000",
            "auto_capture_enabled": "on",
            "auto_capture_interval_minutes": "30",
        })
        assert resp.status_code == 200

        db = TestSession()
        updated = db.query(Device).filter(Device.id == d.id).first()
        assert updated.auto_capture_enabled is True
        assert updated.auto_capture_interval_minutes == 30
        db.close()

    def test_update_auto_capture_disabled_when_checkbox_off(self, client):
        _login(client)
        d = _create_device(device_id="cam_noauto", auto_capture_enabled=True)
        resp = client.put(f"/dashboard/devices/{d.id}", data={
            "device_id": "cam_noauto",
            "name": "Disable Auto",
            "device_type": "camera",
            "task_type": "fissure",
            "connection_type": "rtsp",
            "capture_interval_ms": "60000",
            "auto_capture_interval_minutes": "60",
        })
        assert resp.status_code == 200

        db = TestSession()
        updated = db.query(Device).filter(Device.id == d.id).first()
        assert updated.auto_capture_enabled is False
        db.close()

    def test_to_dict_includes_auto_capture_fields(self, client):
        _login(client)
        d = _create_device(
            device_id="cam_dict_auto",
            auto_capture_enabled=True,
            auto_capture_interval_minutes=15,
        )
        result = d.to_dict()
        assert result["auto_capture_enabled"] is True
        assert result["auto_capture_interval_minutes"] == 15
        assert "last_auto_capture_at" in result

    def test_default_auto_capture_values(self):
        d = Device(device_id="cam_defaults", name="Defaults")
        assert d.auto_capture_enabled is None or d.auto_capture_enabled is False
        assert d.auto_capture_interval_minutes is None or d.auto_capture_interval_minutes == 60
        assert d.last_auto_capture_at is None


# ── Monitoring capture endpoint ──

class TestMonitoringCapture:
    def test_monitoring_page_renders(self, client):
        _login(client)
        resp = client.get("/dashboard/monitoring")
        assert resp.status_code == 200
        assert "Monitoramento" in resp.text or "monitoring" in resp.text.lower()

    def test_monitoring_page_shows_cameras(self, client):
        _login(client)
        _create_device(device_id="cam_mon", name="Camera Mon")
        resp = client.get("/dashboard/monitoring")
        assert "cam_mon" in resp.text

    def test_monitoring_page_requires_auth(self, client):
        resp = client.get("/dashboard/monitoring", follow_redirects=False)
        assert resp.status_code == 302
        assert resp.headers["location"] == "/login"

    def test_monitoring_capture_requires_camera(self, client):
        _login(client)
        resp = client.post("/dashboard/monitoring/capture", data={
            "camera_id": "nonexistent_device",
        })
        assert resp.status_code == 200
        assert "Câmera não disponível" in resp.text or "não disponível" in resp.text


# ── Evidence dir default ──

class TestEvidenceDirDefault:
    def test_default_evidence_dir_is_relative(self):
        from src.config.settings import Settings
        s = Settings()
        assert s.local_evidence_dir == "./evidence"
        assert not s.local_evidence_dir.startswith("/")

    def test_default_data_dir_is_relative(self):
        from src.config.settings import Settings
        s = Settings()
        assert s.local_data_dir == "./data"
        assert not s.local_data_dir.startswith("/")
