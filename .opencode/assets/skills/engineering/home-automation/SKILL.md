---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: home-automation
description: Automate homes with Home Assistant YAML, ESPHome firmware, and MQTT for lights, sensors, and climate.
category: engineering
version: 0.1.0
author: devtiagoabreu
tags: [home-assistant, esphome, mqtt, yaml, iot, automation, smart-home]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A Home Assistant instance (HAOS, container, or supervised install)
  - An MQTT broker (Mosquitto) reachable by HA and devices
  - ESP32/ESP8266 devices for ESPHome
  - Basic YAML knowledge
provides:
  - Home Assistant YAML automations and scene patterns
  - ESPHome device firmware patterns
  - MQTT publish/subscribe integration
  - Reliable trigger and condition design
---

# home-automation

## Overview

Home automation connects sensors, lights, climate devices, and voice
assistants into one coordinated system. Home Assistant (HA) is the hub:
it ingests devices over MQTT, Z-Wave, Zigbee, or local APIs, and runs
automations written in YAML. ESPHome turns ESP32/ESP8266 microcontrollers
into reliable, local-first sensors and relays.

Design for local control first: automations that depend only on the LAN
keep working when the internet drops. This skill covers the three core
pieces — HA YAML, ESPHome firmware, and MQTT glue.

## Prerequisites

- A running Home Assistant instance with SSH or a file-editor add-on
- An MQTT broker reachable by HA and your devices
- ESPHome installed (`pip install esphome`) or the HA ESPHome add-on
- YAML familiarity and a basic understanding of MQTT topics

## Usage Instructions

### 1. Home Assistant Automation YAML

An automation has triggers, conditions, and actions. Triggers fire the
automation; conditions gate it; actions do the work. Keep them in one
place and prefer blueprint reuse for common patterns.

```yaml
alias: Turn on hallway light at dusk
triggers:
  - trigger: sun
    event: sunset
    offset: "-00:30:00"
conditions:
  - condition: state
    entity_id: input_boolean.hallway_auto
    state: "on"
actions:
  - action: light.turn_on
    target:
      entity_id: light.hallway
    data:
      brightness_pct: 60
mode: single
```

### 2. ESPHome Device Firmware

ESPHome flashes ESP32/ESP8266 with firmware generated from a YAML config.
The device boots, connects to WiFi and MQTT, and reports sensors. Define
the hardware pins and report intervals once:

```yaml
esphome:
  name: office-sensor
  platform: ESP32
  board: esp32dev

wifi:
  ssid: "HomeNet"
  password: "secret"

mqtt:
  broker: 192.168.1.10
  topic_prefix: office/sensor

sensor:
  - platform: dht
    pin: GPIO4
    temperature:
      name: "Office Temperature"
    humidity:
      name: "Office Humidity"
    update_interval: 30s
```

### 3. MQTT Publish/Subscribe

MQTT decouples devices from the hub. Devices publish state to a topic;
HA subscribes. Design a topic hierarchy from the start
(`<room>/<device>/<metric>`) because retagging later is painful.

```python
import paho.mqtt.publish as publish

publish.single(
    "office/sensor/temperature",
    "23.4",
    hostname="192.168.1.10",
)
```

### 4. Subscribing in Home Assistant

Wire a raw MQTT value into a sensor entity and trigger on it:

```yaml
mqtt:
  sensor:
    - name: "Office Temperature"
      state_topic: "office/sensor/temperature"
      unit_of_measurement: "\u00b0C"
      device_class: temperature
```

## Best Practices

- Use `mode: single` with `restart`/`queued` semantics to avoid duplicate actions.
- Keep MQTT topics lowercase with a slash hierarchy; use retained messages for state.
- Add availability/birth messages so HA knows when a device goes offline.
- Prefer local (LAN) services over cloud integrations for latency and privacy.
- Back up `configuration.yaml` and the `.esphome` config in git.

## Pitfalls / Common Mistakes

- Publishing sensor values every second, flooding the broker and HA's history DB.
- Confusing trigger and condition: a condition never fires an automation.
- Devices that reconnect and publish stale retained values.
- Using secrets inline in YAML — use the `!secret` reference instead.
- Powering relays from the same rail as the ESP, causing brownout resets.

## Examples

### Example 1: Notify on a window left open

```yaml
alias: Alert on open window
triggers:
  - trigger: numeric_state
    entity_id: sensor.window_sensor
    below: 5
conditions:
  - condition: time
    after: "22:00:00"
actions:
  - action: notify.mobile_app_phone
    data:
      message: "Window is open!"
```

### Example 2: Movie-night scene

```yaml
scene:
  - name: Movie Night
    entities:
      light.living_room: { brightness_pct: 20 }
      light.tv_backlight: { brightness_pct: 100 }
      media_player.tv: on
```

## References

- [Home Assistant Automation docs](https://www.home-assistant.io/docs/automation/)
- [ESPHome configuration guide](https://esphome.io/)
- [MQTT 3.1.1 specification](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)
