# Plano: Settings Global + MQTT + Sensores + Multi-device

> Data: 2026-08-22 | Status: APROVADO PELO USUÁRIO

## Visão Geral

Expandir o vision-platform-local para suportar:
1. **Configurações globais** editáveis pelo dashboard (DB)
2. **MQTT (Mosquitto)** no Orange Pi para sensores ESP
3. **SensorReadings** — armazenamento de dados de sensores (sem imagem)
4. **Fallback global→device** — device herda config global se não tiver própria
5. **Observation genérico** — camera_id → device_id, suporta qualquer tipo

## Decisões

| Decisão | Escolha | Motivo |
|---------|---------|--------|
| Broker MQTT | Mosquitto | Leve, padrão industria, Orange Pi |
| Storage configs | Banco de dados (SystemSettings) | Editavel pelo dashboard, sem restart |
| Config sensíveis | .env (jwt_secret, api_token, db_password) | Segurança |
| Sensores | ESP8266+DHT22, ESP32+multi | Confirmado pelo usuário |
| Fallback | device.connection_config → global defaults | Flexibilidade |

## Fase 1 — SystemSettings (DB)

### Novo ORM: `SystemSettings`

```python
class SystemSettings(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, nullable=False, indexed=True)
    value = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, onupdate=utcnow)
```

### Settings seeds (defaults)

```python
DEFAULT_SETTINGS = {
    # Geral
    "local_id": "sl000001",
    "local_name": "Orange Pi 001",
    "timezone": "America/Sao_Paulo",
    
    # Captura global
    "capture_interval_minutes": 60,
    "capture_evidence_dir": "/var/lib/vision-platform-local/evidence",
    "capture_jpeg_quality": 90,
    "capture_width": 1920,
    "capture_height": 1080,
    
    # Câmera padrão
    "camera_default_username": "admin",
    "camera_default_password": "",
    "camera_default_stream_type": "main",
    "camera_default_channel": 1,
    "camera_default_transport": "tcp",
    "camera_connect_timeout_ms": 10000,
    
    # Delivery
    "delivery_interval_seconds": 60,
    "central_api_base_url": "",
    "central_api_token": "",
    
    # MQTT
    "mqtt_broker_host": "localhost",
    "mqtt_broker_port": 1883,
    "mqtt_username": "",
    "mqtt_password": "",
    "mqtt_topic_prefix": "geofissura/",
    "mqtt_enabled": False,
    
    # Processamento
    "processing_enabled": False,
    "processing_auto_on_capture": True,
}
```

### Hierarquia de config

```
Device.connection_config[key]
    ↓ (se não existir)
SystemSettings[key]
    ↓ (se não existir)
Settings(.env)[key]
    ↓ (se não existir)
DEFAULT_SETTINGS[key]
```

### Arquivos

- `src/storage/models.py` — adicionar `SystemSettings` ORM
- `database/migrations/versions/008_system_settings.py` — migration
- `src/config/global_settings.py` — `get_setting(key)`, `set_setting(key, value)`, `get_all_settings()`
- `src/api/routes.py` — endpoints GET/POST `/api/v1/settings`
- `src/api/dashboard_routes.py` — página settings completa
- `src/templates/settings.html` — reescrever com todas seções

## Fase 2 — MQTT (Mosquitto)

### Instalação no Orange Pi

```bash
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto
# Configurar auth (opcional)
sudo tee /etc/mosquitto/conf.d/geofissura.conf << EOF
listener 1883
allow_anonymous true
password_file /etc/mosquitto/passwd
EOF
```

### MQTT Client no app

```
src/mqtt/
├── __init__.py
├── client.py          # MQTTClient wrapper (paho-mqtt)
├── sensor_handler.py  # processa mensagens de sensores
└── publisher.py       # publica comandos (opcional)
```

### Topics

```
geofissura/{device_id}/sensors       ← dados de sensores (ESP)
geofissura/{device_id}/status        ← heartbeat do ESP
geofissura/{device_id}/commands      ← comandos do server → ESP
```

### SensorReading ORM

```python
class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id = Column(Integer, primary_key=True)
    device_id = Column(String(64), nullable=False, indexed=True)
    topic = Column(String(256))
    reading_type = Column(String(32))  # temperature, humidity, pressure, etc.
    value_float = Column(Float)
    value_text = Column(Text)
    unit = Column(String(16))          # °C, %, hPa, etc.
    raw_payload = Column(Text)         # JSON original
    recorded_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=utcnow)
```

### Arquivos

- `src/mqtt/__init__.py`
- `src/mqtt/client.py` — connect, subscribe, reconnect
- `src/mqtt/sensor_handler.py` — parse payload, salvar SensorReading
- `database/migrations/versions/009_sensor_readings.py`
- `src/storage/models.py` — adicionar `SensorReading` ORM
- `src/api/routes.py` — GET `/api/v1/sensors/readings`
- `src/api/dashboard_routes.py` — página sensores
- `src/templates/sensors.html`
- `pyproject.toml` — adicionar `paho-mqtt>=2.0.0`

### Lifespan

```python
# src/main.py
# task existente: _processing_task (vision pipeline)
# task existente: _delivery_task
# NOVA task: _mqtt_task (conecta e mantém vivo)
```

## Fase 3 — Device Fallback

### `src/config/device_config.py`

```python
def resolve_device_config(device: Device) -> dict:
    """Resolva config do device com fallback global."""
    cfg = device.connection_config or {}
    
    # Globais do SystemSettings
    defaults = {
        "username": get_setting("camera_default_username"),
        "password": get_setting("camera_default_password"),
        "stream_type": get_setting("camera_default_stream_type"),
        "channel": int(get_setting("camera_default_channel")),
        "transport": get_setting("camera_default_transport"),
        "connect_timeout_ms": int(get_setting("camera_connect_timeout_ms")),
        "capture_interval_ms": int(get_setting("capture_interval_minutes")) * 60000,
        "jpeg_quality": int(get_setting("capture_jpeg_quality")),
        "capture_width": int(get_setting("capture_width")),
        "capture_height": int(get_setting("capture_height")),
    }
    
    # Device sobrescreve globals
    for k, v in defaults.items():
        cfg.setdefault(k, v)
    
    return cfg
```

### Atualizar CaptureWorker

Usar `resolve_device_config()` em vez de ler `connection_config` direto.

## Fase 4 — Dashboard Settings

### Seções da página

```
┌─────────────────────────────────────────┐
│ ⚙️  Configurações                       │
├─────────────────────────────────────────┤
│ 📋 Geral                                │
│    Local ID, Nome, Timezone             │
│                                         │
│ 📸 Captura (Global)                     │
│    Intervalo, Resolução, Qualidade      │
│    Diretório de evidências              │
│                                         │
│ 📡 Câmera Padrão                        │
│    Username, Password, Stream, Channel  │
│                                         │
│ 📤 Entrega (Central)                    │
│    URL, Token, Intervalo                │
│                                         │
│ 📶 MQTT                                 │
│    Broker, Porta, User, Pass, Topics    │
│                                         │
│ 🧠 Processamento                        │
│    Habilitado, Auto on capture          │
│                                         │
│ 💾 [Salvar]                             │
└─────────────────────────────────────────┘
```

## Ordem de implementação

1. **SystemSettings ORM + migration** (Fase 1)
2. **global_settings.py** (ler/gravar settings do DB)
3. **Dashboard settings page** (reescrita completa)
4. **device_config.py** (fallback global→device)
5. **Atualizar CaptureWorker** (usar fallback)
6. **SensorReading ORM + migration** (Fase 2)
7. **Mosquitto install script** (deploy/setup-mqtt.sh)
8. **MQTT client + sensor_handler** (paho-mqtt)
9. **Dashboard sensores page**
10. **Testes** para cada módulo

## Testes

| Módulo | Testes |
|--------|--------|
| SystemSettings | CRUD, defaults, fallback chain |
| global_settings | get/set, seed init, cache |
| device_config | fallback device→global→default |
| MQTT client | connect, subscribe, reconnect |
| sensor_handler | parse DHT22, save reading |
| SensorReading | CRUD, query by device/type |
| Dashboard settings | render, save, validation |
| Dashboard sensors | list, filter |
| API settings | GET/POST settings |
| API sensors | GET readings |
| E2E | capture → save → settings → delivery |

## Dependências novas

```
paho-mqtt>=2.0.0
```

## Migrations

| # | Nome | O que cria |
|---|------|------------|
| 008 | system_settings | Tabela system_settings + seeds |
| 009 | sensor_readings | Tabela sensor_readings |
