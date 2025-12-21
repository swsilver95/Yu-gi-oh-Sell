#!/bin/bash
# Django 관리자 계정 생성 스크립트

set -e

echo "=== Django 관리자 계정 생성 ==="
echo ""

cd /srv/dbweb
source venv/bin/activate

echo "관리자 계정을 생성합니다."
echo "사용자명, 이메일(선택), 비밀번호를 입력하세요."
echo ""

python manage.py createsuperuser

echo ""
echo "=== 완료 ==="
echo ""
echo "생성된 관리자 계정으로 로그인할 수 있습니다."

