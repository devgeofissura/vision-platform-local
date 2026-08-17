---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: rtsp-camera-ingestion
description: Ingest video from RTSP/ONVIF IP cameras, USB webcams, and files with reconnection, frame queues, and bandwidth-aware capture
category: vision
version: 0.1.0
author: devtiagoabreu
tags: [rtsp, onvif, camera, video-stream, capture, opencv, iot, ip-camera]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.12 and OpenCV with FFmpeg backend
  - A reachable RTSP camera or test stream for experimentation
  - Basic knowledge of threads and async queues
provides:
  - RTSP/ONVIF discovery and connection patterns
  - Reconnection and health-monitoring logic
  - Frame capture pipeline with bounded queues
  - Bandwidth/encoding guidance for 1080p fleets
---

# RTSP Camera Ingestion

## Overview

The Vision Platform Camera Service consumes video from IP cameras over RTSP
(ONVIF for discovery/PTZ), USB webcams, and files. The reference deployment
targets Intelbras IP cameras (VIPC 1230 B G2), but no camera-specific code may
live in the Core — cameras are abstracted behind drivers (ADR-006). This skill
covers reliable capture: connecting, decoding, reconnecting, and feeding frames
into a bounded queue that the AI Engine consumes.

## Prerequisites

- OpenCV built with FFmpeg (`cv2.getBuildInformation()` shows FFmpeg)
- A test source: real camera, or a local stream like
  `ffmpeg -re -i test.mp4 -f rtsp -rtsp_transport tcp rtsp://localhost:8554/cam`
- `numpy` and `asyncio` for the capture loop

## Usage Instructions

### Step 1: Abstract the camera source

Never hardcode camera vendor logic in the Core. Define a driver interface:

```python
class CameraDriver:
    async def connect(self, config: dict): ...
    async def read_frame(self): ...
    async def close(self): ...
```

Implement one driver per source type (RTSP, USB, file). ONVIF is used for
discovery, credentials, and PTZ; frames still flow over RTSP.

### Step 2: Connect with RTSP transport control

```python
import cv2


def open_rtsp(url: str, timeout: int = 10):
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, timeout * 1000)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    if not cap.isOpened():
        raise ConnectionError(f"Could not open {url}")
    return cap
```

Force TCP transport for reliability (`rtsp://...` → add `?tcp` or set
`cv2.CAP_PROP_OPEN_TIMEOUT_MSEC` and FFmpeg flags) to avoid UDP packet loss.

### Step 3: Bounded frame queue with drop policy

Decoding is faster than inference, so the queue must be bounded and drop old
frames rather than grow memory:

```python
import asyncio

FRAME_QUEUE = asyncio.Queue(maxsize=2)


async def capture_loop(driver, queue: asyncio.Queue):
    while True:
        frame = await driver.read_frame()
        if frame is None:
            await asyncio.sleep(0.5)
            continue
        if queue.full():
            try:
                queue.get_nowait()  # drop oldest
            except asyncio.QueueEmpty:
                pass
        await queue.put(frame)
```

### Step 4: Reconnection and health status

Cameras go offline. Auto-reconnect with backoff and expose status:

```python
async def run_camera(camera_id: str, config: dict):
    backoff = 1
    while True:
        try:
            driver = make_driver(config["source_type"])
            await driver.connect(config)
            backoff = 1
            await set_status(camera_id, "connected")
            await capture_loop(driver, FRAME_QUEUE)
        except Exception:
            await set_status(camera_id, "disconnected")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
```

### Step 5: ONVIF discovery

Use ONVIF WS-Discovery to find cameras on the LAN:

```bash
pip install onvif-zeep
```

Then enumerate devices, verify credentials, and create a Camera row with
`status=connected` if the RTSP stream opens.

## Examples

### Example 1: Frame pipeline in the AI Engine

```python
while True:
    frame = await FRAME_QUEUE.get()
    detections = await run_module_pipeline(frame)   # plugin work, off-thread
    if detections:
        await event_bus.emit({"camera_id": cid, "detections": detections})
```

### Example 2: Health endpoint

```python
@app.get("/api/v1/cameras/{id}/status")
async def camera_status(id: str, tenant=Depends(require_tenant)):
    return ApiResponse(success=True, data={"status": await get_status(id)})
```

## References

- [OpenCV VideoCapture](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
- [ONVIF specification](https://www.onvif.org/)
- [python-onvif (onvif-zeep)](https://github.com/Falko-Goevert/onvif-zeep)
- [FFmpeg RTSP](https://trac.ffmpeg.org/wiki/StreamingGuide)

## Notes

- Camera vendors are abstracted behind drivers (ADR-006); no Intelbras code in Core.
- Use TCP for RTSP transport to avoid UDP packet loss on congested networks.
- Bounded queues (maxsize 2) prevent memory growth on slow inference.
- Always implement reconnect with exponential backoff and status monitoring.
- Bandwidth plan for 20 cams × 1080p @ 30fps; store evidence as JPEG + JSON.
