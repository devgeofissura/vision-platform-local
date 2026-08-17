---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: opencv-basics
description: OpenCV basics covering image processing, filters, contours, and drawing
category: vision
version: 0.1.0
author: devtiagoabreu
tags: [opencv, computer-vision, image-processing, contours, filters, python]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.8 or newer
  - OpenCV installed (`pip install opencv-python`)
  - NumPy for array manipulation
  - An image file or webcam for experimentation
provides:
  - Core image I/O and color space conversion recipes
  - Filtering, thresholding, and edge detection workflows
  - Contour detection and analysis for object boundaries
  - Drawing and annotation helpers for visualization
---

# OpenCV Basics

## Overview

This skill covers the fundamentals of OpenCV for image processing in Python:
loading and converting images, applying filters, thresholding, finding
contours, and drawing results. OpenCV represents images as NumPy arrays, so the
same skills transfer to video frames and camera streams. The examples build a
common pipeline — load, preprocess, segment, analyze, visualize — that handles
most introductory computer vision tasks. No machine learning is required; these
are classic image processing techniques that remain the backbone of many
vision systems.

## Prerequisites

- Python 3.8+ with `pip`
- `opencv-python` and `numpy` installed
- OpenCV's GUI backend (works out of the box on desktop Linux/macOS/Windows)
- A sample image to experiment with (e.g., a photo with distinct objects)

## Usage Instructions

### Step 1: Install and Load an Image

```bash
python -m pip install opencv-python numpy matplotlib
```

```python
import cv2

# BGR is OpenCV's native order
img = cv2.imread("photo.jpg")
if img is None:
    raise SystemExit("Could not read image")

print(img.shape)          # (height, width, channels)
cv2.imshow("window", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Step 2: Convert Color Spaces

Work in grayscale or other spaces as needed:

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Isolate a hue range (e.g., red-ish colors) with HSV thresholds
mask = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
```

HSV makes color-based segmentation far more robust than raw RGB.

### Step 3: Apply Filters

Reduce noise before edge detection or thresholding:

```python
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)
```

`Canny`'s two thresholds: lower detects weak edges, higher confirms strong
ones. Start with (50, 150) and tune per image.

### Step 4: Threshold and Find Contours

Binarize, then extract object boundaries:

```python
_, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    area = cv2.contourArea(c)
    if area > 500:               # filter out noise
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
```

### Step 5: Analyze Contours

Measure shapes by their perimeter-to-area relationship:

```python
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 3:
        label = "triangle"
    elif len(approx) == 4:
        label = "rectangle"
    else:
        label = "circle" if area(c) / (peri * peri) > 0.12 else "polygon"
```

### Step 6: Draw and Annotate

Overlay results and persist output:

```python
cv2.drawContours(img, contours, -1, (255, 0, 0), 2)
cv2.putText(img, label, (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
cv2.imwrite("output.png", img)
```

## Examples

### Example 1: Complete Preprocessing Pipeline

```python
import cv2
import numpy as np

def clean_mask(path):
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))  # greens
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # remove speckles
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # fill holes
    return mask
```

### Example 2: Count Objects in an Image

```python
import cv2

img = cv2.imread("objects.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

count = sum(1 for c in contours if cv2.contourArea(c) > 500)
print(f"Detected {count} objects")
```

## References

- [OpenCV Documentation](https://docs.opencv.org/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Canny Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [Contour Detection Tutorial](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html)
- [OpenCV-Python on PyPI](https://pypi.org/project/opencv-python/)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)

## Notes

- OpenCV loads images in BGR, not RGB; convert before displaying with
  matplotlib (`cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`).
- `cv2.imread` returns `None` silently on missing files — always check.
- `cv2.waitKey(0)` keeps a window open; 30 shows frames for 30 ms (video).
- Morphological open/close are the fastest fixes for mask noise and holes.
- Use `RETR_EXTERNAL` for outer boundaries and `RETR_TREE` for hierarchies.
- Tune thresholds on a few representative images before trusting a pipeline.
