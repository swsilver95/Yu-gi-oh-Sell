#!/usr/bin/env python
"""
유희왕 카드 공식 DB 사이트에서 카드명을 스크래핑하는 스크립트
"""
import requests
from bs4 import BeautifulSoup
import time
import re
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / 'yugioh_card_names.dat'
# 스크립트가 scripts/scraping 폴더에 있으므로 경로는 그대로 유지

def scrape_card_names():
    """유희왕 카드 공식 DB에서 카드명 스크래핑"""
    base_url = "https://www.db.yugioh-card.com/yugiohdb/card_search.action"
    params = {
        'ope': '1',
        'sess': '1',  # sess=1: 한글, sess=2: 영어
        'rp': '100',  # 한 페이지당 100개
        'mode': '1',
        'stype': '1',
        'link_m': '2',
        'othercon': '2',
        'releaseYStart': '1999',
        'releaseMStart': '1',
        'releaseDStart': '1',
        'sort': '1',
    }
    
    all_card_names = []
    max_pages = 133  # 예상 최대 페이지 수
    
    print(f"유희왕 카드명 스크래핑 시작...")
    print(f"예상 페이지 수: {max_pages}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    for page in range(1, max_pages + 1):
        params['page'] = page
        print(f"페이지 {page}/{max_pages} 처리 중...", end=' ')
        
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # card_name 클래스를 가진 span 태그 찾기
            card_name_spans = soup.find_all('span', class_='card_name')
            
            if not card_name_spans:
                print(f"카드명을 찾을 수 없음. 페이지 {page}에서 중단.")
                break
            
            page_card_names = []
            for span in card_name_spans:
                card_name = span.get_text(strip=True)
                if card_name:
                    # HTML 엔티티 디코딩 (&quot; -> ")
                    from html import unescape
                    card_name = unescape(card_name)
                    # 따옴표 제거 및 정리
                    card_name = card_name.strip().strip('"').strip("'")
                    # 공백 정리
                    card_name = re.sub(r'\s+', ' ', card_name)
                    if card_name and len(card_name) > 0 and card_name not in page_card_names:
                        page_card_names.append(card_name)
            
            all_card_names.extend(page_card_names)
            print(f"✓ {len(page_card_names)}개 카드명 발견 (총 {len(all_card_names)}개)")
            
            # 서버 부하를 줄이기 위해 딜레이
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"✗ 오류 발생: {str(e)}")
            print(f"페이지 {page}에서 중단.")
            break
        except Exception as e:
            print(f"✗ 예상치 못한 오류: {str(e)}")
            continue
    
    # 중복 제거 및 정렬
    unique_card_names = sorted(list(set(all_card_names)))
    
    # .dat 파일로 저장
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for card_name in unique_card_names:
            f.write(f"{card_name}\n")
    
    print(f"\n=== 스크래핑 완료 ===")
    print(f"총 {len(unique_card_names)}개의 고유 카드명 발견")
    print(f"파일 저장 위치: {OUTPUT_FILE}")
    
    return unique_card_names

if __name__ == '__main__':
    scrape_card_names()

