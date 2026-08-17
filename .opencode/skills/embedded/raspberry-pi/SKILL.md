---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: raspberry-pi
description: Set up and program Raspberry Pi projects (GPIO, cameras, edge AI, servers, robots). Use when configuring a Raspberry Pi, wiring GPIO, using Pi Camera, building edge/AI or IoT projects, home servers, kiosks, or when users mention Raspberry Pi, RPi, pi zero, GPIO, camera, PiCamera, raspi-config or edge device.
category: embedded
version: 0.1.0
author: devtiagoabreu
tags: [raspberry-pi, gpio, edge-ai, camera, iot, linux, python]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A Raspberry Pi (Zero/3/4/5) with microSD and power supply
  - Raspberry Pi OS (or Ubuntu) flashed with Imager
  - SSH access to the Pi
  - Python 3 with `RPi.GPIO` or `gpiozero` (installed on Raspberry Pi OS)
provides:
  - First-boot and headless setup
  - GPIO programming with gpiozero
  - Camera and computer vision setup
  - Edge AI / ML on device
  - Project templates (kiosk, sensor node, server, robot brain)
  - Common pitfalls (power, SD corruption, permissions)
difficulty: intermediate
frameworks: [raspberry-pi-os, gpiozero, opencv, python]
languages: [python, bash]
---

# Raspberry Pi

## Overview

The Raspberry Pi is a full Linux computer with GPIO — it runs an OS, so you
get Python, systemd, networking and cameras for free. Use it when a task needs
a real OS (servers, kiosks, edge AI, robots) rather than a bare-metal MCU.

## Prerequisites

- A Raspberry Pi (Zero/3/4/5) with microSD and power supply
- Raspberry Pi OS (or Ubuntu) flashed with Imager
- SSH access to the Pi
- Python 3 with `RPi.GPIO` or `gpiozero` (installed on Raspberry Pi OS)

## 1. First Boot and Headless Setup

```bash
# 1. Flash with Raspberry Pi Imager (enable SSH + WiFi in the Imager options!)
# 2. Find it on the network
ping raspberrypi.local          # or scan your router
ssh pi@raspberrypi.local        # default password on first boot
```

```bash
sudo raspi-config               # enable camera/GPIO, change hostname, enable I2C/SPI
sudo apt update && sudo apt full-upgrade -y
```

- Enable **SSH**, set a strong password, and change the default `pi` user if exposed.
- Keep the Pi off the internet directly: firewall + fail2ban, or put it on a VLAN.

## 2. GPIO with gpiozero (safe, debounced, human-friendly)

```python
from gpiozero import LED, Button, Buzzer, MotionSensor
from signal import pause

led = LED(17)          # BCM pin 17
btn = Button(2, pull_up=True)

btn.when_pressed = led.on
btn.when_released = led.off
pause()                # keep the program alive
```

- `gpiozero` uses **BCM numbering** by default (physical pin ≠ GPIO number).
- Pins are 3.3V — level-shift 5V devices; current limit ~16 mA per pin.
- Check the pinout: `pinout` command on Raspberry Pi OS.

### Non-blocking LED blink + button

```python
from gpiozero import LED, Button
from signal import pause

led = LED(17)
led.blink(on_time=0.5, off_time=0.5)   # hardware-timed, no sleep
btn = Button(2)
btn.when_pressed = lambda: led.off()
pause()
```

## 3. Camera and Computer Vision

### Pi Camera (CSI) with picamera2

```python
from picamera2 import Picamera2
from time import sleep

cam = Picamera2()
cam.configure(cam.create_still_configuration())
cam.start()
sleep(2)                      # auto-exposure settle
cam.capture_file("foto.jpg")
cam.stop()
```

### OpenCV pipeline (pi + USB cam or CSI via picamera2)

```python
import cv2
from picamera2 import Picamera2

cam = Picamera2()
cam.configure(cam.create_preview_configuration(main={"size": (640, 480)}))
cam.start()
frame = cam.capture_array()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
cv2.imwrite("edges.jpg", edges)
```

- Full-HD inference is slow on Pi — downscale to 640×480 for CV.
- Use `libcamera-hello` to verify the camera before blaming the code.
- Pair with the `vision`/`deep-learning` skills for model-based detection.

## 4. Edge AI / ML on Device

- Use **lightweight models**: MobileNet/TinyML-style, quantized to int8.
- Frameworks: TFLite Runtime, ONNX Runtime, or Ultralytics YOLO (int8).
- Pi 4: ~1–3 FPS for object detection at 640px; Pi 5 with Hailo-8 accelerator is the fast path.
- Throttle inference (every Nth frame), keep logs small, write results to MQTT/SQLite.

```python
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path="model_int8.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
interpreter.set_tensor(input_details[0]["index"], input_tensor)
interpreter.invoke()
```

## 5. Project Templates

### Kiosk / dashboard screen

```bash
sudo apt install -y chromium-browser unclutter
# autostart: ~/.config/autostart/kiosk.desktop launching chromium --kiosk URL
```

### Sensor node → MQTT

```python
import paho.mqtt.client as mqtt
from gpiozero import MCP3008

client = mqtt.Client("pi-copa")
client.connect("broker.local", 1883)
while True:
    value = MCP3008(channel=0).value
    client.publish("casa/copa/light", round(value, 3))
    time.sleep(30)
```

### Robot brain (Pi + motor driver)

Pair with the `robotics` skill: Pi runs high-level ROS 2 / Python control and
talks to an Arduino/ESP32 (motor controller) over serial or I2C.

## 6. Systemd Service (auto-start your program)

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Pi app
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=/home/pi/app
ExecStart=/usr/bin/python3 /home/pi/app/main.py
Restart=always
RestartSec=5
User=pi

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now myapp
sudo journalctl -u myapp -f     # logs
```

## 7. Common Pitfalls

| Symptom | Cause / Fix |
|---------|-------------|
| Won't boot / SD errors | Bad/cheap SD or corrupted writes — use a good card, always `sudo shutdown`. |
| Random reboots | Underpowered supply; Pi 4/5 need 3A+ official supply. |
| Slow | Full SD card (logs!) — check `df -h`, enable logrotate. |
| PermissionError GPIO | Run as root/systemd service or add user to `gpio` group. |
| Camera not found | Enable in `raspi-config`; verify `libcamera-hello`. |
| Overheating | Add heatsink/fan; check `vcgencmd measure_temp`. |

## Examples

### Example 1: Motion-triggered photo + notification

```python
from gpiozero import MotionSensor
from picamera2 import Picamera2
import time

pir = MotionSensor(4)
cam = Picamera2()
cam.configure(cam.create_still_configuration())
cam.start()

while True:
    pir.wait_for_motion()
    ts = int(time.time())
    cam.capture_file(f"/home/pi/photos/{ts}.jpg")
    # notify via MQTT / HTTP / Telegram here
    pir.wait_for_no_motion()
```

### Example 2: Quick GPIO matrix

```
3.3V (pin 1) ── LED ── resistor ── GPIO17 (pin 11)
GND  (pin 6)  ── LED/button ground
Button (pin 3, GPIO2) ── GND (active low with INPUT_PULLUP)
```

## Notes

- It's a Linux box first: use systemd, Python venvs, and SSH — not the Arduino mental model.
- Backup the SD card image; an SD failure is a full machine loss.
- For micro-power/battery projects prefer an ESP32/ESP8266; the Pi suits powered, OS-heavy tasks.
- Pair with `computer-vision`/`deep-learning` (camera/AI), `mqtt-protocol` (IoT), and `robotics` (robot brain).

## References

- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [gpiozero](https://gpiozero.readthedocs.io/)
- [picamera2](https://github.com/raspberrypi/picamera2)
- [Raspberry Pi OS](https://www.raspberrypi.com/software/)
