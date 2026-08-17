---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: esp32-development
description: Develop firmware for ESP32 with ESP-IDF, GPIO, WiFi, and FreeRTOS
category: embedded
version: 0.1.0
author: devtiagoabreu
tags: [esp32, esp-idf, c, freeRTOS, gpio, wifi, microcontroller]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - C programming fundamentals
  - A ESP32 development board (e.g. ESP32-DevKitC)
  - USB cable and esptool or Espressif IDE
  - Working ESP-IDF installation
provides:
  - ESP-IDF project scaffolding and build workflow
  - GPIO, PWM, and interrupt examples
  - WiFi station and SoftAP connection patterns
  - FreeRTOS task and event loop integration for ESP32
---

# ESP32 Development

## Overview

The ESP32 is a dual-core, WiFi and Bluetooth capable microcontroller from Espressif
whose primary development environment is ESP-IDF, a framework built on FreeRTOS.
Projects are CMake-based, and code runs inside FreeRTOS tasks rather than a bare
`while(1)` loop, so concurrency and event handling are explicit. This skill walks
through the standard ESP-IDF workflow: creating a project, configuring the target,
building and flashing, driving GPIO, connecting to WiFi, and structuring firmware as
FreeRTOS tasks. Debugging relies on the built-in logging library, JTAG or UART output,
and carefully isolated hardware state.

## Prerequisites

- A machine with `idf.py` in PATH and the target toolchains installed
- An ESP32 board with an onboard or wired USB-to-UART bridge
- Basic electronics: pull-up resistors, power and ground wiring
- Comfort with CMake-based build systems and serial monitors

## Usage Instructions

### Step 1: Create and Configure a Project

Use the ESP-IDF templates to scaffold, then set the target and build:

```bash
idf.py create-project my_app
cd my_app
idf.py set-target esp32
idf.py menuconfig        # optional: partition table, flash size, peripherals
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

`idf.py flash monitor` compiles, flashes the firmware over UART, and opens the
serial console so ESP_LOG output is visible.

### Step 2: Drive GPIO Pins

Use the driver API to configure an LED output and a button input with internal pull-up:

```c
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define LED_PIN   GPIO_NUM_2
#define BTN_PIN   GPIO_NUM_0

void app_main(void) {
    gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(BTN_PIN, GPIO_MODE_INPUT);
    gpio_set_pull_mode(BTN_PIN, GPIO_PULLUP_ONLY);

    while (1) {
        int pressed = gpio_get_level(BTN_PIN) == 0;   // active low
        gpio_set_level(LED_PIN, pressed ? 1 : 0);
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}
```

Never block the loop with long delays; use `vTaskDelay` so FreeRTOS can schedule
other tasks.

### Step 3: Use Interrupts for Fast Inputs

For debounced and responsive button handling, install an ISR service and attach an
interrupt handler:

```c
#include "esp_log.h"
#include "driver/gpio.h"

static void IRAM_ATTR button_isr(void *arg) {
    // Keep ISR bodies minimal: only set a flag or notify a task.
    xTaskNotifyFromISR(xGetCurrentTaskHandle(), 0x01, eSetBits, NULL);
}

void app_main(void) {
    gpio_install_isr_service(0);
    gpio_isr_handler_add(BTN_PIN, button_isr, NULL);
    gpio_set_intr_type(BTN_PIN, GPIO_INTR_NEGEDGE);
    // Long-running handling belongs in a FreeRTOS task, not the ISR.
}
```

### Step 4: Connect to WiFi as a Station

Use the event-driven WiFi API with an event handler:

```c
#include "esp_wifi.h"
#include "esp_event.h"

#define WIFI_SSID "my-network"
#define WIFI_PASS "my-password"

static void on_sta_start(void *arg, esp_event_base_t base,
                         int32_t id, void *data) {
    esp_wifi_connect();
}

void app_main(void) {
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    ESP_ERROR_CHECK(esp_event_handler_register(
        WIFI_EVENT, WIFI_EVENT_STA_START, on_sta_start, NULL));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
}
```

### Step 5: Structure Firmware as Tasks

Give each concern its own FreeRTOS task with a stack size generous enough for the
libraries it calls:

```c
void sensor_task(void *arg) {
    while (1) {
        read_sensor();
        vTaskDelay(pdMS_TO_TICKS(5000));   // read every 5 s
    }
}

void app_main(void) {
    xTaskCreate(sensor_task, "sensor", 4096, NULL, 1, NULL);
}
```

## Examples

### Example 1: PWM Dimming with LEDC

```c
#include "driver/ledc.h"

ledc_timer_config_t timer = {
    .speed_mode = LEDC_LOW_SPEED_MODE,
    .duty_resolution = LEDC_TIMER_8_BIT,
    .timer_num = LEDC_TIMER_0,
    .freq_hz = 5000,
    .clk_cfg = LEDC_AUTO_CLK,
};
ledc_timer_config(&timer);

ledc_channel_config_t chan = {
    .gpio_num = 2,
    .speed_mode = LEDC_LOW_SPEED_MODE,
    .channel = LEDC_CHANNEL_0,
    .timer_sel = LEDC_TIMER_0,
    .duty = 128,        // 0-255 for 8-bit resolution
    .hpoint = 0,
};
ledc_channel_config(&chan);
ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 128);
ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
```

### Example 2: Reading Log Output

```c
#include "esp_log.h"
static const char *TAG = "my_app";

ESP_LOGI(TAG, "Booted, heap free: %d", esp_get_free_heap_size());
// Observe with: idf.py -p /dev/ttyUSB0 monitor
```

## References

- [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/index.html)
- [ESP-IDF API Reference - GPIO](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html)
- [ESP-IDF API Reference - WiFi](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/network/esp_wifi.html)
- [ESP-IDF FreeRTOS Extensions](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/freertos.html)
- [Espressif Boards and Hardware Docs](https://www.espressif.com/en/products/devkits)

## Notes

- Use the chip revision correctly: `idf.py set-target` must match your board's SoC
  (esp32, esp32s2, esp32s3, esp32c3, esp32c6).
- ISR handlers must be short, marked `IRAM_ATTR`, and only communicate via
  `xTaskNotifyFromISR` or queues; never call blocking APIs.
- Prefer `ESP_ERROR_CHECK` during bring-up; switch to explicit error handling for
  production error paths.
- Verify the power budget: WiFi bursts draw up to ~500 mA, so supply a stable 3.3 V.
- Keep `vTaskDelay` instead of `delay()` so other tasks and the WiFi stack keep running.
