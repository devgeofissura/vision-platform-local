from datetime import UTC, datetime, timedelta

from sqlalchemy import desc, func

from src.storage.models import SensorReading
from tests.conftest import TestSession


def _reading(**overrides) -> SensorReading:
    defaults = {
        "device_id": "ESP-001",
        "topic": "geofissura/ESP-001/sensors",
        "reading_type": "temperature",
        "value_float": 25.5,
        "unit": "°C",
        "raw_payload": '{"temperature": 25.5}',
        "recorded_at": datetime.now(UTC).replace(tzinfo=None),
    }
    defaults.update(overrides)
    return SensorReading(**defaults)


class TestSensorReadingModel:
    def test_create_and_query(self):
        db = TestSession()
        db.add(_reading())
        db.commit()

        row = db.query(SensorReading).first()
        assert row.id == 1
        assert row.device_id == "ESP-001"
        assert row.reading_type == "temperature"
        assert row.value_float == 25.5
        assert row.unit == "°C"
        assert row.created_at is not None

    def test_value_text_for_non_numeric(self):
        db = TestSession()
        db.add(_reading(
            reading_type="status",
            value_float=None,
            value_text="door_open",
            unit=None,
        ))
        db.commit()

        row = db.query(SensorReading).first()
        assert row.value_float is None
        assert row.value_text == "door_open"

    def test_multiple_readings_ordering_by_recorded_at(self):
        db = TestSession()
        now = datetime.now(UTC).replace(tzinfo=None)
        db.add(_reading(recorded_at=now - timedelta(minutes=10), value_float=20.0))
        db.add(_reading(recorded_at=now, value_float=22.0))
        db.add(_reading(recorded_at=now - timedelta(minutes=5), value_float=21.0))
        db.commit()

        rows = db.query(SensorReading).order_by(desc(SensorReading.recorded_at)).all()
        assert [r.value_float for r in rows] == [22.0, 21.0, 20.0]

    def test_filter_by_device_and_type(self):
        db = TestSession()
        db.add(_reading(device_id="ESP-001", reading_type="humidity"))
        db.add(_reading(device_id="ESP-002", reading_type="humidity"))
        db.add(_reading(device_id="ESP-001", reading_type="pressure"))
        db.commit()

        count = db.query(func.count(SensorReading.id)).filter(
            SensorReading.device_id == "ESP-001",
            SensorReading.reading_type == "humidity",
        ).scalar()
        assert count == 1

    def test_to_dict_serialization(self):
        recorded = datetime.now(UTC).replace(tzinfo=None)
        db = TestSession()
        db.add(_reading(recorded_at=recorded))
        db.commit()
        db.close()

        db2 = TestSession()
        data = db2.query(SensorReading).first().to_dict()
        assert data["device_id"] == "ESP-001"
        assert data["value_float"] == 25.5
        assert isinstance(data["recorded_at"], str)
        assert "T" in data["recorded_at"]

    def test_raw_payload_preserved(self):
        payload = '{"t": 25.5, "h": 60, "ts": 1690000000}'
        db = TestSession()
        db.add(_reading(raw_payload=payload))
        db.commit()

        row = db.query(SensorReading).first()
        assert row.raw_payload == payload
