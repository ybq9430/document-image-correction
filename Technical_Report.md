# Technical Report (TR)

## 전통적 영상처리 기법 기반 문서 이미지 자동 교정 및 향상 시스템 설계

---

**과목명**: 고급컴퓨터비전 (2026학년도 1학기)

**프로젝트 주제**: 전통적 영상처리 기법 기반 문서 이미지 자동 교정 및 향상 시스템 설계

**제출일**: 2026년 5월

---

# 제1장. TR 개요

## 1.1 연구 배경 및 의의

최근 디지털 전환이 가속화됨에 따라 종이 문서를 디지털 형태로 변환하는 수요가 급격히 증가하고 있다. 기업, 정부 기관, 교육 기관 등에서는 대량의 문서를 효율적으로 관리하기 위해 문서 스캔 및 OCR(Optical Character Recognition) 기술을 적극적으로 활용하고 있다. 특히 스마트폰의 보급으로 인해 전용 스캐너 없이도 카메라를 이용한 문서 촬영이 일상화되었으나, 이러한 방식으로 획득된 문서 이미지에는 다양한 품질 문제가 발생한다.

스마트폰으로 문서를 촬영할 때 발생하는 주요 문제점은 다음과 같다. 첫째, 촬영 각도에 의한 투시 왜곡(perspective distortion)으로 문서가 사다리꼴 형태로 변형된다. 둘째, 실내 조명이나 자연광에 의한 불균일한 조명(uneven illumination)이 발생하여 문서의 일부 영역이 과도하게 밝거나 어두워진다. 셋째, 카메라 센서의 한계로 인한 노이즈(noise)가 이미지 품질을 저하시킨다. 넷째, 낮은 대비(contrast)로 인해 텍스트의 가독성이 떨어지는 문제가 있다.

이러한 문제를 해결하기 위해 딥러닝 기반 접근법이 연구되고 있으나, 높은 계산 비용과 대규모 학습 데이터의 필요성, 그리고 모델의 해석 불가능성 등의 한계가 존재한다. 반면, 전통적 영상처리 기법은 수학적 원리에 기반하여 결과의 해석이 용이하고, 계산 비용이 낮으며, GPU 없이도 실시간 처리가 가능하다는 장점을 갖는다. 따라서 본 프로젝트에서는 전통적 컴퓨터 비전 및 영상처리 기법만을 활용하여 문서 이미지의 자동 교정 및 향상 시스템을 설계하고 구현하였다.

## 1.2 연구 가설

본 프로젝트의 연구 가설은 다음과 같다: 문서 이미지에서 문서의 외곽 경계가 충분히 검출 가능한 경우, Canny 에지 검출, 윤곽선 근사, 투시 변환, CLAHE, 적응적 이진화와 같은 전통적 영상처리 기법만으로도 문서의 기하학적 왜곡을 효과적으로 보정하고 텍스트 가독성을 향상시킬 수 있다.

즉, 스마트폰 촬영 과정에서 기울어지거나 사다리꼴 형태의 원근 왜곡이 발생하더라도, 문서 외곽을 안정적으로 찾을 수 있다면 딥러닝 기반 모델 없이도 충분히 실용적인 수준의 문서 교정 결과를 얻을 수 있다는 가정이다. 또한 조명 불균일, 저대비, 미세 잡음과 같은 품질 저하 요소에 대해서도 CLAHE, Adaptive Thresholding, Morphological Processing의 조합이 가독성 향상에 유의미한 효과를 줄 것으로 예상한다.

## 1.3 연구 목표

본 프로젝트의 핵심 목표는 스마트폰으로 촬영된 문서 이미지를 입력으로 받아 기하학적 교정과 화질 향상을 자동으로 수행하는 완전한 처리 파이프라인을 구축하는 것이다. 구체적인 연구 목표는 다음과 같다.

- **자동 문서 영역 검출**: 복잡한 배경에서 문서 영역을 자동으로 식별하고 경계를 추출한다.
- **투시 기하 교정**: 검출된 문서의 네 꼭짓점을 기반으로 투시 변환을 적용하여 정면에서 촬영한 것과 같은 직사각형 형태로 교정한다.
- **이미지 품질 향상**: 적응적 이진화, 대비 향상, 형태학적 연산 등을 통해 문서의 가독성을 높인다.
- **완전한 처리 흐름 구축**: 딥러닝을 사용하지 않고 전통적 영상처리 기법만으로 입력부터 출력까지의 일관된 파이프라인을 구현한다.

## 1.4 개발 환경 및 제약 조건

| 항목 | 내용 |
|------|------|
| 프로그래밍 언어 | Python 3.x |
| 핵심 라이브러리 | OpenCV 4.13.0, NumPy 2.0.2, Matplotlib, scikit-image, pandas |
| 개발 환경 | Google Colab (CPU 런타임) |
| ML/DL 사용 | **금지** (torch, tensorflow, keras, sklearn 등 불가) |
| 허용 기법 | 전통적 Computer Vision + Image Processing만 사용 |

## 1.5 수행 방법 개요

본 시스템은 스마트폰으로 촬영된 문서 이미지를 입력으로 받아 교정 및 향상된 문서 이미지를 출력하는 파이프라인 구조로 설계되었다. 전체 처리 과정은 전처리(Preprocessing), 문서 검출(Detection), 기하 교정(Geometry Correction), 후처리(Enhancement)의 네 단계로 구성되며, 각 단계는 순차적으로 실행된다.

```
Input Image (RGB)
     │
     ▼
┌─────────────────────────────┐
│  MODULE 1: 전처리            │
│  Step 2. Grayscale 변환      │  cv2.cvtColor(img, COLOR_BGR2GRAY)
│  Step 3. Gaussian Filtering  │  cv2.GaussianBlur(gray, (5,5), 0)
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  MODULE 2: 문서 검출          │
│  Step 4. Canny Edge Det.    │  cv2.Canny(blurred, 75, 200)
│  Step 4b. Edge Dilation     │  cv2.dilate(edges, 3x3, 2iter)
│  Step 5. Contour Detection  │  cv2.findContours(RETR_LIST, ...)
│  Step 6. Quad Approximation │  cv2.approxPolyDP(epsilon=0.02~0.10)
│         + Convex Hull       │  cv2.convexHull()
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  MODULE 3: 기하학적 보정      │
│  Step 7. Corner Ordering    │  TL, TR, BR, BL 정렬 (x+y, x-y)
│  Step 8. Perspective Trans. │  cv2.getPerspectiveTransform()
│                             │  cv2.warpPerspective()
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  MODULE 4: 화질 향상          │
│  Step 9. CLAHE              │  cv2.createCLAHE(clipLimit=2.0)
│          Adaptive Threshold │  cv2.adaptiveThreshold(block=11, C=2)
│  Step 10. Morphology        │  cv2.morphologyEx(MORPH_CLOSE, 3x3)
└─────────────────────────────┘
     │
     ▼
Output Corrected Image
```

---

# 제2장. TR 내용

## 2.1 전체 알고리즘 구조

전체 알고리즘의 처리 파이프라인은 11단계로 구성된다: (1) Input Document Image → (2) Grayscale Conversion → (3) Gaussian Filtering → (4) Canny Edge Detection → (4b) Edge Dilation → (5) Contour Detection → (6) Quadrilateral Approximation + Convex Hull → (7) Corner Point Ordering → (8) Perspective Transformation → (9) CLAHE / Adaptive Thresholding → (10) Morphological Processing → (11) Output Corrected Image.

이 파이프라인은 기능별로 네 개의 모듈로 구분된다: ① 전처리(Preprocessing), ② 문서 검출(Detection), ③ 기하학적 보정(Geometry), ④ 화질 향상(Enhancement).

## 2.2 단계별 알고리즘 상세

### 2.2.1 이미지 전처리 (Step 2-3)

**Step 2: Grayscale Conversion**

입력 RGB 이미지를 Grayscale로 변환하여 채널 수를 3에서 1로 줄임으로써 후속 처리의 계산 효율성을 높인다.

- 공식: `Gray = 0.299 × R + 0.587 × G + 0.114 × B`
- 함수: `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
- 입력: BGR 3채널 이미지
- 출력: 단일 채널 명암 영상

**Step 3: Gaussian Filtering**

가우시안 필터를 적용하여 고주파 노이즈를 제거하고 영상을 평활화한다. 이는 후속 Canny 에지 검출의 안정성을 높이고 불필요한 잡음 에지 생성을 줄이는 효과가 있다.

- 커널 크기: 5×5
- 시그마: 0 (자동 계산)
- 함수: `cv2.GaussianBlur(gray, (5, 5), 0)`

### 2.2.2 문서 영역 검출 (Step 4-6)

**Step 4: Canny Edge Detection**

문서의 외곽 경계 후보를 추출하는 단계이다. Canny 알고리즘은 Gaussian smoothing → Gradient calculation (Sobel) → Non-maximum Suppression → Double Thresholding → Hysteresis Edge Tracking의 순서로 동작한다.

- 하한 임계값: 75
- 상한 임계값: 200
- 함수: `cv2.Canny(blurred, 75, 200)`

**Step 4b: Edge Dilation**

Canny 에지 검출 결과에서 발생하는 조각난 에지 세그먼트를 연결하기 위해 형태학적 팽창(dilation)을 적용한다. 3×3 사각형 커널로 2회 반복 팽창을 수행하여 끊어진 문서 경계를 연결한다.

- 커널: 3×3 MORPH_RECT
- 반복 횟수: 2
- 함수: `cv2.dilate(edges, kernel, iterations=2)`

**Step 5: Contour Detection**

팽창된 에지 맵에서 윤곽선(contour)을 추출한다. 면적 기준 내림차순으로 정렬하여 상위 10개의 후보만을 선택한다.

- 함수: `cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)`
- 정렬: `cv2.contourArea` 기준 내림차순, 상위 10개

**Step 6: Quadrilateral Approximation (3단계 전략)**

문서 경계를 검출하기 위해 다음과 같은 3단계 적응적 전략을 적용한다:

1. **직접 근사 (Direct Approximation)**: 각 contour에 대해 Douglas-Peucker 알고리즘(`cv2.approxPolyDP`)을 적용. epsilon 비율을 0.02, 0.03, 0.05, 0.08, 0.10 순으로 시도하여 4개의 꼭짓점을 가진 근사 다각형을 찾는다.

2. **Convex Hull 근사 (Hull Approximation)**: 개별 contour의 직접 근사가 실패할 경우, 해당 contour의 convex hull(`cv2.convexHull`)을 계산한 후 동일한 근사 과정을 적용한다. 이는 프레임 경계 근처에서 부분적으로 잘린 문서 에지에 효과적이다.

3. **결합 Convex Hull (Combined Hull Fallback)**: 모든 contour가 실패할 경우, 상위 contour들을 결합하여 하나의 큰 contour를 만들고 convex hull 근사를 수행한다. 이는 문서가 이미지 프레임을 대부분 채우는 경우에 특히 효과적이다.

최종적으로 검출된 사각형의 면적이 전체 이미지 면적의 2% 미만인 경우 노이즈로 판단하여 제외한다.

### 2.2.3 기하학적 보정 (Step 7-8)

**Step 7: Corner Point Ordering**

검출된 4개의 꼭짓점을 일관된 순서로 정렬한다. 점의 순서가 잘못되면 투시 변환 결과가 뒤틀리거나 반전될 수 있으므로, 이 단계는 Homography Matrix 계산 이전에 반드시 수행해야 한다.

정렬 기준:
- TL (Top-Left): x + y 값이 가장 작은 점
- TR (Top-Right): x - y 값이 가장 큰 점
- BR (Bottom-Right): x + y 값이 가장 큰 점
- BL (Bottom-Left): x - y 값이 가장 작은 점

결과: `[TL, TR, BR, BL]` 순서의 `(4, 2)` float32 ndarray

**Step 8: Perspective Transformation**

3×3 Homography Matrix H를 계산하여 투시 변환을 적용한다:

```
[x']   [h11 h12 h13] [x]
[y'] = [h21 h22 h23] [y]
[w ]   [h31 h32 h33] [1]

실제 출력 좌표: (x'/w, y'/w)
```

출력 이미지 크기는 검출된 문서의 실제 크기에 맞게 자동 계산된다:
- `width = max(dist(BL, BR), dist(TL, TR))`
- `height = max(dist(TR, BR), dist(TL, BL))`

- 함수: `cv2.getPerspectiveTransform(src_pts, dst_pts)`, `cv2.warpPerspective(img, M, (w, h))`

### 2.2.4 화질 향상 (Step 9-10)

**Step 9: CLAHE + Adaptive Thresholding**

CLAHE(Contrast Limited Adaptive Histogram Equalization)를 적용하여 지역 대비를 향상시킨다. CLAHE는 이미지를 타일(8×8)로 분할하고 각 타일에 대해 히스토그램 균등화를 수행하되, 대비 제한(clip limit=2.0)을 적용하여 노이즈 증폭을 억제한다. 이후 Adaptive Thresholding(Gaussian method, block size=11, C=2)을 적용하여 조명 불균일을 보정하고 전경 문자와 배경을 분리한다.

**Step 10: Morphological Processing**

형태학적 닫힘 연산(MORPH_CLOSE, 3×3 kernel)을 적용하여 문자 내부의 작은 구멍을 메우고 배경의 미세 잡음을 제거한다. 최종적으로 텍스트 영역이 정리되어 가독성이 향상된다.

## 2.3 실험 설계

### 2.3.1 실험 데이터

실험에는 스마트폰(Samsung Galaxy S24 Ultra)으로 직접 촬영한 6장의 문서 이미지를 사용하였다. 모든 이미지는 1280×1706 해상도이다. 촬영 조건은 다음과 같다:

- 약 15°~45° 기울어진 각도에서 촬영
- 실내 형광등 조명 환경
- 책상 위에 놓인 A4 문서
- 문서 유형: 텍스트 문서, 표가 포함된 문서, 필기 노트 등

### 2.3.2 평가 지표

시스템의 성능을 다각적으로 평가하기 위해 알고리즘 설계서에서 정의한 4대 검증 지표를 사용하였다:

| # | 지표 | 측정 방법 |
|---|------|----------|
| ① | 문서 영역 검출 성공률 | 성공한 이미지 수 / 전체 이미지 수 × 100% |
| ② | 처리 시간 | `time.time()` 측정 (초 단위, mean/min/max/total) |
| ③ | 대비 향상도 | PSNR(dB), Laplacian Variance(전/후/배율), SSIM(0~1) |
| ④ | 처리 전후 시각 비교 | 원본 / 투시 교정 / 최종 향상 3단 비교도 |

## 2.4 파라미터 설정

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| Gaussian kernel | (5, 5) | 노이즈 제거 강도 |
| Canny low threshold | 75 | 약한 에지 임계값 |
| Canny high threshold | 200 | 강한 에지 임계값 |
| approxPolyDP epsilon | 0.02~0.10 (자동 탐색) | 다각형 근사 정밀도 |
| CLAHE clipLimit | 2.0 | 대비 향상 강도 |
| CLAHE tileGridSize | (8, 8) | 지역 처리 크기 |
| Adaptive blockSize | 11 | 지역 이진화 블록 크기 |
| Adaptive C | 2 | 이진화 보정값 |
| Morph kernel | (3, 3) | 형태학적 연산 크기 |

---

# 제3장. TR 고찰 및 분석

## 3.1 실험 결과

### 3.1.1 문서 검출 성공률 및 처리 시간

6장의 테스트 이미지에 대한 처리 결과는 다음과 같다.

| 이미지명 | 문서 검출 | 처리 시간(s) | PSNR(dB) | Laplacian 전 | Laplacian 후 | Laplacian 배율 | SSIM |
|---------|---------|------------|----------|-------------|-------------|---------------|------|
| img01 | 성공 | 0.126 | 5.07 | 77.33 | 10,083.79 | 130.40x | 0.4516 |
| img02 | 성공 | 0.096 | 6.59 | 26.81 | 8,213.48 | 306.41x | 0.5938 |
| img03 | 성공 | 0.120 | 6.50 | 67.67 | 10,916.22 | 161.31x | 0.5213 |
| img04 | 성공 | 0.097 | 6.09 | 80.07 | 10,441.34 | 130.40x | 0.5173 |
| img05 | 성공 | 0.098 | 6.32 | 68.96 | 9,906.58 | 143.65x | 0.5411 |
| img06 | 성공 | 0.111 | 6.57 | 74.31 | 9,479.85 | 127.56x | 0.5375 |
| **평균** | **100%** | **0.108** | **6.19** | **65.86** | **9,840.21** | **166.62x** | **0.5271** |

### 3.1.2 결과 분석

**① 문서 영역 검출 성공률: 6/6 = 100.0%**

3단계 적응형 검출 전략(직접 근사 → Convex Hull → 결합 Hull)을 통해 모든 테스트 이미지에서 문서 영역을 성공적으로 검출하였다. 특히 문서가 프레임을 대부분 채우는 경우에도 결합 Convex Hull 전략이 효과적으로 작동하여 100% 검출률을 달성할 수 있었다.

**② 처리 시간: 평균 0.108초 (최소 0.096초, 최대 0.126초)**

Google Colab CPU 환경에서 단일 이미지(1280×1706) 처리에 평균 0.108초가 소요되었다. 이는 NFR-02에서 정의한 "단일 이미지 처리 시간 5초 이내" 요구사항을 크게 상회하는 결과로, 실시간 처리도 충분히 가능한 수준이다. 전체 6장 처리 시간은 약 0.648초에 불과하다.

**③ 대비 향상도**

- **Laplacian Variance**: 평균 65.86 → 9,840.21 (약 **166.62배** 향상)

  Laplacian 분산값은 이미지의 선명도(sharpness)를 나타내는 지표로, 값이 높을수록 더 선명한 이미지를 의미한다. 처리 전 평균 65.86에서 처리 후 평균 9,840.21로 약 166.62배 증가하여, 적응적 이진화와 CLAHE를 통한 화질 향상이 매우 효과적이었음을 확인할 수 있다.

  이미지별 Laplacian Ratio는 127.56x ~ 306.41x 범위로, 모든 이미지에서 100배 이상의 선명도 향상이 관찰되었다. img02의 경우 Laplacian Ratio가 306.41x로 가장 높았는데, 이는 원본 이미지의 조명이 어두워 초기 Laplacian 값이 26.81로 가장 낮았기 때문으로 분석된다. 처리 후에는 8,213.48로 다른 이미지들과 유사한 수준까지 향상되었다.

- **PSNR: 평균 6.19 dB**

  PSNR(Peak Signal-to-Noise Ratio) 값이 5.07~6.59 dB 범위로 상대적으로 낮게 나타났다. 이는 Adaptive Thresholding을 통한 이진화 과정에서 원본 grayscale 이미지가 흑백 이진 이미지로 변환되면서 픽셀 값의 큰 변화가 발생했기 때문이다. 일반적인 영상 압축에서 PSNR 30dB 이상을 "양호"로 평가하지만, 문서 이진화의 경우 원본과 결과의 픽셀 분포가 근본적으로 달라지므로 PSNR만으로 화질을 평가하는 것은 적절하지 않다. 오히려 SSIM과 Laplacian Ratio가 문서 교정 품질 평가에 더 적합한 지표이다.

- **SSIM: 평균 0.5271**

  SSIM(Structural Similarity Index)은 0.4516~0.5938 범위로, 이진화 처리의 특성상 원본 grayscale 이미지와 이진화된 결과 간의 구조적 차이를 반영한다. SSIM이 0.5 내외인 것은 원본의 그라데이션과 텍스처 정보가 이진화 과정에서 손실되었음을 의미하지만, 텍스트 가독성 측면에서는 오히려 향상되었다. 이는 SSIM이 "원본과의 유사성"을 측정하는 반면, 본 시스템의 목표는 "가독성 향상"이기 때문에 SSIM만으로 시스템의 효과를 판단할 수 없음을 시사한다.

**④ 처리 전후 시각 비교**

각 이미지에 대해 원본, 투시 교정, 최종 향상의 3단계 비교도를 생성하였다. 시각적 비교 결과, 모든 이미지에서 다음과 같은 개선이 확인되었다:

- 기울어진 문서가 정면 직사각형으로 교정됨
- 조명 불균일이 제거되고 균일한 배경으로 변환됨
- 텍스트와 배경의 대비가 크게 향상됨
- 문자 윤곽이 선명해지고 배경 잡음이 제거됨

## 3.2 파라미터 민감도 실험 결과

대표 이미지(img01)에 대해 4가지 주요 파라미터의 영향을 실험하였다.

### Experiment 1: Canny Low Threshold

| low | 검출 성공 | PSNR(dB) | SSIM | Laplacian Ratio |
|-----|---------|----------|------|----------------|
| 50  | O | 5.1 | 0.4516 | 130.4x |
| 75  | O | 5.1 | 0.4516 | 130.4x |
| 100 | O | 5.1 | 0.4543 | 127.5x |
| 125 | O | 5.1 | 0.4564 | 125.9x |

**분석**: Canny low threshold 변화가 최종 결과에 미치는 영향은 미미했다. 모든 값에서 검출에 성공했으며 PSNR, SSIM, Laplacian Ratio 모두 유사한 수준을 유지했다. 이는 Edge Dilation 단계가 Canny 파라미터의 작은 변화를 흡수하기 때문으로 해석된다.

### Experiment 2: Canny High Threshold

| high | 검출 성공 | PSNR(dB) | SSIM | Laplacian Ratio |
|------|---------|----------|------|----------------|
| 150  | O | 5.1 | 0.4516 | 130.4x |
| 200  | O | 5.1 | 0.4516 | 130.4x |
| 250  | O | 5.1 | 0.4516 | 130.4x |
| 300  | O | 4.9 | NaN | 0.0x |

**분석**: high=300에서 SSIM이 NaN으로 떨어지고 Laplacian Ratio가 0이 되었다. 이는 임계값이 너무 높아 에지가 거의 검출되지 않아 이진화 결과가 빈 이미지(모두 흰색 또는 검은색)가 되었기 때문이다. high=150~250 범위에서는 안정적인 결과를 보였다.

### Experiment 3: Gaussian Kernel Size

| kernel | 검출 성공 | PSNR(dB) | SSIM | Laplacian Ratio |
|--------|---------|----------|------|----------------|
| (3,3)  | O | 5.1 | 0.4511 | 130.8x |
| (5,5)  | O | 5.1 | 0.4516 | 130.4x |
| (7,7)  | O | 5.1 | 0.4511 | 130.8x |
| (9,9)  | O | 4.9 | 0.6399 | 2.7x |

**분석**: (3,3)~(7,7)까지는 안정적인 성능을 보였다. 그러나 (9,9)에서 SSIM이 갑자기 0.64로 증가하고 Laplacian Ratio가 2.7x로 급감했다. 이는 과도한 블러링으로 인해 문서 에지가 약화되어 검출된 문서 경계가 부정확해졌고, 결과적으로 원본과 유사한(SSIM은 높지만) 선명도가 낮은 결과가 출력되었기 때문이다. Gaussian kernel은 (5,5)가 최적이다.

### Experiment 4: CLAHE clipLimit

| clipLimit | 검출 성공 | PSNR(dB) | SSIM | Laplacian Ratio |
|-----------|---------|----------|------|----------------|
| 1.0 | O | 5.0 | 0.5016 | 94.4x |
| 2.0 | O | 5.1 | 0.4516 | 130.4x |
| 3.0 | O | 5.1 | 0.4177 | 156.7x |
| 4.0 | O | 5.1 | 0.3882 | 178.5x |
| 5.0 | O | 5.2 | 0.3656 | 195.9x |

**분석**: CLAHE clipLimit이 증가할수록 Laplacian Ratio가 94.4x → 195.9x로 지속적으로 증가했으나, SSIM은 반대로 0.5016 → 0.3656으로 감소했다. 이는 clipLimit이 높을수록 대비가 과도하게 증폭되어 노이즈까지 강조되기 때문이다. PSNR은 5.0~5.2 dB로 거의 변화가 없었다. 문서 가독성과 구조 보존 사이의 균형을 고려할 때 clipLimit=2.0이 가장 적절한 값으로 판단된다. 이 값에서 Laplacian Ratio 130.4x와 SSIM 0.4516의 균형 잡힌 결과를 얻을 수 있다.

### 종합 파라미터 권장값

| 파라미터 | 권장값 | 근거 |
|---------|--------|------|
| Canny low | 75 | 넓은 범위(50~125)에서 안정적 |
| Canny high | 200 | 150~250에서 안정적, 300에서 실패 |
| Gaussian kernel | (5,5) | (3,3)~(7,7)에서 안정적, (9,9)에서 성능 저하 |
| CLAHE clipLimit | 2.0 | 선명도(130.4x)와 구조 보존(0.4516) 간 최적 균형 |

## 3.3 가설 검증

본 연구의 가설은 "전통적 영상처리 기법만으로도 문서의 기하학적 왜곡을 효과적으로 보정하고 텍스트 가독성을 향상시킬 수 있다"는 것이었다. 실험 결과를 통해 다음과 같이 가설을 검증할 수 있다:

1. **문서 검출**: 3단계 적응형 검출 전략을 통해 100%의 문서 검출 성공률을 달성하여, 딥러닝 없이도 다양한 촬영 조건에서 문서 영역을 안정적으로 검출할 수 있음을 입증하였다.

2. **기하학적 보정**: 투시 변환을 통해 기울어진 문서를 정면 직사각형으로 성공적으로 교정하였다. Convex Hull 결합 전략을 통해 문서가 프레임을 대부분 채우는 경우에도 안정적인 보정이 가능했다.

3. **화질 향상**: Laplacian 분산값이 평균 166.62배 향상되어, CLAHE + Adaptive Thresholding + Morphological Processing의 조합이 텍스트 가독성 향상에 매우 효과적임을 정량적으로 확인하였다.

4. **처리 속도**: 평균 0.108초/image의 처리 속도로 실시간 응용에도 충분한 성능을 보였다.

따라서 본 연구의 가설은 실험 결과에 의해 지지된다고 결론 내릴 수 있다.

## 3.4 한계점 및 향후 연구

본 시스템의 한계점과 개선 방향은 다음과 같다:

1. **복잡한 배경에서의 검출**: 본 실험에 사용된 이미지는 상대적으로 단순한 배경(책상)에서 촬영되었다. 매우 복잡한 배경(패턴이 있는 바닥, 여러 물체가 있는 환경)에서는 문서 검출 성능이 저하될 수 있다. 이를 개선하기 위해 텍스처 기반 배경 제거 기법이나 적응형 ROI 탐색을 추가할 수 있다.

2. **PSNR의 낮은 값**: Adaptive Thresholding으로 인한 이진화는 PSNR 값을 낮추는 근본 원인이다. OCR 인식률과 같은 실제 활용 지표를 추가 평가 지표로 도입하는 것이 바람직하다.

3. **이진화 결과의 SSIM**: SSIM이 0.45~0.59 범위로 중간 수준에 머문 것은 이진화의 본질적 특성이다. 문서 유형에 따라 Grayscale 보존 모드와 이진화 모드를 선택적으로 적용하는 하이브리드 접근법을 고려할 수 있다.

4. **파라미터 자동 보정**: 현재 파라미터는 수동으로 설정되어 있다. 이미지 특성(조도, 대비, 해상도)에 따라 파라미터를 자동으로 조정하는 적응형 메커니즘을 추가하면 더 넓은 범위의 입력에 대응할 수 있을 것이다.

## 3.5 결론

본 프로젝트에서는 전통적 컴퓨터 비전 및 영상처리 기법만을 사용하여 스마트폰 촬영 문서 이미지의 자동 교정 및 향상 시스템을 성공적으로 설계하고 구현하였다. Canny 에지 검출, Convex Hull 기반 적응형 문서 검출, 투시 변환, CLAHE, 적응적 이진화, 형태학적 연산을 조합한 11단계 파이프라인을 구축하였다.

6장의 테스트 이미지에 대한 실험 결과, 100% 문서 검출 성공률, 평균 0.108초의 처리 속도, 평균 166.62배의 Laplacian 선명도 향상을 달성하였다. 파라미터 민감도 실험을 통해 최적의 파라미터 조합을 도출하였으며, 모든 평가 지표에서 안정적인 성능을 확인하였다.

본 연구는 딥러닝을 사용하지 않고도 전통적 영상처리 기법만으로 실용적인 문서 교정 시스템을 구축할 수 있음을 입증하였으며, 향후 OCR 연계, 모바일 최적화, 실시간 비디오 처리 등으로 확장할 수 있는 기반을 마련하였다.

---

**참고 문헌**

[1] J. Canny, "A Computational Approach to Edge Detection," IEEE TPAMI, vol. 8, no. 6, pp. 679-698, 1986.

[2] R. C. Gonzalez and R. E. Woods, Digital Image Processing, 4th ed., Pearson, 2018.

[3] G. Bradski and A. Kaehler, Learning OpenCV: Computer Vision with the OpenCV Library, O'Reilly Media, 2008.

[4] R. Hartley and A. Zisserman, Multiple View Geometry in Computer Vision, 2nd ed., Cambridge University Press, 2004.

[5] K. Zuiderveld, "Contrast Limited Adaptive Histogram Equalization," in Graphics Gems IV, Academic Press, pp. 474-485, 1994.

[6] D. H. Douglas and T. K. Peucker, "Algorithms for the Reduction of the Number of Points Required to Represent a Digitized Line," Cartographica, vol. 10, no. 2, pp. 112-122, 1973.

[7] S. Suzuki and K. Abe, "Topological Structural Analysis of Digitized Binary Images by Border Following," CVGIP, vol. 30, no. 1, pp. 32-46, 1985.

[8] J. Sauvola and M. Pietikäinen, "Adaptive Document Image Binarization," Pattern Recognition, vol. 33, no. 2, pp. 225-236, 2000.
