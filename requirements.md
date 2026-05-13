# Requirements

## 기능 요구사항 (Functional Requirements)

### FR-01: 입력 처리
- 시스템은 JPG, PNG, BMP 형식의 문서 이미지를 입력으로 받아야 한다.
- 입력 이미지는 스마트폰으로 촬영된 문서를 대상으로 한다.
- 단일 이미지 및 디렉터리 일괄 처리를 모두 지원해야 한다.

### FR-02: 전처리
- 입력 RGB 이미지를 Grayscale로 변환해야 한다. (`cv2.cvtColor`)
- Gaussian Filter를 적용하여 고주파 노이즈를 제거해야 한다. (`cv2.GaussianBlur`)

### FR-03: 문서 영역 검출
- Canny Edge Detection으로 에지를 추출해야 한다. (`cv2.Canny`)
- 에지 영상에서 윤곽선을 추출해야 한다. (`cv2.findContours`)
- Douglas-Peucker 알고리즘으로 사각형 후보를 검출해야 한다. (`cv2.approxPolyDP`)
- 4개의 꼭짓점을 가진 윤곽선을 문서 경계 후보로 판단해야 한다.
- 문서 검출 실패 시 원본 이미지를 반환하고 경고 메시지를 출력해야 한다.

### FR-04: 기하학적 보정
- 검출된 4개 꼭짓점을 TL → TR → BR → BL 순서로 정렬해야 한다.
- Homography Matrix를 계산하여 투시 변환을 적용해야 한다. (`cv2.getPerspectiveTransform`, `cv2.warpPerspective`)
- 출력 이미지 크기는 검출된 문서 크기에 맞게 자동 계산해야 한다.

### FR-05: 화질 향상
- CLAHE를 적용하여 지역 대비를 향상시켜야 한다. (`cv2.createCLAHE`)
- Adaptive Thresholding으로 조명 불균일을 보정해야 한다. (`cv2.adaptiveThreshold`)
- Morphological Processing으로 잡음을 제거해야 한다. (`cv2.morphologyEx`)

### FR-06: 출력 및 결과 저장
- 최종 보정된 이미지를 지정 경로에 저장해야 한다. (`cv2.imwrite`)
- `--save-steps` 옵션 사용 시 각 단계별 중간 결과 이미지를 저장해야 한다.
- 저장 파일명은 `01_original`, `02_grayscale`, ..., `07_enhanced` 형식을 따른다.

---

## 비기능 요구사항 (Non-Functional Requirements)

### NFR-01: 기술 제약
- Machine Learning, Deep Learning, CNN, Neural Network 관련 라이브러리 사용 금지
- 허용 라이브러리: Python 3.x, OpenCV 4.x, NumPy, Matplotlib

### NFR-02: 성능
- 단일 이미지(1080p 기준) 처리 시간은 5초 이내여야 한다.
- 처리 시간은 측정하여 콘솔에 출력해야 한다.

### NFR-03: 코드 품질
- 각 처리 단계는 독립적인 함수로 구현해야 한다.
- 각 함수에는 docstring을 포함해야 한다.
- 모듈 단위로 파일을 분리해야 한다.

### NFR-04: 검증 지표
다음 지표를 측정하여 TR 고찰/분석에 활용한다:
- 문서 영역 검출 성공률 (성공한 이미지 수 / 전체 이미지 수 × 100%)
- 처리 시간 (초 단위)
- 처리 전후 이미지 PSNR / 대비 비교 (선택)
- 처리 전후 이미지 시각적 비교

---

## 테스트 데이터 요구사항

- 테스트 이미지: 스마트폰으로 촬영한 A4 문서 또는 책 페이지 3~5장
- 권장 촬영 조건:
  - 약간 기울어진 각도로 촬영 (15~45도)
  - 다양한 조명 조건 (밝음, 어두움, 조명 불균일)
  - 배경과 문서의 대비가 있는 환경
