#!/bin/bash

# yugioh.silbuntu.mooo.com으로만 접속 가능하도록 설정 변경

set -e

echo "=========================================="
echo "서브도메인 설정 적용: yugioh.silbuntu.mooo.com"
echo "=========================================="

# 1단계: Nginx 설정 변경
echo ""
echo "[1/3] Nginx 설정 변경 중..."

# 현재 설정 읽기
CURRENT_NGINX=$(cat /etc/nginx/sites-available/yugioh_site)

# server_name 변경
NEW_NGINX=$(echo "$CURRENT_NGINX" | sed 's/server_name silbuntu\.mooo\.com;/server_name yugioh.silbuntu.mooo.com;/')

# 임시 파일에 저장
echo "$NEW_NGINX" | sudo tee /etc/nginx/sites-available/yugioh_site > /dev/null

echo "✓ Nginx 설정 변경 완료 (server_name: yugioh.silbuntu.mooo.com)"

# 2단계: Nginx 설정 테스트 및 재시작
echo ""
echo "[2/3] Nginx 재시작 중..."
if sudo nginx -t; then
    sudo systemctl reload nginx
    echo "✓ Nginx 재시작 완료"
else
    echo "✗ Nginx 설정 오류 - 롤백 필요"
    exit 1
fi

# 3단계: Django 설정 변경
echo ""
echo "[3/3] Django 설정 변경 중..."

# settings.py 백업 확인
if [ ! -f /srv/dbweb/backup_settings.py ]; then
    echo "⚠ 백업 파일이 없습니다. 백업을 생성합니다..."
    cp /srv/dbweb/yugioh_site/settings.py /srv/dbweb/backup_settings.py
fi

# ALLOWED_HOSTS 변경
sed -i "s/'silbuntu\.mooo\.com',/'yugioh.silbuntu.mooo.com',/" /srv/dbweb/yugioh_site/settings.py

# CORS_ALLOWED_ORIGINS 변경
sed -i 's|"http://silbuntu\.mooo\.com",|"http://yugioh.silbuntu.mooo.com",|' /srv/dbweb/yugioh_site/settings.py
sed -i 's|"https://silbuntu\.mooo\.com",|"https://yugioh.silbuntu.mooo.com",|' /srv/dbweb/yugioh_site/settings.py

echo "✓ Django 설정 변경 완료"

# Django 서비스 재시작
sudo systemctl restart yugioh-site
echo "✓ Django 서비스 재시작 완료"

echo ""
echo "=========================================="
echo "설정 완료!"
echo "=========================================="
echo ""
echo "변경 사항:"
echo "  - Nginx: server_name → yugioh.silbuntu.mooo.com"
echo "  - Django ALLOWED_HOSTS → yugioh.silbuntu.mooo.com"
echo "  - Django CORS_ALLOWED_ORIGINS → yugioh.silbuntu.mooo.com"
echo ""
echo "롤백 방법:"
echo "  sudo ./scripts/rollback_subdomain.sh"
echo ""
echo "주의: DNS에서 yugioh.silbuntu.mooo.com을 설정해야 접속 가능합니다!"
echo ""

