#!/usr/bin/env python
"""
기존 카드 이미지들을 최적화하는 스크립트
"""
import os
import django

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yugioh_site.settings')
django.setup()

from cards.models import Card
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

def optimize_existing_cards():
    """기존 카드들의 이미지를 최적화"""
    cards = Card.objects.filter(image_optimized__isnull=True).exclude(image='')
    total = cards.count()
    
    print(f"총 {total}개의 카드 이미지를 최적화합니다...")
    
    success_count = 0
    error_count = 0
    
    for idx, card in enumerate(cards, 1):
        try:
            if not card.image:
                print(f"[{idx}/{total}] {card.name}: 이미지가 없습니다. 건너뜁니다.")
                continue
            
            print(f"[{idx}/{total}] {card.name} 최적화 중...")
            
            # 원본 이미지 열기 (EXIF orientation 정보 완전히 무시)
            img = Image.open(card.image.path)
            # EXIF orientation 정보를 완전히 무시하여 자동 회전 방지
            
            # RGB 모드로 변환
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 이미지 최적화: 최대 너비 800px로 리사이즈
            max_width = 800
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # 최적화된 이미지를 메모리에 저장
            img_io = BytesIO()
            # 새로운 이미지로 복사하여 EXIF 데이터를 완전히 제거
            # RGB 모드의 새 이미지 생성 (EXIF 데이터 없음)
            new_img = Image.new('RGB', img.size)
            new_img.paste(img, (0, 0))
            
            # EXIF 데이터 없이 저장
            save_kwargs = {
                'format': 'JPEG',
                'quality': 85,
                'optimize': True,
            }
            try:
                new_img.save(img_io, **save_kwargs, exif=b'')
            except (TypeError, ValueError):
                # exif 파라미터를 지원하지 않는 경우 그냥 저장
                # 새로 생성한 이미지는 EXIF 데이터가 없으므로 안전
                new_img.save(img_io, **save_kwargs)
            img_io.seek(0)
            
            # 파일명 생성
            original_name = os.path.splitext(os.path.basename(card.image.name))[0]
            optimized_filename = f"{original_name}_optimized.jpg"
            
            # 최적화된 이미지 저장
            card.image_optimized.save(
                optimized_filename,
                ContentFile(img_io.read()),
                save=True
            )
            
            success_count += 1
            print(f"  ✓ 완료: {card.image_optimized.name}")
            
        except Exception as e:
            error_count += 1
            print(f"  ✗ 오류: {str(e)}")
            logger.error(f"카드 {card.id} ({card.name}) 최적화 실패: {str(e)}")
    
    print(f"\n=== 완료 ===")
    print(f"성공: {success_count}개")
    print(f"실패: {error_count}개")
    print(f"총 처리: {total}개")

if __name__ == '__main__':
    optimize_existing_cards()

