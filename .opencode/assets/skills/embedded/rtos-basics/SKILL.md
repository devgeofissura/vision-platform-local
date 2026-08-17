---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: rtos-basics
description: Learn real-time operating system fundamentals with tasks, scheduling, and semaphores
category: embedded
version: 0.1.0
author: devtiagoabreu
tags: [rtos, freeRTOS, zephyr, scheduling, semaphore, mutex, queue, realtime]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - C programming fundamentals
  - Understanding of threading and concurrency concepts
  - Access to an RTOS demo project (FreeRTOS or Zephyr)
provides:
  - Task creation and lifecycle management patterns
  - Priority-based and preemptive scheduling guidance
  - Semaphore, mutex, and queue synchronization examples
  - Real-time constraints analysis (deadlines, priority inversion)
---

# Real-Time Operating System Basics

## Overview

A Real-Time Operating System (RTOS) schedules tasks by priority and provides
synchronization primitives so a small microcontroller can reliably run many logical
programs at once. FreeRTOS and Zephyr are the most common choices, and both expose the
same core ideas: tasks with stack, priority and period; a scheduler that preempts lower
priority work; and semaphores, mutexes and queues for safe communication. Correct RTOS
programming is about respecting deadlines, keeping critical sections short, and never
blocking higher-priority work. This skill covers the primitives and the reasoning
needed to design deterministic firmware.

## Prerequisites

- A target platform with a runnable RTOS (e.g. ESP32 with ESP-IDF or a Zephyr board)
- Familiarity with pointers, structs, and function pointers in C
- A debugger or serial console for observing task behavior

## Usage Instructions

### Step 1: Create Tasks with Priorities and Stack

Each task is a function that never returns, with its own stack:

```c
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void blink_task(void *arg) {
    while (1) {
        gpio_toggle(LED_PIN);
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void app_main(void) {
    xTaskCreate(blink_task, "blink", 2048, NULL, 1, NULL);
    vTaskStartScheduler();   // never returns on most builds
}
```

Stack size must cover the deepest call chain of the task, including any library calls.

### Step 2: Understand the Scheduler

FreeRTOS uses fixed-priority preemptive scheduling: the highest-priority ready task
runs, and a task can preempt a lower-priority task at any point. `vTaskDelay` yields
for a fixed time; `taskYIELD()` or blocking on a primitive yields voluntarily:

```c
// Higher priority runs first; equal priorities are time-sliced.
xTaskCreate(high_task, "high", 2048, NULL, 5, NULL);   // prio 5
xTaskCreate(low_task,  "low",  2048, NULL, 1, NULL);   // prio 1
```

### Step 3: Use Semaphores for Signaling

A binary semaphore lets one task wake another without busy-waiting:

```c
#include "freertos/semphr.h"

SemaphoreHandle_t data_ready;

void producer_task(void *arg) {
    while (1) {
        read_sensor();
        xSemaphoreGive(data_ready);            // signal consumer
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void consumer_task(void *arg) {
    while (1) {
        if (xSemaphoreTake(data_ready, portMAX_DELAY) == pdTRUE) {
            process_sensor_data();             // runs after signal
        }
    }
}

void app_main(void) {
    data_ready = xSemaphoreCreateBinary();
    xTaskCreate(producer_task, "producer", 2048, NULL, 2, NULL);
    xTaskCreate(consumer_task, "consumer", 2048, NULL, 3, NULL);
}
```

### Step 4: Protect Shared Data with Mutexes

Use a mutex (with priority inheritance) for shared resources that tasks can hold for a
while, and always release it:

```c
SemaphoreHandle_t bus_mutex;

void write_sensor_bus(int value) {
    xSemaphoreTake(bus_mutex, portMAX_DELAY);
    spi_write(value);                     // critical section
    xSemaphoreGive(bus_mutex);
}
```

### Step 5: Pass Data Between Tasks with Queues

Queues are thread-safe FIFOs that copy data between tasks:

```c
#include "freertos/queue.h"

QueueHandle_t readings;
int sample;

xQueueSend(readings, &sample, pdMS_TO_TICKS(100));
if (xQueueReceive(readings, &sample, portMAX_DELAY) == pdTRUE) {
    handle(sample);
}
```

### Step 6: Reason About Real-Time Constraints

Each periodic task has a deadline; total CPU time plus worst-case blocking must stay
under the scheduler tick budget. Watch for priority inversion (a low-priority task
holding a resource a high-priority task needs) and resolve it with a mutex that
supports priority inheritance, or by bounding the critical section.

## Examples

### Example 1: Periodic Task with Absolute Timing

```c
TickType_t last = xTaskGetTickCount();
while (1) {
    vTaskDelayUntil(&last, pdMS_TO_TICKS(10));   // exact 10 ms period
    control_loop_step();
}
```

### Example 2: ISR to Task Notification

```c
static void IRAM_ATTR timer_isr(void *arg) {
    BaseType_t woken = pdFALSE;
    vTaskNotifyGiveFromISR(control_task, &woken);
    portYIELD_FROM_ISR(woken);
}
```

## References

- [FreeRTOS Documentation](https://www.freertos.org/)
- [FreeRTOS Task Documentation](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/00-Task-creation)
- [FreeRTOS Semaphore/Mutex API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Semaphores-and-mutexes/00-Semaphores-and-mutexes)
- [Zephyr RTOS Documentation](https://docs.zephyrproject.org/latest/kernel/index.html)
- [Wikipedia - Priority inversion](https://en.wikipedia.org/wiki/Priority_inversion)

## Notes

- Never block in a task with `while` busy loops; use `vTaskDelay`, queues, or
  notifications so the scheduler can run other tasks.
- Size stacks honestly; overflowing a task stack corrupts memory silently. Use stack
  high-water-mark checks in development.
- Prefer task notifications over binary semaphores for simple one-to-one signaling,
  as they are faster and need less RAM.
- ISRs communicate with tasks only via `FromISR` APIs; never take a blocking mutex in
  an ISR.
- Enable the trace recorder and monitor task runtimes to prove your timing analysis
  instead of trusting it.
