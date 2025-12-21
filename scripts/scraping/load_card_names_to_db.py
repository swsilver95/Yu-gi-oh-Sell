#!/usr/bin/env python
"""
스크래핑한 카드명을 데이터베이스에 로드하는 스크립트
"""
import os
import django
import sys
from pathlib import Path

# 프로젝트 루트로 이동 (상위 2단계: scripts/scraping -> scripts -> project_root)
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
DAT_FILE = BASE_DIR / 'yugioh_card_names.dat'

# Django 설정 로드 (프로젝트 루트로 이동)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yugioh_site.settings')
django.setup()

from cards.models import CardName

def load_card_names_to_db():
    """카드명 .dat 파일을 읽어서 DB에 저장"""
    if not DAT_FILE.exists():
        print(f"오류: {DAT_FILE} 파일이 존재하지 않습니다.")
        print("먼저 scrape_yugioh_cards.py를 실행하여 카드명을 스크래핑하세요.")
        return
    
    print(f"카드명 파일 읽는 중: {DAT_FILE}")
    
    card_names = []
    with open(DAT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            card_name = line.strip()
            if card_name:
                card_names.append(card_name)
    
    print(f"총 {len(card_names)}개의 카드명 발견")
    print("데이터베이스에 저장 중...")
    
    # 기존 카드명 삭제 (선택사항)
    existing_count = CardName.objects.count()
    if existing_count > 0:
        print(f"기존 {existing_count}개의 카드명이 있습니다. 모두 삭제하고 새로 저장합니다.")
        CardName.objects.all().delete()
    
    # 배치로 저장 (성능 향상)
    batch_size = 100
    created_count = 0
    skipped_count = 0
    
    for i in range(0, len(card_names), batch_size):
        batch = card_names[i:i + batch_size]
        card_name_objects = []
        
        for card_name in batch:
            # 중복 체크
            if not CardName.objects.filter(name=card_name).exists():
                card_name_objects.append(CardName(name=card_name))
            else:
                skipped_count += 1
        
        if card_name_objects:
            CardName.objects.bulk_create(card_name_objects, ignore_conflicts=True)
            created_count += len(card_name_objects)
        
        if (i + batch_size) % 1000 == 0:
            print(f"진행 중... {min(i + batch_size, len(card_names))}/{len(card_names)}")
    
    print(f"\n=== 완료 ===")
    print(f"새로 생성: {created_count}개")
    print(f"건너뜀 (중복): {skipped_count}개")
    print(f"총 DB 카드명 수: {CardName.objects.count()}개")

if __name__ == '__main__':
    load_card_names_to_db()

