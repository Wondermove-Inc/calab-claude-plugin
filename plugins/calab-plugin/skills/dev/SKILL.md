---
name: dev
description: |
  개발 워크플로우를 실행합니다. 기획(Plan), 설계(Design), 태스크 분해(Tasks), 구현(Build)을 순차적으로 진행합니다.
  USE WHEN: 새 기능, new feature, 개발, develop, 프로젝트 시작, 설계, design,
  아키텍처, architecture, PRD, 요구사항, requirement, 기획, plan,
  구현해줘, 만들어줘, build, implement, create,
  스펙, spec, 명세, 정의, define,
  브레인스토밍, brainstorm, 아이디어, idea,
  태스크, task, 스토리, story, 에픽, epic,
  착수, 시작, start, 진행, proceed
argument-hint: "[--plan|--design|--tasks|--build|--status] [기능명]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, mcp__tavily__tavily-search]
agent: dev-workflow
agents:
  primary: dev-workflow
  orchestration:
    plan: [Plan, deep-researcher]
    design: [Plan, Explore]
    tasks: [dev-workflow]
    build: [dev-workflow, code-reviewer, tdd-workflow]
    validate: [validator]
    fix: [reinforcer]
    review: [code-reviewer, security-reviewer, validator]
---

# /dev - 개발 워크플로우

> **Plan → Design → Tasks → Build 전체 사이클 관리**

## 사용법

```bash
/dev [기능명]              # 전체 워크플로우 시작 (순차 실행)
/dev --plan [기능명]       # 기획 단계만 (브레인스토밍 + PRD)
/dev --design [기능명]     # 설계 단계만 (아키텍처 + ERD)
/dev --tasks [기능명]      # 태스크 분해만
/dev --build [TASK-ID]     # 특정 태스크 구현
/dev --status              # 현재 진행 상황 확인
/dev --help                # 도움말
```

## 🤖 에이전트 호출 (필수)

> **이 스킬은 단계별로 적절한 에이전트를 호출해야 합니다.**

### --plan 단계

```
Task(
  subagent_type="Plan",
  description="기능 기획: {기능명}",
  prompt="""
  **역할**: 소프트웨어 아키텍트

  **목표**: {기능명}에 대한 PRD 및 브레인스토밍

  **산출물**:
  1. 브레인스토밍 결과 (.claude/docs/active/{feature}/01-brainstorm.md)
  2. PRD 문서 (.claude/docs/active/{feature}/02-prd.md)

  **템플릿**: templates/prd-template.md 사용
  """
)
```

### --design 단계

```
Task(
  subagent_type="Plan",
  description="아키텍처 설계: {기능명}",
  prompt="""
  **역할**: 시스템 아키텍트

  **목표**: 상세 아키텍처 및 ERD 설계

  **산출물**:
  1. 아키텍처 문서 (.claude/docs/active/{feature}/03-architecture.md)
  2. ERD (.claude/docs/active/{feature}/04-erd.md)
  """
)
```

### --build 단계 (완료 후 검증 필수)

```
// 1. 구현
Task(
  subagent_type="calab-plugin:dev-workflow",
  description="TASK-{ID} 구현",
  prompt="AC 기반 코드 구현..."
)

// 2. 검증 (필수)
Task(
  subagent_type="calab-plugin:validator",
  description="TASK-{ID} 검증",
  prompt="AC 100% 충족 확인..."
)

// 3. 검증 실패 시 보강
Task(
  subagent_type="calab-plugin:reinforcer",
  description="TASK-{ID} 보강",
  prompt="누락 항목 수정..."
)
```

---

## 인자 파싱

입력: $ARGUMENTS

### 옵션별 라우팅

1. **`--help` 또는 `-h`** → 이 파일의 사용법 출력 후 종료

2. **`--plan`** → `references/plan.md` 실행
   - 브레인스토밍 + PRD 작성
   - `--brainstorm` 또는 `--prd` 단독 실행 가능

3. **`--design`** → `references/design.md` 실행
   - 아키텍처 설계 + ERD 작성
   - `--arch` 또는 `--erd` 단독 실행 가능

4. **`--tasks`** → `references/tasks.md` 실행
   - Epic → Story → Task 분해
   - AC(Acceptance Criteria) 정의

5. **`--build [TASK-ID]`** → `references/build.md` 실행
   - 베스트 프랙티스 적용 구현
   - `--tdd` 옵션 지원

6. **`--status`** → `references/status.md` 실행
   - 워크플로우 진행 상황 표시

7. **옵션 없음 (기능명만)** → 전체 워크플로우 순차 실행
   ```
   Plan → Design → Tasks → 첫 번째 Task Build
   ```

## 워크플로우 단계

```
┌─────────────────────────────────────────────────────────┐
│                    /dev 워크플로우                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  PLAN    │───▶│  DESIGN  │───▶│  TASKS   │          │
│  │          │    │          │    │          │          │
│  │ 01-brain │    │ 03-arch  │    │ 05-tasks │          │
│  │ 02-prd   │    │ 04-erd   │    │ worktree │          │
│  └──────────┘    └──────────┘    └──────────┘          │
│                                        │               │
│                                        ▼               │
│  ┌────────────────────────────────────────────────────┐│
│  │                     BUILD                          ││
│  │  ┌────────┐   ┌────────┐   ┌────────┐             ││
│  │  │TASK-001│──▶│TASK-002│──▶│TASK-00N│   ...       ││
│  │  └────────┘   └────────┘   └────────┘             ││
│  └────────────────────────────────────────────────────┘│
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 출력 폴더 구조

```
.claude/docs/active/{feature-name}/
├── 01-brainstorm.md     # /dev --plan --brainstorm
├── 02-prd.md            # /dev --plan --prd
├── 03-architecture.md   # /dev --design --arch
├── 04-erd.md            # /dev --design --erd
├── 05-tasks.md          # /dev --tasks
└── qa/                  # /qa 시 생성
    ├── plan.md
    └── report.md

.claude-state/
└── worktree.json        # /dev --tasks 시 자동 생성
```

## 상태 추적

- **worktree.json**: 태스크 상태 (pending → in_progress → done)
- **CURRENT_CONTEXT.md**: 현재 작업 컨텍스트
- **05-tasks.md**: 전체 태스크 목록 + AC

## 에이전트 오케스트레이션

각 단계별 최적의 에이전트 조합:

```
┌─────────────────────────────────────────────────────────┐
│                 에이전트 오케스트레이션                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  --plan 단계:                                           │
│  ├── Plan 에이전트: 아키텍처 설계, 요구사항 분석          │
│  └── deep-researcher: 베스트 프랙티스 검색               │
│                                                         │
│  --design 단계:                                         │
│  ├── Plan 에이전트: 상세 설계                           │
│  └── Explore 에이전트: 기존 코드 패턴 분석               │
│                                                         │
│  --tasks 단계:                                          │
│  └── dev-workflow: 태스크 분해 및 AC 정의               │
│                                                         │
│  --build 단계:                                          │
│  ├── dev-workflow: 코드 구현                            │
│  ├── code-reviewer: 코드 품질 검증 (병렬)                │
│  └── tdd-workflow 스킬: 테스트 작성 (--tdd 옵션 시)      │
│                                                         │
│  완료 후 검증:                                          │
│  ├── validator: 완전성 검증 (AC, 누락, 엣지케이스)       │
│  ├── code-reviewer: 최종 코드 리뷰                      │
│  └── security-reviewer: 보안 취약점 검사                 │
│                                                         │
│  검증 실패 시:                                          │
│  └── reinforcer: 누락/미흡 항목 자동 수정               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 병렬 실행 가능 조합

| 조합 | 실행 방식 | 용도 |
|------|----------|------|
| Plan + deep-researcher | 병렬 | 설계 + 리서치 동시 |
| dev-workflow + code-reviewer | 순차 | 구현 → 검증 |
| code-reviewer + security-reviewer | 병렬 | 품질 + 보안 동시 검사 |
| validator → reinforcer | 순차 | 검증 → 수정 (필수 체인) |

## 레거시 명령어 호환

| 이전 명령어 | 신규 명령어 |
|------------|------------|
| `/dev-plan` | `/dev --plan` |
| `/dev-design` | `/dev --design` |
| `/dev-tasks` | `/dev --tasks` |
| `/dev-build` | `/dev --build` |
| `/dev-status` | `/dev --status` |

## 다음 단계 안내

| 완료 후 | 권장 명령어 |
|--------|------------|
| /dev --plan | `/dev --design` |
| /dev --design | `/dev --tasks` |
| /dev --tasks | `/dev --build TASK-001` |
| /dev --build | `/worktree` 또는 다음 TASK |
| 전체 완료 | `/qa` |

## 참조 파일

### 템플릿 (필수 사용)

| 단계 | 템플릿 | 용도 |
|------|--------|------|
| --plan | `templates/prd-template.md` | PRD 작성 |
| --design | `templates/architecture-template.md` | 아키텍처 설계 |
| --design | `templates/erd-template.md` | ERD 작성 |
| --tasks | `templates/task-template.md` | 태스크 분해 |

### 베스트 프랙티스 (스킬 내부)

- `references/clean-architecture.md` - 클린 아키텍처
- `references/api-design.md` - API 설계
- `references/typescript.md` - TypeScript 패턴

### 추가 참조 (프로젝트 전역)

- `.claude/best-practices/testing.md` - 테스트 전략
