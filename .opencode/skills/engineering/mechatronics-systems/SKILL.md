---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: mechatronics-systems
description: Design and build mechatronic systems combining sensors, actuators, and embedded control with Arduino and Python.
category: engineering
version: 0.1.0
author: devtiagoabreu
tags: [mechatronics, embedded, sensors, actuators, control, pid, arduino]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic electronics knowledge (voltage, current, pull-ups)
  - An Arduino-compatible board or Raspberry Pi
  - Python 3 with pyserial for host-side supervision
provides:
  - Sensor interfacing and signal-conditioning patterns
  - Actuator control via PWM and H-bridges
  - Closed-loop PID control in firmware and Python
  - Host-side data logging over serial
  - Safety practices for moving machinery
---

# mechatronics-systems

## Overview

Mechatronics merges mechanical engineering, electronics, and software.
A typical system senses the world with transducers, decides with a
microcontroller, and acts with actuators (motors, solenoids, valves).
This skill gives you the wiring, firmware, and host-side Python patterns
to build such systems reliably.

Always separate concerns: sample sensors at a fixed rate, keep control
loops short and deterministic, and stream telemetry to a host for
logging and supervision. Start with a block diagram and a power budget
before writing any code.

## Prerequisites

- Basic electronics: Ohm's law, voltage dividers, pull-up resistors
- An Arduino-compatible board or Raspberry Pi
- Python 3 with `pyserial` installed (`pip install pyserial`)
- Knowledge of non-blocking timing (`millis()`)
- A multimeter for verifying wiring before powering actuators

## Usage Instructions

### 1. Sensor Interfacing and Signal Conditioning

Sensors output analog voltages, digital edges, or serial-bus data.
Condition the signal before trusting it: add a pull-up/down, debounce
edges, and filter analog readings in software.

```cpp
const int TEMP = A0;   // LM35: 10 mV per degree C
const int ENC_A = 2, ENC_B = 3;

void setup() {
  pinMode(ENC_A, INPUT_PULLUP);
  pinMode(ENC_B, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  static long acc = 0;
  static int samples = 0;
  acc += analogRead(TEMP);
  if (++samples == 8) {
    float mv = (acc / 8.0) * (5000.0 / 1024.0);
    float degC = mv / 10.0;
    Serial.print("temp="); Serial.println(degC);
    acc = 0; samples = 0;
  }
}
```

### 2. Actuator Control: PWM and H-Bridges

Never drive a DC motor straight from an MCU pin: stall current far
exceeds the pin rating. Use a transistor or an H-bridge (L298N,
DRV8833) plus a flyback diode. PWM controls speed; the H-bridge
controls direction.

```cpp
const int PWM_PIN = 9;   // PWM-capable pin (3,5,6,9,10,11 on Uno)
const int IN1 = 7, IN2 = 8;

void setMotor(int speed, bool forward) {
  digitalWrite(IN1, forward);
  digitalWrite(IN2, !forward);
  analogWrite(PWM_PIN, constrain(abs(speed), 0, 255));
}
```

For position control of servos use the `Servo` library and supply them
from a separate rail — servo stalls can pull the MCU down.

### 3. Closed-Loop Control (PID) in Firmware

An open loop drifts under load changes; closed-loop control compares
the measured value with a setpoint and corrects the error. A PID
controller combines proportional, integral, and derivative terms:

```cpp
struct PID {
  float kp, ki, kd;
  float integral = 0, lastError = 0;
  unsigned long lastTime = 0;

  float update(float setpoint, float measured, unsigned long now) {
    float dt = (now - lastTime) / 1000.0f;
    if (dt <= 0) return 0;
    float error = setpoint - measured;
    integral += error * dt;
    float derivative = (error - lastError) / dt;
    lastError = error;
    lastTime = now;
    return kp * error + ki * integral + kd * derivative;
  }
};
```

Clamp the integral term to avoid windup, and keep the update rate
regular by calling `update` from a fixed timer.

### 4. Host-Side Supervision in Python

Use the host to log telemetry, plot trends, or run supervisory logic
that does not fit on the MCU. Read line-terminated frames over serial:

```python
import serial, time

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
with open("telemetry.csv", "a") as f:
    while True:
        line = ser.readline().decode("utf-8", "ignore").strip()
        if not line.startswith("temp="):
            continue
        f.write(f"{time.time()},{line.split('=')[1]}\n")
        f.flush()
```

## Best Practices

- Add a pull-up/pull-down to every digital input; never leave pins floating.
- Keep a power budget: motors, servos, and solenoids need separate rails.
- Filter analog reads and debounce edges before acting on them.
- Mark interrupt-shared variables `volatile` and keep ISRs tiny.
- Log labeled telemetry (`temp=23.5`) for easy host-side parsing.
- Put the mechanical system behind an emergency stop for moving parts.

## Pitfalls / Common Mistakes

- Driving motors directly from a digital pin — stalls draw far too much current.
- Using `delay()` inside a control loop, freezing sampling and PID updates.
- Forgetting flyback diodes on relays and motors, destroying the driver.
- Reading `analogRead` back-to-back without settling time, getting noise.
- Tuning PID with a too-high `ki`, causing windup and oscillation — clamp the integral.

## Examples

### Example 1: Line-following robot core loop

```cpp
int l = analogRead(A0), r = analogRead(A1);
if (l < 500 && r < 500)      { setMotor(200, true); setMotor(200, true); }
else if (l < 500)            { setMotor(80, false); setMotor(180, true); }
else if (r < 500)            { setMotor(180, true); setMotor(80, false); }
else                         { setMotor(200, true); setMotor(200, true); }
```

### Example 2: PID speed regulator with encoder feedback

```cpp
PID speedPid; speedPid.kp = 1.2; speedPid.ki = 0.1; speedPid.kd = 0.0;
unsigned long now = millis();
float rpm = readEncoderRpm();
int out = speedPid.update(TARGET_RPM, rpm, now);
setMotor(out, true);
```

## References

- [Arduino Reference](https://www.arduino.cc/reference/en/)
- [PID controller overview](https://en.wikipedia.org/wiki/PID_controller)
- [pyserial documentation](https://pyserial.readthedocs.io/)
