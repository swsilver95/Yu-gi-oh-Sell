from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
import logging

logger = logging.getLogger(__name__)


class CardName(models.Model):
    """유희왕 카드명 데이터베이스 (자동완성용)"""
    name = models.CharField(max_length=200, unique=True, verbose_name='카드명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    class Meta:
        verbose_name = '카드명'
        verbose_name_plural = '카드명들'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name


class Card(models.Model):
    CONDITION_CHOICES = [
        ('S', 'S급'),
        ('A', 'A급'),
        ('B', 'B급'),
        ('C', 'C급'),
    ]
    
    RARITY_CHOICES = [
        ('N', '노멀(N)'),
        ('R', '레어(R)'),
        ('SR', '슈퍼 레어(SR)'),
        ('UR', '울트라 레어(UR)'),
        ('SE', '시크릿 레어(SE)'),
        ('UL', '얼티미트 레어(UL)'),
        ('HR', '홀로그래픽 레어(HR)'),
    ]
    
    SALE_STATUS_CHOICES = [
        ('available', '판매중'),
        ('reserved', '예약중'),
        ('sold', '판매완료'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='카드명')
    serial_number = models.CharField(max_length=50, verbose_name='카드 시리얼', blank=True, null=True)
    image = models.ImageField(upload_to='cards/', verbose_name='카드 이미지')
    image_optimized = models.ImageField(upload_to='cards/optimized/', verbose_name='최적화된 이미지', null=True, blank=True)
    condition = models.CharField(
        max_length=1, 
        choices=CONDITION_CHOICES, 
        verbose_name='상태'
    )
    rarity = models.CharField(
        max_length=2,
        choices=RARITY_CHOICES,
        default='N',
        verbose_name='레어리티'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        verbose_name='판매 가격'
    )
    sale_status = models.CharField(
        max_length=10,
        choices=SALE_STATUS_CHOICES,
        default='available',
        verbose_name='판매 상태'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        verbose_name = '카드'
        verbose_name_plural = '카드들'
        ordering = ['-created_at']
    
    
    def __str__(self):
        return f"{self.name} ({self.get_condition_display()}, {self.get_rarity_display()}) - {self.get_sale_status_display()}"
    
    def delete(self, *args, **kwargs):
        """카드 삭제 시 이미지 파일도 함께 삭제"""
        # 원본 이미지 삭제
        if self.image:
            image_path = self.image.path
            if os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                except OSError:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"이미지 파일 삭제 실패: {image_path}")
        
        # 최적화된 이미지 삭제
        if self.image_optimized:
            optimized_path = self.image_optimized.path
            if os.path.isfile(optimized_path):
                try:
                    os.remove(optimized_path)
                except OSError:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"최적화 이미지 파일 삭제 실패: {optimized_path}")
        
        # 부모 클래스의 delete 메서드 호출
        super().delete(*args, **kwargs)


@receiver(post_save, sender=Card)
def optimize_card_image(sender, instance, created, **kwargs):
    """카드 저장 후 이미지 최적화"""
    # 이미지가 있고 최적화된 이미지가 없는 경우에만 처리
    if instance.image and not instance.image_optimized:
        try:
            # 원본 이미지가 파일 시스템에 저장되어 있는지 확인
            if not os.path.exists(instance.image.path):
                logger.warning(f"이미지 파일이 존재하지 않음: {instance.image.path}")
                return
            
            # 원본 이미지 열기 (EXIF orientation 정보 완전히 무시)
            img = Image.open(instance.image.path)
            # EXIF orientation 정보를 완전히 무시하여 자동 회전 방지
            # Pillow는 기본적으로 EXIF orientation을 자동 적용하지 않지만,
            # 확실하게 하기 위해 EXIF 데이터에서 orientation 태그를 제거
            try:
                # EXIF 데이터가 있으면 orientation 태그 제거
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    exif = img._getexif()
                    # orientation 태그(274)가 있으면 제거
                    if 274 in exif:
                        # EXIF 데이터를 복사하고 orientation 제거
                        from PIL.ExifTags import ORIENTATION
                        # orientation 정보를 무시하고 이미지를 그대로 사용
                        pass
            except (AttributeError, KeyError, TypeError):
                # EXIF 데이터가 없거나 처리할 수 없는 경우 그대로 진행
                pass
            
            # RGB 모드로 변환 (RGBA, P 모드 등 처리)
            if img.mode in ('RGBA', 'LA', 'P'):
                # 투명도가 있는 경우 흰색 배경에 합성
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 이미지 최적화: 최대 너비 800px로 리사이즈 (비율 유지)
            max_width = 800
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # 최적화된 이미지를 메모리에 저장
            img_io = BytesIO()
            # JPEG 형식으로 저장 (품질 85%, EXIF 데이터 완전히 제거하여 회전 방지)
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
            # exif 파라미터로 빈 bytes 전달하여 EXIF 데이터 완전히 제거
            try:
                new_img.save(img_io, **save_kwargs, exif=b'')
            except (TypeError, ValueError):
                # exif 파라미터를 지원하지 않는 경우 그냥 저장
                # 새로 생성한 이미지는 EXIF 데이터가 없으므로 안전
                new_img.save(img_io, **save_kwargs)
            img_io.seek(0)
            
            # 파일명 생성 (원본 파일명 기반)
            original_name = os.path.splitext(os.path.basename(instance.image.name))[0]
            optimized_filename = f"{original_name}_optimized.jpg"
            
            # 최적화된 이미지 저장
            instance.image_optimized.save(
                optimized_filename,
                ContentFile(img_io.read()),
                save=True
            )
            
            logger.info(f"카드 {instance.id} ({instance.name}) 이미지 최적화 완료")
            
        except Exception as e:
            # 최적화 실패 시에도 원본 이미지는 유지
            logger.error(f"카드 {instance.id} ({instance.name}) 이미지 최적화 실패: {str(e)}", exc_info=True)
