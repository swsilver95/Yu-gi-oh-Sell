# DDNS 서브도메인 설정 가이드

## 공유기/DDNS 설정 방법

### 옵션 1: 와일드카드 서브도메인 (권장)

**설정: `*.silbuntu.mooo.com`**

**장점:**
- 한 번 설정하면 모든 서브도메인이 자동으로 동일한 IP로 설정됨
- 새로운 서브도메인 추가 시 DDNS 설정 불필요
- 관리가 편리함

**단점:**
- DDNS 서비스가 와일드카드를 지원해야 함
- 일부 서비스는 와일드카드를 지원하지 않음

**지원 여부 확인:**
- noip.com: 지원 (유료 플랜)
- duckdns.org: 지원
- dynu.com: 지원
- 기타 서비스: 각 서비스 문서 확인 필요

### 옵션 2: 개별 서브도메인 설정

**설정: 각 서브도메인을 개별적으로 추가**
- `yugioh.silbuntu.mooo.com`
- `newsvc.silbuntu.mooo.com` (추후 추가)

**장점:**
- 모든 DDNS 서비스에서 지원
- 더 명확하고 제어 가능
- 서브도메인별로 다른 설정 가능 (필요시)

**단점:**
- 새로운 서브도메인 추가 시마다 DDNS 설정 필요

## 추천 방법

### 현재 상황 (mooo.com 사용 중)

**mooo.com 서비스 확인 필요:**
- 와일드카드 지원 여부 확인
- 지원한다면: `*.silbuntu.mooo.com` 설정 (권장)
- 지원하지 않는다면: `yugioh.silbuntu.mooo.com` 개별 설정

### 일반적인 설정 방법

#### 공유기 DDNS 설정
```
호스트 이름: *.silbuntu.mooo.com
또는
호스트 이름: yugioh.silbuntu.mooo.com
```

#### DDNS 서비스 웹 관리 페이지
1. 서브도메인 추가 메뉴
2. 호스트 이름: `yugioh` (또는 `*` 와일드카드)
3. 도메인: `silbuntu.mooo.com`
4. IP 주소: 자동 업데이트 또는 수동 설정

## 확인 방법

### 1. DNS 전파 확인
```bash
# 서브도메인 확인
nslookup yugioh.silbuntu.mooo.com

# 또는
dig yugioh.silbuntu.mooo.com

# 와일드카드 확인
nslookup test.silbuntu.mooo.com
```

### 2. 브라우저에서 접속 테스트
- `http://yugioh.silbuntu.mooo.com` 접속 시도
- DNS 전파가 완료되면 접속 가능

## 주의사항

1. **DNS 전파 시간**: 서브도메인 추가 후 전파에 몇 분~몇 시간 소요될 수 있음
2. **와일드카드 지원**: 서비스에 따라 와일드카드를 지원하지 않을 수 있음
3. **기존 도메인**: `silbuntu.mooo.com`은 그대로 유지되거나 별도 설정 필요

## 결론

**질문: `*.silbuntu.mooo.com`으로 설정해야 하나?**

**답변:**
- **와일드카드를 지원한다면**: `*.silbuntu.mooo.com` 설정 권장 ✅
- **지원하지 않는다면**: `yugioh.silbuntu.mooo.com` 개별 설정

**확인 방법:**
1. DDNS 서비스(mooo.com) 문서 확인
2. 또는 웹 관리 페이지에서 와일드카드 옵션 확인
3. 테스트: `test.silbuntu.mooo.com` 같은 임의 서브도메인으로 확인

**일반적으로는:**
- 와일드카드 지원 시: `*.silbuntu.mooo.com` (편리함)
- 와일드카드 미지원 시: `yugioh.silbuntu.mooo.com` (개별 설정)

