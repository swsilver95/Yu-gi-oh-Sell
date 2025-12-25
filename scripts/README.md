# 스크립트 폴더

이 폴더에는 프로젝트 운영 및 유지보수를 위한 스크립트들이 포함되어 있습니다.

## 폴더 구조

- `scraping/`: 유희왕 카드명 스크래핑 관련 스크립트
- `create_admin.sh`: Django 관리자 계정 생성
- `optimize_existing_images.py`: 기존 카드 이미지 최적화
- `apply_subdomain.sh`: 서브도메인 설정 적용 (yugioh.silbuntu.mooo.com)
- `rollback_subdomain.sh`: 서브도메인 설정 롤백
- `apply_and_restart.sh`: 서브도메인 설정 적용 및 서비스 재시작

## 사용 방법

### 관리자 계정 생성
```bash
cd /srv/dbweb
sudo ./scripts/create_admin.sh
```

### 기존 이미지 최적화
```bash
cd /srv/dbweb
source venv/bin/activate
python scripts/optimize_existing_images.py
```

### 서브도메인 설정 적용
```bash
cd /srv/dbweb
sudo ./scripts/apply_subdomain.sh
```

### 서브도메인 설정 롤백
```bash
cd /srv/dbweb
sudo ./scripts/rollback_subdomain.sh
```

### 서브도메인 설정 적용 및 서비스 재시작
```bash
cd /srv/dbweb
sudo ./scripts/apply_and_restart.sh
```

### 카드명 스크래핑
자세한 내용은 `scraping/README.md`를 참조하세요.

