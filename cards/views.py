from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings
import logging
from .models import Card, CardName
from .serializers import CardSerializer

logger = logging.getLogger(__name__)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    
    def get_permissions(self):
        """
        카드 생성(등록), 수정, 삭제, 판매 상태 변경은 admin만 가능
        조회는 모두 가능
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'mark_as_sold', 'mark_as_available', 'mark_as_reserved', 'check_auth']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        """카드 생성 시 추가 검증"""
        # sale_status는 항상 'available'로 설정 (보안)
        serializer.save(sale_status='available')
    
    @action(detail=True, methods=['patch'])
    def mark_as_sold(self, request, pk=None):
        """판매 완료로 표시"""
        card = self.get_object()
        card.sale_status = 'sold'
        card.save()
        serializer = self.get_serializer(card)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def mark_as_available(self, request, pk=None):
        """판매중으로 표시"""
        card = self.get_object()
        card.sale_status = 'available'
        card.save()
        serializer = self.get_serializer(card)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def mark_as_reserved(self, request, pk=None):
        """예약중으로 표시"""
        card = self.get_object()
        card.sale_status = 'reserved'
        card.save()
        serializer = self.get_serializer(card)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_card_names(self, request):
        """카드명 자동완성 검색 (레거시 - 사용하지 않음)"""
        query = request.query_params.get('q', '').strip()
        
        if not query or len(query) < 1:
            return Response({'results': []})
        
        # 카드명 검색 (대소문자 구분 없음, 부분 일치)
        card_names = CardName.objects.filter(
            name__icontains=query
        ).order_by('name')[:20]  # 최대 20개만 반환
        
        results = [{'name': card.name} for card in card_names]
        
        return Response({
            'results': results,
            'count': len(results)
        })
    
    @action(detail=False, methods=['get'])
    def get_all_card_names(self, request):
        """모든 카드명 목록 반환 (프론트엔드에서 클라이언트 사이드 검색용)"""
        # 보안: 접근 제어 및 Rate limiting
        client_ip = self._get_client_ip(request)
        referer = request.META.get('HTTP_REFERER', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Rate limiting: IP당 1분에 최대 10회 요청 허용
        cache_key = f'card_names_rate_limit_{client_ip}'
        request_count = cache.get(cache_key, 0)
        
        if request_count >= 10:
            logger.warning(
                f'Rate limit exceeded for get_all_card_names: IP={client_ip}, '
                f'Referer={referer}, User-Agent={user_agent[:100]}'
            )
            return Response(
                {'error': '요청이 너무 많습니다. 잠시 후 다시 시도해주세요.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Referer 체크: 같은 도메인에서만 접근 허용 (선택적)
        # 프론트엔드에서 사용하므로 완전히 차단하지 않음
        allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
        is_same_origin = False
        if referer:
            from urllib.parse import urlparse
            referer_host = urlparse(referer).netloc
            for host in allowed_hosts:
                if host in referer_host or referer_host in host:
                    is_same_origin = True
                    break
        
        # 접근 로깅 (의심스러운 접근만)
        if not is_same_origin or not user_agent or 'bot' in user_agent.lower() or 'crawler' in user_agent.lower():
            logger.info(
                f'get_all_card_names access: IP={client_ip}, '
                f'Referer={referer}, User-Agent={user_agent[:100]}, '
                f'Same-Origin={is_same_origin}'
            )
        
        # Rate limit 카운터 증가 (1분 TTL)
        cache.set(cache_key, request_count + 1, 60)
        
        # 데이터 반환
        card_names = CardName.objects.all().order_by('name').values_list('name', flat=True)
        return Response({
            'card_names': list(card_names),
            'count': len(card_names)
        })
    
    def _get_client_ip(self, request):
        """클라이언트 IP 주소 추출"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def check_auth(self, request):
        """관리자 인증 확인 전용 엔드포인트"""
        return Response({
            'authenticated': True,
            'is_admin': True,
            'username': request.user.username if request.user.is_authenticated else None
        })
