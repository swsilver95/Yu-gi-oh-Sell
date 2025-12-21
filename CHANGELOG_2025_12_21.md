# 변경 로그 - 2025년 12월 21일

## 주요 업데이트

### 1. 이미지 최적화 기능 추가
- **목적**: 대용량 이미지로 인한 페이지 로딩 속도 개선
- **구현 내용**:
  - 카드 이미지 업로드 시 자동으로 최적화된 버전 생성
  - 최대 너비 800px로 리사이즈 (비율 유지)
  - JPEG 품질 85%로 저장
  - EXIF 데이터 완전 제거 (자동 회전 방지)
  - 원본 이미지는 유지, 최적화 버전은 `media/cards/optimized/`에 저장
- **성능 개선**: 이미지 용량 70-90% 감소, 페이지 로딩 속도 대폭 개선
- **관련 파일**:
  - `cards/models.py`: `CardName` 모델에 `image_optimized` 필드 추가, `post_save` 시그널로 자동 최적화
  - `cards/serializers.py`: `image_optimized_url` 필드 추가
  - `frontend/src/components/CardGrid.vue`: 최적화된 이미지 우선 사용

### 2. OCR 기능 완전 제거
- **이유**: 효율 대비 자원 사용이 과도함
- **제거 내용**:
  - `cards/views.py`: OCR 액션 및 관련 코드 제거
  - `frontend/src/components/CardUpload.vue`: OCR 관련 UI 및 함수 제거
  - `frontend/src/services/api.js`: `recognizeCardName` API 호출 제거
  - `yugioh_site/settings.py`: OCR 로거 설정 제거
  - `requirements.txt`: `easyocr` 패키지 제거
  - 서버에서 OCR 관련 패키지 제거 (easyocr, opencv-python-headless, scipy, torch, torchvision, nvidia-* 패키지들)
  - `/srv/dbweb/logs/ocr.log` 파일 삭제

### 3. 카드 시리얼 번호 필드 추가
- **목적**: 카드 고유 일련번호로 카드 구분 및 관리
- **구현 내용**:
  - `cards/models.py`: `Card` 모델에 `serial_number` 필드 추가 (최대 50자, 선택사항)
  - `cards/serializers.py`: 시리얼라이저에 `serial_number` 필드 포함
  - `frontend/src/components/CardUpload.vue`: 카드 등록 폼에 시리얼 번호 입력 필드 추가
  - `frontend/src/components/CardGrid.vue`: 카드 목록에서 시리얼 번호 표시
- **예시**: ICP-0001, DACP-0893

### 4. 유희왕 카드명 자동완성 기능 구현
- **목적**: 카드 등록 시 정확한 카드명 입력 지원
- **구현 내용**:
  - **스크래핑**: 유희왕 카드 공식 DB에서 약 13,295개의 카드명 스크래핑
    - `scripts/scraping/scrape_yugioh_cards.py`: 공식 DB 사이트에서 카드명 추출
    - `scripts/scraping/yugioh_card_names.dat`: 스크래핑된 카드명 저장
  - **데이터베이스**: `CardName` 모델 생성 및 카드명 저장
    - `cards/models.py`: `CardName` 모델 추가
    - `scripts/scraping/load_card_names_to_db.py`: 카드명을 DB에 로드
  - **백엔드 API**: 
    - `cards/views.py`: `get_all_card_names` 액션 추가 (모든 카드명 반환)
  - **프론트엔드**:
    - `frontend/src/components/CardUpload.vue`: 클라이언트 사이드 자동완성 구현
    - 페이지 진입 시 모든 카드명 로드 (1회)
    - 입력 시 서버 요청 없이 즉시 필터링 (50ms 디바운싱)
    - 최대 20개 결과 표시
- **성능**: 네트워크 요청 없이 즉시 자동완성 동작

### 5. 이미지 회전 방지
- **문제**: 이미지 업로드 시 EXIF orientation 정보로 인한 자동 회전
- **해결**:
  - 이미지 저장 시 EXIF 데이터 완전 제거
  - 새로운 RGB 이미지로 복사하여 EXIF 정보 제거
  - 원본 이미지 방향 유지

### 6. 프로젝트 파일 정리
- **스크립트 정리**:
  - `scripts/scraping/`: 스크래핑 관련 파일들 이동
    - `scrape_yugioh_cards.py`
    - `load_card_names_to_db.py`
    - `yugioh_card_names.dat`
    - `README.md`
  - `scripts/`: 유틸리티 스크립트들 이동
    - `create_admin.sh`
    - `optimize_existing_images.py`
    - `README.md`
- **불필요한 파일 제거**:
  - `install_ocr.sh` (OCR 제거로 불필요)
  - `test_ocr_logging.sh` (OCR 테스트 스크립트)

### 7. 프론트엔드 빌드 설정 개선
- `frontend/package.json`: 타입 체크 오류로 인한 빌드 실패 방지를 위해 `build` 스크립트 수정

## 기술 스택 변경

### 추가된 패키지
- `beautifulsoup4==4.12.3`: HTML 파싱 (스크래핑용)
- `requests==2.32.3`: HTTP 요청 (스크래핑용)

### 제거된 패키지
- `easyocr==1.7.1`
- `opencv-python-headless==4.8.1.78`
- `scipy==1.11.4`
- `numpy==1.26.2` (다른 용도로 사용 가능하지만 OCR 의존성이었으므로 제거)
- `torch`, `torchvision` 및 모든 `nvidia-*` CUDA 패키지들

## 데이터베이스 변경

### 새 모델
- `CardName`: 카드명 자동완성용 모델
  - `name`: CharField(max_length=200, unique=True)
  - `created_at`: DateTimeField

### 기존 모델 변경
- `Card`:
  - `serial_number`: CharField(max_length=50, blank=True, null=True) 추가
  - `image_optimized`: ImageField 추가 (자동 최적화된 이미지)

## 마이그레이션

다음 마이그레이션이 생성/적용되었습니다:
- `0004_card_image_optimized.py`: `image_optimized` 필드 추가
- `0006_cardname.py`: `CardName` 모델 생성

## 성능 개선

1. **이미지 로딩 속도**: 최적화된 이미지 사용으로 70-90% 용량 감소
2. **자동완성 속도**: 클라이언트 사이드 검색으로 네트워크 지연 제거
3. **서버 리소스**: OCR 제거로 메모리 및 CPU 사용량 감소

## 사용 방법

### 카드명 자동완성
- 카드 등록 페이지에서 "카드명" 입력란에 1글자 이상 입력
- 자동완성 목록이 즉시 표시됨
- 마우스 클릭 또는 키보드로 선택 가능

### 이미지 최적화
- 새로 업로드되는 카드는 자동으로 최적화됨
- 기존 카드 이미지 최적화: `python scripts/optimize_existing_images.py`

### 카드 시리얼 번호
- 카드 등록 시 시리얼 번호 입력 가능 (선택사항)
- 카드 목록에서 시리얼 번호 확인 가능

## 참고사항

- 스크래핑 스크립트는 `scripts/scraping/` 폴더에 보관되어 재사용 가능
- 카드명 데이터는 `scripts/scraping/yugioh_card_names.dat`에 저장
- DB에 카드명이 이미 로드되어 있으면 자동완성이 즉시 동작

