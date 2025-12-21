# 스크립트 폴더

이 폴더에는 프로젝트 운영 및 유지보수를 위한 스크립트들이 포함되어 있습니다.

## 폴더 구조

- `scraping/`: 유희왕 카드명 스크래핑 관련 스크립트
- `create_admin.sh`: Django 관리자 계정 생성
- `optimize_existing_images.py`: 기존 카드 이미지 최적화

## 사용 방법

### 관리자 계정 생성
```bash
./scripts/create_admin.sh
```

### 기존 이미지 최적화
```bash
cd /srv/dbweb
source venv/bin/activate
python scripts/optimize_existing_images.py
```

### 카드명 스크래핑
자세한 내용은 `scraping/README.md`를 참조하세요.

