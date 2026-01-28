---
name: qa
description: |
  프론트엔드 기능 QA를 수행합니다. QA 계획서 작성, 테스트 실행, 보고서 생성을 담당합니다.
  USE WHEN: QA, 테스트, test, testing, 검증, verify, validation,
  품질, quality, 품질보증, assurance,
  시나리오, scenario, 케이스, case, 테스트케이스,
  통과, pass, 실패, fail, 성공, success,
  커버리지, coverage, 80%, 70%,
  E2E, end-to-end, 통합, integration, 단위, unit,
  자동화, automation, playwright, puppeteer, jest, vitest, cypress,
  회귀, regression, 스모크, smoke
argument-hint: "[--plan|--run|--report|--status]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, mcp__puppeteer__puppeteer_navigate, mcp__puppeteer__puppeteer_screenshot, mcp__puppeteer__puppeteer_click, mcp__puppeteer__puppeteer_fill, mcp__puppeteer__puppeteer_evaluate]
agent: e2e-runner
agents:
  primary: e2e-runner
  orchestration:
    plan: [Plan, Explore]
    run: [e2e-runner]
    debug: [e2e-runner, deep-researcher, build-error-resolver]
    report: [e2e-runner, code-reviewer]
    review: [code-reviewer]
---

# /qa - QA 테스트

> **프론트엔드 기능 QA 프로세스**

## 사용법

```bash
/qa                        # QA 프로세스 시작 (기본)
/qa --plan                 # QA 계획서 생성
/qa --run                  # 테스트 실행
/qa --report               # 보고서 생성
/qa --status               # 진행 상황 확인
/qa --help                 # 도움말
```

## 인자 파싱

입력: $ARGUMENTS

### 옵션별 라우팅

1. **`--help` 또는 `-h`** → 도움말 출력

2. **옵션 없음** → 전체 QA 프로세스 시작
   - 환경 확인 → 기능 수집 → 계획 작성 → 테스트 케이스 생성

3. **`--plan`** → `references/plan.md` 실행
   - 테스트 범위 정의
   - 전략 수립
   - 성공 기준 정의

4. **`--run`** → `references/run.md` 실행
   - MCP Puppeteer로 E2E 테스트
   - 순차 실행 + 스크린샷
   - 100% 완료까지 자동 진행

5. **`--report`** → `references/report.md` 실행
   - 테스트 결과 집계
   - 버그 분석
   - 릴리스 권고

6. **`--status`** → `references/status.md` 실행
   - 진행률 확인
   - 버그 현황
   - 다음 단계 안내

## QA 프로세스

```
┌─────────────────────────────────────────┐
│              QA 프로세스                 │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐    ┌──────────┐          │
│  │   /qa    │───▶│ /qa --plan│          │
│  │  시작    │    │ 계획 수립 │          │
│  └──────────┘    └──────────┘          │
│                       │                 │
│                       ▼                 │
│  ┌──────────┐    ┌──────────┐          │
│  │/qa --status│◄──│/qa --run │          │
│  │ 상태 확인 │    │ 테스트   │          │
│  └──────────┘    └──────────┘          │
│                       │                 │
│                       ▼                 │
│                  ┌──────────┐          │
│                  │/qa --report│         │
│                  │  보고서   │          │
│                  └──────────┘          │
│                                         │
└─────────────────────────────────────────┘
```

## 파일 구조

```
.claude/docs/active/{feature}/qa/
├── QA_PLAN.md           # 계획서
├── TEST_CASES.md        # 테스트 케이스
├── QA_REPORT.md         # 최종 보고서
└── BUG_REPORT.md        # 버그 보고서

.claude-state/qa/
├── qa-status.json       # 진행 상태
├── test-cases.json      # 테스트 케이스 데이터
├── test-results.json    # 실행 결과
├── bugs.json            # 버그 목록
└── screenshots/         # 스크린샷
```

## 우선순위 분류

| 우선순위 | 설명 | 목표 Pass Rate |
|---------|------|---------------|
| P0 | Critical - 핵심 기능 | 100% |
| P1 | High - 중요 기능 | 95%+ |
| P2 | Medium - 일반 기능 | 90%+ |

## 테스트 케이스 형식

```markdown
## TC-001: 로그인 성공

**Given**: 유효한 계정 정보
**When**: 로그인 버튼 클릭
**Then**: 대시보드로 이동

**Steps**:
1. 로그인 페이지 접속
2. 이메일 입력: test@example.com
3. 비밀번호 입력: password123
4. 로그인 버튼 클릭
5. 대시보드 URL 확인
```

## 버그 심각도

| 심각도 | 아이콘 | 설명 |
|--------|------|------|
| Critical | 🔴 | 서비스 불가 |
| Major | 🟠 | 주요 기능 장애 |
| Minor | 🟡 | 불편함 |
| Trivial | ⚪ | 미미한 이슈 |

## 릴리스 권고

| 권고 | 조건 |
|------|------|
| ✅ Approved | P0=100%, Critical=0 |
| ⚠️ Conditional | P0≥95%, Critical=0 |
| ❌ Not Approved | P0<95% 또는 Critical>0 |

## 레거시 명령어 호환

| 이전 명령어 | 신규 명령어 |
|------------|------------|
| `/qa` | `/qa` (유지) |
| `/qa-plan` | `/qa --plan` |
| `/qa-run` | `/qa --run` |
| `/qa-report` | `/qa --report` |
| `/qa-status` | `/qa --status` |

## MCP Puppeteer 사용

```javascript
// 페이지 이동
mcp__puppeteer__puppeteer_navigate({ url: "http://localhost:3000" })

// 스크린샷
mcp__puppeteer__puppeteer_screenshot({ name: "login-page" })

// 입력
mcp__puppeteer__puppeteer_fill({ selector: "#email", value: "test@example.com" })

// 클릭
mcp__puppeteer__puppeteer_click({ selector: "#submit" })

// JavaScript 실행
mcp__puppeteer__puppeteer_evaluate({ script: "document.title" })
```

## 다음 단계

| 상황 | 권장 명령어 |
|------|------------|
| QA 시작 | `/qa` |
| 계획만 필요 | `/qa --plan` |
| 테스트 실행 | `/qa --run` |
| 진행 확인 | `/qa --status` |
| 완료 후 | `/qa --report` |

## 참조 파일

### 템플릿 (스킬 내부)

| 용도 | 템플릿 |
|------|--------|
| QA 계획서 | `templates/qa-plan-template.md` |
| QA 보고서 | `templates/qa-report-template.md` |

### 베스트 프랙티스 (스킬 내부)

- `references/testing.md` - 테스트 전략
- `references/qa-testing.md` - E2E 테스트

### 추가 참조 (프로젝트 전역)

- `.claude/best-practices/react/react-*.md` - React 컴포넌트 테스트
