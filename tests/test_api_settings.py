from src.config.global_settings import clear_cache, get_setting
from src.storage.models import SystemSettings
from tests.conftest import TestSession


def _seed(**overrides):
    values = {"local_name": "Fissura A", "mqtt_enabled": "false"}
    values.update(overrides)
    db = TestSession()
    for key, value in values.items():
        db.add(SystemSettings(key=key, value=value))
    db.commit()
    db.close()


# ── GET /api/v1/settings ──


class TestGetSettingsAPI:
    def test_returns_all_defaults_when_db_empty(self, client):
        data = client.get("/api/v1/settings").json()
        assert data["count"] >= 20
        assert "local_id" in data["settings"]
        assert data["settings"]["local_id"]["value"] == "sl000001"

    def test_db_values_override_defaults(self, client):
        _seed(local_name="Obra Norte")
        data = client.get("/api/v1/settings").json()
        assert data["settings"]["local_name"]["value"] == "Obra Norte"

    def test_entries_have_description_field(self, client):
        data = client.get("/api/v1/settings").json()
        entry = data["settings"]["local_id"]
        assert "description" in entry
        assert isinstance(entry["description"], str)

    def test_mqtt_keys_present(self, client):
        data = client.get("/api/v1/settings").json()
        mqtt_keys = [k for k in data["settings"] if k.startswith("mqtt_")]
        assert len(mqtt_keys) >= 5


# ── POST /api/v1/settings ──


class TestPostSettingsAPI:
    def test_update_single_key(self, client):
        resp = client.post("/api/v1/settings", json={"local_name": "Nova Obra"})
        assert resp.status_code == 200
        assert resp.json() == {"updated": 1, "keys": ["local_name"]}
        assert get_setting("local_name") == "Nova Obra"

    def test_update_batch(self, client):
        resp = client.post(
            "/api/v1/settings",
            json={"local_name": "Obra B", "capture_interval_minutes": "7"},
        )
        assert resp.status_code == 200
        assert resp.json()["updated"] == 2
        assert get_setting("local_name") == "Obra B"
        assert get_setting("capture_interval_minutes") == "7"

    def test_empty_body_rejected(self, client):
        resp = client.post("/api/v1/settings", json={})
        assert resp.status_code == 400

    def test_unknown_key_rejected(self, client):
        resp = client.post("/api/v1/settings", json={"nao_existo": "1"})
        assert resp.status_code == 400
        assert "nao_existo" in resp.json()["detail"]

    def test_unknown_and_valid_mixed_rejects_all(self, client):
        _seed()
        resp = client.post("/api/v1/settings", json={"local_name": "X", "invalida": "y"})
        assert resp.status_code == 400
        assert get_setting("local_name") == "Fissura A"

    def test_non_object_body_rejected(self, client):
        resp = client.post("/api/v1/settings", content=b"[1,2]", headers={"Content-Type": "application/json"})
        assert resp.status_code in (400, 422)

    def test_coerces_non_string_values(self, client):
        resp = client.post("/api/v1/settings", json={"capture_interval_minutes": 12})
        assert resp.status_code == 200
        assert get_setting("capture_interval_minutes") == "12"

    def test_roundtrip_visible_in_get(self, client):
        client.post("/api/v1/settings", json={"local_id": "LOCAL-XYZ"})
        clear_cache()
        data = client.get("/api/v1/settings").json()
        assert data["settings"]["local_id"]["value"] == "LOCAL-XYZ"
