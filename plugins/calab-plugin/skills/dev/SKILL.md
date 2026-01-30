---
name: dev
description: |
  통합 개발 워크플로우 매니저. Plan → Design → Tasks → Build 전체 사이클 관리.
  USE WHEN: 새 기능, 개발, 설계, 아키텍처, PRD, 구현, 태스크, 스토리
argument-hint: "[--plan|--design|--tasks|--build|--status] [기능명]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, WebSearch, AskUserQuestion, EnterPlanMode, ExitPlanMode, mcp__tavily__tavily-search]
skills: [code-quality, best-practices, tdd-workflow, project-rules, work-tracker]
agents:
  primary: planner-phase
  orchestration:
    plan: [calab-plugin:planner-phase, calab-plugin:deep-researcher]
    design: [calab-plugin:design, Explore]
    tasks: [calab-plugin:planner-task, calab-plugin:task-validator]
    build: [calab-plugin:dev-executor, calab-plugin:code-reviewer]
    status: [calab-plugin:dev-workflow]
    validate: [calab-plugin:validator, calab-plugin:qa]
    fix: [calab-plugin:reinforcer]
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/code_quality_validator.py\""
  SubagentStop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/subagent_tracker.py\" stop"
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /dev - 통합 개발 워크플로우

> **Plan → Design → Tasks → Build 전체 사이클 관리**

---

## Data Flow Contract

### Input (스킬 간 데이터 수신)

| 소스 | 데이터 | 용도 |
|------|--------|------|
| `/onboard` | `.claude/project-context/*.md` | 프로젝트 컨텍스트 참조 |
| `/solve` | `.claude/problem-solving/resolved/*/report.md` | 버그 수정 후 기능 전환 시 |

### Output (스킬 간 데이터 전달)

| 단계 | 산출물 | 다음 단계 Input |
|------|--------|----------------|
| `--plan` | `01-brainstorm.md`, `02-PRD.md` | `--design` |
| `--design` | `03-architecture.md`, `04-ERD.md` | `--tasks` |
| `--tasks` | `05-tasks.md`, `.claude-state/worktree.json` | `--build` |
| `--build` | 소스코드, 테스트코드, `worktree.json` 업데이트 | QA |

### State Update

- `.claude-state/worktree.json` - Task 상태 (pending → in_progress → done)
- `.claude/memory/CURRENT_CONTEXT.md` - 현재 작업 컨텍스트

---

## 사용법

```bash
/dev [기능명]              # 전체 워크플로우
/dev --plan [기능명]       # 기획 (PRD)
/dev --design [기능명]     # 설계 (아키텍처)
/dev --tasks [기능명]      # 태스크 분해
/dev --build [TASK-ID]     # 구현 (TDD)
/dev --status              # 진행 상황
```

---

## Structured Handoffs (단계 간 전제 조건)

| 단계 | 전제 조건 (필수 확인) |
|------|---------------------|
| `--plan` | 없음 (첫 단계) |
| `--design` | `01-brainstorm.md` + `02-PRD.md` 존재 확인 |
| `--tasks` | `03-architecture.md` + `04-ERD.md` 존재 확인 |
| `--build` | `05-tasks.md` + `worktree.json` 존재 확인 |

**전제 조건 미충족 시**: 이전 단계 먼저 실행 안내

---

## 에이전트 호출 (필수)

> **⚠️ 이 스킬이 로드되면 아래 지침을 따라 Task 도구를 호출하세요.**

### --plan 단계

**전제 조건**: 없음
**Routing**: `references/plan-phase.md` 참조

```python
Task(
    subagent_type="calab-plugin:planner-phase",
    description="기능 기획",
    prompt="... (references/plan-phase.md 참조)"
)
```

**산출물 필수**: `01-brainstorm.md`, `02-PRD.md`

### --design 단계

**전제 조건**: `01-brainstorm.md` + `02-PRD.md` 존재 필수
**Routing**: `references/design-phase.md` 참조

```python
Task(
    subagent_type="calab-plugin:design",
    description="아키텍처 설계",
    prompt="... (references/design-phase.md 참조)"
)
```

**산출물 필수**: `03-architecture.md`, `04-ERD.md`

### --tasks 단계

**전제 조건**: `03-architecture.md` + `04-ERD.md` 존재 필수
**Routing**: `references/tasks-phase.md` 참조

```python
Task(
    subagent_type="calab-plugin:planner-task",
    description="Task 분해",
    prompt="... (references/tasks-phase.md 참조)"
)
```

**산출물 필수**: `05-tasks.md`, `.claude-state/worktree.json`

### --build 단계

**전제 조건**: `05-tasks.md` + `worktree.json` 존재 필수
**Routing**: `references/build-phase.md` 참조

```python
Task(
    subagent_type="calab-plugin:dev-executor",
    description="TDD 구현",
    prompt="... (references/build-phase.md 참조)"
)
```

**산출물 필수**: 소스코드, 테스트코드, `worktree.json` 업데이트

---

## 검증/보강 체인 (필수)

```
구현 (dev-executor)
    ↓
검증 (validator) ─────┬─ 성공 → 다음 Task
    ↓                 │
실패 → reinforcer ────┴─ 재검증 (validator)
```

**신뢰도 기반 에스컬레이션**:
- 90%+ → 다음 Task
- 70-89% → reinforcer
- <70% → `/solve` 또는 사용자 결정

---

## 워크플로우 다이어그램

```
PLAN ────────→ DESIGN ─────────→ TASKS ──→ BUILD
  │               │                 │         │
  ↓               ↓                 ↓         ↓
01-brainstorm  03-architecture   05-tasks   코드+테스트
02-PRD         04-ERD
```

---

## 레퍼런스 라우팅

| 옵션 | 참조 파일 |
|------|----------|
| `--plan` | `references/plan-phase.md` |
| `--design` | `references/design-phase.md` |
| `--tasks` | `references/tasks-phase.md` |
| `--build` | `references/build-phase.md` |
| `--status` | `references/status.md` |

---

## 다음 단계

| 완료 후 | 권장 |
|--------|------|
| `--plan` | `--design` |
| `--design` | `--tasks` |
| `--tasks` | `--build TASK-001` |
| 모든 Task 완료 | QA 자동 호출 |
| QA 실패 | `/solve` |
