from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from .models import Card, CardName
from .serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    
    def get_permissions(self):
        """
        카드 생성(등록), 수정, 삭제, 판매 상태 변경은 admin만 가능
        조회는 모두 가능
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'mark_as_sold', 'mark_as_available', 'mark_as_reserved']:
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
        card_names = CardName.objects.all().order_by('name').values_list('name', flat=True)
        return Response({
            'card_names': list(card_names),
            'count': len(card_names)
        })
