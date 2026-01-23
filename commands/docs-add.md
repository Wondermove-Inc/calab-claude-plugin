# /docs add - 특정 유형 문서 추가

> 특정 유형의 문서를 개별적으로 추가합니다.

## 핵심 원칙

> **각 문서 유형에는 필수 포함 항목이 있습니다. 모든 항목이 충족되어야 완성입니다.**

## 사용법

```bash
/docs add [type]
/docs add [type] "[제목]"
```

## 문서 유형

| 유형 | 설명 | 필수 항목 수 | 저장 위치 |
|------|------|-------------|----------|
| `getting-started` | 시작 가이드 | **15개** | `.claude/docs-site/getting-started/` |
| `architecture` | 아키텍처 문서 | **12개** | `.claude/docs-site/architecture/` |
| `api` | API 레퍼런스 | **20개/엔드포인트** | `.claude/docs-site/api-reference/` |
| `component` | 컴포넌트 문서 | **18개/컴포넌트** | `.claude/docs-site/components/` |
| `guide` | How-to 가이드 | **10개** | `.claude/docs-site/guides/` |
| `config` | 설정 문서 | **8개/옵션** | `.claude/docs-site/configuration/` |
| `faq` | 자주 묻는 질문 | **5개/질문** | `.claude/docs-site/faq.md` |
| `troubleshooting` | 문제 해결 | **6개/이슈** | `.claude/docs-site/troubleshooting.md` |

## 실행 예시

### API 문서 추가

```bash
/docs add api
```

**결과:**
- 프로젝트의 API 엔드포인트 분석
- `.claude/docs-site/api-reference/` 에 문서 생성
- 각 리소스별 엔드포인트 문서화

### 특정 가이드 추가

```bash
/docs add guide "인증 설정하기"
```

**결과:**
- `.claude/docs-site/guides/authentication-setup.md` 생성
- 인증 관련 코드 분석
- 단계별 가이드 작성

### 특정 컴포넌트 문서 추가

```bash
/docs add component "Button"
```

**결과:**
- Button 컴포넌트 분석
- Props, 사용법, 예시 문서화
- `.claude/docs-site/components/button.md` 생성

---

## 유형별 필수 포함 항목 (상세)

### 1. getting-started - 필수 15개 항목

```
□ 프로젝트 한 줄 소개
□ 프로젝트가 해결하는 문제
□ 주요 기능 목록 (최소 5개)
□ 시스템 요구사항 (OS, Node 버전, 메모리 등)
□ 설치 방법 (npm, yarn, pnpm, Docker 모두)
□ 환경별 설정 (Development, Staging, Production)
□ 첫 번째 실행까지의 단계별 가이드
□ 기본 사용 예시 (3개 이상)
□ 예상 결과/출력 스크린샷
□ 흔한 설치 오류 및 해결책 (5개 이상)
□ 프록시/방화벽 환경 설정
□ 오프라인 설치 방법
□ 업그레이드 가이드
□ 롤백 방법
□ 다음 단계 안내
```

**생성 파일:**
```
.claude/docs-site/getting-started/
├── introduction.md      # 소개 + 문제 + 기능
├── installation.md      # 설치 (모든 환경)
├── quick-start.md       # 첫 실행 가이드
└── basic-usage.md       # 사용 예시 + 결과
```

**분석 대상:**
- README.md, package.json, requirements.txt
- 설치 스크립트, Dockerfile
- 예제 코드, 테스트 파일

---

### 2. architecture - 필수 12개 항목

```
□ 시스템 전체 개요 다이어그램 (Mermaid)
□ 핵심 컴포넌트 설명 (각각 상세히)
□ 컴포넌트 간 의존성 다이어그램
□ 데이터 흐름 다이어그램
□ 요청-응답 시퀀스 다이어그램
□ 디렉토리 구조 및 각 폴더 역할
□ 핵심 디자인 패턴 설명
□ 확장 포인트 (어디서 커스터마이징 가능한지)
□ 성능 고려사항
□ 보안 아키텍처
□ 배포 아키텍처 (선택적)
□ 기술 선택 이유 (Why 문서)
```

**생성 파일:**
```
.claude/docs-site/architecture/
├── overview.md          # 전체 개요 + 다이어그램
├── components.md        # 컴포넌트 상세
├── data-flow.md         # 데이터/요청 흐름
├── patterns.md          # 디자인 패턴
└── decisions.md         # 기술 선택 이유
```

**분석 대상:**
- 프로젝트 구조, 의존성 그래프
- 모듈 간 import 관계
- 데이터 모델, 타입 정의

---

### 3. api - 필수 20개 항목 (엔드포인트당)

```
□ 엔드포인트 URL 및 HTTP 메서드
□ 한 줄 설명
□ 상세 설명 (언제 사용하는지)
□ 인증 요구사항 (토큰 타입, 권한 등)
□ Rate Limiting 정보
□ Path 파라미터 (타입, 필수여부, 설명, 예시)
□ Query 파라미터 (타입, 필수여부, 기본값, 유효값 범위)
□ Request Header (필수/선택)
□ Request Body 전체 스키마 (중첩 객체 포함)
□ 각 필드별 유효성 검사 규칙
□ 성공 응답 (200, 201 등) 전체 스키마
□ 에러 응답 (400, 401, 403, 404, 500) 각각의 스키마
□ 에러 코드별 원인 및 해결 방법
□ curl 예시
□ JavaScript/TypeScript 예시
□ Python 예시 (선택적)
□ 페이지네이션 방식 (있는 경우)
□ 필터링/정렬 옵션 (있는 경우)
□ Webhook 연동 (있는 경우)
□ Deprecation 정보 (있는 경우)
```

**생성 파일:**
```
.claude/docs-site/api-reference/
├── overview.md          # API 개요 + 공통사항
├── authentication.md    # 인증 상세
├── endpoints/           # 엔드포인트별
│   ├── users.md        # 20개 항목 모두 포함
│   ├── products.md
│   └── ...
├── types.md             # 전체 타입 정의
└── errors.md            # 에러 코드 + 해결법
```

**엔드포인트 문서 예시 구조:**
```markdown
## POST /api/users

새로운 사용자를 생성합니다.

### 언제 사용하나요?
회원가입, 관리자의 사용자 추가 시 사용합니다.

### 인증
| 항목 | 값 |
|------|---|
| 필수 | Yes |
| 토큰 타입 | Bearer JWT |
| 필요 권한 | `users:create` |

### Rate Limit
- 인증된 요청: 100 req/min
- 미인증 요청: 10 req/min

### Request Body

| 필드 | 타입 | 필수 | 설명 | 유효성 검사 |
|------|------|------|------|------------|
| email | string | Yes | 사용자 이메일 | RFC 5322, 최대 255자 |
| name | string | Yes | 사용자 이름 | 2-100자, 특수문자 불가 |
| role | enum | No | 역할 | `admin`, `user`, `guest` |

### 응답

**201 Created**
\`\`\`json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "createdAt": "2024-01-20T10:30:00Z"
}
\`\`\`

**400 Bad Request**
\`\`\`json
{
  "error": "VALIDATION_ERROR",
  "message": "이메일 형식이 올바르지 않습니다",
  "field": "email"
}
\`\`\`

### 코드 예시

**curl**
\`\`\`bash
curl -X POST https://api.example.com/users \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"email": "user@example.com", "name": "John"}'
\`\`\`

**TypeScript**
\`\`\`typescript
import { createUser } from '@/api/users';

const user = await createUser({
  email: 'user@example.com',
  name: 'John'
});
\`\`\`
```

---

### 4. component - 필수 18개 항목 (컴포넌트당)

```
□ 컴포넌트 이름 및 한 줄 설명
□ 언제 사용하는지 (Use Cases)
□ 언제 사용하지 말아야 하는지
□ 설치/Import 방법
□ 기본 사용 예시
□ 모든 Props 테이블 (타입, 기본값, 필수, 상세 설명)
□ 복합 타입 Props의 상세 스키마
□ 조건부 Props 설명 (A가 있으면 B 필수 등)
□ 모든 이벤트/콜백 목록 및 파라미터
□ Slots/Children 사용법
□ Ref로 접근 가능한 메서드
□ CSS Variables 목록
□ 커스텀 Class Names
□ 테마/변형(Variants) 예시
□ 제어/비제어 컴포넌트 패턴
□ 접근성(a11y) 정보 (ARIA, 키보드 내비게이션)
□ 성능 최적화 팁 (memo, useCallback 등)
□ 관련 컴포넌트 링크
```

**생성 파일:**
```
.claude/docs-site/components/
└── [component-name].md   # 18개 항목 모두 포함
```

**컴포넌트 문서 예시 구조:**
```markdown
# Button

클릭 가능한 버튼 컴포넌트입니다.

## 언제 사용하나요?
- 폼 제출
- 액션 트리거
- 네비게이션 (보조)

## 언제 사용하지 말아야 하나요?
- 링크로 이동할 때 → `<Link>` 사용
- 토글 상태 관리 → `<Toggle>` 사용

## Import

\`\`\`tsx
import { Button } from '@/components/ui/button';
\`\`\`

## 기본 예시

\`\`\`tsx
<Button onClick={handleClick}>
  Click me
</Button>
\`\`\`

## Props

| Prop | 타입 | 기본값 | 필수 | 설명 |
|------|------|--------|------|------|
| variant | `'default' \| 'destructive' \| 'outline' \| 'ghost'` | `'default'` | No | 버튼 스타일 변형 |
| size | `'sm' \| 'md' \| 'lg'` | `'md'` | No | 버튼 크기 |
| disabled | `boolean` | `false` | No | 비활성화 상태 |
| loading | `boolean` | `false` | No | 로딩 상태 (spinner 표시) |
| asChild | `boolean` | `false` | No | 자식 요소로 렌더링 |

### 복합 타입 상세

**variant 값별 스타일:**
- `default`: 주요 액션, 파란색 배경
- `destructive`: 삭제 등 위험 액션, 빨간색
- `outline`: 보조 액션, 테두리만
- `ghost`: 최소 강조, 배경 없음

## 이벤트

| 이벤트 | 파라미터 | 설명 |
|--------|----------|------|
| onClick | `(event: MouseEvent) => void` | 클릭 시 |
| onFocus | `(event: FocusEvent) => void` | 포커스 시 |
| onBlur | `(event: FocusEvent) => void` | 포커스 해제 시 |

## CSS Variables

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `--button-bg` | `hsl(var(--primary))` | 배경색 |
| `--button-text` | `hsl(var(--primary-foreground))` | 텍스트색 |
| `--button-radius` | `var(--radius)` | 모서리 둥글기 |

## 접근성

- **키보드**: Enter, Space로 활성화
- **ARIA**: `role="button"` 자동 설정
- **포커스 인디케이터**: 기본 제공

## 예시

### 모든 Variants

\`\`\`tsx
<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Cancel</Button>
<Button variant="ghost">More</Button>
\`\`\`

### 로딩 상태

\`\`\`tsx
<Button loading disabled>
  Saving...
</Button>
\`\`\`

## 관련 컴포넌트

- [IconButton](./icon-button.md) - 아이콘만 있는 버튼
- [ButtonGroup](./button-group.md) - 버튼 그룹
- [Link](./link.md) - 네비게이션용
```

---

### 5. guide - 필수 10개 항목

```
□ 가이드 목적 한 줄 설명
□ 이 가이드가 필요한 상황
□ 사전 요구사항 체크리스트
□ 예상 소요 시간
□ 단계별 절차 (각 단계에 코드 예시)
□ 각 단계별 예상 결과
□ 흔한 실수 및 해결책
□ 고급 옵션/커스터마이징
□ 완료 후 검증 방법
□ 다음 단계/관련 가이드
```

**생성 파일:**
```
.claude/docs-site/guides/
└── [guide-name].md   # 10개 항목 모두 포함
```

**가이드 예시 구조:**
```markdown
# 인증 설정하기

OAuth 2.0을 사용한 사용자 인증을 설정합니다.

## 이 가이드가 필요한 상황

- 새 프로젝트에 로그인 기능 추가
- 기존 세션 인증을 OAuth로 마이그레이션

## 사전 요구사항

- [ ] Node.js 18+ 설치됨
- [ ] OAuth 제공자 앱 등록 완료 (Client ID, Secret)
- [ ] 데이터베이스 연결 설정됨

## 예상 소요 시간

약 30분

## 단계

### 1단계: 패키지 설치

\`\`\`bash
npm install next-auth @auth/prisma-adapter
\`\`\`

**예상 결과:**
\`\`\`
added 45 packages in 3s
\`\`\`

### 2단계: 환경 변수 설정

\`\`\`bash
# .env.local
NEXTAUTH_SECRET=your-secret
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
\`\`\`

...(계속)

## 흔한 실수 및 해결책

| 실수 | 원인 | 해결책 |
|------|------|--------|
| "Invalid redirect_uri" | 콜백 URL 미등록 | OAuth 앱에서 URL 추가 |
| 세션 유지 안됨 | NEXTAUTH_SECRET 미설정 | 환경 변수 확인 |

## 완료 후 검증

\`\`\`bash
# 로그인 페이지 접속
open http://localhost:3000/api/auth/signin
\`\`\`

## 다음 단계

- [권한 관리 설정하기](./authorization.md)
- [소셜 로그인 추가하기](./social-login.md)
```

---

### 6. config - 필수 8개 항목 (옵션당)

```
□ 옵션 이름
□ 타입 및 기본값
□ 설명 (무엇을 제어하는지)
□ 유효한 값 범위/목록
□ 환경별 권장값 (dev/staging/prod)
□ 관련된 다른 옵션
□ 설정 예시 (최소 2개)
□ 잘못 설정 시 발생하는 문제
```

**생성 파일:**
```
.claude/docs-site/configuration/
├── environment.md       # 환경 변수 (8개 항목/변수)
└── options.md           # 설정 옵션 (8개 항목/옵션)
```

**설정 문서 예시:**
```markdown
# 환경 변수

## DATABASE_URL

데이터베이스 연결 문자열입니다.

| 항목 | 값 |
|------|---|
| 타입 | `string` |
| 기본값 | 없음 (필수) |
| 유효값 | PostgreSQL/MySQL 연결 문자열 |

### 환경별 권장값

| 환경 | 값 |
|------|---|
| Development | `postgresql://localhost:5432/myapp_dev` |
| Staging | `postgresql://staging-db:5432/myapp_staging` |
| Production | `postgresql://prod-db:5432/myapp?ssl=true&pool=10` |

### 관련 옵션

- `DATABASE_POOL_SIZE` - 커넥션 풀 크기
- `DATABASE_SSL` - SSL 사용 여부

### 설정 예시

**개발 환경:**
\`\`\`bash
DATABASE_URL=postgresql://user:pass@localhost:5432/myapp
\`\`\`

**프로덕션 (Connection Pooling):**
\`\`\`bash
DATABASE_URL=postgresql://user:pass@db.example.com:5432/myapp?ssl=true&connection_limit=10
\`\`\`

### 잘못된 설정 시 문제

| 증상 | 원인 | 해결 |
|------|------|------|
| "Connection refused" | 호스트/포트 오류 | 주소 확인 |
| "Authentication failed" | 자격증명 오류 | user:pass 확인 |
| "Too many connections" | pool 미설정 | connection_limit 추가 |
```

---

### 7. faq - 필수 5개 항목 (질문당)

```
□ 질문 (자연스러운 문장)
□ 짧은 답변 (1-2문장)
□ 상세 설명 (필요시)
□ 코드 예시 (해당시)
□ 관련 문서 링크
```

**생성 파일:**
```
.claude/docs-site/faq.md
```

**FAQ 예시:**
```markdown
# 자주 묻는 질문

## 일반

### 이 프로젝트는 어떤 문제를 해결하나요?

**짧은 답변:** 대규모 데이터 처리 파이프라인을 간단하게 구축할 수 있게 합니다.

**상세:** 기존에는 Spark + Airflow + Kafka를 각각 설정해야 했지만,
이 프로젝트는 통합된 인터페이스로 이를 추상화합니다.

**관련 문서:** [아키텍처 개요](./architecture/overview.md)

---

### TypeScript 대신 JavaScript를 사용할 수 있나요?

**짧은 답변:** 가능하지만, TypeScript를 권장합니다.

**상세:** JavaScript로 작성할 수 있지만, 타입 안전성과 IDE 지원을 위해
TypeScript 사용을 강력히 권장합니다.

**설정 방법:**
\`\`\`javascript
// jsconfig.json
{
  "compilerOptions": {
    "checkJs": true
  }
}
\`\`\`

**관련 문서:** [설치 가이드](./getting-started/installation.md)
```

---

### 8. troubleshooting - 필수 6개 항목 (이슈당)

```
□ 에러 메시지/증상
□ 발생 원인 (가능한 모든 원인)
□ 진단 방법
□ 해결 방법 (단계별)
□ 해결 코드 예시
□ 예방 방법
```

**생성 파일:**
```
.claude/docs-site/troubleshooting.md
```

**Troubleshooting 예시:**
```markdown
# 문제 해결

## 설치 관련

### "EACCES: permission denied" 오류

**에러 메시지:**
\`\`\`
npm ERR! Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules'
\`\`\`

**원인:**
1. npm 글로벌 디렉토리 권한 문제
2. sudo로 npm 설치 후 일반 사용자로 실행
3. nvm 미사용 환경

**진단 방법:**
\`\`\`bash
ls -la /usr/local/lib/node_modules
npm config get prefix
\`\`\`

**해결 방법:**

**방법 1: npm 디렉토리 변경 (권장)**
\`\`\`bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
\`\`\`

**방법 2: nvm 사용**
\`\`\`bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
\`\`\`

**예방 방법:**
- 처음부터 nvm을 사용하여 Node.js 설치
- sudo로 npm install 절대 사용 금지
```

## 실행 결과

```
📝 문서 추가: api

[1/3] API 엔드포인트 분석 중...
  ✓ 라우터 파일 15개 발견
  ✓ 엔드포인트 48개 발견
  ✓ 타입 정의 32개 발견

[2/3] 문서 작성 중...
  ✓ overview.md
  ✓ authentication.md
  ✓ endpoints/users.md
  ✓ endpoints/products.md
  ✓ endpoints/orders.md
  ... (12개 더)
  ✓ types.md
  ✓ errors.md

[3/3] 검증 중...
  ✓ 코드 예시 검증 완료

✅ API 문서 추가 완료

📊 생성 요약:
  - 문서: 17개
  - 위치: .claude/docs-site/api-reference/
```

## 옵션

```bash
# 기존 문서 덮어쓰기
/docs add api --force

# 특정 파일만 대상
/docs add component --file=src/components/Button.tsx
```
