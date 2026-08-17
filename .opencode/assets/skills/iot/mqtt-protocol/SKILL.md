---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: mqtt-protocol
description: Build IoT messaging with MQTT covering brokers, QoS, topics, and pub/sub patterns
category: iot
version: 0.1.0
author: devtiagoabreu
tags: [mqtt, iot, pubsub, mosquitto, qos, broker, topics]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic networking concepts (TCP/IP)
  - Familiarity with JSON payloads
  - A terminal and access to install clients (mosquitto-clients or paho)
provides:
  - Broker setup and security configuration steps
  - Topic design and wildcard usage guidance
  - QoS semantics and message flow explanations
  - Publisher and subscriber client examples in multiple languages
---

# MQTT Protocol

## Overview

MQTT is a lightweight publish/subscribe messaging protocol designed for constrained
devices and unreliable networks. Clients connect to a central broker and communicate
through topics, with the broker forwarding messages to all subscribers of a topic.
It supports three quality-of-service (QoS) levels that trade delivery guarantees for
bandwidth, plus retained messages and persistent sessions for reconnect behavior.
Because it is a binary, connection-oriented protocol, MQTT is well suited to
sensor telemetry, device commands, and large fleets of low-power devices.

## Prerequisites

- Ability to install a local broker such as Eclipse Mosquitto
- Basic command-line skills and one scripting language (Python recommended)
- A broker listener reachable on port 1883 (plaintext) or 8883 (TLS)

## Usage Instructions

### Step 1: Install and Start a Broker

Mosquitto is the reference open-source broker. Install it and start it locally:

```bash
# Debian/Ubuntu
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
mosquitto_sub -h localhost -t test -C 1   # verify it responds
```

### Step 2: Publish and Subscribe with Clients

Test the round trip with two terminals using the CLI clients:

```bash
# Terminal A - subscribe
mosquitto_sub -h localhost -t 'sensors/+/temperature' -v

# Terminal B - publish
mosquitto_pub -h localhost -t 'sensors/room1/temperature' -m '{"value": 21.5}'
```

Terminal A prints `sensors/room1/temperature {"value": 21.5}`.

### Step 3: Design Topics with Hierarchy and Wildcards

Structure topics as a hierarchy of levels separated by `/` and use wildcards where
appropriate:

```
sensors/<room>/temperature     # a specific level
sensors/+/temperature          # '+' matches exactly one level
sensors/#                      # '#' matches the rest of the hierarchy
```

Good topic design keeps common prefixes stable so subscriptions are efficient and
access control can be expressed per prefix. Never put leading or trailing slashes
in topics.

### Step 4: Choose the Right QoS Level

```
QoS 0  at most once  - fire and forget, lowest overhead
QoS 1  at least once - message stored until PUBACK, may duplicate
QoS 2  exactly once  - four-way handshake, highest overhead
```

Use QoS 0 for high-frequency telemetry where a lost sample does not matter, QoS 1 for
most commands and alarms, and QoS 2 only when duplicates are unacceptable (e.g.
financial or actuation messages). A broker and its clients each have a maximum
supported QoS.

### Step 5: Secure the Broker with Authentication and TLS

Never leave a broker open on the public internet with anonymous access. Require
username/password and TLS:

```conf
# /etc/mosquitto/conf.d/secure.conf
allow_anonymous false
password_file /etc/mosquitto/passwd
listener 8883
certfile /etc/mosquitto/certs/server.crt
keyfile  /etc/mosquitto/certs/server.key
tls_version tlsv1.2
```

```bash
mosquitto_passwd -c /etc/mosquitto/passwd device1
mosquitto_sub --cafile ca.crt -p 8883 -h mybroker.local -u device1 -P secret -t 'sensors/#'
```

### Step 6: Use Retained Messages and Last Will

Set the retained flag to store the latest value on a topic for late subscribers, and
use Last Will and Testament (LWT) so the broker publishes a status topic when a device
disconnects unexpectedly:

```bash
mosquitto_pub -h localhost -t 'devices/gateway/state' -m '{"status": "online"}' -r
# The device also configures a will: {topic: devices/gateway/state,
#                                    payload: '{"status": "offline"}', retain: true}
```

## Examples

### Example 1: Python Publisher (Paho)

```python
import json
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)
payload = json.dumps({"temperature": 22.4, "humidity": 41})
client.publish("sensors/room1/telemetry", payload, qos=1)
client.disconnect()
```

### Example 2: Python Subscriber with Callback

```python
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("sensors/+/temperature", qos=0)
client.loop_forever()
```

## References

- [MQTT 3.1.1 OASIS Specification](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)
- [MQTT 5.0 OASIS Specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
- [Eclipse Mosquitto](https://mosquitto.org/)
- [MQTT.org](https://mqtt.org/)
- [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
- [Paho Python Client](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html)

## Notes

- QoS 1 can deliver duplicates; make consumers idempotent (e.g. de-duplicate by
  message ID or timestamp).
- MQTT uses long-lived TCP connections; configure keepalive correctly to detect dead
  devices, and pair it with a Last Will.
- Clients can publish to a topic they are not subscribed to, so enforce authorization
  on the broker per prefix.
- The broker is the single point of failure; run it in a cluster (e.g. with MQTT 5
  shared subscriptions) for production fleets.
- Mind payload size: binary payloads and compact formats (CBOR, protobuf) keep
  constrained links usable.
