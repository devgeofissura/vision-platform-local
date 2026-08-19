from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.storage.database import Base, get_db

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(bind=test_engine)


@pytest.fixture(autouse=True)
def _setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def _override_get_db():
    def _get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def _patch_sessions():
    with patch("src.storage.delivery_queue.SessionLocal", TestSession), \
         patch("src.camera.capture_worker.SessionLocal", TestSession), \
         patch("src.main.create_tables"), \
         patch("src.auth.router.SessionLocal", TestSession), \
         patch("src.auth.dependencies.SessionLocal", TestSession), \
         patch("src.auth.router.settings") as mock_auth_settings, \
         patch("src.auth.dependencies.settings") as mock_dep_settings, \
         patch("src.api.dashboard_routes.settings") as mock_dash_settings, \
         patch("src.camera.capture_worker.settings") as mock_settings:
        mock_settings.camera_auto_discover = False
        mock_settings.camera_rtsp_url = "rtsp://test"
        mock_settings.camera_rtsp_transport = "tcp"
        mock_settings.camera_connect_timeout_ms = 5000
        mock_settings.camera_reconnect_interval_ms = 3000
        mock_settings.local_id = "LOCAL-001"
        mock_settings.camera_id = "GeoFissura_CAM_000001"
        mock_settings.camera_name = "VIPC-1230-B-G2 geofissura"
        mock_settings.camera_username = "admin"
        mock_settings.camera_password = ""
        mock_settings.camera_hostname = "geofissuracam01"
        mock_settings.camera_stream_type = "main"
        mock_settings.camera_channel = 1
        mock_settings.camera_capture_interval_ms = 60000
        mock_settings.camera_capture_width = 1920
        mock_settings.camera_capture_height = 1080
        mock_settings.camera_capture_jpeg_quality = 90
        mock_settings.local_evidence_dir = "/tmp/test_evidence"
        mock_settings.local_data_dir = "/tmp/test_data"
        mock_settings.local_db_url = "sqlite:///test_local.db"
        mock_settings.local_api_host = "0.0.0.0"
        mock_settings.local_api_port = 8080
        mock_settings.local_api_token = "test-token"
        mock_settings.central_api_base_url = "http://localhost:8081"
        mock_settings.central_api_token = "test-token"
        mock_settings.central_delivery_interval_ms = 60000
        mock_settings.timezone = "America/Sao_Paulo"
        mock_settings.jwt_secret_key = "test-secret-key"
        mock_settings.jwt_expire_hours = 24
        mock_settings.admin_username = "admin"
        mock_settings.admin_password = "admin"
        mock_dash_settings.local_data_dir = "/tmp/test_data"
        mock_dash_settings.capture_interval_s = 60
        mock_dash_settings.local_id = "LOCAL-001"
        mock_dash_settings.local_name = "Test Local"
        mock_dash_settings.camera_capture_interval_ms = 60000
        mock_dash_settings.local_api_host = "0.0.0.0"
        mock_dash_settings.local_api_port = 8080
        mock_dash_settings.local_api_token = "test-token"
        mock_dash_settings.central_api_base_url = "http://localhost:8081"
        mock_dash_settings.central_api_token = "test-token"
        mock_dash_settings.central_delivery_interval_ms = 60000
        mock_dash_settings.camera_auto_discover = False
        mock_dash_settings.camera_rtsp_url = "rtsp://test"
        mock_dash_settings.camera_id = "GeoFissura_CAM_000001"
        mock_dash_settings.camera_name = "VIPC-1230-B-G2 geofissura"
        mock_dash_settings.camera_username = "admin"
        mock_dash_settings.camera_password = ""
        mock_dash_settings.camera_hostname = "geofissuracam01"
        mock_dash_settings.camera_stream_type = "main"
        mock_dash_settings.camera_channel = 1
        mock_dash_settings.camera_capture_width = 1920
        mock_dash_settings.camera_capture_height = 1080
        mock_dash_settings.camera_capture_jpeg_quality = 90
        mock_dash_settings.local_evidence_dir = "/tmp/test_evidence"
        mock_dash_settings.local_db_url = "sqlite:///test_local.db"
        mock_dash_settings.timezone = "America/Sao_Paulo"
        mock_dash_settings.jwt_secret_key = "test-secret-key"
        mock_dash_settings.jwt_expire_hours = 24
        mock_dash_settings.admin_username = "admin"
        mock_dash_settings.admin_password = "admin"
        for s in (mock_auth_settings, mock_dep_settings):
            s.jwt_secret_key = "test-secret-key"
            s.jwt_expire_hours = 24
            s.admin_username = "admin"
            s.admin_password = "admin"
        yield


@pytest.fixture
def client():
    return TestClient(app)
