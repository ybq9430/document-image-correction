# Algorithm Design

## 시스템 개요

- **입력**: 스마트폰으로 촬영된 문서 이미지 (JPG/PNG)
- **출력**: 기하학적 왜곡이 보정되고 텍스트 가독성이 향상된 문서 이미지
- **방법**: 전통적 Computer Vision + Image Processing 기법만 사용 (ML/DL 제외)

---

## 전체 파이프라인

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
│  Step 5. Contour Detection  │  cv2.findContours(...)
│  Step 6. Quad Approximation │  cv2.approxPolyDP(...)
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  MODULE 3: 기하학적 보정      │
│  Step 7. Corner Ordering    │  TL, TR, BR, BL 정렬
│  Step 8. Perspective Trans. │  cv2.getPerspectiveTransform()
│                             │  cv2.warpPerspective()
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  MODULE 4: 화질 향상          │
│  Step 9. CLAHE              │  cv2.createCLAHE(clipLimit=2.0)
│          Adaptive Threshold │  cv2.adaptiveThreshold(...)
│  Step 10. Morphology        │  cv2.morphologyEx(MORPH_CLOSE)
└─────────────────────────────┘
     │
     ▼
Output Corrected Image
```

---

## 단계별 알고리즘 상세

### Step 2: Grayscale Conversion
```
공식: Gray = 0.299*R + 0.587*G + 0.114*B
함수: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
입력: BGR 3채널 이미지
출력: 단일 채널 명암 영상
목적: 채널 수 감소로 계산량 절감, 후속 에지 검출 안정화
```

### Step 3: Gaussian Filtering
```
커널 크기: 5×5 (조정 가능)
시그마: 0 (자동 계산)
함수: cv2.GaussianBlur(gray, (5, 5), 0)
입력: Grayscale 이미지
출력: 평활화된 영상
목적: 고주파 노이즈 제거, Canny 검출 안정성 향상
```

### Step 4: Canny Edge Detection
```
lower_threshold: 75
upper_threshold: 200
내부 처리 순서:
  1. Gaussian Smoothing (내장)
  2. Gradient 계산 (Sobel 필터)
  3. Non-maximum Suppression
  4. Double Thresholding
  5. Hysteresis Edge Tracking
함수: cv2.Canny(blurred, 75, 200)
목적: 문서 외곽 경계 후보 검출
```

### Step 5: Contour Detection
```
함수: cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
정렬: contourArea 기준 내림차순 (상위 5개만 처리)
목적: 에지 영상에서 윤곽선 추출
```

### Step 6: Quadrilateral Approximation
```
epsilon: 0.02 × arcLength (contour 둘레의 2%)
함수: cv2.approxPolyDP(contour, epsilon, closed=True)
판단: len(approx) == 4 이면 문서 경계 후보
알고리즘: Douglas-Peucker polygon approximation
목적: 4꼭짓점 사각형 후보 검출
```

### Step 7: Corner Point Ordering
```
정렬 기준:
  - TL (top-left):     x+y 값이 가장 작은 점
  - BR (bottom-right): x+y 값이 가장 큰 점
  - TR (top-right):    x-y 값이 가장 큰 점
  - BL (bottom-left):  x-y 값이 가장 작은 점
목적: Homography 계산 전 꼭짓점 순서 보장
주의: 순서 오류 시 투시 변환 결과 뒤틀림 발생
```

### Step 8: Perspective Transformation
```
변환 행렬:
  [x']   [h11 h12 h13] [x]
  [y'] = [h21 h22 h23] [y]
  [w ]   [h31 h32 h33] [1]

실제 출력 좌표: (x'/w, y'/w)

출력 크기 계산:
  width  = max(dist(BL,BR), dist(TL,TR))
  height = max(dist(TR,BR), dist(TL,BL))

함수:
  M = cv2.getPerspectiveTransform(src_pts, dst_pts)
  warped = cv2.warpPerspective(img, M, (width, height))
목적: 사다리꼴 왜곡 → 정면 직사각형 보정
```

### Step 9: CLAHE + Adaptive Thresholding
```
CLAHE:
  clipLimit = 2.0
  tileGridSize = (8, 8)
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
  cl = clahe.apply(warped_gray)
  목적: 지역 대비 향상, 조명 불균일 완화

Adaptive Thresholding:
  method: ADAPTIVE_THRESH_GAUSSIAN_C
  type: THRESH_BINARY
  blockSize: 11
  C: 2
  함수: cv2.adaptiveThreshold(cl, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 11, 2)
  목적: 문자와 배경 분리, 조명 편차 보정
```

### Step 10: Morphological Processing
```
커널: 3×3 사각형 커널
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

연산 순서:
  1. MORPH_CLOSE: 작은 구멍 메우기 (문자 내부 공백 제거)
  2. MORPH_OPEN: 작은 잡음 제거 (선택적 적용)

함수: cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
목적: 문자 영역 정리, 가독성 향상
```

---

## 오류 처리 전략

| 상황 | 처리 방법 |
|------|----------|
| 문서 경계 미검출 | 원본 이미지 반환 + 경고 메시지 출력 |
| 꼭짓점 4개 미만 | 다음 후보 contour로 시도 |
| 모든 contour 실패 | 향상 처리만 적용 후 반환 |
| 이미지 파일 없음 | FileNotFoundError 발생 및 종료 |

---

## 파라미터 요약

| 파라미터 | 기본값 | 조정 범위 | 설명 |
|---------|--------|----------|------|
| Gaussian kernel | (5,5) | (3,3)~(9,9) | 노이즈 제거 강도 |
| Canny low | 75 | 50~100 | 약한 에지 임계값 |
| Canny high | 200 | 150~250 | 강한 에지 임계값 |
| approxPolyDP epsilon | 0.02 | 0.01~0.05 | 다각형 근사 정밀도 |
| CLAHE clipLimit | 2.0 | 1.0~4.0 | 대비 향상 강도 |
| CLAHE tileGridSize | (8,8) | (4,4)~(16,16) | 지역 처리 크기 |
| Adaptive blockSize | 11 | 7~21 (홀수) | 지역 이진화 블록 크기 |
| Adaptive C | 2 | 1~5 | 이진화 보정값 |
| Morph kernel | (3,3) | (2,2)~(5,5) | 형태학적 연산 크기 |
