---
name: dev
description: |
  통합 개발 워크플로우 매니저. 기획(Plan), 설계(Design), 태스크 분해(Tasks), 구현(Build)을 순차적으로 진행합니다.
  요청 유형을 자동 분류하여 최적의 프로세스를 적용합니다.
  USE WHEN: 새 기능, new feature, 개발, develop, 프로젝트 시작, 설계, design,
  아키텍처, architecture, PRD, 요구사항, requirement, 기획, plan,
  구현해줘, 만들어줘, build, implement, create,
  스펙, spec, 명세, 정의, define,
  브레인스토밍, brainstorm, 아이디어, idea,
  태스크, task, 스토리, story, 에픽, epic,
  착수, 시작, start, 진행, proceed
argument-hint: "[--plan|--design|--tasks|--build|--status] [기능명]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, WebSearch, AskUserQuestion, EnterPlanMode, ExitPlanMode, mcp__tavily__tavily-search]
agents:
  primary: planner-phase
  orchestration:
    plan: [calab-plugin:planner-phase, calab-plugin:deep-researcher]
    design: [calab-plugin:design, Explore]
    tasks: [calab-plugin:planner-task, calab-plugin:task-validator]
    build: [calab-plugin:dev-executor, calab-plugin:code-reviewer]
    validate: [calab-plugin:validator, calab-plugin:qa]
    fix: [calab-plugin:reinforcer]
    review: [calab-plugin:code-reviewer, calab-plugin:security-reviewer, calab-plugin:validator]
---

# /dev - 통합 개발 워크플로우 매니저

> **Plan → Design → Tasks → Build 전체 사이클 관리**
> **요청 유형 자동 분류 + 도메인 분석 + 에이전트 오케스트레이션**

---

## 0. 요청 유형 분류 (자동)

사용자 요청을 분석하여 유형을 결정합니다:

| Type | Description | Example |
|------|-------------|---------|
| NEW_DEVELOPMENT | 새로운 기능 개발 | "인증 기능 추가" |
| MODIFICATION | 기존 기능 수정 | "로그인 방식 변경" |
| BUG_FIX | 버그 수정 | "로그인 오류 수정" |
| MULTI_INTENT | 복합 요청 | "버그 수정하고 기능 추가" |

### 유형별 프로세스 파일

| Type | Process File |
|------|--------------|
| NEW_DEVELOPMENT / MODIFICATION | `rules/processes/development-process.md` |
| BUG_FIX | `/solve` 스킬로 위임 |

---

## 1. 도메인 분석 (자동)

영향받는 도메인을 분석하여 적절한 가이드를 로드합니다:

```python
def detect_domains(request, file_paths):
    domains = set()

    # 디렉토리 기반 감지
    for path in file_paths:
        if "frontend" in path or "components" in path:
            domains.add("frontend")
        elif "api" in path or "services" in path:
            domains.add("backend")
        elif "models" in path or "schema" in path:
            domains.add("database")

    # 키워드 기반 감지
    keywords = {
        "frontend": ["UI", "컴포넌트", "페이지", "React"],
        "backend": ["API", "서비스", "Zod", "엔드포인트"],
        "database": ["SQL", "마이그레이션", "스키마", "테이블"],
    }

    return domains
```

---

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

## 🤖 에이전트 실행 (필수)

**⚠️ 이 스킬이 로드되면 아래 지침을 따라 즉시 Task 도구를 호출하세요.**

### --plan 단계 (PRD + PHASE 분해)

**Task 도구 호출**:
```python
Task(
    subagent_type="calab-plugin:planner-phase",
    description="기능 기획: {기능명}",
    prompt="""
    **역할**: 소프트웨어 아키텍트

    **목표**: {기능명}에 대한 PRD 및 PHASE 분해

    **산출물**:
    1. PRD 문서 (.claude/plans/{feature-name}.md)
       - Overview, Objectives
       - Technical Requirements
       - PHASE Decomposition
       - Acceptance Criteria

    **요청 유형**: {NEW_DEVELOPMENT|MODIFICATION}
    **도메인**: {detected_domains}
    """,
    run_in_background=True
)
```

### --design 단계 (아키텍처 + ERD)

**Task 도구 호출**:
```python
Task(
    subagent_type="calab-plugin:design",
    description="아키텍처 설계: {기능명}",
    prompt="""
    **역할**: 시스템 아키텍트

    **목표**: 상세 아키텍처 및 ERD 설계

    **산출물**:
    1. 아키텍처 문서 (.claude/plans/{feature-name}-DESIGN.md)
       - Component Diagram
       - Layer Responsibilities
       - Data Model (ERD)
       - API Design

    **참조**: PRD 문서 (.claude/plans/{feature-name}.md)
    """,
    run_in_background=True
)
```

### --tasks 단계 (Task 분해 + 검증)

**Task 도구 호출 (순차)**:
```python
# 1. Task 분해
Task(
    subagent_type="calab-plugin:planner-task",
    description="Task 분해: {기능명}",
    prompt="""
    **역할**: 개발 플래너

    **목표**: PHASE를 개별 Task로 분해 (TDD 워크플로우)

    **산출물**:
    - TaskCreate로 각 Task 생성
    - AC, 의존성, TDD 단계 명시
    """,
    run_in_background=True
)

# 2. Task 검증 (HARD GATE)
Task(
    subagent_type="calab-plugin:task-validator",
    description="Task 검증: {기능명}",
    prompt="""
    **역할**: 품질 게이트

    **목표**: Task 분해 검증
    - PHASE 커버리지
    - PRD 목표 매핑
    - 의존성 순서
    - 완전성
    """,
    run_in_background=True
)
```

### --build 단계 (TDD 구현 + 검증)

**Task 도구 호출 (TaskList 기반 병렬 실행)**:
```python
# 1. 실행 가능한 Task 조회
all_tasks = TaskList()
executable = [t for t in all_tasks if t.status == "pending" and not t.blockedBy]

# 2. 병렬 구현 (독립 Task)
for task in executable:
    TaskUpdate(taskId=task.id, status="in_progress")
    Task(
        subagent_type="calab-plugin:dev-executor",
        description=f"구현: {task.subject}",
        prompt=f"""
        **Task**: {task.id}
        **AC**: {task.description}

        TDD 워크플로우:
        1. RED: 실패하는 테스트 작성
        2. GREEN: 테스트 통과하는 코드 작성
        3. REFACTOR: 코드 정리
        """,
        run_in_background=True
    )

# 3. 검증 필수
Task(
    subagent_type="calab-plugin:validator",
    description="구현 검증",
    prompt="AC 100% 충족 확인, 엣지 케이스, 품질 기준"
)

# 4. 검증 실패 시 보강
if validator_result == "reinforcer 필요":
    Task(
        subagent_type="calab-plugin:reinforcer",
        description="누락 항목 보강",
        prompt="validator 결과 기반 수정"
    )
```

**⚠️ 중요**: 이 지침을 읽고 있다면, 사용자에게 텍스트로 응답하지 말고 **Task 도구를 호출**하세요!

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
│  ├── planner-phase: PRD 작성, PHASE 분해                │
│  └── deep-researcher: 베스트 프랙티스 검색 (병렬)        │
│                                                         │
│  --design 단계:                                         │
│  ├── design: 아키텍처 설계, ERD 작성                    │
│  └── Explore: 기존 코드 패턴 분석 (병렬)                 │
│                                                         │
│  --tasks 단계:                                          │
│  ├── planner-task: Task 분해 (TDD 워크플로우)           │
│  └── task-validator: Task 검증 (HARD GATE)              │
│                                                         │
│  --build 단계:                                          │
│  ├── dev-executor: TDD 구현 (RED→GREEN→REFACTOR)        │
│  └── code-reviewer: 코드 품질 검증 (병렬)                │
│                                                         │
│  완료 후 검증:                                          │
│  ├── validator: 완전성 검증 (AC, 누락, 엣지케이스)       │
│  ├── qa: 8단계 QA 프로세스                              │
│  └── security-reviewer: 보안 취약점 검사                 │
│                                                         │
│  검증 실패 시:                                          │
│  └── reinforcer: 누락/미흡 항목 자동 수정               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Agent Execution Log 템플릿

계획 문서에 포함되는 에이전트 실행 로그:

```markdown
## Agent Execution Log

| Agent | agentId | Status | Timestamp | Purpose |
|-------|---------|--------|-----------|---------|
| planner-phase | - | pending | - | PRD detailing |
| design | - | pending | - | Architecture design |
| planner-task | - | pending | - | Task decomposition |
| task-validator | - | pending | - | Task validation |
| dev-executor | - | pending | - | Implementation |
| qa | - | pending | - | Test verification |
```

> **agentId 기록**: 에이전트 실행 후 반드시 agentId를 로그에 기록하여 컨텍스트 압축 후에도 재개 가능

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
