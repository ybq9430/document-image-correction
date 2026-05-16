# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Document image auto-correction system using **only classical CV/image-processing** (Python 3.x + OpenCV 4.x + NumPy + Matplotlib). No ML/DL libraries allowed (no torch, tensorflow, keras, sklearn).

## Commands

```bash
pip install -r document_correction/requirements.txt
python document_correction/main.py --input test_images/sample.jpg --output output/
python document_correction/main.py --input test_images/ --output output/ --batch
python document_correction/main.py --input test_images/sample.jpg --output output/ --save-steps
```

No linter, test framework, or other tooling is configured.

## Architecture

The pipeline is split into 4 modules, orchestrated by `pipeline.py`:

```
Input → [Preprocessing] Grayscale → Gaussian Blur
     → [Detection] Canny → Edge Dilation → Contours → approxPolyDP (multi-strategy)
     → [Geometry] Corner ordering → Perspective Transform (homography)
     → [Enhancement] Grayscale → CLAHE → Adaptive Threshold → Morphology Close
     → Output
```

### Module responsibilities

| Module | Key functions |
|--------|---------------|
| `modules/preprocessing.py` | `to_grayscale()`, `apply_gaussian_blur()` |
| `modules/detection.py` | `detect_edges()`, `dilate_edges()`, `find_contours()`, `find_document_contour()`, `draw_contour()` |
| `modules/geometry.py` | `order_points()`, `calculate_output_size()`, `apply_perspective_transform()` |
| `modules/enhancement.py` | `apply_clahe()`, `apply_adaptive_threshold()`, `apply_morphology()`, `enhance()` |
| `utils/image_io.py` | `load_image()`, `save_image()`, `save_step()`, `show_comparison()` |

### Document detection strategy (`find_document_contour`)

Three-tier fallback, evaluated per-contour (sorted by area desc, top 10):

1. **Direct polygon approximation** — `approxPolyDP` at epsilon ratios [0.02, 0.03, 0.05, 0.08, 0.10], check for 4 vertices.
2. **Convex hull + approximation** — if direct fails on a large contour, compute `convexHull` first, then approximate.
3. **Combined hull fallback** — if all individual contours fail, stack all contours together, compute a single convex hull, and approximate.

Quads covering less than 2% of image area are rejected. If no quad is found, the pipeline falls back to enhancement-only on the original image.

### Pipeline return value (`pipeline.py`)

`run_pipeline()` returns a dict: `{success: bool, output_path: str, processing_time: float}`. On document detection failure, falls back to enhancement-only and sets `success=False`.

### Corner ordering convention

TL (min x+y), BR (max x+y), TR (max x-y), BL (min x-y) — returned as `[TL, TR, BR, BL]` (shape 4×2).

### Enhancement pipeline (`enhance()`)

Internally converts the warped color image to grayscale, then applies CLAHE → adaptive threshold → morphological close → converts back to BGR for consistent I/O.

### Default parameters

| Param | Default | Range |
|-------|---------|-------|
| Gaussian kernel | (5,5) | (3,3)–(9,9) |
| Canny thresholds | 75 / 200 | 50–100 / 150–250 |
| Edge dilation kernel | (3,3), 2 iterations | — |
| approxPolyDP epsilon | 0.02–0.10 (auto-explored) | 0.01–0.10 |
| CLAHE clipLimit | 2.0 | 1.0–4.0 |
| CLAHE tileGridSize | (8,8) | (4,4)–(16,16) |
| Adaptive blockSize | 11 | 7–21 (odd) |
| Adaptive C | 2 | 1–5 |
| Morph kernel | (3,3) | (2,2)–(5,5) |

## Constraints

- **Strictly forbidden**: `torch`, `tensorflow`, `keras`, `sklearn`, or any ML/DL import.
- Every function must have a docstring naming the OpenCV function used.
- Single-image processing (1080p) must complete within 5 seconds.
- `findContours` uses `RETR_LIST` + `CHAIN_APPROX_SIMPLE`, sorted by area descending (top 10 only).
- Detection failure → return original with enhancement-only, do not crash.
- Intermediate step images saved per-image in `{name}_steps/` directory, named `01_original.jpg` through `07_enhanced.jpg`.

## Project docs

- `requirements.md` — functional/non-functional requirements, test data specs
- `algorithm_design.md` — detailed per-step algorithm descriptions and error-handling strategy
- `coding_tasks.md` — implementation task breakdown (TASK-01 through TASK-10), all completed
- `README.md` — project overview, install/run instructions, performance results
