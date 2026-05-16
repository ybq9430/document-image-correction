# 문서 이미지 자동 교정 및 향상 시스템
# Document Image Auto-Correction & Enhancement System

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)](https://opencv.org/)
[![No ML/DL](https://img.shields.io/badge/ML%2FDL-%EA%B8%88%EC%A7%80-red)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

스마트폰으로 촬영된 문서 이미지를 **전통적 영상처리 기법만으로** 자동 보정하는 Python + OpenCV 기반 파이프라인입니다.

> **제약 조건**: Machine Learning / Deep Learning 사용 금지  
> **허용 기법**: Classical Computer Vision + Image Processing

---

## 실험 결과 요약

| 지표 | 측정값 | 비고 |
|------|--------|------|
| 문서 검출 성공률 | **100%** (6/6) | 3단계 적응형 검출 전략 |
| 평균 처리 시간 | **0.119 s/image** | Google Colab CPU, 1280×1706 |
| Laplacian 선명도 향상 | **166.62×** | CLAHE + Adaptive Threshold |
| PSNR (Grayscale-level) | **14.64 dB** | 2계층 평가 — 주 지표 |
| SSIM (Grayscale-level) | **0.6271** | 2계층 평가 — 주 지표 |

> 자세한 결과는 [`Technical_Report.md`](Technical_Report.md) 및 [`연구보고서_문서이미지교정.docx`](연구보고서_문서이미지교정.docx) 참조

---

## 프로젝트 구조

```
document_correction/
├── main.py                                   # CLI 진입점 (단일/배치 처리)
├── pipeline.py                               # 11단계 파이프라인 오케스트레이션
├── modules/
│   ├── preprocessing.py                      # Gray 변환, Gaussian Filter
│   ├── detection.py                          # Canny, Contour, 3단계 Quad 검출
│   ├── geometry.py                           # Corner Ordering, Perspective Transform
│   └── enhancement.py                        # CLAHE, Adaptive Threshold, Morphology
├── utils/
│   └── image_io.py                           # 이미지 I/O 및 중간 결과 저장
├── build_report.py                           # 연구보고서 .docx 생성기
├── document_correction_colab .ipynb           # Colab 실행 노트북 (실행 완료)
├── output/                                   # 처리 결과 + 차트 이미지
├── test_images/                              # 테스트 입력 이미지 (6장)
└── requirements.txt                          # Python 의존성
```

---

## 알고리즘 파이프라인

```
Input (RGB) → Grayscale → Gaussian Blur → Canny Edge → Edge Dilation
    → Contour Detection → Quad Approximation (3-tier strategy)
    → Corner Ordering → Perspective Transform
    → CLAHE + Adaptive Threshold → Morphology Close → Output
```

### 3단계 문서 검출 전략

| Tier | Strategy | Fallback 조건 |
|------|----------|---------------|
| 1 | Direct approxPolyDP (ε=0.02~0.10) | 개별 contour 근사 |
| 2 | Convex Hull + approxPolyDP | Tier 1 실패 시 |
| 3 | Combined Contours → Convex Hull | 모든 개별 contour 실패 시 |

---

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 단일 이미지 처리

```bash
python main.py --input test_images/img01.jpg --output output/
```

### 3. 중간 결과 저장

```bash
python main.py --input test_images/img01.jpg --output output/ --save-steps
```

### 4. 일괄 처리

```bash
python main.py --input test_images/ --output output/ --batch --save-steps
```

### 5. 연구보고서 .docx 생성

```bash
python build_report.py
# → 연구보고서_문서이미지교정.docx
```

---

## 평가 지표 (5대 지표)

| # | 지표 | 측정 방법 |
|---|------|----------|
| ① | 문서 검출 성공률 | 성공 수 / 전체 × 100% |
| ② | 처리 시간 | `time.perf_counter()` (mean/min/max/total) |
| ③ | 대비 향상도 (Grayscale) | PSNR-Gray(dB), SSIM-Gray — CLAHE vs 원본 Gray |
| ④ | 대비 향상도 (Binary, 참고용) | PSNR-Binary(dB), SSIM-Binary — 이진화 vs 원본 Color |
| ⑤ | 선명도 향상도 | Laplacian Variance (전/후/배율) |

> **2계층 평가의 의의**: 이진화(grayscale→binary)는 픽셀 도메인을 근본적으로 변화시키므로, 이진화 이전 CLAHE 단계에서 Grayscale-level PSNR/SSIM을 주 지표로 사용합니다. Binary-level은 참고용입니다.

---

## 파라미터

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| Gaussian kernel | (5, 5) | 노이즈 제거 |
| Canny low / high | 75 / 200 | 에지 검출 임계값 |
| Edge dilation | (3,3), 2 iter | 에지 연결 |
| approxPolyDP ε | 0.02~0.10 (auto) | 다각형 근사 정밀도 |
| CLAHE clipLimit | 2.0 | 대비 향상 강도 |
| CLAHE tileGridSize | (8, 8) | 지역 처리 크기 |
| Adaptive blockSize | 11 | 지역 이진화 블록 |
| Adaptive C | 2 | 이진화 보정값 |
| Morph kernel | (3, 3) | 형태학적 연산 |

---

## 출력 파일

### 최종 결과

| 파일 | 설명 |
|------|------|
| `{name}_corrected.jpg` | 최종 교정 + 향상 이미지 |

### `--save-steps` 옵션 (이미지별 `{name}_steps/`)

| 파일 | 단계 |
|------|------|
| `01_original.jpg` | 원본 입력 |
| `02_grayscale.jpg` | Grayscale 변환 |
| `03_blurred.jpg` | Gaussian Filter |
| `04_edges.jpg` | Canny Edge Detection |
| `05_contours.jpg` | Contour + 문서 경계 |
| `06_perspective.jpg` | Perspective Transform |
| `07_enhanced.jpg` | 최종 향상 |

### 분석 차트 (`output/*.png`)

| 파일 | 내용 |
|------|------|
| `_comparison.png` | 6장 원본/교정/향상 비교 그리드 |
| `stage_timing.png` | 단계별 처리 시간 누적 막대 |
| `detection_strategy.png` | 검출 전략 분포 파이차트 |
| `clahe_histogram.png` | CLAHE 전후 히스토그램 |
| `sensitivity_heatmap.png` | 파라미터 민감도 히트맵 |
| `canny_dilation.png` | Canny + Dilation 효과 |
| `_flowchart.png` | 파이프라인 흐름도 |

---

## 문서

| 문서 | 형식 | 설명 |
|------|------|------|
| [`Technical_Report.md`](Technical_Report.md) | Markdown | 기술 보고서 (TR) — 한글, 알고리즘 상세 + 실험 결과 |
| `연구보고서_문서이미지교정.docx` | Word | 최종 연구보고서 — 삼선표, 수식 번호, 차트 삽입 |
| `document_correction_colab .ipynb` | Jupyter | Colab 실행 노트북 (B1-B6 차트 셀 포함) |

---

## 개발 환경

| 항목 | 내용 |
|------|------|
| 언어 | Python 3.x |
| 라이브러리 | OpenCV 4.13.0, NumPy 2.0.2, Matplotlib, scikit-image, pandas |
| 실행 환경 | Google Colab (CPU Runtime) |
| ML/DL | **사용 금지** |

---

## 과목 정보

- **과목명**: 고급컴퓨터비전 (Advanced Computer Vision, 2026-1)
- **프로젝트**: 기말 대체 Project — 전통적 영상처리 기반 문서 교정
- **참고문헌**: Canny (1986), Gonzalez & Woods (2018), Hartley & Zisserman (2004) 등
