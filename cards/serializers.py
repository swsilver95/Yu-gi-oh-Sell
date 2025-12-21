from rest_framework import serializers
from django.core.exceptions import ValidationError
from PIL import Image
import os
from .models import Card


class CardSerializer(serializers.ModelSerializer):
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)
    rarity_display = serializers.CharField(source='get_rarity_display', read_only=True)
    sale_status_display = serializers.CharField(source='get_sale_status_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    image_optimized_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Card
        fields = [
            'id', 'name', 'serial_number', 'image', 'image_url', 'image_optimized', 'image_optimized_url',
            'condition', 'condition_display', 'rarity', 'rarity_display',
            'price', 'sale_status', 'sale_status_display', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'image_optimized']
    
    def validate_name(self, value):
        """카드명 검증"""
        if not value or not value.strip():
            raise serializers.ValidationError("카드명을 입력해주세요.")
        if len(value) > 200:
            raise serializers.ValidationError("카드명은 200자 이하여야 합니다.")
        # XSS 방지를 위한 기본적인 검증
        if '<' in value or '>' in value:
            raise serializers.ValidationError("카드명에 허용되지 않은 문자가 포함되어 있습니다.")
        return value.strip()
    
    def validate_price(self, value):
        """가격 검증"""
        if value is None:
            raise serializers.ValidationError("가격을 입력해주세요.")
        if value < 0:
            raise serializers.ValidationError("가격은 0 이상이어야 합니다.")
        if value > 9999999999:
            raise serializers.ValidationError("가격이 너무 큽니다.")
        return value
    
    def validate_image(self, value):
        """이미지 파일 검증"""
        if not value:
            return value
        
        # 파일 크기 검증 (20MB 제한)
        max_size = 20 * 1024 * 1024  # 20MB
        if value.size > max_size:
            raise serializers.ValidationError("이미지 파일 크기는 20MB 이하여야 합니다.")
        
        # 파일 확장자 검증
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        file_ext = os.path.splitext(value.name)[1].lower()
        if file_ext not in allowed_extensions:
            raise serializers.ValidationError(f"허용된 이미지 형식: {', '.join(allowed_extensions)}")
        
        # 실제 이미지 파일인지 확인
        try:
            img = Image.open(value)
            img.verify()
            # 파일 포인터를 처음으로 되돌림
            value.seek(0)
        except Exception:
            raise serializers.ValidationError("유효한 이미지 파일이 아닙니다.")
        
        return value
    
    def get_image_url(self, obj):
        """원본 이미지 URL (관리자용)"""
        if obj.image:
            request = self.context.get('request')
            if request:
                host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST') or request.get_host()
                scheme = request.META.get('HTTP_X_FORWARDED_PROTO') or request.scheme
                base_url = f"{scheme}://{host}"
                image_path = obj.image.url
                if image_path.startswith('/'):
                    return f"{base_url}{image_path}"
                return f"{base_url}/{image_path}"
            return obj.image.url
        return None
    
    def get_image_optimized_url(self, obj):
        """최적화된 이미지 URL (프론트엔드에서 사용)"""
        # 최적화된 이미지가 있으면 우선 사용, 없으면 원본 사용
        image_to_use = obj.image_optimized if obj.image_optimized else obj.image
        
        if image_to_use:
            request = self.context.get('request')
            if request:
                host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST') or request.get_host()
                scheme = request.META.get('HTTP_X_FORWARDED_PROTO') or request.scheme
                base_url = f"{scheme}://{host}"
                image_path = image_to_use.url
                if image_path.startswith('/'):
                    return f"{base_url}{image_path}"
                return f"{base_url}/{image_path}"
            return image_to_use.url
        return None

