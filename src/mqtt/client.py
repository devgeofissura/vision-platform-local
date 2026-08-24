"""Cliente MQTT para recepção de dados de sensores (paho-mqtt)."""
import logging
import threading
from datetime import UTC, datetime

import paho.mqtt.client as paho_mqtt

from src.config.global_settings import get_setting, get_setting_bool
from src.mqtt.sensor_handler import SensorHandler

logger = logging.getLogger(__name__)


class MQTTClient:
    """Wrapper do paho-mqtt com configuração vinda de SystemSettings.

    Conecta em thread própria do paho (loop_start), assina
    '{prefix}+/sensors' e despacha mensagens para o SensorHandler.
    """

    def __init__(self, handler: SensorHandler | None = None):
        self._handler = handler or SensorHandler()
        self._client: paho_mqtt.Client | None = None
        self._lock = threading.Lock()
        self.connected = False
        self.last_message_at: datetime | None = None
        self.message_count = 0

    @property
    def enabled(self) -> bool:
        return get_setting_bool("mqtt_enabled")

    def _build_client(self) -> paho_mqtt.Client:
        client = paho_mqtt.Client(
            callback_api_version=paho_mqtt.CallbackAPIVersion.VERSION2,
            client_id="vision-local",
        )
        username = get_setting("mqtt_username")
        if username:
            client.username_pw_set(username, get_setting("mqtt_password") or None)
        client.reconnect_delay_set(min_delay=1, max_delay=60)
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect
        client.on_message = self._on_message
        return client

    def start(self) -> bool:
        """Conecta e inicia o loop de rede. Retorna True se iniciado."""
        with self._lock:
            if self._client is not None:
                logger.warning("MQTTClient já está em execução")
                return False
            host = get_setting("mqtt_broker_host") or "localhost"
            port = int(get_setting("mqtt_broker_port", "1883") or "1883")
            client = self._build_client()
            try:
                client.connect(host, port, keepalive=30)
            except OSError as exc:
                logger.error("Falha ao conectar ao broker MQTT %s:%d: %s", host, port, exc)
                return False
            client.loop_start()
            self._client = client
            logger.info("MQTTClient iniciado contra %s:%d", host, port)
            return True

    def stop(self):
        with self._lock:
            if self._client is None:
                return
            try:
                self._client.disconnect()
                self._client.loop_stop()
            except Exception:
                logger.exception("Erro ao parar MQTTClient")
            finally:
                self._client = None
                self.connected = False

    def _subscribe_sensors(self):
        prefix = get_setting("mqtt_topic_prefix") or "geofissura/"
        pattern = f"{prefix}+/sensors"
        result, _mid = self._client.subscribe(pattern, qos=1)
        status = "ok" if result == paho_mqtt.MQTT_ERR_SUCCESS else f"erro {result}"
        logger.info("Subscribe '%s': %s", pattern, status)

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        if getattr(reason_code, "is_failure", False):
            logger.error("Conexão MQTT recusada: %s", reason_code)
            return
        self.connected = True
        logger.info("MQTT conectado")
        self._subscribe_sensors()

    def _on_disconnect(self, client, userdata, flags, reason_code, properties=None):
        self.connected = False
        logger.warning("MQTT desconectado (%s); paho vai reconectar", reason_code)

    def _on_message(self, client, userdata, msg):
        try:
            saved = self._handler.handle(msg.topic, msg.payload)
            self.message_count += saved
            self.last_message_at = datetime.now(UTC).replace(tzinfo=None)
        except Exception:
            logger.exception("Erro processando mensagem de %s", msg.topic)

    def status_dict(self) -> dict:
        return {
            "enabled": self.enabled,
            "connected": self.connected,
            "message_count": self.message_count,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at else None,
        }
