# 유희왕 카드명 스크래핑 스크립트

이 폴더에는 유희왕 카드 공식 DB에서 카드명을 스크래핑하는 스크립트들이 포함되어 있습니다.

## 파일 설명

- `scrape_yugioh_cards.py`: 유희왕 카드 공식 DB 사이트에서 카드명을 스크래핑하여 `yugioh_card_names.dat` 파일로 저장
- `load_card_names_to_db.py`: 스크래핑한 카드명을 데이터베이스에 로드
- `yugioh_card_names.dat`: 스크래핑된 카드명 목록 (13,295개)

## 사용 방법

### 1. 카드명 스크래핑
```bash
cd /srv/dbweb/scripts/scraping
python scrape_yugioh_cards.py
```

### 2. DB에 로드
```bash
cd /srv/dbweb
source venv/bin/activate
python scripts/scraping/load_card_names_to_db.py
```

## 주의사항

- 스크래핑 시 서버 부하를 줄이기 위해 페이지당 1초 딜레이가 있습니다
- 전체 스크래핑에는 약 2-3분이 소요됩니다
- 스크래핑 결과는 `yugioh_card_names.dat` 파일에 저장됩니다

