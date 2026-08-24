from datetime import UTC, datetime, timedelta

from src.auth.password import hash_password
from src.storage.models import SensorReading, User
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


def _add_reading(**overrides) -> SensorReading:
    defaults = {
        "device_id": "ESP-001",
        "topic": "geofissura/ESP-001/sensors",
        "reading_type": "temperature",
        "value_float": 25.5,
        "unit": "°C",
        "recorded_at": datetime.now(UTC).replace(tzinfo=None),
    }
    defaults.update(overrides)
    db = TestSession()
    row = SensorReading(**defaults)
    db.add(row)
    db.commit()
    db.refresh(row)
    db.close()
    return row


# ── API /api/v1/sensors/readings ──


class TestSensorsAPI:
    def test_empty_list(self, client):
        resp = client.get("/api/v1/sensors/readings")
        assert resp.status_code == 200
        data = resp.json()
        assert data["readings"] == []
        assert data["next_since_id"] is None
        assert data["count"] == 0

    def test_lists_readings_newest_first(self, client):
        now = datetime.now(UTC).replace(tzinfo=None)
        _add_reading(recorded_at=now - timedelta(minutes=10), value_float=20.0)
        _add_reading(recorded_at=now, value_float=22.0)

        data = client.get("/api/v1/sensors/readings").json()
        values = [r["value_float"] for r in data["readings"]]
        assert values == [22.0, 20.0]
        assert data["count"] == 2

    def test_filter_by_device(self, client):
        _add_reading(device_id="ESP-001")
        _add_reading(device_id="ESP-002")

        data = client.get("/api/v1/sensors/readings?device_id=ESP-002").json()
        assert len(data["readings"]) == 1
        assert data["readings"][0]["device_id"] == "ESP-002"

    def test_filter_by_type(self, client):
        _add_reading(reading_type="temperature")
        _add_reading(reading_type="humidity")

        data = client.get("/api/v1/sensors/readings?reading_type=humidity").json()
        assert len(data["readings"]) == 1
        assert data["readings"][0]["reading_type"] == "humidity"

    def test_pagination_with_since_id(self, client):
        r1 = _add_reading()
        r2 = _add_reading()

        data = client.get(f"/api/v1/sensors/readings?since_id={r1.id}&limit=1").json()
        assert data["count"] == 1
        assert data["readings"][0]["id"] == r2.id

    def test_limit_respected(self, client):
        for i in range(5):
            _add_reading(value_float=float(i))

        data = client.get("/api/v1/sensors/readings?limit=3").json()
        assert data["count"] == 3

    def test_serialization_fields(self, client):
        row = _add_reading(raw_payload='{"temperature": 25.5}')
        reading = client.get("/api/v1/sensors/readings").json()["readings"][0]
        assert reading["id"] == row.id
        assert reading["device_id"] == "ESP-001"
        assert reading["topic"].endswith("/sensors")
        assert isinstance(reading["recorded_at"], str)


# ── Dashboard page ──


class TestSensorsPage:
    def test_requires_auth(self, client):
        resp = client.get("/dashboard/sensors", follow_redirects=False)
        assert resp.status_code == 302
        assert "/login" in resp.headers["location"]

    def test_page_renders(self, client):
        _login(client)
        _add_reading()
        resp = client.get("/dashboard/sensors")
        assert resp.status_code == 200
        assert "Sensores" in resp.text
        assert "ESP-001" in resp.text
        assert "temperature" in resp.text

    def test_mqtt_status_card_disabled_by_default(self, client):
        _login(client)
        resp = client.get("/dashboard/sensors")
        assert "desabilitado" in resp.text

    def test_filter_links_present(self, client):
        _login(client)
        _add_reading(device_id="ESP-007")
        _add_reading(device_id="ESP-008", reading_type="pressure")

        resp = client.get("/dashboard/sensors")
        assert "ESP-007" in resp.text
        assert "ESP-008" in resp.text

    def test_device_filter_applied(self, client):
        _login(client)
        _add_reading(device_id="ESP-001")
        _add_reading(device_id="ESP-002", value_float=99.0)

        resp = client.get("/dashboard/sensors?device_id=ESP-002")
        assert "99" in resp.text
        assert "25.5" not in resp.text

    def test_refresh_partial_renders(self, client):
        _login(client)
        _add_reading()
        resp = client.get("/dashboard/sensors/refresh")
        assert resp.status_code == 200
        assert "ESP-001" in resp.text
        assert "<table" in resp.text

    def test_refresh_requires_auth(self, client):
        resp = client.get("/dashboard/sensors/refresh", follow_redirects=False)
        assert resp.status_code == 302

    def test_refresh_respects_filters(self, client):
        _login(client)
        _add_reading(device_id="ESP-001")
        _add_reading(device_id="ESP-002", topic="geofissura/ESP-002/sensors")

        resp = client.get("/dashboard/sensors/refresh?device_id=ESP-002")
        assert "ESP-002" in resp.text
        assert "ESP-001" not in resp.text

    def test_empty_state_message(self, client):
        _login(client)
        resp = client.get("/dashboard/sensors")
        assert "Nenhuma leitura encontrada" in resp.text
