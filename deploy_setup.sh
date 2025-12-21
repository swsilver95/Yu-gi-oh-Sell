#!/bin/bash
# 배포 설정 스크립트

set -e

echo "=== 유희왕 카드 판매 사이트 배포 설정 ==="

# 1. nginx 설정 파일 생성
echo "1. nginx 설정 파일 생성 중..."
sudo tee /etc/nginx/sites-available/yugioh_site > /dev/null << 'EOF'
server {
    listen 80;
    server_name silbuntu.mooo.com;

    # Vue.js 정적 파일
    root /srv/dbweb/frontend/dist;
    index index.html;

    # 정적 파일 캐싱
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Vue.js SPA 라우팅
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Django API 프록시
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Django 미디어 파일
    location /media/ {
        alias /srv/dbweb/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Django 정적 파일
    location /static/ {
        alias /srv/dbweb/staticfiles/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # 보안 헤더
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF

# 2. nginx 사이트 활성화
echo "2. nginx 사이트 활성화 중..."
sudo ln -sf /etc/nginx/sites-available/yugioh_site /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 3. nginx 설정 테스트
echo "3. nginx 설정 테스트 중..."
sudo nginx -t

# 4. systemd 서비스 파일 생성
echo "4. systemd 서비스 파일 생성 중..."
sudo tee /etc/systemd/system/yugioh-site.service > /dev/null << 'EOF'
[Unit]
Description=Yu-gi-oh Card Sell Site (Django)
After=network.target postgresql.service

[Service]
Type=notify
User=silbuntu
Group=silbuntu
WorkingDirectory=/srv/dbweb
Environment="PATH=/srv/dbweb/venv/bin"
ExecStart=/srv/dbweb/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 3 --timeout 120 yugioh_site.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 5. gunicorn 설치 확인 및 설치
echo "5. gunicorn 설치 확인 중..."
if ! /srv/dbweb/venv/bin/pip show gunicorn > /dev/null 2>&1; then
    echo "gunicorn 설치 중..."
    /srv/dbweb/venv/bin/pip install gunicorn
fi

# 6. Django 정적 파일 수집
echo "6. Django 정적 파일 수집 중..."
cd /srv/dbweb
source venv/bin/activate
python manage.py collectstatic --noinput

# 7. systemd 데몬 리로드
echo "7. systemd 데몬 리로드 중..."
sudo systemctl daemon-reload

# 8. 방화벽 설정 확인
echo "8. 방화벽 설정 확인 중..."
echo "다음 명령어로 방화벽을 설정하세요:"
echo "  sudo ufw allow 80/tcp"
echo "  sudo ufw allow 443/tcp"
echo "  sudo ufw status"

echo ""
echo "=== 배포 설정 완료 ==="
echo ""
echo "다음 단계:"
echo "1. 방화벽 설정: sudo ufw allow 80/tcp && sudo ufw allow 443/tcp"
echo "2. 서비스 시작: sudo systemctl start yugioh-site"
echo "3. 서비스 자동 시작 설정: sudo systemctl enable yugioh-site"
echo "4. nginx 재시작: sudo systemctl restart nginx"
echo "5. 서비스 상태 확인: sudo systemctl status yugioh-site"

