# 문서 이미지 자동 교정 및 향상 시스템
# Document Image Auto-Correction & Enhancement System

## 프로젝트 개요

스마트폰으로 촬영된 문서 이미지를 입력받아, 전통적 영상처리 기법만을 사용하여
기하학적 왜곡을 보정하고 텍스트 가독성을 향상시키는 Python + OpenCV 기반 시스템.

> ⚠️ **제약 조건**: Machine Learning / Deep Learning 사용 금지
> ✅ **허용**: 전통적 Computer Vision + Image Processing 기법만 사용

---

## 프로젝트 구조

```
document_correction/
├── main.py                  # 메인 실행 파일 (CLI)
├── pipeline.py              # 전체 파이프라인 관리
├── modules/
│   ├── preprocessing.py     # Step 2-3: Grayscale, Gaussian Filter
│   ├── detection.py         # Step 4-6: Canny, Contour, Approximation
│   ├── geometry.py          # Step 7-8: Corner Ordering, Perspective Transform
│   └── enhancement.py       # Step 9-10: CLAHE, Thresholding, Morphology
├── utils/
│   └── image_io.py          # 이미지 입출력 및 중간결과 저장
├── output/                  # 처리 결과 이미지 저장 디렉터리
├── test_images/             # 테스트용 문서 이미지
└── requirements.txt         # 의존성 패키지
```

---

## 알고리즘 파이프라인 (11단계)

```
Input Image
    ↓
[전처리] Grayscale Conversion → Gaussian Filtering
    ↓
[검출] Canny Edge Detection → Edge Dilation → Contour Detection → Convex Hull → Quadrilateral Approximation
    ↓
[보정] Corner Point Ordering → Perspective Transformation
    ↓
[향상] CLAHE / Adaptive Thresholding → Morphological Processing
    ↓
Output Corrected Image
```

### 문서 검출 전략

1. Canny Edge Detection (low=75, high=200)
2. Edge Dilation (3x3 kernel, 2 iterations) — 조각난 에지 연결
3. Contour 추출 (RETR_LIST, 면적 기준 상위 10개)
4. 각 Contour에 대해 Douglas-Peucker Polygon Approximation (epsilon = 0.02~0.10 × arcLength)
5. 개별 Contour 실패 시 Convex Hull 적용 후 재시도
6. 전체 Contour 결합 Convex Hull로 최종 시도 (문서가 프레임에 가까운 경우 대응)
7. 최종 4개 꼭짓점을 가진 사각형을 문서 경계로 판단

---

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r document_correction/requirements.txt
```

### 2. 단일 이미지 처리

```bash
cd document_correction
python main.py --input test_images/img01.jpg --output output/
```

### 3. 중간 결과 저장 (7단계 이미지)

```bash
python main.py --input test_images/img01.jpg --output output/ --save-steps
```

### 4. 디렉터리 일괄 처리

```bash
python main.py --input test_images/ --output output/ --batch
```

### 5. 일괄 처리 + 중간 결과 저장

```bash
python main.py --input test_images/ --output output/ --save-steps --batch
```

---

## 출력 결과

### 최종 출력

| 파일명 | 설명 |
|--------|------|
| `{name}_corrected.jpg` | 최종 교정 및 향상 결과 |

### --save-steps 옵션 사용 시 (각 이미지별 `{name}_steps/` 디렉터리)

| 파일명 | 설명 |
|--------|------|
| `01_original.jpg` | 원본 입력 이미지 |
| `02_grayscale.jpg` | Grayscale 변환 결과 |
| `03_blurred.jpg` | Gaussian Filter 적용 결과 |
| `04_edges.jpg` | Canny Edge Detection 결과 |
| `05_contours.jpg` | Contour 검출 결과 (문서 경계 표시) |
| `06_perspective.jpg` | Perspective Transform 결과 |
| `07_enhanced.jpg` | 최종 향상 결과 |

---

## 파라미터

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| Gaussian kernel | (5,5) | 노이즈 제거 강도 |
| Canny low | 75 | 약한 에지 임계값 |
| Canny high | 200 | 강한 에지 임계값 |
| approxPolyDP epsilon | 0.02~0.10 | 다각형 근사 정밀도 (자동 탐색) |
| CLAHE clipLimit | 2.0 | 대비 향상 강도 |
| CLAHE tileGridSize | (8,8) | 지역 처리 크기 |
| Adaptive blockSize | 11 | 지역 이진화 블록 크기 |
| Adaptive C | 2 | 이진화 보정값 |
| Morph kernel | (3,3) | 형태학적 연산 크기 |

---

## 처리 성능

- 단일 이미지(1280×1706) 처리 시간: 약 0.05~0.08초
- 6장 일괄 처리: 약 0.36초
- 테스트 이미지 6장 문서 검출 성공률: 100%

---

## 개발 환경

- Python 3.x
- OpenCV 4.x
- NumPy
- Matplotlib

---

## 오류 처리

| 상황 | 처리 방법 |
|------|----------|
| 문서 경계 미검출 | 이미지 향상만 적용 후 반환 (success=False) |
| 모든 contour 실패 | Convex Hull 결합 전략으로 대응 |
| 이미지 파일 없음 | FileNotFoundError 발생 |
| 문서가 프레임을 채우는 경우 | 전체 Contour Convex Hull로 경계 추정 |

---

## 과목 정보

- 과목명: 고급컴퓨터비전 (2026년 1학기)
- 프로젝트 단계: 3단계 내용 작성 (source code & data)
- 주제: 전통적 영상처리 기법 기반 문서 이미지 자동 교정 및 향상 시스템 설계
