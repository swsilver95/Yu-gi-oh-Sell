# 다중 서비스 설정 가이드 (서브도메인 기반)

## 핵심 개념

**포트 설정을 새로 할 필요 없습니다!**

Nginx는 **같은 포트 80**에서 여러 `server` 블록을 사용하여 서브도메인별로 다른 서비스로 라우팅할 수 있습니다.

## 구조 설명

```
외부 요청 (포트 80)
    ↓
Nginx (포트 80에서 리스닝)
    ↓
서브도메인에 따라 분기
    ├─ yugioh.silbuntu.mooo.com → proxy_pass → Django (127.0.0.1:8000)
    └─ newsvc.silbuntu.mooo.com → proxy_pass → 새 서비스 (127.0.0.1:8001)
```

## 설정 방법

### 1. Nginx 설정 파일 구조

각 서브도메인마다 별도의 `server` 블록을 생성합니다:

```nginx
# yugioh 서비스
server {
    listen 80;
    server_name yugioh.silbuntu.mooo.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;  # Django 서비스
        # ... 기타 설정
    }
}

# 새 서비스
server {
    listen 80;
    server_name newsvc.silbuntu.mooo.com;
    
    location / {
        proxy_pass http://127.0.0.1:8001;  # 새 서비스 (다른 포트)
        # 또는
        # root /srv/newsvc/dist;  # 정적 파일 서비스
        # ... 기타 설정
    }
}

# 기존 도메인 차단 (선택사항)
server {
    listen 80;
    server_name silbuntu.mooo.com;
    
    return 404;  # 또는 403 Forbidden
}
```

### 2. 포트는 어떻게?

**Nginx는 모두 80번 포트로 받습니다.**

각 서비스는 **내부적으로 다른 포트**에서 실행됩니다:
- Django (yugioh): `127.0.0.1:8000`
- 새 서비스: `127.0.0.1:8001` (또는 다른 포트)

**중요**: 
- 외부에서는 모두 **포트 80**으로 접속
- Nginx가 서브도메인을 보고 내부 포트로 프록시
- 각 서비스는 localhost의 다른 포트에서 실행

### 3. 실제 설정 예시

#### 옵션 A: 같은 파일에 여러 server 블록

`/etc/nginx/sites-available/yugioh_site`:
```nginx
# yugioh 서비스
server {
    listen 80;
    server_name yugioh.silbuntu.mooo.com;
    
    root /srv/dbweb/frontend/dist;
    index index.html;
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        # ... 기타 설정
    }
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

# 기존 도메인 차단
server {
    listen 80;
    server_name silbuntu.mooo.com;
    return 404;
}
```

`/etc/nginx/sites-available/newsvc`:
```nginx
# 새 서비스
server {
    listen 80;
    server_name newsvc.silbuntu.mooo.com;
    
    location / {
        proxy_pass http://127.0.0.1:8001;  # 새 서비스 포트
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 옵션 B: 별도 파일로 분리 (권장)

각 서비스마다 별도의 설정 파일을 만드는 것이 관리하기 쉽습니다:

```
/etc/nginx/sites-available/
  ├── yugioh_site      # yugioh.silbuntu.mooo.com
  ├── newsvc           # newsvc.silbuntu.mooo.com
  └── default_block    # silbuntu.mooo.com (차단용)
```

각 파일을 `sites-enabled`에 심볼릭 링크로 연결:
```bash
sudo ln -s /etc/nginx/sites-available/yugioh_site /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/newsvc /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/default_block /etc/nginx/sites-enabled/
```

## 작업 순서

### 1단계: 기존 도메인 차단 설정

`/etc/nginx/sites-available/default_block`:
```nginx
server {
    listen 80;
    server_name silbuntu.mooo.com;
    return 404;  # 또는 403 Forbidden
}
```

### 2단계: yugioh 서비스 설정 수정

`/etc/nginx/sites-available/yugioh_site`:
```nginx
server {
    listen 80;
    server_name yugioh.silbuntu.mooo.com;  # 변경
    
    # ... 기존 설정 유지
}
```

### 3단계: Django 설정 수정

`yugioh_site/settings.py`:
```python
ALLOWED_HOSTS = [
    'yugioh.silbuntu.mooo.com',  # 변경
    # 'silbuntu.mooo.com',  # 제거 또는 주석 처리
    'localhost',
    '127.0.0.1',
]

CORS_ALLOWED_ORIGINS = [
    "http://yugioh.silbuntu.mooo.com",  # 변경
    # "http://silbuntu.mooo.com",  # 제거
    # ... 기타 설정
]
```

### 4단계: 새 서비스 설정 파일 생성

`/etc/nginx/sites-available/newsvc`:
```nginx
server {
    listen 80;
    server_name newsvc.silbuntu.mooo.com;
    
    # 예시 1: 다른 포트의 서비스로 프록시
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 예시 2: 정적 파일 서비스
    # root /srv/newsvc/dist;
    # index index.html;
    # location / {
    #     try_files $uri $uri/ /index.html;
    # }
}
```

### 5단계: 새 서비스 실행

새 서비스를 다른 포트에서 실행:
```bash
# 예시: 새 Django 서비스
cd /srv/newsvc
gunicorn --bind 127.0.0.1:8001 newsvc.wsgi:application

# 또는 systemd 서비스로 등록
```

## 포트 정리

| 서비스 | 외부 접속 | Nginx 포트 | 내부 포트 | 설명 |
|--------|----------|-----------|----------|------|
| yugioh | yugioh.silbuntu.mooo.com | 80 | 8000 | 기존 Django 서비스 |
| newsvc | newsvc.silbuntu.mooo.com | 80 | 8001 | 새 서비스 |
| 차단 | silbuntu.mooo.com | 80 | - | 404 반환 |

**핵심**: 
- 외부에서는 모두 **포트 80**으로 접속
- Nginx가 서브도메인을 보고 내부 포트로 분기
- 각 서비스는 **localhost의 다른 포트**에서 실행

## 주의사항

1. **포트 충돌**: 새 서비스가 사용할 포트(예: 8001)가 다른 서비스와 충돌하지 않는지 확인
2. **방화벽**: 외부 포트는 80만 열어두면 됨 (내부 포트는 localhost만 접근)
3. **DNS 설정**: 각 서브도메인을 DDNS 서비스에서 설정해야 함
4. **서비스 관리**: 각 서비스를 systemd로 관리하면 편리함

## 결론

**포트 설정을 새로 할 필요 없습니다!**

- Nginx는 모두 포트 80에서 리스닝
- 서브도메인별로 다른 내부 포트로 프록시
- 각 서비스는 localhost의 다른 포트에서 실행
- 외부에서는 모두 포트 80으로 접속

이 방식이 가장 일반적이고 관리하기 쉬운 방법입니다.

