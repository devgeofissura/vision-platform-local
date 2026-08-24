import json
from datetime import UTC, datetime

from src.mqtt.sensor_handler import SensorHandler, extract_device_id, parse_payload
from src.storage.models import SensorReading, SystemSettings
from tests.conftest import TestSession


class TestExtractDeviceId:
    def test_valid_topic(self):
        assert extract_device_id("geofissura/ESP-001/sensors") == "ESP-001"

    def test_custom_prefix_from_settings(self):
        db = TestSession()
        db.add(SystemSettings(key="mqtt_topic_prefix", value="gf/"))
        db.commit()
        db.close()
        assert extract_device_id("gf/SENSOR-X/sensors") == "SENSOR-X"

    def test_wrong_prefix_returns_none(self):
        assert extract_device_id("other/ESP-001/sensors") is None

    def test_empty_device_id_returns_none(self):
        assert extract_device_id("geofissura//sensors") is None

    def test_no_suffix_still_extracts_first_segment(self):
        assert extract_device_id("geofissura/ESP-9/other") == "ESP-9"


class TestParsePayload:
    def test_explicit_form_numeric(self):
        readings = parse_payload({"type": "temperature", "value": 25.5, "unit": "°C"})
        assert len(readings) == 1
        r = readings[0]
        assert r["reading_type"] == "temperature"
        assert r["value_float"] == 25.5
        assert r["value_text"] is None
        assert r["unit"] == "°C"

    def test_explicit_form_text_value(self):
        readings = parse_payload('{"type": "status", "value": "door_open"}')
        assert len(readings) == 1
        assert readings[0]["value_float"] is None
        assert readings[0]["value_text"] == "door_open"

    def test_multi_metric_numeric(self):
        payload = {"temperature": 25.5, "humidity": 61.2, "pressure": 1013.2}
        readings = parse_payload(json.dumps(payload))
        types = {r["reading_type"]: r for r in readings}
        assert set(types) == {"temperature", "humidity", "pressure"}
        assert types["temperature"]["unit"] == "°C"
        assert types["humidity"]["unit"] == "%"
        assert types["pressure"]["unit"] == "hPa"
        assert types["temperature"]["value_float"] == 25.5

    def test_string_values_become_text(self):
        readings = parse_payload('{"mode": "night"}')
        assert len(readings) == 1
        assert readings[0]["value_float"] is None
        assert readings[0]["value_text"] == "night"

    def test_bool_values_become_0_1(self):
        readings = parse_payload('{"door_open": true}')
        assert readings[0]["value_float"] == 1.0
        readings = parse_payload('{"door_open": false}')
        assert readings[0]["value_float"] == 0.0

    def test_ts_seconds(self):
        ts = 1756000000
        readings = parse_payload(f'{{"type": "temperature", "value": 1.0, "ts": {ts}}}')
        expected = datetime.fromtimestamp(ts, tz=UTC).replace(tzinfo=None)
        assert readings[0]["recorded_at"] == expected

    def test_ts_milliseconds_normalized(self):
        ts_ms = 1756000000000
        readings = parse_payload(f'{{"type": "temperature", "value": 1.0, "ts": {ts_ms}}}')
        expected = datetime.fromtimestamp(ts_ms / 1000, tz=UTC).replace(tzinfo=None)
        assert readings[0]["recorded_at"] == expected

    def test_invalid_json_returns_empty(self):
        assert parse_payload(b"not json at all") == []

    def test_non_object_json_returns_empty(self):
        assert parse_payload("[1, 2, 3]") == []

    def test_ts_and_device_id_not_treated_as_readings(self):
        readings = parse_payload('{"temperature": 20.0, "device_id": "X", "ts": 123}')
        assert len(readings) == 1
        assert readings[0]["reading_type"] == "temperature"


class TestSensorHandler:
    def test_handle_saves_readings(self):
        handler = SensorHandler(session_factory=TestSession)
        saved = handler.handle("geofissura/ESP-001/sensors", b'{"temperature": 25.5}')

        assert saved == 1
        db = TestSession()
        row = db.query(SensorReading).first()
        assert row.device_id == "ESP-001"
        assert row.topic == "geofissura/ESP-001/sensors"
        assert row.reading_type == "temperature"
        assert row.value_float == 25.5
        assert row.recorded_at is not None
        assert row.raw_payload == '{"temperature": 25.5}'

    def test_handle_multi_metrics_saves_all(self):
        handler = SensorHandler(session_factory=TestSession)
        saved = handler.handle(
            "geofissura/ESP-002/sensors",
            b'{"temperature": 21.0, "humidity": 55.0}',
        )
        assert saved == 2
        db = TestSession()
        rows = db.query(SensorReading).order_by(SensorReading.id).all()
        assert [r.reading_type for r in rows] == ["temperature", "humidity"]

    def test_handle_bad_topic_returns_zero(self):
        handler = SensorHandler(session_factory=TestSession)
        assert handler.handle("wrong/topic", b'{"temperature": 1.0}') == 0
        db = TestSession()
        assert db.query(SensorReading).count() == 0

    def test_handle_invalid_payload_returns_zero(self):
        handler = SensorHandler(session_factory=TestSession)
        assert handler.handle("geofissura/ESP-001/sensors", b"garbage") == 0

    def test_recorded_at_defaults_to_now_when_missing(self):
        before = datetime.now(UTC).replace(tzinfo=None)
        handler = SensorHandler(session_factory=TestSession)
        handler.handle("geofissura/ESP-001/sensors", '{"type": "t", "value": 2.0}')
        db = TestSession()
        row = db.query(SensorReading).first()
        assert row.recorded_at >= before

    def test_handler_error_does_not_raise(self):
        class ExplodingFactory:
            def __call__(self):
                raise RuntimeError("boom")

        handler = SensorHandler(session_factory=ExplodingFactory())
        assert handler.handle("geofissura/ESP-001/sensors", b'{"t": 1}') == 0
