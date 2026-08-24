from unittest.mock import MagicMock, patch

import pytest

from src.mqtt.client import MQTTClient
from src.storage.models import SystemSettings
from tests.conftest import TestSession


@pytest.fixture
def mock_paho():
    with patch("src.mqtt.client.paho_mqtt") as m:
        m.MQTT_ERR_SUCCESS = 0
        client_instance = MagicMock()
        client_instance.subscribe.return_value = (0, 1)
        m.Client.return_value = client_instance
        yield m, client_instance


def _seed_settings(**overrides):
    defaults = {
        "mqtt_enabled": "true",
        "mqtt_broker_host": "broker.local",
        "mqtt_broker_port": "1884",
        "mqtt_username": "sensor-user",
        "mqtt_password": "sensor-pass",
        "mqtt_topic_prefix": "gf/",
    }
    defaults.update(overrides)
    db = TestSession()
    for key, value in defaults.items():
        db.add(SystemSettings(key=key, value=value))
    db.commit()
    db.close()


def _started_client(mock_paho):
    _, instance = mock_paho
    _seed_settings()
    client = MQTTClient()
    client.start()
    return client, instance


class TestMQTTClientStartStop:
    def test_start_connects_with_settings(self, mock_paho):
        _, instance = mock_paho
        _seed_settings()
        client = MQTTClient()

        assert client.start() is True
        instance.connect.assert_called_once_with("broker.local", 1884, keepalive=30)
        instance.loop_start.assert_called_once()

    def test_start_sets_credentials_when_configured(self, mock_paho):
        _, instance = mock_paho
        _seed_settings(mqtt_username="u1", mqtt_password="p1")
        MQTTClient().start()
        instance.username_pw_set.assert_called_once_with("u1", "p1")

    def test_start_without_username_skips_credentials(self, mock_paho):
        _, instance = mock_paho
        _seed_settings(mqtt_username="", mqtt_password="")
        MQTTClient().start()
        instance.username_pw_set.assert_not_called()

    def test_start_twice_is_noop(self, mock_paho):
        _, instance = mock_paho
        _seed_settings()
        client = MQTTClient()
        assert client.start() is True
        assert client.start() is False

    def test_stop_disconnects(self, mock_paho):
        _, instance = mock_paho
        _seed_settings()
        client = MQTTClient()
        client.start()
        client.stop()

        instance.disconnect.assert_called_once()
        instance.loop_stop.assert_called_once()
        assert client._client is None
        assert client.connected is False

    def test_stop_without_start_is_safe(self, mock_paho):
        client = MQTTClient()
        client.stop()
        assert client._client is None


class TestMQTTClientCallbacks:
    def test_on_connect_subscribes_sensors_pattern(self, mock_paho):
        _, instance = mock_paho
        client, _ = _started_client(mock_paho)
        reason = MagicMock()
        reason.is_failure = False

        client._on_connect(instance, None, None, reason)
        instance.subscribe.assert_called_once_with("gf/+/sensors", qos=1)
        assert client.connected is True

    def test_on_connect_failure_does_not_subscribe(self, mock_paho):
        _, instance = mock_paho
        client, _ = _started_client(mock_paho)
        reason = MagicMock()
        reason.is_failure = True

        client._on_connect(instance, None, None, reason)
        instance.subscribe.assert_not_called()
        assert client.connected is False

    def test_on_disconnect_clears_flag(self, mock_paho):
        client, instance = _started_client(mock_paho)
        reason = MagicMock()
        reason.is_failure = False
        client._on_connect(instance, None, None, reason)

        client._on_disconnect(instance, None, None, reason)
        assert client.connected is False

    def test_on_message_dispatches_to_handler_and_counts(self, mock_paho):
        handler = MagicMock()
        handler.handle.return_value = 2
        with patch("src.mqtt.client.SensorHandler", return_value=handler):
            client, instance = _started_client(mock_paho)

        msg = MagicMock()
        msg.topic = "gf/ESP-001/sensors"
        msg.payload = b'{"temperature": 22.5}'

        client._on_message(instance, None, msg)

        handler.handle.assert_called_once_with(msg.topic, msg.payload)
        assert client.message_count == 2
        assert client.last_message_at is not None

    def test_on_message_handler_exception_is_swallowed(self, mock_paho):
        handler = MagicMock()
        handler.handle.side_effect = RuntimeError("boom")
        with patch("src.mqtt.client.SensorHandler", return_value=handler):
            client, instance = _started_client(mock_paho)

        msg = MagicMock()
        msg.topic = "gf/ESP-001/sensors"
        msg.payload = b"{}"

        client._on_message(instance, None, msg)
        assert client.message_count == 0


class TestMQTTClientStatus:
    def test_status_dict_reflects_state(self, mock_paho):
        client, instance = _started_client(mock_paho)
        status = client.status_dict()

        assert status["enabled"] is True
        assert status["connected"] is False
        assert status["message_count"] == 0
        assert status["last_message_at"] is None

    def test_disabled_when_setting_false(self, mock_paho):
        _seed_settings(mqtt_enabled="false")
        client = MQTTClient()
        assert client.enabled is False
