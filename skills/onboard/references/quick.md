# /onboard --quick - 빠른 온보딩

> **핵심 정보만 빠르게 분석 (~1분)**

## 사용법

```bash
/onboard --quick
```

## 실행 절차 (4단계, ~1분)

### Step 1: 기술 스택 감지 (15초)

**package.json 분석:**

```javascript
// 프레임워크 감지
dependencies: {
  "next": "14.x"     → Next.js
  "react": "18.x"    → React
  "express": "4.x"   → Express
  "nestjs": "10.x"   → NestJS
}

// 언어 감지
devDependencies: {
  "typescript": "5.x" → TypeScript
}

// ORM 감지
dependencies: {
  "prisma": "5.x"    → Prisma
  "@prisma/client"   → Prisma Client
}

// 스타일링 감지
dependencies: {
  "tailwindcss"      → Tailwind CSS
  "styled-components" → Styled Components
}

// 테스트 감지
devDependencies: {
  "jest"             → Jest
  "vitest"           → Vitest
  "@testing-library" → Testing Library
}
```

### Step 2: 디렉토리 구조 파악 (15초)

**프로젝트 타입 식별:**

| 패턴 | 타입 |
|------|------|
| `src/app/` | Next.js App Router |
| `src/pages/` | Next.js Pages Router |
| `src/components/` + `src/index.tsx` | React SPA |
| `src/controllers/` | Backend (Express/NestJS) |
| `src/features/` | Feature-based |

**구조 스캔:**
```bash
ls -la src/
ls -la src/app/ 2>/dev/null
ls -la src/components/ 2>/dev/null
```

### Step 3: 대표 파일 분석 (20초)

**분석 대상 (최대 3개):**

1. **진입점**
   - `src/app/page.tsx` (Next.js)
   - `src/index.tsx` (React SPA)
   - `src/main.ts` (NestJS)

2. **가장 큰 컴포넌트**
   ```bash
   find src -name "*.tsx" -exec wc -l {} + | sort -n | tail -5
   ```

3. **API 예시**
   - `src/app/api/*/route.ts`
   - `src/controllers/*.ts`

**추출 패턴:**
- 컴포넌트 구조 (FC, Props)
- 상태 관리 방식
- API 호출 패턴

### Step 4: PROJECT_SUMMARY.md 생성 (10초)

```markdown
# 프로젝트 요약

> 빠른 분석: {날짜}

## 기술 스택

| 영역 | 기술 |
|------|------|
| Framework | Next.js 14 |
| Language | TypeScript 5.x |
| Styling | Tailwind CSS |
| Database | PostgreSQL + Prisma |
| Testing | Jest + Testing Library |

## 디렉토리 구조

```
src/
├── app/           # App Router
├── components/    # UI 컴포넌트
├── lib/           # 유틸리티
└── types/         # 타입 정의
```

## 주요 명령어

```bash
npm run dev        # 개발 서버
npm run build      # 빌드
npm run test       # 테스트
npm run lint       # 린트
```

## 핵심 패턴 (Quick)

### 컴포넌트
- FC + Props 인터페이스
- Tailwind 클래스 사용

### 상태 관리
- useState (로컬)
- TanStack Query (서버 상태)

---

*전체 분석: `/onboard --full`*
```

### 완료 보고

```
============================================
 ONBOARD QUICK 완료
============================================

 ⏱️ 소요 시간: ~45초

 🔧 감지된 기술 스택:
 • Framework: Next.js 14
 • Language: TypeScript
 • Styling: Tailwind CSS
 • Database: PostgreSQL + Prisma

 📁 프로젝트 타입: Next.js App Router

 📄 생성된 문서:
 • .claude/project-context/PROJECT_SUMMARY.md

============================================
 전체 분석: /onboard --full
 컨텍스트 확인: /context
============================================
```

## Quick vs Full 비교

| 항목 | Quick | Full |
|------|-------|------|
| 시간 | ~1분 | ~10분 |
| 문서 | 1개 | 5개 |
| 패턴 분석 | 필수만 | 전체 |
| C4 다이어그램 | 없음 | 있음 |
| 도메인 인터뷰 | 없음 | 있음 |
| 추천 상황 | 빠른 시작 | 깊은 이해 |

## 제한사항

- 코드 패턴: 3개 파일만 분석
- 아키텍처: 디렉토리 구조만
- 컨벤션: 기본 추론만
- 도메인: 수집 안 함
