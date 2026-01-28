# /context --show - 컨텍스트 표시

> **현재 프로젝트 컨텍스트 표시**

## 실행 절차

### Step 1: 컨텍스트 파일 확인

```
.claude/project-context/ 존재 여부 확인

없으면:
⚠️ 프로젝트 컨텍스트가 없습니다.
→ /onboard 안내
```

### Step 2: 문서 로드

```
필터 없음: 전체 로드
- PROJECT_SUMMARY.md
- ARCHITECTURE.md
- CODE_PATTERNS.md
- DOMAIN_KNOWLEDGE.md

필터 있음: 해당 문서만 로드
- tech → PROJECT_SUMMARY.md
- patterns → CODE_PATTERNS.md
- architecture → ARCHITECTURE.md
- domain → DOMAIN_KNOWLEDGE.md
```

### Step 3: 정보 추출 및 표시

**전체 출력 형식:**

```
============================================
 PROJECT CONTEXT: {프로젝트명}
============================================

 📋 프로젝트 정보
 • 이름: {name}
 • 설명: {description}
 • 분석일: {date}

 🔧 기술 스택
 ┌────────────────────────────────────────┐
 │ Frontend │ {프레임워크, 버전}           │
 │ Backend  │ {런타임, 프레임워크}         │
 │ Database │ {DB, ORM}                  │
 │ Testing  │ {테스트 프레임워크}          │
 │ Styling  │ {스타일링 방식}             │
 └────────────────────────────────────────┘

 📁 디렉토리 구조
 {PROJECT_SUMMARY.md에서 추출}

 📝 주요 패턴
 • 컴포넌트: {패턴 요약}
 • API: {패턴 요약}
 • 상태 관리: {패턴 요약}
 • 에러 처리: {패턴 요약}

 🏗️ 아키텍처
 • 타입: {Feature-based / Layer-based / etc}
 • 레이어: {레이어 구조}
 • 데이터 플로우: {흐름}

 📖 도메인
 • 핵심 엔티티: {엔티티 목록}
 • 비즈니스 규칙: {주요 규칙}
 • 주요 용어: {도메인 용어}

============================================
 마지막 갱신: {timestamp}
 명령어: /context --refresh (갱신)
============================================
```

### Step 4: 필터별 출력

**tech 필터:**
```
============================================
 기술 스택: {프로젝트명}
============================================

 Frontend:
 • Framework: Next.js 14
 • Language: TypeScript 5.x
 • State: TanStack Query, Zustand
 • Styling: Tailwind CSS

 Backend:
 • Runtime: Node.js 20
 • Framework: Express / NestJS
 • Validation: Zod

 Database:
 • Primary: PostgreSQL 15
 • ORM: Prisma 5.x
 • Cache: Redis (선택)

 Testing:
 • Unit: Jest, Vitest
 • E2E: Playwright
 • Component: Testing Library

 DevOps:
 • CI/CD: GitHub Actions
 • Deploy: Vercel / Docker

============================================
```

**patterns 필터:**
```
============================================
 코드 패턴: {프로젝트명}
============================================

 📦 컴포넌트 패턴
 {CODE_PATTERNS.md 컴포넌트 섹션}

 🌐 API 패턴
 {CODE_PATTERNS.md API 섹션}

 🔄 Hook 패턴
 {CODE_PATTERNS.md Hook 섹션}

 ⚠️ 에러 처리 패턴
 {CODE_PATTERNS.md 에러 처리 섹션}

============================================
```

## 주의사항

- 읽기 전용 명령어 (파일 수정 없음)
- 허용 도구: `Read`, `Glob`만 사용
- 에이전트로 문서/코드 검증 필수
