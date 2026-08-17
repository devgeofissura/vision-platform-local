---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: onnx-object-detection
description: Run YOLO object-detection models on CPU with ONNX Runtime, including preprocessing, NMS, ByteTrack tracking, and confidence thresholds
category: vision
version: 0.1.0
author: devtiagoabreu
tags: [onnx, yolo, object-detection, inference, bytetrack, computer-vision, python]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.12 and OpenCV
  - onnxruntime and a YOLO model exported to ONNX
  - Basic understanding of image preprocessing and bounding boxes
provides:
  - YOLO ONNX export and quantization guidance
  - Preprocessing, inference, and NMS pipeline
  - ByteTrack multi-object tracking patterns
  - Confidence threshold and class-filtering rules
---

# ONNX Object Detection (YOLO)

## Overview

The Vision Platform AI Engine runs computer vision models as plugins. The
standard inference engine is **ONNX Runtime** (ADR-004) because it runs on
CPU-only servers (reference hardware is an i5 2nd gen with 4GB RAM). Models are
exported from Ultralytics YOLO (Nano for the EPI module) to ONNX. This skill
covers the full pipeline: export, preprocessing (letterboxing), inference,
non-max suppression (NMS), and object tracking with ByteTrack.

## Prerequisites

- Python 3.12+, `onnxruntime`, `opencv-python`, `numpy`
- A YOLO model (`.pt`) to export, or an existing `.onnx` model
- `ultralytics` package for export only (not required at runtime)

## Usage Instructions

### Step 1: Export YOLO to ONNX

```bash
pip install ultralytics onnxruntime
yolo export model=yolo11n.pt format=onnx opset=17 imgsz=640
```

Quantize for CPU speed (optional, with `onnxruntime`):

```python
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic("yolo11n.onnx", "yolo11n_int8.onnx", weight_type=QuantType.QInt8)
```

### Step 2: Letterbox preprocessing

Resize while preserving aspect ratio and pad to the model input size:

```python
import cv2
import numpy as np


def letterbox(img: np.ndarray, size: int = 640) -> np.ndarray:
    h, w = img.shape[:2]
    r = min(size / w, size / h)
    nw, nh = int(round(w * r)), int(round(h * r))
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
    canvas = np.full((size, size, 3), 114, dtype=np.uint8)
    x0, y0 = (size - nw) // 2, (size - nh) // 2
    canvas[y0:y0 + nh, x0:x0 + nw] = resized
    return canvas  # remember offsets (x0, y0) and ratio r to map back
```

### Step 3: Inference with ONNX Runtime

```python
import onnxruntime as ort


class Detector:
    def __init__(self, model_path: str):
        self.sess = ort.InferenceSession(
            model_path, providers=["CPUExecutionProvider"]
        )
        self.input_name = self.sess.get_inputs()[0].name

    def predict(self, blob: np.ndarray):
        inp = blob[None].astype(np.float32) / 255.0
        return self.sess.run(None, {self.input_name: inp})[0][0]
```

### Step 4: NMS and class filtering

Filter low-confidence boxes, apply NMS, then map back to original coordinates:

```python
def postprocess(raw, conf_threshold=0.45, nms_threshold=0.45, classes=None):
    boxes, scores, labels = [], [], []
    for pred in raw:
        conf = float(pred[4:].max())
        if conf < conf_threshold:
            continue
        label = int(pred[4:].argmax())
        if classes and label not in classes:
            continue
        cx, cy, w, h = pred[:4]
        boxes.append([cx - w / 2, cy - h / 2, w, h])
        scores.append(conf)
        labels.append(label)
    indices = cv2.dnn.NMSBoxes(boxes, scores, conf_threshold, nms_threshold)
    return [boxes[i] + [scores[i], labels[i]] for i in indices]
```

### Step 5: Track objects with ByteTrack

ByteTrack matches boxes across frames by score to keep stable object ids:

```python
from boxmot import BYTETracker  # pip install boxmot


tracker = BYTETracker()
tracks = tracker.update(boxes_xyxy, img_shape=(h, w))  # each track has .id
```

Use track ids for persistence (e.g., "person missing helmet for 10s").

### Step 6: Run inference off the request path

Never run the model inside a FastAPI route. The AI Engine consumes frames from
a queue, runs the plugin pipeline, and emits results to the Event Bus.

## Examples

### Example 1: End-to-end detection on a frame

```python
frame = cv2.imread("frame.jpg")
blob = letterbox(frame, 640)
raw = detector.predict(blob)
detections = postprocess(raw, conf_threshold=0.45, classes=[0])  # class 0 = person
```

### Example 2: EPI plugin rule (person without helmet)

```python
for track in tracks:
    if "helmet" not in labels_for(track.id) and track.time_since_update > 5:
        emit_event("EPI_MISSING", track_id=track.id, item="helmet")
```

## References

- [ONNX Runtime](https://onnxruntime.ai/)
- [Ultralytics YOLO](https://docs.ultralytics.com/)
- [ByteTrack](https://github.com/ifzhang/ByteTrack)
- [boxmot](https://github.com/mikel-brostrom/yolo_tracking)

## Notes

- ONNX Runtime is the standard engine (ADR-004); TensorRT is optional GPU-only.
- Prefer YOLO Nano for CPU-only deployments to keep latency usable.
- Always map boxes back to original coordinates using the letterbox offset/ratio.
- Track ids must be stable across frames before you trigger "missing PPE" rules.
- Evidence is stored as JPEG + JSON to save bandwidth on 1080p camera fleets.
