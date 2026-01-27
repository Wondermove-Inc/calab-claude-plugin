# Security Best Practices

> 보안 코딩 가이드라인 및 취약점 방지

## OWASP Top 10 체크리스트

### 1. Injection (A01:2021)

**SQL Injection 방지:**
```typescript
// Bad
const query = `SELECT * FROM users WHERE id = ${userId}`;

// Good - Parameterized Query
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

**Command Injection 방지:**
```typescript
// Bad
exec(`rm -rf ${userInput}`);

// Good - Sanitize input
const sanitized = userInput.replace(/[;&|`$]/g, '');
```

### 2. Broken Authentication (A07:2021)

**세션 관리:**
- 강력한 세션 ID 생성 (최소 128비트 엔트로피)
- 로그인 후 세션 ID 재생성
- 적절한 세션 만료 시간 설정
- httpOnly, secure 플래그 사용

**비밀번호 정책:**
```typescript
// 최소 요구사항
const passwordPolicy = {
  minLength: 12,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: true,
};
```

### 3. Sensitive Data Exposure (A02:2021)

**민감 데이터 처리:**
```typescript
// 로깅에서 민감 정보 제외
const sanitizeForLog = (data: any) => {
  const sensitive = ['password', 'token', 'secret', 'key', 'credit'];
  return JSON.stringify(data, (key, value) =>
    sensitive.some(s => key.toLowerCase().includes(s)) ? '[REDACTED]' : value
  );
};
```

**암호화:**
- 전송 중: TLS 1.2+ 필수
- 저장 시: AES-256 권장
- 비밀번호: bcrypt, argon2 사용

### 4. XML External Entities (A05:2021)

**XXE 방지:**
```typescript
// XML 파서 설정
const parser = new DOMParser();
parser.setFeature('http://xml.org/sax/features/external-general-entities', false);
parser.setFeature('http://xml.org/sax/features/external-parameter-entities', false);
```

### 5. Broken Access Control (A01:2021)

**권한 검사:**
```typescript
// 모든 민감한 작업 전 권한 확인
async function deleteUser(requesterId: string, targetId: string) {
  const requester = await getUser(requesterId);

  if (!requester.isAdmin && requesterId !== targetId) {
    throw new ForbiddenError('권한 없음');
  }

  // 삭제 진행
}
```

### 6. Security Misconfiguration (A05:2021)

**환경 설정:**
```typescript
// 프로덕션 환경 체크리스트
const securityConfig = {
  // 디버그 모드 비활성화
  debug: process.env.NODE_ENV !== 'production',

  // 에러 상세 정보 숨김
  exposeStackTraces: false,

  // 보안 헤더 활성화
  helmet: {
    contentSecurityPolicy: true,
    xssFilter: true,
    noSniff: true,
    frameguard: { action: 'deny' },
  },
};
```

### 7. Cross-Site Scripting (A03:2021)

**XSS 방지:**
```typescript
// HTML 이스케이프
const escapeHtml = (str: string): string => {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;',
  };
  return str.replace(/[&<>"']/g, m => map[m]);
};

// React에서 dangerouslySetInnerHTML 주의
// Bad
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// Good
<div>{sanitizedContent}</div>
```

### 8. Insecure Deserialization (A08:2021)

**역직렬화 주의:**
```typescript
// JSON.parse 전 검증
const safeJsonParse = (str: string) => {
  try {
    const parsed = JSON.parse(str);
    // 스키마 검증
    if (!isValidSchema(parsed)) {
      throw new Error('Invalid schema');
    }
    return parsed;
  } catch (e) {
    throw new Error('Invalid JSON');
  }
};
```

### 9. Using Components with Known Vulnerabilities (A06:2021)

**의존성 관리:**
```bash
# 정기적인 취약점 스캔
npm audit
yarn audit

# 자동 업데이트
npm update
```

### 10. Insufficient Logging & Monitoring (A09:2021)

**보안 로깅:**
```typescript
const securityLogger = {
  loginAttempt: (userId: string, success: boolean, ip: string) => {
    log.info('LOGIN_ATTEMPT', { userId, success, ip, timestamp: new Date() });
  },

  privilegedAction: (userId: string, action: string, target: string) => {
    log.info('PRIVILEGED_ACTION', { userId, action, target, timestamp: new Date() });
  },

  suspiciousActivity: (details: any) => {
    log.warn('SUSPICIOUS_ACTIVITY', { ...details, timestamp: new Date() });
  },
};
```

## 시크릿 관리

### 금지 사항

```typescript
// 절대 금지
const API_KEY = 'sk-1234567890abcdef';  // 하드코딩 금지
const password = 'admin123';             // 평문 저장 금지
```

### 권장 사항

```typescript
// 환경 변수 사용
const API_KEY = process.env.API_KEY;

// 시크릿 매니저 사용
const secret = await secretManager.getSecret('api-key');

// .env 파일은 .gitignore에 추가
```

## 파일 보호

### 민감 파일 패턴

```
.env
.env.*
*.pem
*.key
*credentials*
*secret*
*password*
config/production.json
```

### .gitignore 필수 항목

```gitignore
# 환경 설정
.env
.env.local
.env.production

# 인증서 및 키
*.pem
*.key
*.p12

# 설정 파일
config/secrets.json
credentials/
```

## API 보안

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15분
  max: 100, // IP당 최대 요청
  message: 'Too many requests',
});

app.use('/api/', limiter);
```

### CORS 설정

```typescript
const corsOptions = {
  origin: ['https://trusted-domain.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
};
```

## 참조

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
