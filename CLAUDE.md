> **어떤 상황에서든 동일한 개발 품질을 보장하는** Claude Code 행동 규칙

---

## 목차

1. [플러그인 개요](#플러그인-개요)
2. [핵심 원칙 (5대 규칙)](#핵심-원칙-5대-규칙)
3. [에이전트 마스터 가이드](#에이전트-마스터-가이드)
4. [검증/보강 에이전트 패턴](#검증보강-에이전트-패턴-2025-best-practices) ⭐ NEW
5. [스킬 활용 전략](#스킬-활용-전략)
6. [워크플로우 가이드](#워크플로우-가이드)
7. [명령어 참조](#명령어-참조)
8. [자동화 규칙](#자동화-규칙)
9. [품질 규칙](#품질-규칙)
10. [세션 관리](#세션-관리)

---

## 플러그인 개요

### 이 플러그인이 하는 일

| 영역 | 자동화 내용 |
|------|------------|
| **개발 워크플로우** | Plan → Design → Tasks → Build 단계별 진행 |
| **코드 품질** | 베스트 프랙티스 자동 적용, 500줄 제한, 주석 필수 |
| **문제 해결** | 5 Whys, RCA, 가설 검증 체계적 접근 |
| **문서화** | 코드 변경 시 문서 자동 동기화 |
| **작업 추적** | Worktree로 진행률 실시간 관리 |
| **컨텍스트 유지** | Compact 후에도 작업 상태 복원 |

### 핵심 구성

```
9개 스킬 + 23개 에이전트 + 22개 훅
```

### 설치 확인

```bash
/onboard   # 프로젝트 분석 및 컨텍스트 생성
```

---

## 핵심 원칙 (5대 규칙)

> **모든 응답에서 반드시 준수해야 하는 5가지 핵심 규칙**

### 1. 🔴 할루시네이션 금지 (Anthropic 공식)

> **출처**: docs.anthropic.com - Claude Best Practices

```
❌ 읽지 않은 코드 추측 금지
❌ 확인 없이 주장 금지
✅ 파일 먼저 읽고 답변
✅ 불확실하면 "확인 필요" 인정
```

**필수 행동:**
1. 관련 파일 먼저 읽고 이해
2. 코드베이스 스타일/컨벤션 파악
3. 충분한 컨텍스트 확보 후 답변

### 2. 🔴 에이전트 100% 활용 필수

> **"Give each subagent one job, and let an orchestrator coordinate"** - Anthropic Engineering 2025

| 작업 | 에이전트 (호출 시 이름) | 이유 |
|------|------------------------|------|
| 코드베이스 탐색 | `Explore` | 구조, 패턴, 의존성 파악 |
| 복잡한 검색 | `general-purpose` | 다중 파일 키워드 검색 |
| 구현 계획 | `Plan` | 아키텍처 설계 |
| 코드 리뷰 | `calab-plugin:code-reviewer` | 품질 검사, 버그 탐지 |
| 보안 검사 | `calab-plugin:security-reviewer` | OWASP 취약점 분석 |
| 규칙 검증 | `calab-plugin:project-guardian` | 프로젝트 규칙 준수 |
| 완전성 검증 | `calab-plugin:validator` | AC 충족, 누락 탐지 |
| 웹 리서치 | `calab-plugin:web-researcher` | 최신 정보 검색 |

### 3. 🔴 Task 완료 검증 필수

> **AC 100% 충족 전까지 다음 Task 금지**

**완료 조건 (Definition of Done):**
- [ ] AC 100% 충족 - 각 항목 명시적 검증
- [ ] 기능 동작 확인 - 빌드/실행 가능
- [ ] 엣지 케이스 처리 - null, 빈값, 경계값
- [ ] 코드 품질 - 500줄↓, 주석, 타입

**검증 출력 형식:**
```
[TASK 완료 검증] TASK-001
✅ AC1: 충족 | ✅ AC2: 충족 | ❌ AC3: 미충족 → 추가 구현
결과: ❌ 완료 불가 → 다음 Task 진행 금지
```

### 4. 🔴 사용자 선택권 보장

> **복수 방안 또는 리스크 작업 시 반드시 선택지 제시**

**표시 형식:**
```
**방안 1**: [설명] ⭐ 권장 (근본적 해결)
**방안 2**: [설명] ⚡ 빠른 적용
**방안 3**: [설명] ⚠️ 리스크 있음
```

### 5. 🔴 컨텍스트 유지

> **작업 시작 전 Memory 확인, 완료 시 기록**

**확인 파일:**
- `.claude/memory/CURRENT_CONTEXT.md` - 현재 작업 상태
- `.claude/memory/PROJECT_RULES.md` - 프로젝트 규칙

---

## 에이전트 마스터 가이드

> **2025 Best Practices** - Anthropic Engineering, Claude Agent SDK 공식 문서 기반
> **핵심**: "The most stable agents follow a simple rule: give each subagent one job"

### 에이전트 오케스트레이션 패턴

```
┌─────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (Main)                   │
│  - 전체 작업 분석 및 분해                                │
│  - 서브에이전트에 작업 위임                              │
│  - 결과 수집 및 통합                                     │
└─────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Subagent 1     │ │  Subagent 2     │ │  Subagent 3     │
│  (단일 책임)    │ │  (단일 책임)    │ │  (단일 책임)    │
│  - 리서치       │ │  - 구현         │ │  - 검증         │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 사용 가능한 에이전트 (23개)

> **🚨 중요: 에이전트 호출 시 네임스페이스 규칙**
>
> | 에이전트 유형 | 호출 방식 | 예시 |
> |--------------|----------|------|
> | **기본 에이전트** | prefix 없음 | `subagent_type="Explore"` |
> | **플러그인 에이전트** | `calab-plugin:` 필수 | `subagent_type="calab-plugin:validator"` |

#### 기본 에이전트 (3개) - prefix 없음

| 에이전트 | 역할 | 허용 도구 | 자동 호출 조건 |
|----------|------|----------|---------------|
| **Explore** | 코드베이스 빠른 탐색 | Read, Glob, Grep | 구조/패턴 분석 요청 |
| **Plan** | 구현 계획 수립 | Read, Glob, Grep | 아키텍처 설계 |
| **general-purpose** | 범용 작업 수행 | All | 복잡한 멀티스텝 |

#### 플러그인 에이전트 (20개) - `calab-plugin:` prefix 필수

| 에이전트 | 호출 시 이름 | 역할 | 허용 도구 |
|----------|-------------|------|----------|
| **code-reviewer** | `calab-plugin:code-reviewer` | 코드 품질 검토 | Read, Grep, Glob |
| **security-reviewer** | `calab-plugin:security-reviewer` | 보안 취약점 분석 | Read, Grep, Glob, Bash |
| **project-guardian** | `calab-plugin:project-guardian` | 규칙 준수 검증 | Read, Grep, Glob |
| **build-error-resolver** | `calab-plugin:build-error-resolver` | 빌드 오류 해결 | Read, Edit, Bash |
| **refactor-cleaner** | `calab-plugin:refactor-cleaner` | 데드 코드 정리 | Read, Write, Edit, Bash |
| **e2e-runner** | `calab-plugin:e2e-runner` | E2E 테스트 실행 | All + Puppeteer |
| **doc-updater** | `calab-plugin:doc-updater` | 문서 자동 업데이트 | Read, Write, Edit |
| **deep-researcher** | `calab-plugin:deep-researcher` | 심층 리서치 분석 | Read, WebSearch, Tavily |
| **web-researcher** | `calab-plugin:web-researcher` | 웹 검색 및 수집 | Tavily MCP 도구 |
| **project-onboarder** | `calab-plugin:project-onboarder` | 프로젝트 온보딩 | Read, Glob, Grep, Write |
| **validator** | `calab-plugin:validator` | 완전성/AC 검증 | Read, Grep, Glob |
| **reinforcer** | `calab-plugin:reinforcer` | 검증 실패 항목 수정 | Read, Write, Edit |
| **planner-phase** | `calab-plugin:planner-phase` | PRD 및 PHASE 분해 | Read, Glob, Grep, Task |
| **planner-task** | `calab-plugin:planner-task` | Task 분해 (TDD) | Read, Glob, Grep, TaskCreate |
| **design** | `calab-plugin:design` | 아키텍처/ERD 설계 | Read, Glob, Grep, Write |
| **dev-executor** | `calab-plugin:dev-executor` | TDD 구현 실행 | Read, Write, Edit, Bash |
| **task-validator** | `calab-plugin:task-validator` | Task 분해 검증 | Read, Grep, Glob |
| **qa** | `calab-plugin:qa` | 8단계 QA 검증 | Read, Bash, Glob, Grep |
| **root-cause-finder** | `calab-plugin:root-cause-finder` | 근본 원인 분석 | Read, Glob, Grep, Bash |
| **bug-fixer** | `calab-plugin:bug-fixer` | TDD 버그 수정 | Read, Write, Edit, Bash |

### 🚨 에이전트 프롬프트 작성 필수 규칙 (2025)

> **"The more specific your system prompt, the better the agent performs"** - Anthropic

#### 1. 단일 책임 원칙 (Single Responsibility)

```
❌ 나쁜 예:
"코드 분석하고 리팩토링하고 테스트 작성해줘"

✅ 좋은 예:
"src/auth 모듈의 인증 로직 구조만 분석"
```

**규칙:**
- 에이전트당 **하나의 명확한 목표**만 부여
- 복합 작업은 **여러 에이전트로 분할**
- 각 에이전트 결과를 조합하여 최종 완료

#### 2. 프롬프트 필수 7요소 (RGOSWOC)

| 요소 | 영문 | 설명 | 필수 |
|------|------|------|------|
| **R** | Role | 역할 정의 (전문 분야) | ✅ |
| **G** | Goal | 달성 목표 (구체적, 측정 가능) | ✅ |
| **O** | Objective | 세부 목표 (1-3개) | ✅ |
| **S** | Scope | 작업 범위 (파일/디렉토리) | ✅ |
| **W** | Workflow | 단계별 수행 순서 | ✅ |
| **O** | Output | 출력 형식 (JSON, 표, 목록) | ✅ |
| **C** | Constraints | 제약 조건 (하지 말 것) | ⚠️ |

#### 3. 상세 프롬프트 템플릿

```markdown
**역할 (Role)**:
[전문 분야] 전문가로서 작업 수행

**목표 (Goal)**:
[구체적이고 측정 가능한 단일 목표]

**세부 목표 (Objectives)**:
1. [첫 번째 세부 목표]
2. [두 번째 세부 목표]

**범위 (Scope)**:
- 포함: [파일/디렉토리 명시]
- 제외: [제외할 영역]

**수행 단계 (Workflow)**:
1. [첫 번째 단계] → [기대 결과]
2. [두 번째 단계] → [기대 결과]
3. [세 번째 단계] → [기대 결과]

**출력 형식 (Output)**:
```[형식]
[예시 구조]
```

**제약 조건 (Constraints)**:
- ❌ [하지 말아야 할 것 1]
- ❌ [하지 말아야 할 것 2]
- ✅ [반드시 해야 할 것]
```

#### 4. 실제 사용 예시 (Best → Worst)

**🏆 최고 품질 프롬프트:**

```
Task(
  subagent_type="calab-plugin:security-reviewer",
  description="인증 API 보안 취약점 분석",
  prompt="""
  **역할**: OWASP Top 10 전문 보안 분석가

  **목표**: src/api/auth/ 디렉토리의 SQL Injection,
  XSS, CSRF 취약점 탐지

  **세부 목표**:
  1. 사용자 입력 검증 로직 분석
  2. 쿼리 파라미터 sanitization 확인
  3. 세션 토큰 처리 방식 검토

  **범위**:
  - 포함: src/api/auth/*.ts
  - 제외: *.test.ts, *.spec.ts

  **수행 단계**:
  1. auth/ 디렉토리 파일 목록 확인 → 분석 대상 선정
  2. 각 파일의 입력 처리 로직 분석 → 취약점 후보 식별
  3. 취약점 심각도 평가 → CVSS 점수 산정

  **출력 형식**:
  | 파일 | 라인 | 취약점 유형 | 심각도 | 권장 수정 |
  |------|------|------------|--------|----------|

  **제약 조건**:
  - ❌ 코드 수정하지 말 것 (분석만)
  - ❌ 테스트 파일 분석하지 말 것
  - ✅ 모든 발견사항에 라인 번호 포함
  """
)
```

**⚠️ 보통 품질:**
```
Task(subagent_type=Explore, "src/auth 분석해서 구조 알려줘")
```

**❌ 나쁜 품질:**
```
Task(subagent_type=Explore, "코드 확인해줘")
```

#### 5. 에이전트 유형별 프롬프트 가이드

| 에이전트 | 필수 포함 요소 | 예시 |
|----------|---------------|------|
| **Explore** | 탐색 범위, 깊이(quick/medium/thorough), 찾을 패턴 | "src/components/**/*.tsx에서 useState 사용 패턴 분석, medium 깊이" |
| **Plan** | 목표 기능, 제약 조건, 기술 스택, 아키텍처 선호 | "Next.js 14 App Router 기반, 인증 시스템 설계, JWT 사용" |
| **code-reviewer** | 리뷰 기준, 체크 항목, 허용/금지 패턴 | "성능 최적화 관점, 불필요한 리렌더링 탐지, 500줄 이상 파일 경고" |
| **security-reviewer** | OWASP 카테고리, 검사 대상, 심각도 기준 | "Injection, XSS 집중, HIGH 이상만 보고" |
| **general-purpose** | 구체적 질문, 기대 결과 형식, 충분한 컨텍스트 | "package.json 분석하여 사용하지 않는 의존성 목록 JSON 반환" |

#### 6. 프롬프트 품질 체크리스트

에이전트 호출 전 **반드시** 확인:

| 체크 | 항목 | 확인 질문 |
|------|------|----------|
| [ ] | **목표 명확성** | 무엇을 달성해야 하는지 구체적인가? |
| [ ] | **범위 한정** | 어디서 작업할지 명시되어 있는가? |
| [ ] | **단계 논리성** | 순서대로 수행 가능한가? |
| [ ] | **출력 형식** | 결과물 예상이 가능한가? |
| [ ] | **단일 책임** | 하나의 목표만 존재하는가? |
| [ ] | **컨텍스트 충분** | 배경 정보가 충분한가? |
| [ ] | **제약 조건** | 하지 말아야 할 것이 명시되어 있는가? |

### 병렬 에이전트 실행 패턴

> **"Run parallel research - spawn multiple subagents to work simultaneously"** - Claude Code Docs

#### 언제 병렬 실행하는가?

| 상황 | 실행 방식 | 이유 |
|------|----------|------|
| 독립적인 조사 작업 | **병렬** | 의존성 없음 |
| 결과가 다음 단계 입력 | **순차** | 의존성 있음 |
| 대량 출력 생성 작업 | **병렬** (격리) | 컨텍스트 보존 |
| 파일 수정 작업 | **순차** | 충돌 방지 |

#### 병렬 실행 예시

```
// 3개 에이전트 동시 실행 - 한 응답에서 여러 Task 호출
Task(subagent_type=Explore,
     description="프론트엔드 분석",
     prompt="React 컴포넌트 구조와 상태 관리 패턴 분석...")

Task(subagent_type=Explore,
     description="백엔드 분석",
     prompt="API 엔드포인트와 미들웨어 구조 분석...")

Task(subagent_type="calab-plugin:security-reviewer",
     description="인증 보안 검토",
     prompt="인증/인가 로직 OWASP 기준 검토...")
```

**규칙:**
- 서로 의존성이 없는 작업만 병렬 실행
- 결과 조합이 필요하면 순차 실행
- 최대 3-4개 동시 실행 권장
- 파일 수정 작업은 절대 병렬 금지

### 컨텍스트 격리 패턴

> **"Isolate high-volume operations"** - 대용량 출력은 서브에이전트로 격리

```
// 테스트 실행 결과를 서브에이전트로 격리
Task(
  subagent_type=general-purpose,
  description="테스트 실행 및 요약",
  prompt="""
  전체 테스트 스위트 실행 후 실패한 테스트만 요약.

  출력 형식:
  - 총 테스트: N개
  - 성공: N개
  - 실패: N개 (목록 포함)
  """
)
```

**이점:**
- 대용량 로그가 메인 컨텍스트를 오염시키지 않음
- 요약된 결과만 메인 컨텍스트로 반환
- 토큰 비용 절약

### Permission Hygiene (권한 위생)

> **"Scope tools per agent"** - 에이전트별 필요한 도구만 허용

| 에이전트 유형 | 허용 도구 | 금지 도구 |
|--------------|----------|----------|
| **리서치 전용** | Read, Glob, Grep, WebSearch | Write, Edit, Bash |
| **분석 전용** | Read, Grep | Write, Edit, Bash |
| **구현 전용** | Read, Write, Edit, Bash | - |
| **검증 전용** | Read, Bash (실행만) | Write, Edit |

---

## 🚨 검증/보강 에이전트 패턴 (2025 Best Practices)

> **"Always provide verification - If you can't verify it, don't ship it"** - Claude Code Best Practices
> **핵심**: 작업 완료 후 반드시 검증 에이전트로 누락/오류 확인

### 왜 검증 에이전트가 필수인가?

| 문제 | 원인 | 해결책 |
|------|------|--------|
| **누락 발생** | 단일 에이전트 한계 | 별도 검증 에이전트 |
| **할루시네이션** | 확인 없이 진행 | 교차 검증 패턴 |
| **품질 저하** | 자가 검토 한계 | 분리된 컨텍스트 리뷰 |
| **엣지 케이스 누락** | 편향된 시각 | 다중 관점 검증 |

### Plan-Validate-Execute 패턴 (PVE)

> **"The most reliable pattern for complex tasks"** - Anthropic Skill Authoring Guide

```
┌─────────────────────────────────────────────────────────────────┐
│  1. PLAN (계획)                                                  │
│     - 작업 분석 및 계획 수립                                     │
│     - 중간 산출물 생성 (JSON, Markdown)                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. VALIDATE (검증) ← 🚨 별도 에이전트 필수                      │
│     - 계획의 완전성 검증                                         │
│     - 누락 항목 탐지                                             │
│     - 잠재적 문제점 식별                                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. EXECUTE (실행)                                               │
│     - 검증된 계획만 실행                                         │
│     - 문제 발견 시 중단 → 재계획                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. VERIFY (최종 검증) ← 🚨 다른 에이전트 필수                   │
│     - 결과물이 원본 요청 충족 확인                               │
│     - AC 100% 달성 검증                                          │
│     - 누락 없음 확인                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Multi-Agent Verification 패턴

> **"Separate contexts for writing and reviewing"** - Claude Code Best Practices

```
// 1단계: 구현 에이전트 (작성)
Task(
  subagent_type=general-purpose,
  description="사용자 인증 API 구현",
  prompt="..."
)

// 2단계: 검증 에이전트 (리뷰) ← 🚨 필수
Task(
  subagent_type="calab-plugin:code-reviewer",
  description="구현된 인증 API 검증",
  prompt="""
  **역할**: 코드 품질 검증 전문가

  **목표**: 위 구현의 완전성과 품질 검증

  **검증 항목**:
  1. 요청된 모든 기능 구현 여부
  2. 엣지 케이스 처리 (null, 빈값, 경계값)
  3. 에러 처리 완전성
  4. 타입 정의 완전성
  5. 주석/문서화 충분성
  6. 500줄 이하 규칙 준수

  **출력 형식**:
  | 항목 | 상태 | 누락/문제점 | 권장 수정 |
  |------|------|------------|----------|
  """
)

// 3단계: 보강 에이전트 (수정) ← 검증 결과 기반
Task(
  subagent_type=general-purpose,
  description="검증 결과 기반 코드 보강",
  prompt="""
  위 검증에서 발견된 문제점 수정:
  [검증 결과 붙여넣기]
  """
)
```

### 필수 검증 에이전트 체인

> **모든 중요 작업은 아래 체인을 따라야 함**

| 단계 | 에이전트 (호출 시 이름) | 역할 | 필수 여부 |
|------|------------------------|------|----------|
| 1 | 구현 에이전트 | 코드/문서 작성 | ✅ |
| 2 | `calab-plugin:validator` | AC/완전성/엣지케이스 검증 | ✅ 필수 |
| 3 | `calab-plugin:code-reviewer` | 품질/스타일 검증 | ✅ |
| 4 | `calab-plugin:security-reviewer` | 보안 취약점 검사 | ⚠️ (API/인증) |
| 5 | `calab-plugin:project-guardian` | 프로젝트 규칙 준수 | ⚠️ |
| 6 | `calab-plugin:reinforcer` | 누락/문제 수정 | ✅ (실패 시) |
| 7 | `calab-plugin:validator` (재검증) | 수정 완료 확인 | ✅ |

### 자동 검증 프롬프트 템플릿

#### validator 에이전트 (완전성 검증) - 필수

```
Task(
  subagent_type="calab-plugin:validator",
  description="[TASK-ID] 구현 완전성 검증",
  prompt="""
  **역할 (Role)**: 완전성 검증 전문가 - AC/기능/품질 검증 담당

  **목표 (Goal)**: [TASK-ID]의 모든 AC(Acceptance Criteria) 100% 충족 확인

  **원본 요청**:
  [Task 정의 전체 내용]

  **AC 목록** (각각 명시적 검증):
  - AC1: [내용]
  - AC2: [내용]
  - AC3: [내용]

  **세부 목표 (Objectives)**:
  1. AC 항목별 충족/미충족 판정
  2. 누락된 기능/코드 식별
  3. 엣지 케이스 처리 확인 (null, 빈값, 경계값)
  4. 에러 핸들링 완전성 확인

  **범위 (Scope)**:
  - 포함: [변경된 파일 목록]
  - 제외: node_modules, *.test.ts

  **수행 단계 (Workflow)**:
  1. 변경된 파일 모두 읽기 → 코드 이해
  2. AC1~N 각각에 대해 충족 여부 판정 → 근거 제시
  3. 누락된 기능 목록화 → 구체적 내용
  4. 엣지 케이스 검사 → null/undefined/빈값/경계값
  5. 품질 기준 확인 → 500줄, 주석, 타입

  **출력 형식 (Output)**:
  ```
  ============================================
  [VALIDATOR] TASK-ID 검증 결과
  ============================================

  📋 AC 검증:
  ✅ AC1: [내용] | 충족 | 근거: [코드 위치]
  ❌ AC2: [내용] | 미충족 | 누락: [구체적 내용]
  ⚠️ AC3: [내용] | 부분 충족 | 이유: [설명]

  📦 완전성 검증:
  ✅/❌ 모든 기능 구현됨
  ✅/❌ 파일 구조 완전함
  ✅/❌ 의존성 연결 완료

  🔍 엣지 케이스:
  ✅/❌ null 처리
  ✅/❌ 빈값 처리
  ✅/❌ 에러 핸들링

  📊 품질 기준:
  ✅/❌ 줄 수: Xㅜ줄
  ✅/❌ 주석: 함수별 존재
  ✅/❌ 타입: 완전함

  ============================================
  🎯 결과: 통과 / reinforcer 필요
  ============================================
  ```

  **제약 조건 (Constraints)**:
  - ❌ 코드 수정 금지 (검증만)
  - ❌ 추측으로 판정 금지 (파일 읽어서 확인)
  - ✅ 모든 AC 명시적 검증
  - ✅ 미충족 시 구체적 내용 기술
  """
)
```

#### reinforcer 에이전트 (보강/수정) - 검증 실패 시

```
Task(
  subagent_type="calab-plugin:reinforcer",
  description="validator 결과 기반 [TASK-ID] 보강",
  prompt="""
  **역할 (Role)**: 품질 보강 전문가 - 누락/미흡 항목 수정 담당

  **목표 (Goal)**: validator가 발견한 모든 문제 해결

  **validator 검증 결과**:
  [validator 출력 전체 붙여넣기]

  **수정 대상** (우선순위순):
  [P0] AC 미충족:
  - [구체적 내용 1]
  - [구체적 내용 2]

  [P1] 기능 누락:
  - [구체적 내용]

  [P2] 엣지 케이스:
  - [구체적 내용]

  [P3] 품질 개선:
  - [구체적 내용]

  **세부 목표 (Objectives)**:
  1. P0 항목 100% 수정
  2. P1 항목 100% 수정
  3. P2 항목 가능한 수정
  4. P3 항목 가능한 수정

  **수행 단계 (Workflow)**:
  1. 대상 파일 읽기 → 현재 코드 이해
  2. P0 항목 수정 → 각 수정 후 주석 포함
  3. P1 항목 수정 → 누락 기능 구현
  4. P2 항목 수정 → 엣지 케이스 추가
  5. 변경 사항 목록화 → 파일:라인 형식

  **출력 형식 (Output)**:
  ```
  ============================================
  [REINFORCER] 수정 완료
  ============================================

  [P0] AC 미충족 수정:
  ✅ [내용] → [파일:라인-라인]

  [P1] 기능 누락 수정:
  ✅ [내용] → [파일:라인-라인]

  [P2] 엣지 케이스 추가:
  ✅ [내용] → [파일:라인-라인]

  [P3] 품질 개선:
  ✅ [내용] → [파일:라인-라인]

  📁 변경된 파일:
  • [파일명] (+X lines, -Y lines)

  ============================================
  🔄 validator 재검증 필요
  ============================================
  ```

  **제약 조건 (Constraints)**:
  - ❌ validator 결과 없이 수정 금지
  - ❌ 기존 기능 파괴하는 수정 금지
  - ❌ 3회 이상 수정 시도 금지 (사용자 확인 요청)
  - ✅ 기존 코드 스타일 유지
  - ✅ 모든 수정에 주석 포함
  - ✅ 최소 변경으로 문제 해결
  """
)
```

#### 필수 호출 순서 (validator → reinforcer → validator)

```
// 1. 구현 완료 후 필수 검증
Task(subagent_type="calab-plugin:validator", description="TASK-001 검증", ...)

// 2. 검증 실패 시 보강
if (validator.result === "reinforcer 필요") {
  Task(subagent_type="calab-plugin:reinforcer", description="TASK-001 보강", ...)
}

// 3. 보강 후 재검증 (필수)
Task(subagent_type="calab-plugin:validator", description="TASK-001 재검증", ...)

// 4. 최대 2회 반복 후 사용자 확인
```

### Hook 기반 자동 검증 (권장)

> **"No mess left behind - Clean, formatted, error-free code"** - Claude Code Best Practices

```
Claude 응답 완료
  ↓
Hook 1: 포맷터 실행 → 코드 자동 정렬
  ↓
Hook 2: 빌드 체크 → TypeScript 오류 즉시 감지
  ↓
Hook 3: 린트 체크 → ESLint 규칙 위반 감지
  ↓
Hook 4: 테스트 실행 → 회귀 버그 감지
  ↓
오류 발견 시 → Claude가 즉시 수정
  ↓
5개 이상 오류 → build-error-resolver 에이전트 권장
  ↓
결과: 검증된 깨끗한 코드
```

### 검증 우회 금지 규칙

> **🔴 아래 상황에서는 검증 에이전트 생략 절대 금지**

| 상황 | 필수 검증 에이전트 |
|------|-------------------|
| 새 파일 생성 | `calab-plugin:code-reviewer` |
| API 엔드포인트 추가 | `calab-plugin:code-reviewer` + `calab-plugin:security-reviewer` |
| 인증/인가 로직 | `calab-plugin:security-reviewer` 필수 |
| 데이터베이스 스키마 변경 | `calab-plugin:code-reviewer` + 마이그레이션 검증 |
| 10줄 이상 코드 변경 | `calab-plugin:code-reviewer` |
| 사용자 입력 처리 | `calab-plugin:security-reviewer` |
| Task 완료 시 | `calab-plugin:validator` 필수 |
| 외부 API 호출 | 에러 처리 검증 |

### 검증 결과 보고 형식

```
[검증 보고서] {작업명}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 통과 항목 (N개)
- 항목1: 설명
- 항목2: 설명

❌ 누락 항목 (N개)
1. 항목: [구체적 내용] → 권장 수정
2. 항목: [구체적 내용] → 권장 수정

⚠️ 개선 필요 (N개)
1. 항목: [현재 상태] → [권장 개선]

📊 종합
- 완전성: X/10
- 품질: X/10
- 보안: X/10

🎯 결론: [통과 ✅ / 보강 필요 ❌]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 스킬 활용 전략

### 스킬 vs 에이전트 차이

| 구분 | 스킬 (Skill) | 에이전트 (Agent) |
|------|-------------|-----------------|
| **정의** | 사전 정의된 작업 템플릿 | 독립적 실행 주체 |
| **호출 방식** | `/명령어` 또는 자동 | `Task()` 도구 |
| **컨텍스트** | 공유 | 격리 (선택적) |
| **지속성** | 세션 내 | 작업 완료 후 종료 |

### 스킬 카테고리 (9개)

#### 메타 스킬 (3개) - 명시적 호출

| 스킬 | 명령어 | 역할 |
|------|--------|------|
| **dev** | `/dev --plan/--design/--tasks/--build` | 전체 개발 워크플로우 (기획→설계→구현) |
| **solve** | `/solve --5whys/--rca/--hypothesis` | 문제 해결 (디버깅, 버그 수정) |
| **onboard** | `/onboard --quick/--phases` | 프로젝트 분석 및 컨텍스트 생성 |

#### 패시브 스킬 (6개) - 자동 활성화

| 스킬 | 트리거 조건 | 역할 |
|------|------------|------|
| `best-practices` | 기술 키워드 감지 | 언어별 베스트 프랙티스 로드 |
| `code-quality` | 코드 생성/수정 | 500줄 제한, 주석 필수 |
| `tdd-workflow` | `--tdd`, 테스트 키워드 | RED→GREEN→REFACTOR 강제 |
| `project-rules` | 모든 코드 작성 | PROJECT_RULES.md 참조 |
| `work-tracker` | 소스 파일 수정 | Worktree 자동 업데이트 |
| `clarification-protocol` | 서브에이전트 실행 | 플래그 기반 명확화 |

### 스킬 연계 전략

#### 개발 워크플로우 (권장)

```mermaid
/onboard → /dev --plan → /dev --design → /dev --tasks → /dev --build
    ↓                                                        ↓
 PROJECT_RULES                                          validator
    ↓                                                        ↓
 best-practices                                         reinforcer
```

#### 문제 해결 워크플로우

```mermaid
에러 발생 → /solve (자동 방법론 선택)
              ├─ --5whys (반복 문제)
              ├─ --rca (시스템 문제)
              └─ --hypothesis (불명확 원인)
                     ↓
              root-cause-finder → bug-fixer → validator
```

### 통합된 기능 (삭제된 스킬 → 대체)

| 기존 스킬 | 대체 방법 |
|----------|----------|
| `/clean` | `/dev --design` (아키텍처 설계) |
| `/docs` | `calab-plugin:doc-updater` 에이전트 |
| `/jira` | `calab-plugin:jira-connector` 에이전트 |
| `/qa` | `calab-plugin:qa` 에이전트 |
| `/security` | `calab-plugin:security-reviewer` 에이전트 |
| `/quality` | `calab-plugin:code-reviewer` 에이전트 |
| `/restore`, `/save` | `.claude/memory/` 자동 관리 |
| `/research` | `calab-plugin:web-researcher` 에이전트 |

---

## 워크플로우 가이드

### 새 프로젝트 시작

```bash
/onboard              # 1. 프로젝트 분석 및 컨텍스트 생성
/context --show       # 2. 생성된 컨텍스트 확인
/rules                # 3. 프로젝트 규칙 확인
```

### 기능 개발 (권장 워크플로우)

```bash
/dev --plan [기능명]   # 1. PRD 작성
/dev --design         # 2. 아키텍처 설계
/dev --tasks          # 3. 태스크 분해
/dev --build TASK-001 # 4. 태스크별 구현
/dev --status         # 5. 진행 상태 확인
```

### 문제 해결

```bash
/solve [에러 메시지]   # 자동으로 적절한 방법론 선택
/solve --5whys        # 5 Whys 분석
/solve --rca          # Root Cause Analysis
/solve --hypothesis   # 가설 검증
```

### 코드 품질 관리

```bash
/quality              # 전체 코드 품질 검사
/security             # OWASP Top 10 보안 검사
```

### 세션 복원

```bash
/restore              # Compact 후 컨텍스트 복원
/save                 # 중요 시점 체크포인트 저장
```

---

## 명령어 참조

### 메타커맨드 (8개)

| 명령어 | 자연어 | 설명 |
|--------|--------|------|
| `/dev [--plan\|--design\|--tasks\|--build\|--status]` | "기획/설계/구현" | 개발 워크플로우 |
| `/clean [--init\|--entity\|--usecase\|--validate]` | "클린 아키텍처" | 4-Layer 관리 |
| `/docs [--generate\|--add\|--update\|--validate\|--status]` | "문서화" | 문서 자동화 |
| `/jira [--init\|--pull\|--push\|--link\|--status\|--sync]` | "지라 연동" | JIRA 동기화 |
| `/qa [--plan\|--run\|--report\|--status]` | "QA 테스트" | E2E 관리 |
| `/solve [--5whys\|--rca\|--hypothesis\|--log\|--report]` | "문제 해결" | 체계적 해결 |
| `/onboard [--quick\|--phases]` | "프로젝트 분석" | 컨텍스트 생성 |
| `/context [--show\|--refresh]` | "컨텍스트" | 표시/갱신 |

### 독립 명령어 (8개)

| 명령어 | 자연어 | 설명 |
|--------|--------|------|
| `/security` | "보안 검사" | OWASP Top 10 |
| `/quality` | "품질 검사" | 코드 품질 |
| `/restore` | "복원" | 상태 복원 |
| `/save` | "저장" | 체크포인트 |
| `/rules` | "규칙" | 규칙 표시 |
| `/worktree` | "작업 트리" | 진행률 |
| `/learn [영역]` | "학습" | 심층 학습 |
| `/research [주제]` | "조사" | 검색 + 요약 |

---

## 자동화 규칙

### 자동 동작 요약

| 트리거 | 자동 동작 |
|--------|----------|
| **코드 작성** | 품질 검사 + 베스트 프랙티스 적용 |
| **파일 수정** | 변경 이력 기록 + worktree 업데이트 |
| **세션 시작** | 이전 컨텍스트 안내 |
| **Compact** | 체크포인트 자동 저장 |
| **빌드 오류** | `calab-plugin:build-error-resolver` 자동 호출 |
| **보안 이슈** | `calab-plugin:security-reviewer` 자동 호출 |
| **구현 완료** | `calab-plugin:validator` 검증 필수 |

---

## 품질 규칙

### 코드 품질 기준

| 항목 | 기준 |
|------|------|
| **파일 크기** | 500줄 이하 |
| **함수 주석** | 모든 함수 필수 (JSDoc/Docstring) |
| **타입 정의** | 100% 타입 커버리지 |
| **네이밍** | 기술별 컨벤션 (best-practices 참조) |

### 테스트 커버리지

| 커버리지 | 최소 | 권장 |
|---------|------|------|
| 라인 | 70% | 80% |
| 브랜치 | 60% | 70% |
| 함수 | 80% | 90% |

---

## 세션 관리

### Compact 발생 시

```bash
/restore   # 규칙 + 작업 상태 즉시 복원
```

### 작업 스택 유지

```
[상위] 사용자 인증 시스템 구현
  └─[하위] JWT 토큰 생성 함수 작성
      └─[현재] 토큰 만료 검증 로직
```

하위 작업 완료 후 **반드시 상위 작업으로 복귀**

---

## 빠른 참조 카드

### 에이전트 호출 Quick Reference

```
// ========================================
// 기본 에이전트 (prefix 없음)
// ========================================

// 코드베이스 탐색
Task(subagent_type="Explore", "src/ 구조 분석, medium 깊이")

// 구현 계획
Task(subagent_type="Plan", "사용자 인증 시스템, JWT 기반, Next.js 14")

// 범용 작업
Task(subagent_type="general-purpose", "복잡한 멀티스텝 작업...")

// ========================================
// 플러그인 에이전트 (calab-plugin: 필수)
// ========================================

// 보안 검사
Task(subagent_type="calab-plugin:security-reviewer", "OWASP Top 10 기준 인증 API 검사")

// 코드 리뷰
Task(subagent_type="calab-plugin:code-reviewer", "성능 관점 PR 리뷰, 리렌더링 체크")

// 완전성 검증 (구현 후 필수)
Task(subagent_type="calab-plugin:validator", "TASK-001 AC 검증")

// 보강 (검증 실패 시)
Task(subagent_type="calab-plugin:reinforcer", "validator 결과 기반 수정")

// 웹 리서치
Task(subagent_type="calab-plugin:web-researcher", "React 19 변경사항 조사")

// 심층 분석
Task(subagent_type="calab-plugin:deep-researcher", "리서치 결과 종합 보고서")

// ========================================
// 병렬 실행 (의존성 없는 작업만)
// ========================================
Task(subagent_type="Explore", "프론트엔드 분석")
Task(subagent_type="Explore", "백엔드 분석")
Task(subagent_type="Explore", "DB 스키마 분석")
```

### 스킬 호출 Quick Reference

```bash
# 개발 워크플로우
/dev --plan 사용자 인증 → /dev --design → /dev --tasks → /dev --build

# 문제 해결
/solve TypeError: Cannot read property 'id' of undefined

# 품질 검사
/quality && /security

# 컨텍스트 관리
/save → /restore
```

