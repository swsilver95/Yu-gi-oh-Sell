# 보안 가이드

## 구현된 보안 기능

### 1. 입력 검증
- **카드명**: 길이 제한 (200자), XSS 방지 문자 필터링
- **가격**: 범위 검증 (0 ~ 9,999,999,999)
- **이미지 파일**: 크기 제한 (20MB), 타입 검증 (JPG, PNG, GIF, WEBP), 실제 이미지 파일 검증

### 2. 파일 업로드 보안
- **프론트엔드**: 파일 크기, 타입, 확장자 검증
- **백엔드**: Pillow를 사용한 실제 이미지 파일 검증
- **크기 제한**: 20MB
- **허용 형식**: JPG, JPEG, PNG, GIF, WEBP

### 3. 인증 및 권한
- **관리자 전용 기능**: 카드 생성, 수정, 삭제, 상태 변경
- **Basic Authentication**: 관리자 인증
- **권한 검증**: IsAdminUser permission class 사용

### 4. Django 보안 설정
- **DEBUG**: 환경 변수로 제어 (프로덕션에서는 False)
- **SECRET_KEY**: 환경 변수로 관리
- **ALLOWED_HOSTS**: 허용된 호스트만 접근 가능
- **보안 헤더**: XSS, Clickjacking, MIME 타입 스니핑 방지
- **HSTS**: HTTPS 강제 (SSL 인증서 설치 시)
- **세션 쿠키**: HttpOnly, Secure, SameSite 설정

### 5. CORS 설정
- **허용된 Origin**: 명시적으로 지정된 도메인만 허용
- **CORS_ALLOW_ALL_ORIGINS**: False (보안 강화)

### 6. 데이터베이스 보안
- **ORM 사용**: SQL Injection 방지
- **환경 변수**: 데이터베이스 비밀번호를 환경 변수로 관리

## 보안 권장 사항

### 즉시 적용 가능
1. ✅ 파일 업로드 검증 구현 완료
2. ✅ 입력 검증 구현 완료
3. ✅ 보안 헤더 설정 완료

### 추가 권장 사항

#### 1. SECRET_KEY 관리
```bash
# /etc/dbweb/db.env에 추가
DJANGO_SECRET_KEY=your-strong-secret-key-here
```

강력한 SECRET_KEY 생성:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### 2. SSL 인증서 설치 (HTTPS)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d silbuntu.mooo.com
```

설치 후 `settings.py`에서 다음 주석 해제:
```python
SECURE_SSL_REDIRECT = True
```

#### 3. Rate Limiting (선택사항)
DDoS 공격 방지를 위해 rate limiting 추가 고려:
```bash
pip install django-ratelimit
```

#### 4. 로그 모니터링
- nginx 접근 로그 모니터링
- Django 에러 로그 모니터링
- 의심스러운 활동 감지

#### 5. 정기적인 업데이트
```bash
# 패키지 업데이트 확인
pip list --outdated
# Django 보안 업데이트 확인
python manage.py check --deploy
```

## 보안 체크리스트

- [x] DEBUG = False (프로덕션)
- [x] SECRET_KEY 환경 변수 관리
- [x] ALLOWED_HOSTS 설정
- [x] 입력 검증
- [x] 파일 업로드 검증
- [x] 권한 검증
- [x] 보안 헤더 설정
- [x] CORS 제한
- [ ] SSL 인증서 설치 (HTTPS)
- [ ] Rate Limiting
- [ ] 로그 모니터링

## 주의사항

1. **localStorage 보안**: Basic Auth 토큰을 localStorage에 저장하는 것은 XSS 공격에 취약할 수 있습니다. 프로덕션에서는 세션 기반 인증을 고려하세요.

2. **파일 업로드**: 업로드된 파일은 정기적으로 검사하고, 필요시 바이러스 스캔을 고려하세요.

3. **백업**: 정기적인 데이터베이스 백업을 수행하세요.

4. **업데이트**: Django 및 의존성 패키지를 정기적으로 업데이트하세요.

