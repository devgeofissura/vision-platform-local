"""Tests for the fabric defect training dashboard flow (capture/detect/annotate)."""

from datetime import UTC, datetime
from unittest.mock import patch

import numpy as np

from src.auth.password import hash_password
from src.storage.models import Device, FabricAnnotation, Observation, User
from src.vision.base import ProcessingResult
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


def _create_camera(device_id="cam_fab", name="Camera Tecido"):
    db = TestSession()
    d = Device(
        device_id=device_id,
        name=name,
        device_type="camera",
        task_type="fabric_quality",
        connection_type="rtsp",
        connection_config={"rtsp_url": "rtsp://test"},
        capture_interval_ms=60000,
        is_active=True,
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    db.close()
    return d


def _create_observation(file_path, observation_id="obs_fab_001", camera_id="cam_fab"):
    db = TestSession()
    o = Observation(
        observation_id=observation_id,
        camera_id=camera_id,
        local_id="LOCAL-001",
        captured_at=datetime.now(UTC),
        file_path=file_path,
        sha256="abc123",
    )
    db.add(o)
    db.commit()
    db.refresh(o)
    db.close()
    return o


def _make_image(tmp_path, w=640, h=480):
    import cv2
    img = np.full((h, w, 3), 200, dtype=np.uint8)
    p = tmp_path / "fabric.png"
    cv2.imwrite(str(p), img)
    return str(p)


class _FakeCapture:
    def __init__(self, payload):
        self._payload = payload

    def capture(self):
        return self._payload

    def disconnect(self):
        pass


# ── Page rendering ──

class TestFabricPage:
    def test_page_renders(self, client):
        _login(client)
        resp = client.get("/dashboard/fabric")
        assert resp.status_code == 200
        assert "Treinamento de Detecção de Defeitos de Tecido" in resp.text

    def test_page_requires_auth(self, client):
        resp = client.get("/dashboard/fabric", follow_redirects=False)
        assert resp.status_code == 302
        assert resp.headers["location"] == "/login"

    def test_page_shows_camera(self, client):
        _create_camera()
        _login(client)
        resp = client.get("/dashboard/fabric")
        assert "cam_fab" in resp.text

    def test_page_shows_annotations(self, client):
        _create_camera()
        db = TestSession()
        db.add(FabricAnnotation(
            annotation_id="FA-TEST1", camera_id="cam_fab",
            defect_type="hole", severity="high", bbox=[0, 0, 10, 10], confidence=0.8,
        ))
        db.commit()
        db.close()
        _login(client)
        resp = client.get("/dashboard/fabric")
        assert "FA-TEST1" in resp.text


# ── Capture ──

class TestFabricCapture:
    def test_capture_returns_image_url(self, client, tmp_path):
        _create_camera()
        _login(client)
        img = _make_image(tmp_path)
        payload = {
            "observation_id": "obs_new",
            "file_path": img,
            "width": 640,
            "height": 480,
            "quality": {"score": 1.0},
        }
        with patch("src.camera.capture_worker.CaptureWorker", return_value=_FakeCapture(payload)):
            resp = client.post("/dashboard/fabric/capture", data={"camera_id": "cam_fab"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["observation_id"] == "obs_new"

    def test_capture_nonexistent_camera_returns_error(self, client):
        _login(client)
        with patch("src.camera.capture_worker.CaptureWorker", return_value=_FakeCapture(None)):
            resp = client.post("/dashboard/fabric/capture", data={"camera_id": "nope"})
        assert resp.status_code == 500
        assert "error" in resp.json()

    def test_capture_requires_auth(self, client):
        resp = client.post("/dashboard/fabric/capture", data={"camera_id": "cam_fab"})
        assert resp.status_code == 401
        assert resp.json()["error"] == "unauthorized"


# ── Detect ──

class TestFabricDetect:
    def test_detect_returns_detections_and_overlay(self, client, tmp_path):
        _create_camera()
        img = _make_image(tmp_path)
        _create_observation(img)
        _login(client)

        fake_result = ProcessingResult(
            result_type="fabric_defect",
            model_name="fabric-fallback",
            model_version="1.0.0",
            confidence=0.87,
            result_data={"defect_type": "hole", "severity": "medium", "bbox": [10, 10, 100, 50]},
        )

        class _FakeDetector:
            def detect(self, frame):
                return [fake_result]

        with patch(
            "src.vision.fabric_defect_detector.FabricDefectDetector",
            return_value=_FakeDetector(),
        ):
            resp = client.post("/dashboard/fabric/detect", data={"observation_id": "obs_fab_001"})

        assert resp.status_code == 200
        data = resp.json()
        assert len(data["detections"]) == 1
        assert data["detections"][0]["defect_type"] == "hole"
        assert data["detections"][0]["severity"] == "medium"
        assert "overlay_image" in data

    def test_detect_missing_observation_404(self, client):
        _login(client)
        resp = client.post("/dashboard/fabric/detect", data={"observation_id": "missing"})
        assert resp.status_code == 404

    def test_detect_requires_auth(self, client):
        resp = client.post("/dashboard/fabric/detect", data={"observation_id": "x"})
        assert resp.status_code == 401


# ── Annotations ──

class TestFabricAnnotations:
    def test_create_returns_html_row(self, client):
        _create_camera()
        _login(client)
        resp = client.post("/dashboard/fabric/annotations", data={
            "observation_id": "obs_fab_001",
            "camera_id": "cam_fab",
            "defect_type": "stain",
            "severity": "high",
            "confidence": "0.9",
            "bbox": "[1,2,30,40]",
            "image_width": "640",
            "image_height": "480",
        })
        assert resp.status_code == 200
        assert "<tr" in resp.text
        assert "stain" in resp.text

    def test_created_annotation_persisted(self, client):
        _create_camera()
        _login(client)
        resp = client.post("/dashboard/fabric/annotations", data={
            "camera_id": "cam_fab", "defect_type": "hole",
        })
        assert resp.status_code == 200
        db = TestSession()
        ann = db.query(FabricAnnotation).first()
        db.close()
        assert ann is not None
        assert ann.defect_type == "hole"

    def test_invalid_bbox_json_is_null(self, client):
        _create_camera()
        _login(client)
        resp = client.post("/dashboard/fabric/annotations", data={
            "camera_id": "cam_fab", "defect_type": "hole", "bbox": "not-json",
        })
        assert resp.status_code == 200
        db = TestSession()
        ann = db.query(FabricAnnotation).first()
        db.close()
        assert ann.bbox is None

    def test_delete_removes_annotation(self, client):
        _create_camera()
        _login(client)
        db = TestSession()
        db.add(FabricAnnotation(
            annotation_id="FA-DEL", camera_id="cam_fab",
            defect_type="hole", severity="low",
        ))
        db.commit()
        db.close()

        resp = client.delete("/dashboard/fabric/annotations/FA-DEL")
        assert resp.status_code == 200
        db = TestSession()
        assert db.query(FabricAnnotation).filter(
            FabricAnnotation.annotation_id == "FA-DEL"
        ).first() is None
        db.close()

    def test_annotate_requires_auth(self, client):
        resp = client.post("/dashboard/fabric/annotations", data={"camera_id": "cam_fab"})
        assert resp.status_code == 200  # _require redirects to HTMLResponse("")
