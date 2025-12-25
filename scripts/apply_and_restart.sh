#!/bin/bash

# 서브도메인 설정 적용 및 서비스 재시작

set -e

echo "=========================================="
echo "서브도메인 설정 적용 및 서비스 재시작"
echo "=========================================="

# 1단계: Nginx 설정 확인
echo ""
echo "[1/3] Nginx 설정 확인 중..."
if grep -q "server_name yugioh.silbuntu.mooo.com" /etc/nginx/sites-available/yugioh_site; then
    echo "✓ Nginx 설정이 올바릅니다."
else
    echo "⚠ Nginx 설정을 확인하세요."
    exit 1
fi

# 2단계: Nginx 재시작
echo ""
echo "[2/3] Nginx 재시작 중..."
if sudo nginx -t; then
    sudo systemctl reload nginx
    echo "✓ Nginx 재시작 완료"
else
    echo "✗ Nginx 설정 오류"
    exit 1
fi

# 3단계: Django 설정 확인 및 재시작
echo ""
echo "[3/3] Django 서비스 재시작 중..."
if grep -q "yugioh.silbuntu.mooo.com" /srv/dbweb/yugioh_site/settings.py; then
    echo "✓ Django 설정이 올바릅니다."
    sudo systemctl restart yugioh-site
    echo "✓ Django 서비스 재시작 완료"
else
    echo "⚠ Django 설정을 확인하세요."
    exit 1
fi

echo ""
echo "=========================================="
echo "설정 적용 완료!"
echo "=========================================="
echo ""
echo "현재 설정:"
echo "  - Nginx: server_name → yugioh.silbuntu.mooo.com"
echo "  - Django: ALLOWED_HOSTS → yugioh.silbuntu.mooo.com"
echo ""
echo "다음 단계:"
echo "  1. DNS 전파 대기 (몇 분~몇 시간 소요 가능)"
echo "  2. nslookup yugioh.silbuntu.mooo.com 으로 DNS 확인"
echo "  3. http://yugioh.silbuntu.mooo.com 접속 테스트"
echo ""
echo "롤백 방법:"
echo "  sudo ./scripts/rollback_subdomain.sh"
echo ""

