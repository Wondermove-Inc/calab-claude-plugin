---
name: security-review
description: 코드 보안 취약점을 자동으로 검사합니다. 보안, 취약점, 시크릿, 인젝션, XSS 키워드 시 자동 활성화.
allowed-tools: Read, Grep, Glob
---

# Security Review Skill

> **보안 중심 코드 검토 - OWASP Top 10 및 시크릿 탐지**

## 목적

코드 작성/수정 시 보안 취약점을 자동으로 탐지하고 경고합니다.

## 활성화 조건

다음 상황에서 **자동 활성화**:
- 코드 작성/수정 시 (백그라운드 검사)
- "보안", "취약점", "시크릿", "인젝션", "XSS" 키워드 언급 시
- `/security-review` 명령어 실행 시
- PR/커밋 전 검토 요청 시

## 핵심 검사 항목

### 1. 하드코딩된 시크릿 탐지

```
# 탐지 패턴
- API 키: api[_-]?key\s*[=:]\s*['"][^'"]+['"]
- 비밀번호: password\s*[=:]\s*['"][^'"]+['"]
- 토큰: (access|auth|bearer)[_-]?token\s*[=:]\s*['"][^'"]+['"]
- AWS: AKIA[0-9A-Z]{16}
- Private Key: -----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----
```

**검사 대상 파일**:
- 소스 코드 (*.ts, *.js, *.py, *.go, *.java, *.rs)
- 설정 파일 (*.json, *.yaml, *.yml, *.toml)
- 환경 파일 (*.env* 제외 - 이미 차단됨)

### 2. SQL Injection

```
# 위험 패턴
- 문자열 연결 쿼리: "SELECT.*" + variable
- f-string 쿼리: f"SELECT.*{variable}"
- 템플릿 리터럴: `SELECT...${variable}`

# 안전 패턴 (권장)
- 파라미터화된 쿼리
- ORM 사용 (Prisma, TypeORM, SQLAlchemy)
- Prepared Statements
```

### 3. XSS (Cross-Site Scripting)

```
# 위험 패턴
- innerHTML 직접 할당
- dangerouslySetInnerHTML (React)
- document.write()
- eval() 사용

# 안전 패턴 (권장)
- textContent 사용
- DOMPurify 라이브러리
- React의 기본 이스케이핑
```

### 4. 경로 탐색 (Path Traversal)

```
# 위험 패턴
- 사용자 입력을 경로에 직접 사용
- ../ 패턴 미필터링
- path.join(userInput) 직접 사용

# 안전 패턴 (권장)
- path.resolve() + 화이트리스트 검증
- 경로 정규화 후 기본 경로 포함 확인
```

### 5. 안전하지 않은 역직렬화

```
# 위험 패턴
- pickle.loads(untrusted_data) [Python]
- eval(JSON.parse(...)) [JavaScript]
- ObjectInputStream(untrusted) [Java]
- yaml.load(untrusted, Loader=yaml.FullLoader) [Python]

# 안전 패턴 (권장)
- JSON.parse() 만 사용
- yaml.safe_load() 사용
- 스키마 검증 후 역직렬화
```

### 6. 인증/인가 취약점

```
# 검사 항목
- 하드코딩된 JWT 시크릿
- 약한 비밀번호 정책
- 세션 토큰 노출
- CORS 와일드카드 (*)
- 누락된 인증 미들웨어
```

### 7. 의존성 취약점

```
# 검사 항목
- 알려진 취약한 버전 사용
- 오래된 패키지
- 미검증 소스에서 설치
```

## 적용 프로토콜

### Step 1: 즉시 중단 조건 (CRITICAL)

발견 시 **즉시 작업 중단** 및 경고:

```
⛔ CRITICAL SECURITY ISSUE DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
파일: [파일 경로]:[라인 번호]
유형: [취약점 유형]
심각도: CRITICAL
내용: [발견된 코드]

🚫 작업이 중단되었습니다.
이 보안 이슈를 먼저 해결해주세요.
```

**즉시 중단 대상**:
- 하드코딩된 실제 API 키/비밀번호
- Private Key 노출
- 프로덕션 DB 자격 증명

### Step 2: 경고 조건 (HIGH/MEDIUM)

발견 시 **경고 출력** 후 계속:

```
⚠️ SECURITY WARNING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
파일: [파일 경로]:[라인 번호]
유형: [취약점 유형]
심각도: HIGH / MEDIUM
내용: [발견된 코드]

💡 권장 수정:
[수정 제안]

계속 진행하시겠습니까? (Y/N)
```

### Step 3: 정보 조건 (LOW/INFO)

발견 시 **정보 출력**:

```
ℹ️ SECURITY INFO
파일: [파일 경로]:[라인 번호]
유형: [잠재적 이슈]
권장: [베스트 프랙티스]
```

## 심각도 분류

| 심각도 | 조치 | 예시 |
|--------|------|------|
| **CRITICAL** | 즉시 중단 | 하드코딩된 실제 시크릿, Private Key |
| **HIGH** | 경고 + 확인 | SQL Injection, XSS, 인증 우회 |
| **MEDIUM** | 경고 | 약한 암호화, 누락된 입력 검증 |
| **LOW** | 정보 | 오래된 API 사용, 비효율적 패턴 |
| **INFO** | 정보 | 베스트 프랙티스 권장 |

## 출력 형식

### 전체 검사 결과

```
🔒 보안 검사 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
검사 파일: 42개
발견된 이슈: 5개

⛔ CRITICAL: 1개
  • src/config.ts:15 - 하드코딩된 API 키

⚠️ HIGH: 2개
  • src/api/user.ts:45 - SQL Injection 가능성
  • src/components/Comment.tsx:23 - XSS 위험

🔶 MEDIUM: 1개
  • src/auth/login.ts:67 - 약한 비밀번호 정책

ℹ️ LOW: 1개
  • src/utils/hash.ts:12 - MD5 사용 (SHA-256 권장)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚫 CRITICAL 이슈 해결 필수
```

## 안전한 대안 제시

### 시크릿 관리

```typescript
// ❌ 위험
const API_KEY = "sk-1234567890abcdef";

// ✅ 안전
const API_KEY = process.env.API_KEY;
// 또는
import { getSecret } from '@aws-sdk/client-secrets-manager';
```

### SQL Injection 방지

```typescript
// ❌ 위험
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ 안전 (파라미터화)
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);

// ✅ 안전 (ORM)
await prisma.user.findUnique({ where: { id: userId } });
```

### XSS 방지

```typescript
// ❌ 위험
element.innerHTML = userInput;

// ✅ 안전
element.textContent = userInput;

// ✅ 안전 (React)
<div>{userInput}</div>  // 자동 이스케이핑

// ✅ 안전 (HTML 필요 시)
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

## 자동 적용 규칙

1. **코드 생성 시**: 보안 패턴 자동 적용
2. **코드 수정 시**: 취약점 검사 자동 실행
3. **커밋 전**: 전체 보안 스캔 권장
4. **PR 리뷰 시**: 보안 체크리스트 포함

## 참조 자료

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE Top 25: https://cwe.mitre.org/top25/
- SANS Top 25: https://www.sans.org/top25-software-errors/
