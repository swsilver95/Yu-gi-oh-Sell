#!/bin/bash
# Django SECRET_KEY 환경 변수 설정 스크립트

set -e

echo "=========================================="
echo "Django SECRET_KEY 환경 변수 설정"
echo "=========================================="

# 새로운 SECRET_KEY 생성
NEW_SECRET_KEY=$(cd /srv/dbweb && source venv/bin/activate && python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

echo ""
echo "생성된 SECRET_KEY: ${NEW_SECRET_KEY:0:20}..."
echo ""

# 환경 변수 파일에 추가
ENV_FILE="/etc/dbweb/db.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "⚠ 경고: $ENV_FILE 파일이 없습니다. 생성합니다..."
    sudo mkdir -p /etc/dbweb
    sudo touch "$ENV_FILE"
    sudo chown silbuntu:silbuntu "$ENV_FILE"
fi

# 기존 SECRET_KEY가 있는지 확인
if grep -q "^DJANGO_SECRET_KEY=" "$ENV_FILE" 2>/dev/null; then
    echo "⚠ 기존 DJANGO_SECRET_KEY가 있습니다. 덮어쓰시겠습니까? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "취소되었습니다."
        exit 0
    fi
    # 기존 라인 제거
    sudo sed -i '/^DJANGO_SECRET_KEY=/d' "$ENV_FILE"
fi

# 새로운 SECRET_KEY 추가
echo "" | sudo tee -a "$ENV_FILE" > /dev/null
echo "# Django Secret Key" | sudo tee -a "$ENV_FILE" > /dev/null
echo "DJANGO_SECRET_KEY=$NEW_SECRET_KEY" | sudo tee -a "$ENV_FILE" > /dev/null

echo ""
echo "✓ SECRET_KEY가 환경 변수 파일에 추가되었습니다."
echo ""
echo "다음 단계:"
echo "  1. Django 서비스 재시작: sudo systemctl restart yugioh-site"
echo "  2. 서비스 상태 확인: sudo systemctl status yugioh-site"
echo ""

