from src.auth.password import hash_password
from src.config.settings import Settings
from src.storage.models import SystemSettings, User
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


def _form_headers():
    return {"Content-Type": "application/x-www-form-urlencoded"}


# ── Page rendering ──

class TestSettingsPage:
    def test_settings_page_renders(self, client):
        _login(client)
        resp = client.get("/dashboard/settings")
        assert resp.status_code == 200
        assert "Configurações" in resp.text

    def test_settings_page_requires_auth(self, client):
        resp = client.get("/dashboard/settings", follow_redirects=False)
        assert resp.status_code == 302
        assert resp.headers["location"] == "/login"

    def test_settings_page_shows_default_values(self, client):
        _login(client)
        resp = client.get("/dashboard/settings")
        assert "sl000001" in resp.text
        assert "Orange Pi 001" in resp.text

    def test_settings_page_shows_saved_message(self, client):
        _login(client)
        resp = client.get("/dashboard/settings?saved=1")
        assert resp.status_code == 200
        assert "sucesso" in resp.text.lower()

    def test_settings_page_has_all_sections(self, client):
        _login(client)
        resp = client.get("/dashboard/settings")
        for section in ("Geral", "Captura", "Câmera Padrão", "Entrega", "MQTT", "Processamento"):
            assert section in resp.text

    def test_settings_page_shows_descriptions(self, client):
        _login(client)
        resp = client.get("/dashboard/settings")
        assert "Fuso horário" in resp.text


# ── save_to_env unit tests ──

class TestSaveToEnv:
    def test_updates_existing_key(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("LOCAL_ID=OLD\nCAMERA_HOSTNAME=old-host\n")
        s = Settings()
        s.save_to_env({"LOCAL_ID": "NEW"}, env_path=env_file)
        content = env_file.read_text()
        assert "LOCAL_ID=NEW" in content
        assert "CAMERA_HOSTNAME=old-host" in content

    def test_preserves_unrelated_keys(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("LOCAL_ID=OLD\nOTHER_KEY=preserved\n")
        s = Settings()
        s.save_to_env({"LOCAL_ID": "NEW"}, env_path=env_file)
        content = env_file.read_text()
        assert "OTHER_KEY=preserved" in content
        assert "LOCAL_ID=NEW" in content

    def test_adds_new_key(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("LOCAL_ID=OLD\n")
        s = Settings()
        s.save_to_env({"CAMERA_PASSWORD": "secret123"}, env_path=env_file)
        content = env_file.read_text()
        assert "CAMERA_PASSWORD=secret123" in content

    def test_creates_file_if_missing(self, tmp_path):
        env_file = tmp_path / ".env"
        s = Settings()
        s.save_to_env({"LOCAL_ID": "NEW"}, env_path=env_file)
        assert env_file.read_text().strip() == "LOCAL_ID=NEW"

    def test_preserves_comments(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("# My config\nLOCAL_ID=OLD\n")
        s = Settings()
        s.save_to_env({"LOCAL_ID": "NEW"}, env_path=env_file)
        content = env_file.read_text()
        assert "# My config" in content
        assert "LOCAL_ID=NEW" in content

    def test_multiple_updates(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("")
        s = Settings()
        s.save_to_env({
            "LOCAL_ID": "LOC-01",
            "CAMERA_PASSWORD": "pass",
            "CENTRAL_DELIVERY_INTERVAL_MS": "30000",
            "CAMERA_CAPTURE_WIDTH": "1280",
        }, env_path=env_file)
        content = env_file.read_text()
        assert "LOCAL_ID=LOC-01" in content
        assert "CAMERA_PASSWORD=pass" in content
        assert "CENTRAL_DELIVERY_INTERVAL_MS=30000" in content
        assert "CAMERA_CAPTURE_WIDTH=1280" in content


# ── Route integration ──

class TestSettingsRoute:
    def test_save_redirects_with_saved_param(self, client):
        _login(client)
        resp = client.post("/dashboard/settings", data={
            "local_id": "sl000042",
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert "saved=1" in resp.headers["location"]

    def test_save_without_auth_redirects(self, client):
        resp = client.post("/dashboard/settings", data={"local_id": "X"}, follow_redirects=False)
        assert resp.status_code == 302
        assert resp.headers["location"] == "/login"

    def test_save_persists_to_db(self, client):
        _login(client)
        client.post("/dashboard/settings", data={"local_name": "Orange Pi Teste"})
        row = TestSession().query(SystemSettings).filter(SystemSettings.key == "local_name").first()
        assert row is not None and row.value == "Orange Pi Teste"

    def test_save_multiple_fields(self, client):
        _login(client)
        client.post("/dashboard/settings", data={
            "local_id": "sl000099",
            "capture_jpeg_quality": "75",
            "central_api_base_url": "http://10.0.0.5:8081",
        })
        db = TestSession()
        values = {r.key: r.value for r in db.query(SystemSettings).all()}
        db.close()
        assert values["local_id"] == "sl000099"
        assert values["capture_jpeg_quality"] == "75"
        assert values["central_api_base_url"] == "http://10.0.0.5:8081"

    def test_save_checkbox_checked(self, client):
        _login(client)
        client.post("/dashboard/settings", headers=_form_headers(),
                    content=b"mqtt_enabled=false&mqtt_enabled=true")
        assert TestSession().query(SystemSettings).filter(
            SystemSettings.key == "mqtt_enabled").first().value == "true"

    def test_save_checkbox_unchecked_saves_false(self, client):
        _login(client)
        client.post("/dashboard/settings", headers=_form_headers(),
                    content=b"mqtt_enabled=false")
        assert TestSession().query(SystemSettings).filter(
            SystemSettings.key == "mqtt_enabled").first().value == "false"

    def test_saved_value_shown_on_reload(self, client):
        _login(client)
        client.post("/dashboard/settings", data={"timezone": "UTC"})
        resp = client.get("/dashboard/settings")
        assert 'value="UTC"' in resp.text

    def test_form_has_all_sections_fields(self, client):
        _login(client)
        resp = client.get("/dashboard/settings")
        for field in (
            "local_id", "local_name", "timezone",
            "capture_interval_minutes", "capture_jpeg_quality",
            "camera_default_username", "camera_default_stream_type",
            "delivery_interval_seconds", "central_api_token",
            "mqtt_broker_host", "mqtt_topic_prefix",
            "processing_enabled", "processing_auto_on_capture",
        ):
            assert f'name="{field}"' in resp.text
