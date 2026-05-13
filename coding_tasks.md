# Coding Tasks

## 프로젝트 목표
전통적 영상처리 기법만을 사용하여 스마트폰 촬영 문서 이미지를 자동으로 교정하고 향상시키는 Python + OpenCV 시스템 구현.

> ML/DL/CNN 관련 코드 절대 사용 금지 (torch, tensorflow, keras, sklearn 등 import 금지)

---

## Task 목록

### TASK-01: 프로젝트 기본 구조 생성
우선순위: 높음

다음 디렉터리 및 파일 구조를 생성하라:
```
document_correction/
├── main.py
├── pipeline.py
├── modules/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── detection.py
│   ├── geometry.py
│   └── enhancement.py
├── utils/
│   ├── __init__.py
│   └── image_io.py
├── output/
├── test_images/
└── requirements.txt
```

requirements.txt:
```
opencv-python>=4.5.0
numpy>=1.21.0
matplotlib>=3.4.0
```

---

### TASK-02: utils/image_io.py 구현

구현 함수:
- load_image(path) : BGR ndarray 로드, 파일 없으면 FileNotFoundError
- save_image(img, path) : 이미지 저장
- save_step(img, output_dir, step_num, step_name) : "01_original.jpg" 형식으로 저장
- show_comparison(original, result, title) : matplotlib으로 나란히 시각화

---

### TASK-03: modules/preprocessing.py 구현

구현 함수:
- to_grayscale(img)
  공식: Gray = 0.299R + 0.587G + 0.114B
  사용: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

- apply_gaussian_blur(gray, kernel_size=(5,5), sigma=0)
  사용: cv2.GaussianBlur(gray, kernel_size, sigma)

---

### TASK-04: modules/detection.py 구현

구현 함수:
- detect_edges(blurred, low=75, high=200)
  사용: cv2.Canny(blurred, low, high)

- find_contours(edges)
  사용: cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  정렬: contourArea 기준 내림차순, 상위 5개 반환

- find_document_contour(contours)
  epsilon = 0.02 * cv2.arcLength(contour, True)
  사용: cv2.approxPolyDP(contour, epsilon, True)
  꼭짓점 4개이면 반환, 없으면 None 반환

- draw_contour(img, contour)
  초록색으로 문서 경계 시각화

---

### TASK-05: modules/geometry.py 구현

구현 함수:
- order_points(pts)
  TL: x+y 최소 / BR: x+y 최대 / TR: x-y 최대 / BL: x-y 최소
  반환: [TL, TR, BR, BL] 순서의 shape=(4,2) ndarray

- calculate_output_size(ordered_pts)
  width  = max(dist(BL,BR), dist(TL,TR))
  height = max(dist(TR,BR), dist(TL,BL))
  반환: (width, height)

- apply_perspective_transform(img, ordered_pts)
  사용: cv2.getPerspectiveTransform(src_pts, dst_pts)
       cv2.warpPerspective(img, M, (width, height))

---

### TASK-06: modules/enhancement.py 구현

구현 함수:
- apply_clahe(img_gray, clip_limit=2.0, tile_size=(8,8))
  사용: cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)

- apply_adaptive_threshold(img_gray, block_size=11, C=2)
  사용: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)

- apply_morphology(img_binary, kernel_size=(3,3))
  사용: cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

- enhance(warped)
  순서: CLAHE -> Adaptive Threshold -> Morphology

---

### TASK-07: pipeline.py 구현

run_pipeline(input_path, output_dir, save_steps=False) 함수 구현.

처리 순서 (save_steps=True 시 각 단계 이미지 저장):
1. load_image                -> 01_original.jpg
2. to_grayscale              -> 02_grayscale.jpg
3. apply_gaussian_blur       -> 03_blurred.jpg
4. detect_edges              -> 04_edges.jpg
5. find_contours + draw      -> 05_contours.jpg
6. find_document_contour
7. order_points + perspective_transform -> 06_perspective.jpg
8. enhance                   -> 07_enhanced.jpg
9. save_image (최종 결과)

반환값 (dict):
- success: bool
- output_path: str
- processing_time: float (time.time() 사용, 초 단위)

오류 처리:
- 문서 경계 미검출 시: enhance만 적용, success=False 반환

---

### TASK-08: main.py 구현

argparse 인수:
- --input  : 입력 이미지 경로 또는 디렉터리 (필수)
- --output : 출력 디렉터리 (기본값: ./output)
- --save-steps : 중간 단계 이미지 저장 플래그
- --batch  : 디렉터리 일괄 처리 플래그

콘솔 출력 형식:
```
[INFO] Processing: sample.jpg
[INFO] Document detected: True
[INFO] Processing time: 1.23s
[INFO] Saved: output/sample_corrected.jpg
```

---

### TASK-09: 테스트 및 결과 기록

검증 항목:
1. 3~5장의 테스트 이미지로 파이프라인 실행
2. --save-steps 옵션으로 7개 중간 결과 이미지 생성 확인
3. 문서 검출 성공률 계산 및 기록
4. 각 이미지의 처리 시간 기록

결과 기록 형식 (TR 고찰/분석에 사용):
```
| 이미지명    | 검출 성공 | 처리 시간(s) | 비고            |
|-----------|---------|------------|----------------|
| img01.jpg | O       | 1.2        | 정상 처리        |
| img02.jpg | O       | 0.9        | 정상 처리        |
| img03.jpg | X       | 0.4        | 배경 대비 부족   |
```

---

### TASK-10: 파라미터 튜닝 (선택)

- Canny threshold 조정으로 검출 실패 케이스 개선 시도
- CLAHE clipLimit 조정으로 향상 효과 비교
- 결과를 TR 고찰/분석 섹션에 기록

---

## 구현 완료 체크리스트

- [x] TASK-01: 프로젝트 구조 생성
- [x] TASK-02: image_io.py
- [x] TASK-03: preprocessing.py
- [x] TASK-04: detection.py
- [x] TASK-05: geometry.py
- [x] TASK-06: enhancement.py
- [x] TASK-07: pipeline.py
- [x] TASK-08: main.py
- [x] TASK-09: 테스트 및 결과 기록
- [x] TASK-10: 파라미터 튜닝 (선택)

---

## 테스트 결과

| 이미지명 | 검출 성공 | 처리 시간(s) | 비고 |
|-----------|---------|------------|----------------|
| img01.jpg | O | 0.07 | 정상 처리 |
| img02.jpg | O | 0.06 | 정상 처리 |
| img03.jpg | O | 0.06 | 정상 처리 |
| img04.jpg | O | 0.06 | 정상 처리 |
| img05.jpg | O | 0.06 | 정상 처리 |
| img06.jpg | O | 0.05 | 정상 처리 |

- **검출 성공률**: 6/6 (100%)
- **총 처리 시간**: 0.36초
- **이미지 해상도**: 1280×1706
- **검출 전략**: Convex Hull 결합 방식으로 안정적 문서 경계 검출

---

## AI에게 코드 생성 요청 시 참고사항

- algorithm_design.md 의 파라미터 기본값을 반드시 준수할 것
- 각 함수의 docstring에 사용 OpenCV 함수명 명시할 것
- ML/DL 관련 import 절대 포함하지 말 것
- 오류 처리 전략은 requirements.md 의 오류 처리 섹션을 따를 것
