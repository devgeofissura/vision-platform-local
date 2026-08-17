---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: sensor-integration
description: Integrate sensors over I2C and SPI and build an end-to-end telemetry pipeline
category: iot
version: 0.1.0
author: devtiagoabreu
tags: [i2c, spi, sensors, telemetry, embedded, iot, data-pipeline]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A microcontroller board (ESP32 or similar) with I2C/SPI peripherals
  - A sensor module with a documented register map (e.g. BME280, MPU6050, TSL2591)
  - Basic C or MicroPython skills and wiring (pull-ups, level shifting)
provides:
  - I2C and SPI bus fundamentals and driver examples
  - Sensor initialization, reading, and calibration patterns
  - Telemetry pipeline design from device to cloud
  - Data validation and edge batching best practices
---

# IoT Sensor Integration

## Overview

Sensor integration is the bridge between a physical measurement and usable data: the
firmware must configure the sensor over a bus, read registers, apply calibration, and
package readings into telemetry. The two dominant serial buses are I2C, which uses two
wires and address-based device selection, and SPI, which uses a shared clock plus a
chip-select line per device and supports higher throughput. Beyond the driver, a solid
integration defines a telemetry pipeline: edge sampling, validation, batching, and
delivery to a broker or cloud ingest point. This skill covers the bus fundamentals,
register-level drivers, and the pipeline that turns raw counts into reliable signals.

## Prerequisites

- A board with exposed I2C (SDA/SCL) and SPI (SCLK/MOSI/MISO/CS) pins
- A sensor with a datasheet listing its I2C address and control/data registers
- Patience with wiring; verify bus detection before writing application logic

## Usage Instructions

### Step 1: Wire the Bus Correctly

For I2C, pull SDA and SCL up (typically 4.7k-10k ohms to 3.3 V) and keep the bus
short. For SPI, each device needs its own chip-select line:

```
I2C:  MCU SDA <-> sensor SDA, MCU SCL <-> sensor SCL  (shared bus, addresses)
SPI:  MCU SCLK <-> sensor SCLK
      MCU MOSI <-> sensor MOSI, MCU MISO <-> sensor MISO
      MCU CS0  <-> sensor1 CS,  MCU CS1  <-> sensor2 CS
```

Level-shift any sensor that runs at a different logic voltage than the MCU.

### Step 2: Detect the Device on the Bus

Probe for the expected I2C address (e.g. BME280 responds at 0x76 or 0x77) before
writing the driver:

```python
from machine import Pin, I2C

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
print(i2c.scan())          # expect [118] for 0x76, [119] for 0x77
```

For SPI, verifying the presence is done by reading a chip ID register; the
chip-select toggling confirms your wiring.

### Step 3: Initialize and Read the Sensor Registers

Read the datasheet register map, then initialize and sample. BME280 temperature as a
device driver sketch:

```python
REG_ID = 0xD0
REG_CTRL_MEAS = 0xF4
REG_DATA = 0xFA  # MSB of temperature

def read_u8(reg):
    return i2c.readfrom_mem(0x76, reg, 1)[0]

assert read_u8(REG_ID) == 0x60, "BME280 not found"

i2c.writeto_mem(0x76, REG_CTRL_MEAS, bytes([0x27]))  # normal mode, osrs_t=1, osrs_p=1

msb, lsb = i2c.readfrom_mem(0x76, REG_DATA, 2)
raw = (msb << 8) | lsb
temperature_c = raw / 16.0 - 273.15   # simplified; apply calibration for accuracy
```

### Step 4: Batch and Validate at the Edge

Validate readings (range checks, stale timestamps) and batch them before sending to
reduce connection overhead:

```python
import time

SAMPLE_WINDOW = 60  # seconds
samples = []

while time.time() - start < SAMPLE_WINDOW:
    t = read_temperature()
    if -40 <= t <= 125:          # reject out-of-range readings
        samples.append(t)
    time.sleep(2)

batch = {"device": "gw-001", "ts": int(time.time()), "temp_c": sum(samples) / len(samples)}
```

### Step 5: Ship Telemetry Through the Pipeline

Publish the batch to a broker or cloud ingest point with QoS, and add retry with
backoff on failure:

```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("broker.local", 1883, 60)
rc = client.publish("sensors/gw-001/telemetry", json.dumps(batch), qos=1)
if rc.rc != 0:
    store_locally(batch)   # spool to flash and replay on next connect
```

A complete pipeline looks like: sensor -> bus driver -> calibration -> validation ->
edge batching -> broker -> stream processor -> time-series store -> dashboard.

## Examples

### Example 1: SPI Temperature Sensor Read (C, ESP-IDF style)

```c
#include "driver/spi_master.h"
#include "esp_log.h"

spi_device_handle_t sensor;

void sensor_init(void) {
    spi_bus_config_t bus = {
        .mosi_io_num = 13, .miso_io_num = 12,
        .sclk_io_num = 14, .quadwp_io_num = -1, .quadhd_io_num = -1,
    };
    spi_bus_initialize(SPI2_HOST, &bus, 0);

    spi_device_interface_config_t dev = {
        .mode = 0, .clock_speed_hz = 1000000,
        .spics_io_num = 15, .queue_size = 1,
    };
    spi_bus_add_device(SPI2_HOST, &dev, &sensor);
}

int sensor_read_id(void) {
    uint8_t tx[2] = { 0x0F, 0x00 };   // read-only register 0x0F
    uint8_t rx[2] = { 0, 0 };
    spi_transaction_t t = {
        .tx_buffer = tx, .rx_buffer = rx, .length = 16,
    };
    spi_device_transmit(sensor, &t);
    return rx[1];
}
```

### Example 2: Telemetry with Retry and Backoff

```python
def publish_with_retry(client, topic, payload, attempts=5):
    for n in range(attempts):
        if client.publish(topic, payload, qos=1).rc == 0:
            return True
        time.sleep(2 ** n)   # 1s, 2s, 4s... exponential backoff
    return False
```

## References

- [I2C Specification and Overview](https://www.nxp.com/docs/en/user-guide/UM10204.pdf)
- [SPI Bus Overview](https://learn.sparkfun.com/tutorials/serial-peripheral-interface-spi)
- [Bosch BME280 Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf)
- [Espressif ESP-IDF I2C Driver](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2c.html)
- [InfluxDB - Time Series Telemetry](https://docs.influxdata.com/influxdb/)

## Notes

- Read the datasheet register map before writing code; addressing, endianness, and
  startup times vary per part.
- I2C is slower (100-400 kHz) and fine for a few sensors; switch to SPI for high-rate
  streaming sensors.
- Never hardcode calibration constants; store them in NVS/flash per device so sensor
  drift can be corrected in the field.
- Reject invalid samples at the edge, but log them; a sensor reading stuck at zero is
  usually a wiring or power fault.
- Add a device time source (RTC or NTP) so telemetry timestamps are comparable across
  a fleet.
