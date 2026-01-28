---
name: security
description: |
  코드 보안 취약점을 검사합니다. OWASP Top 10, 시크릿 탐지, SQL Injection, XSS 등을 검사합니다.
  USE WHEN: 보안, security, 취약점, vulnerability, 시크릿, secret, 인젝션, injection,
  XSS, CSRF, OWASP, 해킹, hacking, 공격, attack, 위험, risk,
  인증, auth, 권한, permission, 토큰, token, 비밀번호, password,
  암호화, encryption, 노출, expose, 유출, leak,
  SQL injection, 코드 삽입, sanitize, escape, validate,
  .env, credentials, API key, 민감정보, sensitive
argument-hint: "[경로] [--full] [--fix]"
allowed-tools: [Read, Grep, Glob, Bash, WebSearch, mcp__tavily__tavily-search]
agent: security-reviewer
agents:
  primary: security-reviewer
  orchestration:
    scan: [security-reviewer, Explore]
    research: [deep-researcher]
    analyze: [security-reviewer, code-reviewer]
    fix: [security-reviewer, build-error-resolver]
---

# /security - 코드 보안 취약점 검사

> **OWASP Top 10 기반 보안 검사**

## 사용법

```bash
/security                    # 전체 프로젝트 검사
/security src/api/          # 특정 경로 검사
/security --full            # 전체 검사 (의존성 포함)
/security --fix             # 자동 수정 제안 포함
```

## 실행 절차

### Step 1: 검사 대상 파일 수집

```bash
# 소스 코드 파일 목록
**/*.{ts,tsx,js,jsx,py,go,java,rs,rb,php}

# 설정 파일
**/*.{json,yaml,yml,toml,xml}

# 제외 대상
node_modules/, .git/, dist/, build/, __pycache__/
```

### Step 2: 시크릿 탐지

다음 패턴 검색:

```
# API 키
api[_-]?key\s*[=:]\s*['"][A-Za-z0-9_\-]{20,}['"]

# 비밀번호
password\s*[=:]\s*['"][^'"]{8,}['"]

# 토큰
(access|auth|bearer|refresh)[_-]?token\s*[=:]\s*['"][^'"]+['"]

# AWS 키
AKIA[0-9A-Z]{16}
aws[_-]?secret[_-]?access[_-]?key

# Private Key
-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----

# JWT Secret
jwt[_-]?secret\s*[=:]\s*['"][^'"]+['"]

# Database URL with credentials
(mysql|postgres|mongodb)://[^:]+:[^@]+@
```

### Step 3: SQL Injection 검사

```
# 위험 패턴 검색
- 문자열 연결: "SELECT.*" \+
- f-string: f["']SELECT.*\{
- 템플릿 리터럴: `SELECT.*\$\{
- format(): .format\(.*SELECT
```

### Step 4: XSS 검사

```
# 위험 패턴 검색
- innerHTML\s*=
- dangerouslySetInnerHTML
- document\.write\(
- eval\(
- v-html=
- [innerHTML]= (Angular)
```

### Step 5: 경로 탐색 검사

```
# 위험 패턴 검색
- path\.join\(.*req\.(params|query|body)
- fs\.(read|write).*\+.*req\.
- open\(.*request\.
```

### Step 6: 인증/인가 검사

```
# 검사 항목
- CORS: Access-Control-Allow-Origin: '*'
- 하드코딩된 JWT 시크릿
- 비밀번호 최소 길이 검증 누락
- 세션 쿠키 secure/httpOnly 플래그
```

### Step 7: 결과 출력

```
🔒 보안 검사 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
프로젝트: [프로젝트명]
검사 시간: [시간]
검사 파일: [N]개

📊 요약
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ CRITICAL: [N]개
⚠️ HIGH: [N]개
🔶 MEDIUM: [N]개
ℹ️ LOW: [N]개

📋 상세 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[각 이슈별 상세 정보]

💡 권장 조치
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. CRITICAL 이슈 즉시 수정
2. HIGH 이슈 PR 전 수정
3. MEDIUM 이슈 계획적 수정
4. LOW 이슈 리팩토링 시 수정
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--full` | 의존성 취약점까지 검사 (npm audit, pip-audit 등) |
| `--fix` | 자동 수정 가능한 항목 수정 제안 |
| `--json` | JSON 형식으로 출력 |
| `--sarif` | SARIF 형식으로 출력 (CI/CD 연동) |

## 심각도별 조치

| 심각도 | 조치 | 시간 제한 |
|--------|------|----------|
| **CRITICAL** | 즉시 수정 필수 | 즉시 |
| **HIGH** | PR 전 수정 필수 | 24시간 |
| **MEDIUM** | 스프린트 내 수정 | 1주 |
| **LOW** | 백로그 등록 | 계획적 |

## 레거시 명령어

`/security-review` → `/security` (자동 매핑됨)

## 참조 파일

### 베스트 프랙티스 (스킬 내부)

- `references/security.md` - **보안 가이드 (최우선)**
- `references/api-design.md` - API 보안
- `references/database.md` - SQL Injection 방지
