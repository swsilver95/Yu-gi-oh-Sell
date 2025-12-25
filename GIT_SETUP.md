# Git 인증 설정 가이드

## 문제 상황
GitHub는 2021년 8월부터 패스워드 인증을 중단했습니다. 현재 HTTPS로 설정된 저장소에서 인증 오류가 발생하고 있습니다.

## 해결 방법

### 방법 1: Personal Access Token (PAT) 사용 (권장)

#### 1. GitHub에서 Personal Access Token 생성
1. GitHub에 로그인
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. "Generate new token (classic)" 클릭
4. Note: "Yu-gi-oh-Sell" (설명)
5. Expiration: 원하는 기간 선택
6. Scopes: `repo` 체크 (전체 저장소 접근)
7. "Generate token" 클릭
8. **토큰을 복사해두세요** (한 번만 표시됩니다)

#### 2. Git Credential Helper 설정
```bash
# Credential helper 설정 (메모리에 저장)
git config --global credential.helper store

# 또는 캐시에 저장 (15분간 유효)
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'  # 1시간
```

#### 3. Push 시 토큰 사용
```bash
cd /srv/dbweb
git push origin main
# Username: swsilver95
# Password: [생성한 Personal Access Token 붙여넣기]
```

#### 4. 자동 인증 설정 (선택사항)
```bash
# URL에 토큰 포함 (보안상 권장하지 않음)
git remote set-url origin https://swsilver95:[TOKEN]@github.com/swsilver95/Yu-gi-oh-Sell.git
```

### 방법 2: SSH 키 사용 (더 안전)

#### 1. SSH 키 생성
```bash
ssh-keygen -t ed25519 -C "dmstmddnjs@hanmail.net"
# Enter를 눌러 기본 경로 사용
# Passphrase는 선택사항 (보안을 위해 설정 권장)
```

#### 2. 공개 키를 GitHub에 등록
```bash
# 공개 키 내용 복사
cat ~/.ssh/id_ed25519.pub

# GitHub → Settings → SSH and GPG keys → New SSH key
# 위에서 복사한 공개 키를 붙여넣기
```

#### 3. 원격 저장소 URL을 SSH로 변경
```bash
cd /srv/dbweb
git remote set-url origin git@github.com:swsilver95/Yu-gi-oh-Sell.git
```

#### 4. 연결 테스트
```bash
ssh -T git@github.com
# "Hi swsilver95! You've successfully authenticated..." 메시지 확인
```

## 현재 설정 확인

```bash
# 원격 저장소 URL 확인
git remote -v

# Git 사용자 정보 확인
git config --global user.name
git config --global user.email

# Credential helper 확인
git config --global credential.helper
```

## 추천 방법

**SSH 키 사용을 권장합니다:**
- 더 안전함 (토큰이 URL에 노출되지 않음)
- 한 번 설정하면 계속 사용 가능
- 패스워드 입력 불필요

## 문제 해결

### "Permission denied" 오류
- SSH 키가 GitHub에 등록되었는지 확인
- SSH 에이전트가 실행 중인지 확인: `eval "$(ssh-agent -s)"`

### "Authentication failed" 오류
- Personal Access Token이 올바른지 확인
- Token의 `repo` 권한이 있는지 확인
- Token이 만료되지 않았는지 확인


