# 배포 가이드

## 배포 전 확인 사항

### 1. PostgreSQL 설정 확인
```bash
/srv/dbweb/check_postgresql.sh
```

### 2. 환경 변수 확인
- `/etc/dbweb/db.env` 파일이 존재하고 올바른 설정이 있는지 확인
- 필요시 `DJANGO_SECRET_KEY` 환경 변수 설정 (선택사항)

## 배포 단계

### 1. 배포 스크립트 실행
```bash
cd /srv/dbweb
sudo ./deploy_setup.sh
```

이 스크립트는 다음을 수행합니다:
- nginx 설정 파일 생성 (`/etc/nginx/sites-available/yugioh_site`)
- nginx 사이트 활성화
- systemd 서비스 파일 생성 (`/etc/systemd/system/yugioh-site.service`)
- gunicorn 설치 (없는 경우)
- Django 정적 파일 수집

### 2. 방화벽 설정
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw status
```

### 3. 서비스 시작
```bash
# Django 서비스 시작
sudo systemctl start yugioh-site

# 서비스 자동 시작 설정
sudo systemctl enable yugioh-site

# nginx 재시작
sudo systemctl restart nginx
```

### 4. 서비스 상태 확인
```bash
# Django 서비스 상태
sudo systemctl status yugioh-site

# nginx 상태
sudo systemctl status nginx

# 로그 확인
sudo journalctl -u yugioh-site -f
```

## 배포 후 확인

1. 브라우저에서 `http://silbuntu.mooo.com` 접속
2. 카드 목록이 정상적으로 표시되는지 확인
3. 관리자 로그인 테스트
4. 카드 등록 테스트

## 문제 해결

### Django 서비스가 시작되지 않는 경우
```bash
# 로그 확인
sudo journalctl -u yugioh-site -n 50

# 수동으로 테스트
cd /srv/dbweb
source venv/bin/activate
gunicorn --bind 127.0.0.1:8000 yugioh_site.wsgi:application
```

### nginx 오류
```bash
# 설정 테스트
sudo nginx -t

# 로그 확인
sudo tail -f /var/log/nginx/error.log
```

### 정적 파일이 표시되지 않는 경우
```bash
cd /srv/dbweb
source venv/bin/activate
python manage.py collectstatic --noinput
```

## 프로덕션 설정

### 환경 변수 설정 (선택사항)
`/etc/dbweb/db.env`에 다음을 추가할 수 있습니다:
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
```

### SSL 인증서 설정 (선택사항)
Let's Encrypt를 사용하여 SSL 인증서를 설정할 수 있습니다:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d silbuntu.mooo.com
```

## 서비스 관리

### 서비스 재시작
```bash
sudo systemctl restart yugioh-site
sudo systemctl restart nginx
```

### 서비스 중지
```bash
sudo systemctl stop yugioh-site
```

### 서비스 로그 확인
```bash
sudo journalctl -u yugioh-site -f
```

