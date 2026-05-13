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

The 11-step pipeline is split into 4 modules, orchestrated by `pipeline.py`:

```
Input → [Preprocessing] Grayscale → Gaussian Blur
     → [Detection] Canny → Contours → approxPolyDP (quadrilateral)
     → [Geometry] Corner ordering → Perspective Transform (homography)
     → [Enhancement] CLAHE → Adaptive Threshold → Morphology Close
     → Output
```

### Module responsibilities

| Module | Steps | Key functions |
|--------|-------|---------------|
| `modules/preprocessing.py` | 2-3 | `to_grayscale()`, `apply_gaussian_blur()` |
| `modules/detection.py` | 4-6 | `detect_edges()`, `find_contours()`, `find_document_contour()` |
| `modules/geometry.py` | 7-8 | `order_points()`, `calculate_output_size()`, `apply_perspective_transform()` |
| `modules/enhancement.py` | 9-10 | `apply_clahe()`, `apply_adaptive_threshold()`, `apply_morphology()`, `enhance()` |
| `utils/image_io.py` | — | `load_image()`, `save_image()`, `save_step()`, `show_comparison()` |

### Pipeline return value (`pipeline.py`)

`run_pipeline()` returns a dict: `{success: bool, output_path: str, processing_time: float}`. On document detection failure, falls back to enhancement-only and sets `success=False`.

### Corner ordering convention

TL (min x+y), BR (max x+y), TR (max x-y), BL (min x-y) — returned as `[TL, TR, BR, BL]` (shape 4×2).

### Default parameters (from `algorithm_design.md`)

| Param | Default | Range |
|-------|---------|-------|
| Gaussian kernel | (5,5) | (3,3)–(9,9) |
| Canny thresholds | 75 / 200 | 50–100 / 150–250 |
| approxPolyDP epsilon | 0.02 × arcLength | 0.01–0.05 |
| CLAHE clipLimit | 2.0 | 1.0–4.0 |
| CLAHE tileGridSize | (8,8) | (4,4)–(16,16) |
| Adaptive blockSize | 11 | 7–21 (odd) |
| Adaptive C | 2 | 1–5 |
| Morph kernel | (3,3) | (2,2)–(5,5) |

## Constraints

- **Strictly forbidden**: `torch`, `tensorflow`, `keras`, `sklearn`, or any ML/DL import.
- Every function must have a docstring naming the OpenCV function used.
- Single-image processing (1080p) must complete within 5 seconds.
- `findContours` uses `RETR_LIST` + `CHAIN_APPROX_SIMPLE`, sorted by area descending (top 5 only).
- Detection failure → return original with warning, do not crash.
- Intermediate step images use naming: `01_original.jpg`, `02_grayscale.jpg`, ..., `07_enhanced.jpg`.

## Project docs

- `requirements.md` — functional/non-functional requirements, test data specs
- `algorithm_design.md` — detailed per-step algorithm descriptions and error-handling strategy
- `coding_tasks.md` — implementation task breakdown (TASK-01 through TASK-10), currently all unchecked
