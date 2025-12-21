# Yu-gi-oh Sell

유희왕 카드 판매 사이트 - Django + Vue.js 기반 웹 애플리케이션

## 프로젝트 개요

이 프로젝트는 유희왕 카드를 판매하기 위한 웹사이트입니다. 관리자는 카드를 등록하고 관리할 수 있으며, 사용자는 등록된 카드를 조회할 수 있습니다.

## 주요 기능

### 카드 관리
- **카드 등록**: 관리자만 카드 등록 가능
  - 카드명 (자동완성 지원)
  - 카드 시리얼 번호
  - 카드 이미지 업로드 (최대 20MB)
  - 상태 (S급, A급, B급, C급)
  - 레어리티 (N, R, SR, UR, SE, UL, HR)
  - 판매 가격
- **카드 조회**: 모든 사용자 가능
  - 반응형 그리드 레이아웃 (모바일: 1개, 태블릿: 2-3개, 데스크톱: 4개)
  - 판매 상태 표시 (판매중, 예약중, 판매완료)
  - 이미지 최적화로 빠른 로딩
- **카드 관리**: 관리자 전용
  - 판매 상태 변경 (판매중 ↔ 예약중 ↔ 판매완료)
  - 카드 삭제 (이미지 파일 자동 삭제)

### 이미지 최적화
- 업로드 시 자동으로 최적화된 버전 생성
- 최대 너비 800px로 리사이즈
- JPEG 품질 85%로 저장
- EXIF 데이터 제거 (자동 회전 방지)
- 원본 이미지는 유지, 최적화 버전은 자동 사용

### 카드명 자동완성
- 유희왕 카드 공식 DB에서 약 13,000개 이상의 카드명 제공
- 클라이언트 사이드 검색으로 즉시 자동완성
- 부분 일치 검색 지원

## 기술 스택

### 백엔드
- **Django 6.0**: 웹 프레임워크
- **Django REST Framework**: REST API
- **PostgreSQL**: 데이터베이스
- **Pillow**: 이미지 처리
- **Gunicorn**: WSGI 서버
- **BeautifulSoup4**: HTML 파싱 (스크래핑용)
- **Requests**: HTTP 요청 (스크래핑용)

### 프론트엔드
- **Vue.js 3**: 프론트엔드 프레임워크
- **Vite**: 빌드 도구
- **Axios**: HTTP 클라이언트

### 인프라
- **Nginx**: 웹 서버 및 리버스 프록시
- **Systemd**: 서비스 관리

## 프로젝트 구조

```
/srv/dbweb/
├── cards/              # Django 앱 (카드 모델, 뷰, 시리얼라이저)
├── frontend/           # Vue.js 프론트엔드
│   ├── src/
│   │   ├── components/ # Vue 컴포넌트
│   │   └── services/   # API 서비스
│   └── dist/           # 빌드 결과물
├── scripts/            # 유틸리티 스크립트
│   ├── scraping/       # 카드명 스크래핑 관련
│   ├── create_admin.sh
│   └── optimize_existing_images.py
├── media/              # 업로드된 이미지
│   └── cards/          # 카드 이미지
│       └── optimized/  # 최적화된 이미지
├── staticfiles/        # Django 정적 파일
├── logs/               # 로그 파일
├── yugioh_site/        # Django 프로젝트 설정
├── manage.py           # Django 관리 스크립트
└── requirements.txt    # Python 패키지 목록
```

## 설치 및 설정

### 1. 환경 변수 설정
```bash
# /etc/dbweb/db.env 또는 .env 파일 생성
DB_NAME=yugioh_db
DB_USER=django
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DJANGO_SECRET_KEY=your_secret_key
DEBUG=False
```

### 2. Python 패키지 설치
```bash
cd /srv/dbweb
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

### 4. 관리자 계정 생성
```bash
./scripts/create_admin.sh
# 또는
python manage.py createsuperuser
```

### 5. 카드명 데이터 로드 (선택사항)
```bash
# 스크래핑 (처음 한 번만)
cd scripts/scraping
python scrape_yugioh_cards.py

# DB에 로드
cd /srv/dbweb
source venv/bin/activate
python scripts/scraping/load_card_names_to_db.py
```

### 6. 정적 파일 수집
```bash
python manage.py collectstatic --noinput
```

### 7. 프론트엔드 빌드
```bash
cd frontend
npm install
npm run build
```

## 배포

배포 관련 자세한 내용은 `DEPLOYMENT.md`를 참조하세요.

### 빠른 배포
```bash
./deploy_setup.sh
```

## 개발

### 로컬 개발 서버 실행

**Django (백엔드)**:
```bash
cd /srv/dbweb
source venv/bin/activate
python manage.py runserver
```

**Vue.js (프론트엔드)**:
```bash
cd frontend
npm run dev
```

프론트엔드는 `http://localhost:5173`에서 접속 가능합니다.

## 주요 스크립트

### 카드명 스크래핑
```bash
cd scripts/scraping
python scrape_yugioh_cards.py
```

### 기존 이미지 최적화
```bash
cd /srv/dbweb
source venv/bin/activate
python scripts/optimize_existing_images.py
```

### 관리자 계정 생성
```bash
./scripts/create_admin.sh
```

## 보안

보안 관련 자세한 내용은 `SECURITY.md`를 참조하세요.

주요 보안 기능:
- 입력 검증 (XSS 방지, 파일 업로드 검증)
- 세션/CSRF 쿠키 보안 설정
- HSTS, Referrer Policy
- 파일 업로드 크기 제한 (20MB)
- 이미지 파일 타입 및 내용 검증

## 변경 로그

최근 변경사항은 `CHANGELOG_2025_12_21.md`를 참조하세요.

## 라이선스

이 프로젝트는 개인 사용 목적으로 개발되었습니다.

## 문의

문제가 발생하거나 개선 사항이 있으면 이슈를 등록해주세요.
