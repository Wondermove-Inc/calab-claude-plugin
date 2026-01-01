---
description: 빠른 프로젝트 온보딩을 실행합니다. 핵심 정보만 분석하여 최소 컨텍스트를 구축합니다.
allowed-tools: Read, Write, Glob
---

# /onboard-quick - 빠른 온보딩

## 설명

핵심 정보만 **빠르게 분석**하여 최소한의 컨텍스트를 구축합니다.
시간이 촉박하거나 간단한 작업을 위해 사용합니다.

**목표**: 5분 이내에 개발 시작 가능한 상태로 만들기

## 사용법

```bash
/onboard-quick
```

---

## Quick Scan 프로세스

### Step 1: 기술 스택 파악 (1분)

**package.json 분석:**

```bash
# 핵심 정보 추출
cat package.json | jq '{
  name,
  scripts,
  dependencies: (.dependencies | keys),
  devDependencies: (.devDependencies | keys)
}'
```

**추출 항목:**

| 항목 | 확인 위치 | 예시 |
|------|----------|------|
| Framework | dependencies | `next`, `react`, `vue` |
| Language | devDependencies | `typescript` |
| ORM | dependencies | `prisma`, `typeorm` |
| Styling | dependencies | `tailwindcss` |
| Testing | devDependencies | `jest`, `vitest` |

**빠른 판단 기준:**

```yaml
Next.js 프로젝트:
  - "next" in dependencies
  - app/ 또는 pages/ 폴더 존재

React SPA:
  - "react" + "vite" or "create-react-app"
  - src/ 폴더 존재

Node.js Backend:
  - "express" or "fastify" or "nestjs"
  - src/ 또는 routes/ 폴더 존재
```

### Step 2: 디렉토리 구조 확인 (1분)

**최상위 구조만 확인:**

```bash
# 소스 디렉토리 구조 (1레벨)
ls -la src/ 2>/dev/null || ls -la app/ 2>/dev/null
```

**구조 유형 빠른 판단:**

| 폴더 구조 | 프로젝트 유형 |
|----------|--------------|
| `app/`, `components/`, `lib/` | Next.js App Router |
| `pages/`, `components/` | Next.js Pages Router |
| `src/features/` | Feature-based |
| `src/controllers/`, `src/services/` | Layer-based |

### Step 3: 대표 파일 분석 (2분)

**분석할 파일 (최대 3개):**

1. **메인 진입점**
   - `src/app/page.tsx` (Next.js App Router)
   - `src/pages/index.tsx` (Next.js Pages Router)
   - `src/App.tsx` (React SPA)
   - `src/index.ts` (Node.js)

2. **대표 컴포넌트** (가장 큰 파일 1개)
   ```bash
   find src/components -name "*.tsx" -exec wc -l {} + | sort -rn | head -3
   ```

3. **API 예시** (있는 경우)
   - `src/app/api/*/route.ts`
   - `src/routes/*.ts`

**추출할 패턴 (필수만):**

```typescript
// 빠른 체크리스트
□ Props 정의: interface or type?
□ 스타일링: Tailwind, CSS Modules, styled-components?
□ 상태 관리: useState, Zustand, Redux?
□ 데이터 페칭: React Query, SWR, fetch?
```

### Step 4: PROJECT_SUMMARY.md 생성 (1분)

**간소화된 템플릿:**

```markdown
# 프로젝트 요약 (Quick)

> 생성 시간: {timestamp}
> 유형: 빠른 온보딩 (상세 분석: /onboard)

## 기술 스택

| 분류 | 기술 |
|------|------|
| Framework | {framework} |
| Language | {language} |
| Styling | {styling} |
| Database | {database} |

## 디렉토리 구조

```
src/
├── {folder1}/  # {description}
├── {folder2}/  # {description}
└── {folder3}/  # {description}
```

## 개발 명령어

| 명령어 | 설명 |
|--------|------|
| `{dev_command}` | 개발 서버 시작 |
| `{build_command}` | 프로덕션 빌드 |
| `{test_command}` | 테스트 실행 |

## 코드 스타일 (추정)

- Props: {props_style}
- Styling: {styling_method}
- State: {state_management}

---

💡 상세 분석이 필요하면 `/onboard` 실행
```

---

## 출력 예시

```
⚡ 빠른 온보딩 시작...

══════════════════════════════════════════════
 Step 1: 기술 스택 파악
══════════════════════════════════════════════
✅ Framework: Next.js 14.1.0
✅ Language: TypeScript 5.3.3
✅ Styling: Tailwind CSS 3.4.0
✅ Database: PostgreSQL (Prisma 5.8.0)
✅ Testing: Vitest + RTL

══════════════════════════════════════════════
 Step 2: 디렉토리 구조
══════════════════════════════════════════════
✅ 구조 유형: Next.js App Router
   src/
   ├── app/          # 라우팅 (App Router)
   ├── components/   # UI 컴포넌트
   ├── lib/          # 유틸리티
   └── types/        # 타입 정의

══════════════════════════════════════════════
 Step 3: 코드 스타일
══════════════════════════════════════════════
✅ Props 정의: interface
✅ 스타일링: Tailwind + cn() 유틸
✅ 상태 관리: React Query + Zustand

══════════════════════════════════════════════
 Step 4: 문서 생성
══════════════════════════════════════════════
📄 PROJECT_SUMMARY.md 생성 완료

══════════════════════════════════════════════
⚡ 빠른 온보딩 완료! (45초)
══════════════════════════════════════════════

📁 생성된 문서:
└── .claude/project-context/PROJECT_SUMMARY.md

💡 다음 단계:
   /onboard          → 상세 분석 (5개 문서)
   /learn <path>     → 특정 영역 학습
   바로 코딩 시작!    → 기본 컨텍스트 적용됨
```

---

## /onboard vs /onboard-quick 비교

| 항목 | /onboard-quick | /onboard |
|------|----------------|----------|
| **소요 시간** | ~1분 | ~10분 |
| **분석 깊이** | 표면적 | 심층적 |
| **생성 문서** | 1개 | 5개 |
| **패턴 추출** | 필수만 | 전체 |
| **C4 다이어그램** | ❌ | ✅ |
| **도메인 지식** | ❌ | ✅ |

## 언제 사용하나요?

| 상황 | 권장 명령어 |
|------|------------|
| 새 프로젝트 투입, 장기 개발 | `/onboard` |
| 간단한 버그 수정 | `/onboard-quick` |
| 빠른 코드 리뷰 | `/onboard-quick` |
| PR 리뷰 전 빠른 파악 | `/onboard-quick` |
| 기능 추가 (단기) | `/onboard-quick` → 필요시 `/onboard` |
| 아키텍처 이해 필요 | `/onboard` |
| 신규 팀원 온보딩 | `/onboard` |

---

## 다음 단계

| 상황 | 명령어 |
|------|--------|
| 더 자세한 분석 필요 | `/onboard` |
| 특정 폴더 심층 학습 | `/learn <path>` |
| 컨텍스트 확인 | `/context-show` |
| 바로 작업 시작 | 코드 작성 (컨텍스트 자동 참조) |

---

## 빠른 판단 가이드

### Framework 감지

```javascript
// package.json 확인
if (dependencies.next) return "Next.js";
if (dependencies.nuxt) return "Nuxt.js";
if (dependencies.vue) return "Vue.js";
if (dependencies.react && dependencies.vite) return "React + Vite";
if (dependencies.express) return "Express.js";
if (dependencies["@nestjs/core"]) return "NestJS";
```

### 스타일링 감지

```javascript
// package.json 확인
if (dependencies.tailwindcss || devDependencies.tailwindcss) return "Tailwind";
if (dependencies["styled-components"]) return "Styled-components";
if (dependencies["@emotion/react"]) return "Emotion";
// tailwind.config.js 존재 확인
if (exists("tailwind.config.js")) return "Tailwind";
```

### 상태 관리 감지

```javascript
// package.json 확인
if (dependencies.zustand) return "Zustand";
if (dependencies["@reduxjs/toolkit"]) return "Redux Toolkit";
if (dependencies.recoil) return "Recoil";
if (dependencies.jotai) return "Jotai";
if (dependencies["@tanstack/react-query"]) return "React Query (서버 상태)";
```

---

## 참조

- `/onboard` - 전체 온보딩
- `.claude/skills/project-onboarding/SKILL.md`
- `.claude/best-practices/project-onboarding.md`
