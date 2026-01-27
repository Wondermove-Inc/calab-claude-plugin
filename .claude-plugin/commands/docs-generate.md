---
description: 전체 문서를 자동 생성합니다. 프로젝트를 분석하여 극도로 상세한 문서 콘텐츠를 생성합니다.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [--all | --api | --components | --architecture]
---

# /docs generate - 전체 문서 자동 생성

> 프로젝트를 분석하여 **극도로 상세한** 전체 문서 콘텐츠를 자동으로 생성합니다.

## 핵심 원칙

> **모든 문서는 독자가 추가 질문 없이 완벽하게 이해하고 사용할 수 있어야 합니다.**

- 모든 파라미터, 옵션, 반환값, 에러 케이스 문서화
- 기능당 최소 4개 코드 예시 (기본, 실전, 고급, 에러처리)
- 모든 코드는 복사-붙여넣기로 즉시 실행 가능
- **Mermaid 다이어그램**으로 복잡한 구조/흐름 시각화 필수
- **이미지 플레이스홀더**로 스크린샷 필요 위치 명시

---

## 시각화 규칙 (필수)

### Mermaid 다이어그램

> **복잡한 개념은 반드시 다이어그램으로 시각화합니다.**

**필수 다이어그램:**
| 문서 | 필수 다이어그램 |
|------|----------------|
| Architecture | 시스템 개요, 컴포넌트 의존성, 데이터 흐름, 시퀀스 |
| API | 인증 흐름, 요청-응답 시퀀스 |
| Guide | 프로세스 흐름, 상태 전이 |
| Component | 컴포넌트 계층, 상태 머신 |

**가독성 규칙 (필수 준수):**
```
🎨 색상 대비 원칙:
- 어두운 배경 → 밝은 글자 (#ffffff, #fef3c7, #e0f2fe)
- 밝은 배경 → 어두운 글자 (#1e293b, #166534, #92400e)
```

**권장 스타일:**
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#4f46e5',
  'primaryTextColor': '#ffffff',
  'secondaryColor': '#f0fdf4',
  'tertiaryColor': '#fef3c7'
}}}%%
```

### 이미지 플레이스홀더

> **실제 스크린샷이 필요한 위치에 명시적으로 표기합니다.**

**플레이스홀더 형식:**
```markdown
<!-- 📸 스크린샷 필요: [설명] -->
![스크린샷: 설명](./images/category/filename.png)
*캡션: [상세 설명]*
```

**필수 스크린샷:**
- 설치 완료 화면
- 초기 실행 화면
- UI 컴포넌트 변형들
- 에러 메시지 화면
- 대시보드/메인 화면

---

## 실행 단계

### 1단계: 프로젝트 심층 분석

```
[분석 항목]
├── 기술 스택 (package.json, requirements.txt 등)
├── 프로젝트 구조 (디렉토리, 파일 패턴)
├── API 엔드포인트 (라우터, 컨트롤러, 미들웨어)
│   ├── 모든 HTTP 메서드
│   ├── 모든 파라미터 (path, query, body)
│   ├── 모든 응답 타입
│   └── 에러 핸들링 패턴
├── 컴포넌트 (React, Vue 등)
│   ├── 모든 Props 정의
│   ├── 모든 이벤트/콜백
│   ├── Ref 메서드
│   └── 스타일 옵션
├── 타입 정의 (TypeScript, Python 타입 힌트)
├── 설정 파일 (환경 변수, 설정 옵션)
├── 기존 문서 (README, CHANGELOG, JSDoc 등)
└── 테스트 파일 (테스트 케이스에서 사용 패턴 추출)
```

### 2단계: 문서 구조 생성

`.claude/docs-site/` 폴더에 문서 구조를 생성합니다:

```
.claude/docs-site/
├── images/                      # 📸 스크린샷 저장 폴더
│   ├── getting-started/         # 시작하기 관련 이미지
│   ├── architecture/            # 아키텍처 관련 이미지
│   ├── components/              # 컴포넌트 관련 이미지
│   └── guides/                  # 가이드 관련 이미지
├── getting-started/
│   ├── introduction.md          # 프로젝트 소개 (필수 15개 항목)
│   ├── installation.md          # 설치 가이드 + 📸 설치 결과 스크린샷
│   ├── quick-start.md           # 빠른 시작 + 📸 실행 결과 스크린샷
│   └── basic-usage.md           # 기본 사용법
├── architecture/
│   ├── overview.md              # 시스템 개요 (필수 12개 항목) + Mermaid 필수
│   ├── components.md            # 컴포넌트 구조 + Mermaid 의존성 다이어그램
│   ├── data-flow.md             # 데이터 흐름 + Mermaid 시퀀스 다이어그램
│   └── diagrams.md              # 아키텍처 다이어그램 모음
├── api-reference/
│   ├── overview.md              # API 개요 + Mermaid 인증 흐름
│   ├── authentication.md        # 인증 상세 + Mermaid 시퀀스
│   ├── endpoints/               # 엔드포인트별 문서 (필수 20개 항목/엔드포인트)
│   │   └── [resource].md
│   ├── types.md                 # 타입 정의
│   └── errors.md                # 에러 코드 전체
├── components/
│   └── [component-name].md      # 컴포넌트별 문서 (필수 18개 항목) + 📸 UI 스크린샷
├── guides/
│   └── [guide-name].md          # 기능별 가이드 (필수 10개 항목) + Mermaid 흐름도
├── configuration/
│   ├── environment.md           # 환경 변수 (필수 8개 항목/옵션)
│   └── options.md               # 설정 옵션
├── faq.md                       # 자주 묻는 질문
├── troubleshooting.md           # 문제 해결 + 📸 에러 화면 스크린샷
└── index.md                     # 문서 인덱스
```

---

## 상세 문서 템플릿

### Getting Started - Installation (설치 가이드)

```markdown
# 설치 가이드

> [프로젝트명]을 설치하고 실행하는 완벽한 가이드입니다.

## 시스템 요구사항

| 항목 | 최소 요구사항 | 권장 사양 |
|------|-------------|----------|
| Node.js | v18.0.0 이상 | v20.x LTS |
| npm/yarn | npm 9.x / yarn 1.22.x | 최신 버전 |
| OS | Windows 10, macOS 12, Ubuntu 20.04 | - |
| 메모리 | 4GB RAM | 8GB RAM |
| 디스크 | 500MB 여유 공간 | 1GB 여유 공간 |

## 설치 방법

### npm 사용

```bash
# 전역 설치
npm install -g [패키지명]

# 프로젝트 로컬 설치
npm install [패키지명]

# 개발 의존성으로 설치
npm install -D [패키지명]
```

### yarn 사용

```bash
# 전역 설치
yarn global add [패키지명]

# 프로젝트 로컬 설치
yarn add [패키지명]

# 개발 의존성으로 설치
yarn add -D [패키지명]
```

### pnpm 사용

```bash
# 전역 설치
pnpm add -g [패키지명]

# 프로젝트 로컬 설치
pnpm add [패키지명]
```

### Docker 사용

```bash
# 이미지 다운로드
docker pull [이미지명]:latest

# 컨테이너 실행
docker run -d \
  --name [컨테이너명] \
  -p 3000:3000 \
  -v $(pwd)/data:/app/data \
  -e NODE_ENV=production \
  [이미지명]:latest
```

## 환경별 설정

### Development (개발)

```bash
# .env.development
NODE_ENV=development
API_URL=http://localhost:3000
DEBUG=true
LOG_LEVEL=debug
```

### Staging (스테이징)

```bash
# .env.staging
NODE_ENV=staging
API_URL=https://staging-api.example.com
DEBUG=false
LOG_LEVEL=info
```

### Production (프로덕션)

```bash
# .env.production
NODE_ENV=production
API_URL=https://api.example.com
DEBUG=false
LOG_LEVEL=error
```

## 설치 확인

```bash
# 버전 확인
[명령어] --version
# 예상 출력: v1.2.3

# 헬스 체크
[명령어] health
# 예상 출력: ✓ All systems operational
```

## 흔한 설치 오류 및 해결책

### 1. EACCES 권한 오류

**증상:**
```
npm ERR! Error: EACCES: permission denied, access '/usr/local/lib/node_modules'
```

**원인:** npm 글로벌 디렉토리에 쓰기 권한 없음

**해결:**
```bash
# 방법 1: npm 디렉토리 권한 변경
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 방법 2: nvm 사용 (권장)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
```

### 2. ENOENT 파일 없음 오류

**증상:**
```
npm ERR! enoent ENOENT: no such file or directory, open 'package.json'
```

**원인:** package.json이 없는 디렉토리에서 실행

**해결:**
```bash
# 프로젝트 루트로 이동
cd /path/to/your/project

# 또는 새 프로젝트 초기화
npm init -y
```

### 3. 네트워크 타임아웃

**증상:**
```
npm ERR! network timeout
```

**원인:** 네트워크 연결 문제 또는 레지스트리 접근 불가

**해결:**
```bash
# 레지스트리 변경
npm config set registry https://registry.npmmirror.com

# 타임아웃 늘리기
npm config set fetch-timeout 60000
```

### 4. 버전 충돌

**증상:**
```
npm ERR! peer dep missing: react@^18.0.0, required by [패키지명]
```

**원인:** 피어 의존성 버전 불일치

**해결:**
```bash
# 강제 설치 (권장하지 않음)
npm install --legacy-peer-deps

# 의존성 버전 맞추기 (권장)
npm install react@18
```

### 5. node-gyp 빌드 실패

**증상:**
```
gyp ERR! build error
```

**원인:** 네이티브 모듈 컴파일 도구 없음

**해결:**
```bash
# Windows
npm install --global windows-build-tools

# macOS
xcode-select --install

# Ubuntu
sudo apt-get install build-essential
```

## 프록시/방화벽 환경

### 프록시 설정

```bash
# HTTP 프록시
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080

# 인증이 필요한 경우
npm config set proxy http://user:password@proxy.company.com:8080
```

### SSL 인증서 문제

```bash
# 자체 서명 인증서 허용 (보안 주의)
npm config set strict-ssl false

# 또는 CA 인증서 지정
npm config set cafile /path/to/certificate.pem
```

## 오프라인 설치

```bash
# 온라인 환경에서 패키지 다운로드
npm pack [패키지명]

# 오프라인 환경에서 설치
npm install ./[패키지명]-1.2.3.tgz
```

## 업그레이드 가이드

### 마이너 버전 업그레이드 (1.2.x → 1.3.x)

```bash
npm update [패키지명]
```

### 메이저 버전 업그레이드 (1.x → 2.x)

1. 릴리즈 노트 확인
2. Breaking Changes 검토
3. 테스트 환경에서 먼저 업그레이드
4. 마이그레이션 스크립트 실행 (필요시)

```bash
npm install [패키지명]@latest
npx [패키지명] migrate
```

## 롤백 방법

```bash
# 이전 버전으로 롤백
npm install [패키지명]@1.2.3

# package-lock.json으로 정확한 버전 복원
git checkout HEAD~1 -- package-lock.json
npm ci
```

## 다음 단계

- [빠른 시작](./quick-start.md) - 5분 안에 첫 번째 기능 실행하기
- [기본 사용법](./basic-usage.md) - 핵심 기능 사용법 익히기
- [설정 가이드](../configuration/environment.md) - 상세 설정 옵션
```

---

### API Reference - Endpoint (상세 템플릿)

```markdown
# Users API

> 사용자 계정을 생성, 조회, 수정, 삭제하는 API입니다.

## 개요

Users API를 사용하면 애플리케이션의 사용자를 관리할 수 있습니다.
사용자 생성 시 자동으로 환영 이메일이 발송됩니다.

## 인증

모든 Users API는 Bearer 토큰 인증이 필요합니다.

```http
Authorization: Bearer your-api-token-here
```

**필요한 권한:**
- `users:read` - 사용자 조회
- `users:write` - 사용자 생성/수정
- `users:delete` - 사용자 삭제

## Rate Limiting

| 엔드포인트 | 제한 | 윈도우 |
|-----------|------|--------|
| GET /users | 100 req | 1분 |
| POST /users | 10 req | 1분 |
| PUT /users/:id | 30 req | 1분 |
| DELETE /users/:id | 5 req | 1분 |

Rate limit 초과 시 `429 Too Many Requests` 응답과 함께
`Retry-After` 헤더가 반환됩니다.

---

## POST /api/users - 사용자 생성

새 사용자 계정을 생성합니다.

### 요청

```http
POST /api/users
Authorization: Bearer {token}
Content-Type: application/json
```

### Request Body

| 필드 | 타입 | 필수 | 설명 | 유효성 검사 |
|------|------|------|------|-------------|
| email | string | ✓ | 사용자 이메일 | 유효한 이메일 형식, 최대 255자 |
| password | string | ✓ | 비밀번호 | 최소 8자, 대/소/숫자/특수문자 포함 |
| name | string | ✓ | 사용자 이름 | 2-50자, 특수문자 불가 |
| role | string | - | 역할 | `admin`, `user`, `guest` 중 하나. 기본값: `user` |
| metadata | object | - | 추가 정보 | 최대 10개 키, 각 값 최대 1000자 |

**metadata 스키마:**
```typescript
interface Metadata {
  [key: string]: string | number | boolean;
}
```

### 성공 응답 (201 Created)

```json
{
  "success": true,
  "data": {
    "id": "usr_abc123def456",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "metadata": {},
    "emailVerified": false,
    "createdAt": "2024-01-20T10:30:00.000Z",
    "updatedAt": "2024-01-20T10:30:00.000Z"
  }
}
```

### 에러 응답

#### 400 Bad Request - 유효성 검사 실패

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "입력값이 유효하지 않습니다.",
    "details": [
      {
        "field": "email",
        "message": "유효한 이메일 형식이 아닙니다."
      },
      {
        "field": "password",
        "message": "비밀번호는 최소 8자 이상이어야 합니다."
      }
    ]
  }
}
```

#### 401 Unauthorized - 인증 실패

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "유효하지 않은 인증 토큰입니다."
  }
}
```

#### 403 Forbidden - 권한 없음

```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "이 작업을 수행할 권한이 없습니다.",
    "requiredPermission": "users:write"
  }
}
```

#### 409 Conflict - 중복 이메일

```json
{
  "success": false,
  "error": {
    "code": "USER_EXISTS",
    "message": "이미 등록된 이메일입니다.",
    "field": "email"
  }
}
```

#### 500 Internal Server Error

```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "서버 오류가 발생했습니다.",
    "requestId": "req_xyz789"
  }
}
```

### 코드 예시

#### curl

```bash
curl -X POST https://api.example.com/api/users \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecureP@ss123",
    "name": "John Doe",
    "role": "user"
  }'
```

#### JavaScript/TypeScript

```typescript
import { ApiClient } from '@example/sdk';

const client = new ApiClient({ token: 'your-token' });

// 기본 예시
async function createUserBasic() {
  const user = await client.users.create({
    email: 'user@example.com',
    password: 'SecureP@ss123',
    name: 'John Doe',
  });
  console.log('Created user:', user.id);
}

// 실전 예시 - 모든 옵션 사용
async function createUserAdvanced() {
  const user = await client.users.create({
    email: 'admin@example.com',
    password: 'SecureP@ss123',
    name: 'Admin User',
    role: 'admin',
    metadata: {
      department: 'Engineering',
      employeeId: 'EMP001',
    },
  });

  // 이메일 인증 링크 발송
  await client.users.sendVerificationEmail(user.id);

  return user;
}

// 에러 처리 예시
async function createUserWithErrorHandling() {
  try {
    const user = await client.users.create({
      email: 'user@example.com',
      password: 'weak',  // 유효성 검사 실패할 예시
      name: 'John',
    });
    return user;
  } catch (error) {
    if (error.code === 'VALIDATION_ERROR') {
      console.error('입력값 오류:', error.details);
      // 사용자에게 구체적인 오류 표시
      error.details.forEach(d => {
        console.error(`- ${d.field}: ${d.message}`);
      });
    } else if (error.code === 'USER_EXISTS') {
      console.error('이미 존재하는 이메일입니다.');
      // 로그인 페이지로 리다이렉트
    } else {
      console.error('알 수 없는 오류:', error.message);
      // 에러 리포팅 서비스로 전송
    }
    throw error;
  }
}

// 배치 생성 예시 (고급)
async function createUsersBatch(users: CreateUserInput[]) {
  const results = await Promise.allSettled(
    users.map(user => client.users.create(user))
  );

  const succeeded = results.filter(r => r.status === 'fulfilled');
  const failed = results.filter(r => r.status === 'rejected');

  console.log(`성공: ${succeeded.length}, 실패: ${failed.length}`);

  return { succeeded, failed };
}
```

#### Python

```python
from example_sdk import ApiClient, ApiError

client = ApiClient(token="your-token")

# 기본 예시
def create_user_basic():
    user = client.users.create(
        email="user@example.com",
        password="SecureP@ss123",
        name="John Doe"
    )
    print(f"Created user: {user.id}")
    return user

# 에러 처리 예시
def create_user_with_error_handling():
    try:
        user = client.users.create(
            email="user@example.com",
            password="SecureP@ss123",
            name="John Doe"
        )
        return user
    except ApiError as e:
        if e.code == "USER_EXISTS":
            print("이미 존재하는 이메일입니다.")
        elif e.code == "VALIDATION_ERROR":
            for detail in e.details:
                print(f"- {detail['field']}: {detail['message']}")
        raise
```

---

## GET /api/users - 사용자 목록 조회

등록된 사용자 목록을 페이지네이션하여 조회합니다.

### 요청

```http
GET /api/users?page=1&limit=20&role=user&sort=-createdAt
Authorization: Bearer {token}
```

### Query Parameters

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| page | number | - | 1 | 페이지 번호 (1부터 시작) |
| limit | number | - | 20 | 페이지당 항목 수 (최대 100) |
| role | string | - | - | 역할로 필터링: `admin`, `user`, `guest` |
| search | string | - | - | 이름 또는 이메일로 검색 |
| sort | string | - | `-createdAt` | 정렬 기준. `-`는 내림차순 |
| createdAfter | ISO8601 | - | - | 특정 날짜 이후 생성된 사용자 |
| createdBefore | ISO8601 | - | - | 특정 날짜 이전 생성된 사용자 |

**정렬 가능 필드:**
- `createdAt` - 생성일
- `updatedAt` - 수정일
- `name` - 이름
- `email` - 이메일

### 성공 응답 (200 OK)

```json
{
  "success": true,
  "data": [
    {
      "id": "usr_abc123",
      "email": "user1@example.com",
      "name": "User One",
      "role": "user",
      "createdAt": "2024-01-20T10:30:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8,
    "hasNext": true,
    "hasPrev": false
  }
}
```

### 코드 예시

```typescript
// 기본 조회
const users = await client.users.list();

// 필터링 및 정렬
const adminUsers = await client.users.list({
  role: 'admin',
  sort: '-createdAt',
  limit: 50,
});

// 검색
const searchResults = await client.users.list({
  search: 'john',
});

// 전체 목록 순회 (페이지네이션 처리)
async function* getAllUsers() {
  let page = 1;
  let hasNext = true;

  while (hasNext) {
    const result = await client.users.list({ page, limit: 100 });
    yield* result.data;
    hasNext = result.pagination.hasNext;
    page++;
  }
}

// 사용법
for await (const user of getAllUsers()) {
  console.log(user.email);
}
```
```

---

### Component Documentation (상세 템플릿)

```markdown
# Button

> 다양한 스타일과 크기를 지원하는 클릭 가능한 버튼 컴포넌트입니다.

## 언제 사용하나요?

- 폼 제출 (Submit)
- 액션 트리거 (저장, 삭제, 취소 등)
- 페이지 네비게이션
- 모달/다이얼로그 열기

## 언제 사용하지 말아야 하나요?

- 텍스트 링크가 더 적절한 경우 → `<Link>` 사용
- 탭 전환 → `<Tabs>` 사용
- 토글 스위치 → `<Switch>` 사용

## Import

```tsx
import { Button } from '@/components/ui';
// 또는
import Button from '@/components/ui/Button';
```

## 기본 사용법

```tsx
<Button onClick={() => console.log('clicked')}>
  버튼 텍스트
</Button>
```

## Props

### 필수 Props

| Prop | 타입 | 설명 |
|------|------|------|
| children | `ReactNode` | 버튼 내용 (텍스트 또는 아이콘) |

### 선택 Props

| Prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| variant | `'primary' \| 'secondary' \| 'outline' \| 'ghost' \| 'danger'` | `'primary'` | 버튼 스타일 변형 |
| size | `'xs' \| 'sm' \| 'md' \| 'lg' \| 'xl'` | `'md'` | 버튼 크기 |
| disabled | `boolean` | `false` | 비활성화 상태 |
| loading | `boolean` | `false` | 로딩 상태 (스피너 표시) |
| fullWidth | `boolean` | `false` | 부모 너비에 맞춤 |
| type | `'button' \| 'submit' \| 'reset'` | `'button'` | HTML 버튼 타입 |
| leftIcon | `ReactNode` | - | 텍스트 왼쪽 아이콘 |
| rightIcon | `ReactNode` | - | 텍스트 오른쪽 아이콘 |
| className | `string` | - | 추가 CSS 클래스 |

### 조건부 Props

| 조건 | 필수 Prop | 설명 |
|------|-----------|------|
| `variant="danger"` | `confirmMessage` | 위험 액션 확인 메시지 |
| `loading={true}` | `loadingText` | 로딩 중 표시할 텍스트 (권장) |

## 이벤트

| 이벤트 | 타입 | 설명 |
|--------|------|------|
| onClick | `(event: MouseEvent) => void` | 클릭 시 호출 |
| onFocus | `(event: FocusEvent) => void` | 포커스 시 호출 |
| onBlur | `(event: FocusEvent) => void` | 포커스 해제 시 호출 |

## Ref 메서드

```tsx
const buttonRef = useRef<ButtonRef>(null);

// 사용 가능한 메서드
buttonRef.current?.focus();     // 포커스
buttonRef.current?.blur();      // 포커스 해제
buttonRef.current?.click();     // 프로그래매틱 클릭
```

## CSS Variables

```css
:root {
  --button-primary-bg: #3b82f6;
  --button-primary-hover: #2563eb;
  --button-primary-text: #ffffff;
  --button-border-radius: 6px;
  --button-font-weight: 500;
  --button-transition: all 0.2s ease;
}
```

## 커스텀 Class Names

| Class | 설명 |
|-------|------|
| `.btn` | 기본 버튼 클래스 |
| `.btn--primary` | Primary 변형 |
| `.btn--loading` | 로딩 상태 |
| `.btn--disabled` | 비활성화 상태 |
| `.btn--fullwidth` | 전체 너비 |

## 예시

### 1. 기본 예시

```tsx
import { Button } from '@/components/ui';

function BasicExample() {
  return (
    <Button onClick={() => alert('클릭!')}>
      기본 버튼
    </Button>
  );
}
```

### 2. 실전 예시 - 폼 제출

```tsx
import { Button } from '@/components/ui';
import { useState } from 'react';

function FormSubmitExample() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      await saveData();
      toast.success('저장되었습니다.');
    } catch (error) {
      toast.error('저장에 실패했습니다.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Button
      type="submit"
      loading={isSubmitting}
      loadingText="저장 중..."
      onClick={handleSubmit}
    >
      저장
    </Button>
  );
}
```

### 3. 고급 예시 - 모든 옵션 활용

```tsx
import { Button } from '@/components/ui';
import { SaveIcon, ChevronRightIcon } from '@/icons';

function AdvancedExample() {
  return (
    <Button
      variant="primary"
      size="lg"
      leftIcon={<SaveIcon />}
      rightIcon={<ChevronRightIcon />}
      loading={false}
      disabled={false}
      fullWidth
      className="my-custom-class"
      onClick={(e) => {
        e.preventDefault();
        console.log('클릭 위치:', e.clientX, e.clientY);
      }}
    >
      저장하고 계속
    </Button>
  );
}
```

### 4. 에러 처리 예시 - 위험 액션

```tsx
import { Button } from '@/components/ui';
import { TrashIcon } from '@/icons';

function DangerActionExample() {
  const handleDelete = async () => {
    if (!window.confirm('정말 삭제하시겠습니까?')) {
      return;
    }

    try {
      await deleteItem();
    } catch (error) {
      if (error.code === 'PERMISSION_DENIED') {
        toast.error('삭제 권한이 없습니다.');
      } else {
        toast.error('삭제에 실패했습니다. 다시 시도해주세요.');
      }
    }
  };

  return (
    <Button
      variant="danger"
      leftIcon={<TrashIcon />}
      onClick={handleDelete}
    >
      삭제
    </Button>
  );
}
```

## 접근성 (a11y)

- `disabled` 상태일 때 `aria-disabled="true"` 자동 적용
- `loading` 상태일 때 `aria-busy="true"` 자동 적용
- 키보드로 `Enter` 또는 `Space` 키로 활성화 가능
- 포커스 시 명확한 포커스 링 표시

### 키보드 내비게이션

| 키 | 동작 |
|---|-----|
| `Tab` | 다음 요소로 이동 |
| `Shift + Tab` | 이전 요소로 이동 |
| `Enter` | 버튼 활성화 |
| `Space` | 버튼 활성화 |

## 성능 최적화

```tsx
// onClick 핸들러 메모이제이션
const handleClick = useCallback(() => {
  // 로직
}, [dependencies]);

// 부모 리렌더링 시 버튼 리렌더링 방지
const MemoizedButton = memo(Button);
```

## 관련 컴포넌트

- [IconButton](./icon-button.md) - 아이콘만 있는 버튼
- [ButtonGroup](./button-group.md) - 버튼 그룹
- [Link](./link.md) - 네비게이션 링크
```

---

## 검증 단계

### 4단계: 자동 검증

```
[4/5] 검증 중...
  ✓ 필수 섹션 포함 여부 검증 (Getting Started: 15개 항목)
  ✓ 필수 섹션 포함 여부 검증 (API: 20개 항목/엔드포인트)
  ✓ 필수 섹션 포함 여부 검증 (Component: 18개 항목/컴포넌트)
  ✓ 코드 예시 개수 검증 (기능당 최소 4개)
  ✓ 코드 예시 실행 가능성 검증 (import문 포함)
  ✓ 예상 출력 포함 여부 검증
  ✓ 링크 유효성 검증
  ✓ TypeScript 컴파일 검증

[5/5] 품질 점수 계산...
  - 완성도: 98%
  - 코드 예시 다양성: 95%
  - 실행 가능성: 100%
  - 링크 유효성: 100%

✅ 문서 생성 완료 (품질 점수: 98/100)
```

---

## 옵션

```bash
# 특정 카테고리만 생성
/docs generate --only=api,components

# 기존 문서 덮어쓰기
/docs generate --force

# 상세 로그
/docs generate --verbose

# 품질 검증 건너뛰기 (권장하지 않음)
/docs generate --skip-validation
```

## 주의사항

> ⚠️ 기존 `.claude/docs-site/` 폴더가 있으면 백업 후 진행합니다.

> 📘 생성된 문서는 고품질이지만, 프로젝트 특성에 맞게 추가 편집을 권장합니다.
