---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: esp8266-development
description: Develop firmware for ESP8266 (NodeMCU/Wemos D1) with Arduino core and ESP8266RTOS SDK. Use when building WiFi-connected sensor devices, IoT nodes, HTTP/MQTT clients on ESP8266, OTA updates, deep sleep, or when users mention ESP8266, NodeMCU, Wemos D1, ESP-01, IoT, WiFi firmware.
category: embedded
version: 0.1.0
author: devtiagoabreu
tags: [esp8266, nodemcu, wemos, iot, wifi, mqtt, arduino, ota]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - ESP8266 board (NodeMCU, Wemos D1 mini, ESP-01)
  - Arduino IDE with esp8266 core, or PlatformIO
  - USB-serial driver (CP210x/CH340)
  - 3.3V logic; NOT 5V tolerant — level shifters for 5V sensors
provides:
  - Project setup for Arduino core and PlatformIO
  - WiFi connection with reconnect logic
  - MQTT/HTTP client patterns for IoT
  - Deep sleep for battery operation
  - OTA update workflow
  - Common troubleshooting (reset loops, brownouts)
difficulty: intermediate
frameworks: [arduino, platformio, mqtt, nodemcu]
languages: [cpp]
---

# ESP8266 Development

## Overview

The ESP8266 is a cheap WiFi MCU (80/160 MHz, ~80 KB RAM) ideal for IoT nodes
that read sensors and talk to the network. RAM is tiny — keep buffers small,
avoid `String` in hot paths, and design for **reconnect + deep sleep**.

## Prerequisites

- ESP8266 board (NodeMCU, Wemos D1 mini, ESP-01)
- Arduino IDE with esp8266 core, or PlatformIO
- USB-serial driver (CP210x/CH340)
- 3.3V logic; NOT 5V tolerant — level shifters for 5V sensors

## 1. Project Setup

### Arduino core (fastest start)

- Board Manager URL: `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
- Boards: `NodeMCU 1.0 (ESP-12E)` or `LOLIN(WEMOS) D1 mini`

### PlatformIO (recommended for serious work)

```ini
; platformio.ini
[env:nodemcuv2]
platform = espressif8266
board = nodemcuv2
framework = arduino
monitor_speed = 115200
upload_port = /dev/ttyUSB0
```

## 2. WiFi with Auto-Reconnect

```cpp
#include <ESP8266WiFi.h>

const char* SSID = "rede";
const char* PASS = "senha";

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
    delay(500);
    Serial.print(".");
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\nIP: %s\n", WiFi.localIP().toString().c_str());
  }
}
```

- Call `connectWiFi()` when `WiFi.status() != WL_CONNECTED` (in `loop()` or a timer) — do not `ESP.restart()` on every blip.
- `WiFi.setAutoReconnect(true)` + `WiFi.persistent(true)`.

## 3. MQTT Client (the default IoT protocol)

```cpp
#include <PubSubClient.h>

WiFiClient net;
PubSubClient mqtt(net);

void setupMqtt() {
  mqtt.setServer("broker.local", 1883);
  mqtt.setCallback(onMessage);
}

void loopMqtt() {
  if (!mqtt.connected()) {
    if (mqtt.connect("sensor-copa")) {   // unique client id!
      mqtt.subscribe("casa/copa/set");
    } else {
      delay(2000);
    }
  }
  mqtt.loop();
}

void onMessage(char* topic, byte* payload, unsigned int len) {
  // parse payload; avoid heap growth
}
```

- **Unique client id** per device — duplicate ids kick each other off.
- QoS 1 for control topics; QoS 0 for telemetry.
- Include a `will` (last will) so the broker reports device death.

## 4. HTTP Requests (lighter alternative)

```cpp
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>

void postReading() {
  WiFiClient client;
  HTTPClient http;
  if (http.begin(client, "http://api.example.com/ingest")) {
    http.addHeader("Content-Type", "application/json");
    int code = http.POST("{\"sensor\":\"copa\",\"temp\":23.5}");
    http.end();
  }
}
```

## 5. Deep Sleep (battery operation)

```cpp
#include <ESP8266Sleep.h> // or ESP.deepSleep()

void setup() {
  // wake up, read sensor, publish
  Serial.begin(115200);
  float temp = readTemp();
  postReading();
  Serial.println("sleeping");
  ESP.deepSleep(15 * 60e6); // 15 minutes, in microseconds
}

void loop() { /* empty: we never loop */ }
```

- Deep sleep **RTC wake** needs `GPIO16` wired to `RST` on most boards.
- Total current in deep sleep ≈ 20 µA (great battery life); modem-off light sleep is a middle ground.
- Keep the sensor warm-up before reading — first analog read after wake is noisy.

## 6. OTA Updates

```cpp
#include <ArduinoOTA.h>

void setupOta() {
  ArduinoOTA.begin();
}
// in loop(): ArduinoOTA.handle();
```

- Upload the first firmware over serial, then updates go over WiFi — no more USB cable.
- Set an OTA password (`ArduinoOTA.setPassword`).
- Do not OTA while a critical process (e.g. EEPROM write) is mid-flight.

## 7. Common Pitfalls

| Symptom | Cause / Fix |
|---------|-------------|
| Brownout/reset in a loop | Power supply can't handle WiFi TX spikes (200–300 mA). Use ≥ 500 mA, big capacitor at VCC. |
| Serial garbage | Wrong baud (115200 default) or wrong drivers (CH340 vs CP210x). |
| `rst cause: 4` (watchdog) | `delay()` too long inside loops, or heavy work blocking WiFi — avoid blocking calls. |
| Random disconnects | Distance/power; enable `WiFi.setSleep(false)` if idle disconnect matters. |
| GPIO pulled low on boot | Some pins (GPIO0/2/15) have boot strapping constraints — don't use them for outputs expecting HIGH at boot. |
| Flashing fails | Hold GPIO0/`FLASH` during upload on ESP-01; use a proper programmer. |

## Examples

### Example 1: Temperature + deep sleep node

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* SSID = "..."; const char* PASS = "...";
const char* URL = "http://api.example.com/ingest";
const float OFFSET = -0.4;

void setup() {
  Serial.begin(115200);
  delay(100);
  int raw = analogRead(A0);
  float mv = raw * (3300.0 / 1024.0);
  float temp = mv / 10.0 + OFFSET;   // ex.: LM35
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);
  unsigned long t0 = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t0 < 10000) delay(100);
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient c; HTTPClient http;
    if (http.begin(c, URL)) {
      http.addHeader("Content-Type", "application/json");
      char body[64];
      snprintf(body, sizeof(body), "{\"temp\":%.1f}", temp);
      http.POST(body); http.end();
    }
  }
  ESP.deepSleep(15 * 60e6);
}
void loop() {}
```

### Example 2: Wemos D1 pin map (quick reference)

| Function | GPIO | Pin on D1 mini |
|----------|------|----------------|
| I2C SDA | GPIO4 | D2 |
| I2C SCL | GPIO5 | D1 |
| ADC | A0 | A0 |
| PWM | GPIO12 | D6 |

## Notes

- 3.3V only — logic-level shift 5V sensors; the ADC reads 0–3.3V.
- Keep RAM small: use `char[]` buffers and `snprintf` over `String` concatenation.
- Every networked device needs reconnect + OTA, or it will be unmaintainable in the field.
- See `iot` skills (`mqtt-protocol`, `sensor-integration`) and `arduino-development` for shared MCU patterns.

## References

- [ESP8266 Arduino Core](https://github.com/esp8266/Arduino)
- [PubSubClient](https://github.com/knolleary/pubsubclient)
- [ESP8266 Pinout guide](https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/)
