# 서브도메인 설정 가이드

## 기술적 난이도: ⭐ 매우 쉬움

서브도메인 설정은 매우 일반적이고 간단한 작업입니다. 설정 파일 몇 개만 수정하면 됩니다.

## 필요한 작업

### 1. DNS 설정 (DDNS 서비스)
- **작업**: DDNS 서비스에서 `yugioh.silbuntu.mooo.com` 서브도메인 추가
- **난이도**: ⭐ 매우 쉬움
- **방법**: 
  - 사용 중인 DDNS 서비스 (mooo.com)의 관리 페이지에서 서브도메인 추가
  - A 레코드로 동일한 IP 주소 설정
  - 또는 와일드카드 서브도메인 (`*.silbuntu.mooo.com`) 설정 가능

### 2. Nginx 설정 수정
- **작업**: `server_name`에 서브도메인 추가
- **난이도**: ⭐ 매우 쉬움
- **변경 위치**: `/etc/nginx/sites-available/yugioh_site`
- **변경 내용**:
  ```nginx
  server_name yugioh.silbuntu.mooo.com;
  # 또는 여러 도메인 허용:
  server_name yugioh.silbuntu.mooo.com silbuntu.mooo.com;
  ```

### 3. Django 설정 수정
- **작업**: `ALLOWED_HOSTS`에 서브도메인 추가
- **난이도**: ⭐ 매우 쉬움
- **변경 위치**: `yugioh_site/settings.py`
- **변경 내용**:
  ```python
  ALLOWED_HOSTS = [
      'yugioh.silbuntu.mooo.com',
      'silbuntu.mooo.com',  # 기존 도메인 유지 (선택사항)
      'localhost',
      '127.0.0.1',
  ]
  ```

### 4. CORS 설정 수정
- **작업**: `CORS_ALLOWED_ORIGINS`에 서브도메인 추가
- **난이도**: ⭐ 매우 쉬움
- **변경 위치**: `yugioh_site/settings.py`
- **변경 내용**:
  ```python
  CORS_ALLOWED_ORIGINS = [
      "http://yugioh.silbuntu.mooo.com",
      "https://yugioh.silbuntu.mooo.com",  # HTTPS 사용 시
      "http://silbuntu.mooo.com",  # 기존 도메인 유지 (선택사항)
      # ... 기타 localhost 설정
  ]
  ```

## 추후 확장성 고려사항

### 옵션 1: 와일드카드 서브도메인 (권장)
여러 서브도메인을 쉽게 추가할 수 있도록 설정:

**Django settings.py:**
```python
# 와일드카드 패턴 사용
ALLOWED_HOSTS = [
    '*.silbuntu.mooo.com',  # 모든 서브도메인 허용
    'silbuntu.mooo.com',
    'localhost',
    '127.0.0.1',
]

# 또는 환경 변수로 관리
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

**Nginx:**
```nginx
# 여러 서브도메인을 하나의 server 블록에서 처리
server_name *.silbuntu.mooo.com silbuntu.mooo.com;
```

**장점:**
- 새로운 서브도메인 추가 시 설정 파일 수정 불필요
- 확장성이 좋음

**단점:**
- 보안상 모든 서브도메인을 허용하게 됨 (주의 필요)

### 옵션 2: 개별 서브도메인 설정
각 서브도메인을 명시적으로 관리:

**장점:**
- 보안상 더 안전 (명시적 허용)
- 각 서브도메인별로 다른 설정 가능

**단점:**
- 새로운 서브도메인 추가 시마다 설정 파일 수정 필요

### 옵션 3: Nginx에서 여러 서비스 분리
각 서브도메인마다 별도의 Nginx 설정 파일 생성:

```
/etc/nginx/sites-available/
  ├── yugioh_site          # yugioh.silbuntu.mooo.com
  ├── other_service        # other.silbuntu.mooo.com
  └── ...
```

**장점:**
- 각 서비스 독립적 관리
- 서비스별로 다른 설정 가능 (포트, 경로 등)

**단점:**
- 설정 파일이 많아짐
- 관리 복잡도 증가

## 추천 방법

**단기적으로는 옵션 2 (개별 설정)를 권장합니다:**
- 보안상 안전
- 설정이 명확함
- 서브도메인이 많지 않다면 충분

**장기적으로는 옵션 1 (와일드카드) 고려:**
- 서브도메인이 많아질 경우
- 빠른 확장이 필요한 경우

## 작업 순서

1. **DNS 설정** (DDNS 서비스에서 서브도메인 추가)
2. **Nginx 설정 수정** (`server_name` 추가)
3. **Django 설정 수정** (`ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` 추가)
4. **서비스 재시작** (Nginx, Django)
5. **테스트** (브라우저에서 접속 확인)

## 예상 소요 시간

- DNS 설정: 5분 (DDNS 서비스에 따라 다름)
- 설정 파일 수정: 5분
- 테스트: 5분
- **총 예상 시간: 15분 이내**

## 주의사항

1. **DNS 전파 시간**: 서브도메인 추가 후 DNS 전파에 몇 분~몇 시간 소요될 수 있음
2. **기존 도메인 유지**: `silbuntu.mooo.com`도 계속 사용하려면 설정에 함께 추가
3. **HTTPS 설정**: 추후 HTTPS를 사용할 경우 각 서브도메인마다 SSL 인증서 필요 (Let's Encrypt는 와일드카드 인증서 지원)

## 결론

**기술적 난이도: 매우 쉬움** ⭐

서브도메인 설정은 매우 간단한 작업이며, 설정 파일 몇 개만 수정하면 됩니다. 
추후 다른 서비스 추가도 동일한 방식으로 쉽게 확장 가능합니다.

