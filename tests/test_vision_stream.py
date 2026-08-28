"""Tests for the live vision stream endpoint validation (/api/v1/stream/{id}/vision)."""

from src.api.routes import LIVE_TASK_TYPES


class TestLiveTaskTypes:
    def test_all_expected_types_present(self):
        expected = {"person_tracking", "fabric_quality", "fissure", "ppe", "plate"}
        assert set(LIVE_TASK_TYPES) == expected

    def test_person_tracking_first(self):
        assert LIVE_TASK_TYPES[0] == "person_tracking"


class TestVisionStreamAuth:
    def test_invalid_token_401(self, client):
        resp = client.get("/api/v1/stream/cam_x/vision?token=wrong")
        assert resp.status_code == 401

    def test_missing_token_401(self, client):
        resp = client.get("/api/v1/stream/cam_x/vision")
        assert resp.status_code == 401

    def test_invalid_x_api_token_header_401(self, client):
        resp = client.get(
            "/api/v1/stream/cam_x/vision", headers={"x-api-token": "wrong"}
        )
        assert resp.status_code == 401


class TestVisionStreamTaskType:
    def test_unknown_task_type_400(self, client):
        resp = client.get("/api/v1/stream/cam_x/vision?token=test-token&task_type=bogus")
        assert resp.status_code == 400
        assert "bogus" in resp.text

    def test_structural_not_allowed_400(self, client):
        resp = client.get("/api/v1/stream/cam_x/vision?token=test-token&task_type=structural")
        assert resp.status_code == 400
