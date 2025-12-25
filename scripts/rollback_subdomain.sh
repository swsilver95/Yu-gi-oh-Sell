#!/bin/bash

# 서브도메인 설정 롤백 스크립트

set -e

echo "=========================================="
echo "서브도메인 설정 롤백: silbuntu.mooo.com으로 복원"
echo "=========================================="

# 백업 파일 확인
if [ ! -f /srv/dbweb/backup_nginx_yugioh_site.conf ]; then
    echo "✗ 백업 파일이 없습니다: backup_nginx_yugioh_site.conf"
    exit 1
fi

if [ ! -f /srv/dbweb/backup_settings.py ]; then
    echo "✗ 백업 파일이 없습니다: backup_settings.py"
    exit 1
fi

# 1단계: Nginx 설정 복원
echo ""
echo "[1/3] Nginx 설정 복원 중..."
sudo cp /srv/dbweb/backup_nginx_yugioh_site.conf /etc/nginx/sites-available/yugioh_site
echo "✓ Nginx 설정 복원 완료"

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

# 3단계: Django 설정 복원
echo ""
echo "[3/3] Django 설정 복원 중..."
cp /srv/dbweb/backup_settings.py /srv/dbweb/yugioh_site/settings.py
echo "✓ Django 설정 복원 완료"

# Django 서비스 재시작
sudo systemctl restart yugioh-site
echo "✓ Django 서비스 재시작 완료"

echo ""
echo "=========================================="
echo "롤백 완료!"
echo "=========================================="
echo ""
echo "복원된 설정:"
echo "  - Nginx: server_name → silbuntu.mooo.com"
echo "  - Django: 원래 설정으로 복원"
echo ""

