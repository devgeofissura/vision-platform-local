---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: arduino-development
description: Develop Arduino firmware for Uno/Nano/Mega and compatible boards. Use when writing or debugging Arduino sketches, controlling pins, sensors, motors, displays, serial communication, timers, interrupts, or when users mention Arduino, sketch, Uno, Nano, Mega, ATmega, sensors or embedded C++.
category: embedded
version: 0.1.0
author: devtiagoabreu
tags: [arduino, microcontroller, avr, sensors, motors, serial, cpp]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - An Arduino board (Uno/Nano/Mega) and USB cable
  - Arduino IDE (2.x) or PlatformIO
  - Basic electronics knowledge (resistors, breadboard, pull-ups)
provides:
  - Sketch structure and best practices
  - Pin I/O, interrupts, and timer patterns
  - Serial communication and debugging
  - Sensor and actuator integration patterns
  - Non-blocking code patterns (blink-without-delay)
  - Common pitfalls and fixes
difficulty: beginner
frameworks: [arduino, platformio, avr]
languages: [cpp]
---

# Arduino Development

## Overview

Arduino boards (ATmega328P on Uno/Nano) are the workhorse of hobby and
prototype electronics. The key skill is **non-blocking code**: `delay()` is a
trap — the MCU does nothing else while waiting. Design loops around state
machines and `millis()`.

## Prerequisites

- An Arduino board (Uno/Nano/Mega) and USB cable
- Arduino IDE (2.x) or PlatformIO
- Basic electronics knowledge (resistors, breadboard, pull-ups)

## 1. Sketch Structure

```cpp
#include <LiquidCrystal.h>

const int LED = 13;

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  blinkLed();
  readSerial();
}
```

- `setup()`: one-time init (pins, Serial, libraries).
- `loop()`: must never block for long — call short functions and return.
- Use `const` for pins; a pin map comment helps.

## 2. Non-blocking pattern (blink without delay)

```cpp
unsigned long lastToggle = 0;
const unsigned long INTERVAL = 500;

void loop() {
  unsigned long now = millis();
  if (now - lastToggle >= INTERVAL) {
    lastToggle = now;
    digitalWrite(LED, !digitalRead(LED));
  }
  // other tasks run here — nothing is blocked
}
```

Use this pattern for any periodic task: sampling, debouncing, beeping.

## 3. Digital and Analog I/O

```cpp
pinMode(BTN, INPUT_PULLUP);          // internal pull-up: button to GND
int reading = digitalRead(BTN);      // LOW when pressed (active low)
int pot = analogRead(A0);            // 0..1023
int pwm = map(pot, 0, 1023, 0, 255); // scale for analogWrite
analogWrite(PWM_PIN, pwm);           // 0..255
```

### Button debounce (state-machine)

```cpp
const unsigned long DEBOUNCE = 30;
unsigned long lastPress = 0;
bool lastState = HIGH;

void loop() {
  bool nowState = digitalRead(BTN);
  if (nowState != lastState && millis() - lastPress > DEBOUNCE) {
    lastPress = millis();
    if (nowState == LOW) onPress();   // debounced press
  }
  lastState = nowState;
}
```

## 4. Serial Debugging (your best friend)

```cpp
Serial.begin(115200);
Serial.print("temp="); Serial.print(temp); Serial.println("C");
```

- Print **labeled values** (`temp=23.5C`) — raw numbers are unreadable in logs.
- Use `Serial.available()` to receive bytes; prefer newline-terminated commands:

```cpp
void readSerial() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    if (line == "on") digitalWrite(LED, HIGH);
    else if (line == "off") digitalWrite(LED, LOW);
  }
}
```

- Baud mismatch (9600 vs 115200) shows garbage — always match both ends.

## 5. Interrupts (for time-critical edges)

```cpp
volatile unsigned long pulses = 0;

void countPulse() { pulses++; }           // ISR: keep it tiny

void setup() {
  attachInterrupt(digitalPinToInterrupt(2), countPulse, RISING);
}
```

- ISRs must be **short** — no `delay()`, no `Serial.print()`, no `millis()` reliance.
- Mark shared variables `volatile`.
- Interrupt-safe rotary encoders / flow meters: count in ISR, process in `loop()`.

## 6. Sensors and Actuators

| Component | Pattern |
|-----------|---------|
| DHT22 (temp/hum) | library (`DHT.h`); sample every ≥ 2s |
| HC-SR04 (ultrasonic) | `pulseIn` trig/echo; 4 m range, 30° cone |
| Servo | `Servo.h`, `servo.write(angle)`, separate power |
| DC motor | transistor/H-bridge + PWM; flyback diode |
| Relay | `digitalWrite` HIGH/LOW; diode + opto-isolator for inductive loads |
| 16x2 LCD | `LiquidCrystal` (4-bit wiring), or I2C with `LiquidCrystal_I2C` |

### Ultrasonic distance example

```cpp
void loop() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long us = pulseIn(ECHO, HIGH);
  float cm = us / 58.0;            // us → cm (round-trip at ~340 m/s)
  Serial.print("dist="); Serial.print(cm); Serial.println("cm");
  delay(100);
}
```

## 7. Memory on ATmega328P (2 KB SRAM!)

- Avoid `String` concatenation in loops; use `char buf[32]; snprintf(buf, sizeof(buf), ...)`.
- Keep global/large arrays out of SRAM — use `PROGMEM` for constants (`const char msg[] PROGMEM`).
- Watch for stack overflow: recursive calls, huge local buffers.
- Long `delay()` in one place starves everything else; restructure with timers.

## 8. Common Pitfalls

| Symptom | Cause / Fix |
|---------|-------------|
| Board won't upload | Wrong port/board selected; unplug other serial devices; check drivers (CH340). |
| Random resets | Power sag (motors/servos on same rail) — separate supplies, decoupling caps. |
| Floating inputs | Enable `INPUT_PULLUP` or add external pull-up/down. |
| `analogRead` noisy | Short delay after pin switch; filter with averaging; decouple AREF. |
| PWM not working on pin | `analogWrite` works only on PWM-capable pins (3,5,6,9,10,11 on Uno). |
| I2C hangs | Pull-ups (4.7 kΩ), same voltage, check addresses with I2C scanner. |

## Examples

### Example 1: Temperature-controlled fan

```cpp
const int LM35 = A0, FAN = 9;

void loop() {
  int raw = analogRead(LM35);
  float mv = raw * (5000.0 / 1024.0);
  float temp = mv / 10.0;
  int speed = constrain(map(temp, 25, 40, 0, 255), 0, 255);
  analogWrite(FAN, speed);
  delay(200);
}
```

### Example 2: State-machine menu (non-blocking)

```cpp
enum Mode { IDLE, MENU, RUN };
Mode mode = IDLE;

void loop() {
  switch (mode) {
    case IDLE: mode = handleIdle(); break;
    case MENU: mode = handleMenu(); break;
    case RUN:  mode = handleRun();  break;
  }
}
```

## Notes

- Measure before wiring power: motors/servos need their own supply.
- Use pull-up for buttons to GND (active-low) — simplest and safest.
- Comment the wiring (pin map) at the top of each sketch; you will forget it.
- Pair with `esp32-development`/`esp8266-development` when the project needs WiFi, and `robotics` for robot builds.

## References

- [Arduino Reference](https://www.arduino.cc/reference/en/)
- [Arduino Language Docs](https://docs.arduino.cc/language-reference/)
- [PlatformIO](https://platformio.org/)
