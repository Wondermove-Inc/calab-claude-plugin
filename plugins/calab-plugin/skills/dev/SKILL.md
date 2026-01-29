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
argument-hint: "[--plan|--design|--tasks|--build|--architecture|--status] [기능명]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, WebSearch, AskUserQuestion, EnterPlanMode, ExitPlanMode, mcp__tavily__tavily-search]
skills: [code-quality, best-practices, tdd-workflow, project-rules, work-tracker]
agents:
  primary: planner-phase
  orchestration:
    plan: [calab-plugin:planner-phase, calab-plugin:deep-researcher]
    design: [calab-plugin:design, Explore]
    tasks: [calab-plugin:planner-task, calab-plugin:task-validator]
    build: [calab-plugin:dev-executor, calab-plugin:code-reviewer]
    architecture: [calab-plugin:refactor-cleaner, calab-plugin:code-reviewer]
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
/dev --architecture --init         # 4-Layer 클린 아키텍처 초기화
/dev --architecture --entity User  # 도메인 엔티티 생성
/dev --architecture --usecase CreateUser  # 유스케이스 생성
/dev --architecture --validate     # 아키텍처 규칙 검증
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

# 3. 빌드 오류 발생 시 자동 해결
if build_result.has_errors:
    Task(
        subagent_type="calab-plugin:build-error-resolver",
        description="빌드 오류 해결",
        prompt=f"""
        **오류 로그**: {build_result.errors}
        **대상 파일**: {build_result.files}

        자동 수정 후 빌드 재시도.
        3회 실패 시 /solve 에스컬레이션 제안.
        """
    )

# 4. 검증 필수
Task(
    subagent_type="calab-plugin:validator",
    description="구현 검증",
    prompt="AC 100% 충족 확인, 엣지 케이스, 품질 기준"
)

# 5. 검증 실패 시 보강 (validator → reinforcer → validator 체인)
if validator_result == "reinforcer 필요":
    Task(
        subagent_type="calab-plugin:reinforcer",
        description="누락 항목 보강",
        prompt="validator 결과 기반 수정"
    )

    # 6. 재검증 필수 (reinforcer 후 반드시 실행)
    revalidation_result = Task(
        subagent_type="calab-plugin:validator",
        description="수정 사항 재검증",
        prompt="""
        **역할**: 완전성 재검증 전문가

        **목표**: reinforcer 수정 결과 검증

        **검증 항목**:
        1. 이전 validator 실패 항목 모두 해결되었는지
        2. 새로운 문제 도입되지 않았는지
        3. AC 100% 충족 확인

        **출력**: 신뢰도 점수 + 상세 검증 결과
        """
    )

    # 7. 2차 실패 시 사용자 결정 (무한 루프 방지)
    if revalidation_result == "reinforcer 필요":
        # 최대 2회까지만 자동 시도
        return {
            "needs_clarification": True,
            "clarification_type": "validation_loop",
            "clarification_data": {
                "question": "2회 자동 수정 후에도 검증 실패. 어떻게 진행할까요?",
                "header": "검증 반복 실패",
                "options": [
                    {"value": "solve", "label": "/solve --rca 실행 (권장)", "description": "근본 원인 분석"},
                    {"value": "manual", "label": "수동 수정", "description": "직접 코드 확인"},
                    {"value": "skip", "label": "현재 상태로 진행", "description": "경고와 함께 계속"}
                ]
            }
        }
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

6. **`--architecture [하위옵션]`** → 4-Layer 클린 아키텍처 관리
   - `--init` → `references/architecture-init.md` 실행 (디렉토리 구조 생성)
   - `--entity [이름]` → `references/architecture-entity.md` 실행 (도메인 엔티티)
   - `--usecase [이름]` → `references/architecture-usecase.md` 실행 (유스케이스)
   - `--validate` → `references/architecture-validate.md` 실행 (규칙 검증)

7. **`--status`** → `references/status.md` 실행
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
├── worktree.json              # /dev --tasks 시 자동 생성
├── checkpoint.json            # 체크포인트 (체크섬 포함)
├── circuit-breaker.json       # Circuit Breaker 상태
├── request-log.jsonl          # 요청 로그
└── pre_modification_snapshot.json  # 수정 전 스냅샷
```

## 📦 단계별 산출물 (CRITICAL - 누락 금지)

> **모든 단계는 산출물을 생성해야 합니다. 산출물 없이 완료 처리 금지!**

### 필수 산출물 매트릭스

| 단계 | 산출물 | 파일 경로 | 생성 시점 | 검증 |
|------|--------|----------|----------|------|
| **--plan** | PRD 문서 | `.claude/docs/active/{feature}/02-prd.md` | Plan 완료 시 | ✅ 필수 |
| **--plan** | 브레인스토밍 | `.claude/docs/active/{feature}/01-brainstorm.md` | Plan 완료 시 | ⚠️ 권장 |
| **--design** | 아키텍처 문서 | `.claude/docs/active/{feature}/03-architecture.md` | Design 완료 시 | ✅ 필수 |
| **--design** | ERD 문서 | `.claude/docs/active/{feature}/04-erd.md` | Design 완료 시 | ⚠️ DB 있을 때 |
| **--tasks** | Task 목록 | `.claude/docs/active/{feature}/05-tasks.md` | Tasks 완료 시 | ✅ 필수 |
| **--tasks** | Worktree | `.claude-state/worktree.json` | Tasks 완료 시 | ✅ 필수 |
| **--build** | 소스 코드 | `src/...` | Build 완료 시 | ✅ 필수 |
| **--build** | 테스트 코드 | `test/...` or `*.test.ts` | Build 완료 시 | ✅ 필수 |
| **--build** | Worktree 업데이트 | `.claude-state/worktree.json` | Build 완료 시 | ✅ 필수 |

### 산출물 생성 프로토콜

```python
def verify_artifacts_created(stage, feature_name):
    """단계 완료 전 산출물 존재 확인"""

    REQUIRED_ARTIFACTS = {
        "plan": [
            f".claude/docs/active/{feature_name}/02-prd.md"
        ],
        "design": [
            f".claude/docs/active/{feature_name}/03-architecture.md"
        ],
        "tasks": [
            f".claude/docs/active/{feature_name}/05-tasks.md",
            ".claude-state/worktree.json"
        ],
        "build": [
            ".claude-state/worktree.json"  # status 업데이트 확인
        ]
    }

    missing = []
    for artifact in REQUIRED_ARTIFACTS.get(stage, []):
        if not file_exists(artifact):
            missing.append(artifact)

    if missing:
        return {
            "complete": False,
            "missing_artifacts": missing,
            "action": "CREATE_BEFORE_PROCEED",
            "message": f"⚠️ 산출물 누락: {', '.join(missing)}"
        }

    return {"complete": True}
```

### 산출물 누락 시 처리

```
============================================
[ARTIFACT CHECK] 산출물 검증
============================================

❌ 단계 완료 불가 - 산출물 누락

누락된 산출물:
1. .claude/docs/active/user-auth/02-prd.md (필수)
2. .claude-state/worktree.json (필수)

🔧 조치:
→ 산출물 생성 후 다시 완료 처리하세요.
→ 산출물 없이 다음 단계 진행 금지

============================================
```

## 🔄 Worktree 업데이트 책임 (CRITICAL)

> **"누가, 언제 worktree를 업데이트하는가?"** - 책임 명확화

### 업데이트 책임 매트릭스

| 시점 | 담당 | 업데이트 내용 | 파일 |
|------|------|-------------|------|
| **--tasks 완료** | planner-task | worktree 최초 생성 | worktree.json |
| **--build 시작** | dev-executor | `status: "in_progress"`, `started_at` | worktree.json |
| **--build 완료** | dev-executor | `status: "done"`, `completed_at`, `progress` | worktree.json |
| **빌드 오류** | build-error-resolver | `status: "blocked"`, `error_info` | worktree.json |
| **검증 실패** | validator | `validation_status`, `issues` | worktree.json |
| **수정 완료** | reinforcer | `status` 갱신, `fix_log` | worktree.json |

### 업데이트 타이밍 (필수 준수)

```python
# --build 시작 시 (dev-executor 내부)
def on_build_start(task_id):
    worktree = read_worktree()
    update_task_status(worktree, task_id, {
        "status": "in_progress",
        "started_at": datetime.now().isoformat(),
        "last_heartbeat": datetime.now().isoformat()
    })
    save_worktree(worktree)

# --build 완료 시 (dev-executor 내부)
def on_build_complete(task_id, success):
    worktree = read_worktree()
    update_task_status(worktree, task_id, {
        "status": "done" if success else "failed",
        "completed_at": datetime.now().isoformat()
    })
    update_progress(worktree)
    save_worktree(worktree)

# 빌드 오류 시 (build-error-resolver 내부)
def on_build_error(task_id, errors):
    worktree = read_worktree()
    update_task_status(worktree, task_id, {
        "status": "blocked",
        "error_info": {
            "count": len(errors),
            "types": categorize_errors(errors),
            "timestamp": datetime.now().isoformat()
        }
    })
    save_worktree(worktree)
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
│  --architecture 단계:                                    │
│  ├── refactor-cleaner: 구조 생성/엔티티/유스케이스       │
│  └── code-reviewer: 아키텍처 규칙 검증 (병렬)            │
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

| 완료 후 | 권장 명령어 | 자동 전환 |
|--------|------------|----------|
| /dev --plan | `/dev --design` | 수동 |
| /dev --design | `/dev --tasks` | 수동 |
| /dev --tasks | `/dev --build TASK-001` | 수동 |
| /dev --build | 다음 TASK 또는 QA | 자동 제안 |
| 모든 TASK 완료 | `calab-plugin:qa` | **자동 호출** |
| QA 실패 | `/solve` | 자동 제안 |

### 자동 전환 로직

```python
# 모든 Task 완료 시 자동 QA
all_tasks = TaskList()
completed = [t for t in all_tasks if t.status == "completed"]

if len(completed) == len(all_tasks):
    # 자동 QA 실행
    Task(
        subagent_type="calab-plugin:qa",
        description="전체 기능 QA",
        prompt="""
        **역할**: QA 전문가
        **목표**: 구현된 기능 전체 검증
        **범위**: 완료된 모든 Task
        """
    )

# QA 실패 시 solve 제안
if qa_result.status == "failed":
    return {
        "needs_clarification": True,
        "clarification_type": "qa_failure",
        "clarification_data": {
            "question": "QA에서 문제가 발견되었습니다. 문제 해결을 진행할까요?",
            "header": "QA 실패",
            "options": [
                {"value": "solve", "label": "/solve 실행 (권장)", "description": "근본 원인 분석 후 수정"},
                {"value": "manual", "label": "수동 수정", "description": "직접 코드 수정"},
                {"value": "skip", "label": "건너뛰기", "description": "나중에 처리"}
            ]
        }
    }
```

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

---

## 🔄 Partial Completion Handling (중간 실패 처리)

> **"Tasks that fail mid-way should be handled in isolation"** - AI Agent Best Practice 2025

### 중간 실패 시나리오

| 시나리오 | 상태 | 처리 방법 |
|----------|------|----------|
| Task 50% 완료 후 오류 | `partial` | 완료된 부분 저장, 남은 부분 새 Task 생성 |
| 외부 의존성 실패 | `blocked` | 해당 Task만 블로킹, 독립 Task 계속 진행 |
| 빌드 실패 | `failed` | 롤백 후 원인 분석, 수정 Task 생성 |
| 세션 중단 (Compact) | `interrupted` | 체크포인트에서 재개 |

### Partial Completion 프로토콜

```python
def handle_partial_completion(task_id, completed_steps, remaining_steps, error):
    """중간 실패 처리 프로토콜"""

    # 1. 현재 진행 상황 스냅샷 저장
    snapshot = {
        "task_id": task_id,
        "status": "partial",
        "completed_steps": completed_steps,
        "remaining_steps": remaining_steps,
        "error": str(error),
        "timestamp": datetime.now().isoformat(),
        "recoverable": is_recoverable(error)
    }

    save_to_checkpoint(snapshot)

    # 2. 실패 유형 분류
    failure_type = classify_failure(error)

    if failure_type == "RETRIABLE":
        # 재시도 가능한 오류 → 자동 재시도
        return {
            "action": "retry",
            "delay": calculate_backoff(task_id),
            "max_retries": 2
        }

    elif failure_type == "RECOVERABLE":
        # 복구 가능 → 남은 작업 새 Task로 분리
        new_task = create_continuation_task(
            original_task=task_id,
            steps=remaining_steps,
            context=snapshot
        )
        return {
            "action": "continue_with_new_task",
            "new_task_id": new_task.id,
            "completed_preserved": True
        }

    else:  # NON_RECOVERABLE
        # 복구 불가 → 롤백 후 사용자 결정
        return {
            "action": "escalate",
            "rollback_needed": True,
            "user_decision_required": True,
            "options": [
                "/solve --rca",
                "/dev --design 재설계",
                "수동 수정"
            ]
        }


def is_recoverable(error):
    """복구 가능 여부 판단"""
    NON_RECOVERABLE = [
        "circular_dependency",
        "missing_core_module",
        "database_schema_conflict",
        "authentication_failure"
    ]
    return error.type not in NON_RECOVERABLE
```

### Task 격리 (Task Isolation)

> **"Failures don't cascade to other tasks"** - 실패 격리

```python
def execute_with_isolation(task):
    """격리된 환경에서 Task 실행"""

    # 1. Task별 독립 트랜잭션 시작
    transaction_id = start_task_transaction(task.id)

    try:
        # 2. Task 실행
        result = execute_task(task)

        # 3. 성공 시 커밋
        commit_transaction(transaction_id)
        return result

    except Exception as e:
        # 4. 실패 시 해당 Task만 롤백
        rollback_transaction(transaction_id)

        # 5. 다른 Task에 영향 없이 상태 기록
        mark_task_failed(task.id, e)

        # 6. 독립적인 Task는 계속 진행 가능
        return {
            "task_id": task.id,
            "status": "failed",
            "independent_tasks_continue": True,
            "blocked_tasks": get_dependent_tasks(task.id)
        }
```

### Partial Completion 체크포인트 형식

```json
{
  "task_id": "TASK-003",
  "status": "partial",
  "progress": {
    "total_steps": 5,
    "completed": 3,
    "percentage": 60
  },
  "completed_steps": [
    {"step": 1, "description": "테스트 작성", "artifacts": ["test/auth.test.ts"]},
    {"step": 2, "description": "인터페이스 정의", "artifacts": ["types/auth.ts"]},
    {"step": 3, "description": "기본 구현", "artifacts": ["services/auth.ts"]}
  ],
  "remaining_steps": [
    {"step": 4, "description": "에러 핸들링"},
    {"step": 5, "description": "통합 테스트"}
  ],
  "error": {
    "type": "external_dependency",
    "message": "Redis 연결 실패",
    "recoverable": true
  },
  "checkpoint_timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🔁 Three Developer Loops (개발자 루프 프레임워크)

> **"Different iteration speeds for different concerns"** - Anthropic Engineering 2025

### 세 가지 루프

```
┌─────────────────────────────────────────────────────────────────┐
│                     OUTER LOOP (weeks-months)                    │
│  - 프로젝트 전체 계획                                            │
│  - 아키텍처 결정                                                 │
│  - 기술 스택 선정                                                │
│  - /dev --plan, /dev --design                                   │
├─────────────────────────────────────────────────────────────────┤
│                     MIDDLE LOOP (hours-days)                     │
│  - Epic/Story 단위 작업                                          │
│  - Task 분해 및 구현                                             │
│  - /dev --tasks, /dev --build                                   │
│  - QA 및 검증 사이클                                             │
├─────────────────────────────────────────────────────────────────┤
│                     INNER LOOP (seconds-minutes)                 │
│  - 코드 작성 → 테스트 → 수정                                     │
│  - TDD 사이클 (Red-Green-Refactor)                              │
│  - validator → reinforcer 사이클                                │
│  - 빌드 오류 즉시 수정                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 루프별 에이전트 매핑

| 루프 | 주기 | 에이전트 | 산출물 |
|------|------|----------|--------|
| **Outer** | weeks-months | planner-phase, deep-researcher | PRD, 아키텍처 문서 |
| **Middle** | hours-days | dev-executor, qa, validator | 기능 구현, 테스트 |
| **Inner** | seconds-minutes | code-reviewer, reinforcer | 코드 수정, 즉시 피드백 |

### 루프 전환 조건

```python
def determine_current_loop(context):
    """현재 작업이 어떤 루프에 있는지 판단"""

    if context.type in ["architecture", "tech_decision", "major_refactor"]:
        return {
            "loop": "OUTER",
            "expected_duration": "days-weeks",
            "agents": ["planner-phase", "deep-researcher", "Plan"],
            "checkpoints": "daily",
            "user_involvement": "high"
        }

    elif context.type in ["feature", "story", "epic"]:
        return {
            "loop": "MIDDLE",
            "expected_duration": "hours-days",
            "agents": ["dev-executor", "validator", "qa"],
            "checkpoints": "per_task",
            "user_involvement": "medium"
        }

    else:  # code_fix, small_change, test_fix
        return {
            "loop": "INNER",
            "expected_duration": "seconds-minutes",
            "agents": ["code-reviewer", "reinforcer", "build-error-resolver"],
            "checkpoints": "on_error",
            "user_involvement": "low"
        }


def escalate_loop(current_loop, reason):
    """하위 루프에서 상위 루프로 에스컬레이션"""

    ESCALATION_MAP = {
        "INNER": {
            "threshold": 3,  # 3회 실패 시
            "escalate_to": "MIDDLE",
            "action": "validator + reinforcer 체인"
        },
        "MIDDLE": {
            "threshold": 2,  # 2회 Task 실패 시
            "escalate_to": "OUTER",
            "action": "/solve 또는 /dev --design 재설계"
        }
    }

    return ESCALATION_MAP.get(current_loop)
```

### 루프 출력 형식

```
============================================
[LOOP CONTEXT] 현재 작업 루프
============================================

🔄 현재 루프: MIDDLE (hours-days)
📋 작업 유형: Feature Implementation

├─ Outer Loop (완료)
│  ✅ PRD 작성
│  ✅ 아키텍처 설계
│
├─ Middle Loop (진행중) ← 현재
│  ✅ TASK-001: DB 마이그레이션
│  ✅ TASK-002: API 엔드포인트
│  🔄 TASK-003: 비즈니스 로직 ← 현재
│  ⬚ TASK-004: 프론트엔드 연동
│
└─ Inner Loop (TASK-003 내)
   🔄 TDD 사이클 3회차
   └─ Red → Green → Refactor

============================================
```

---

## 🔒 Deadlock Prevention (데드락 방지)

> **"Cycle detection at task creation"** - 작업 생성 시 순환 의존성 감지

### 의존성 검증 프로토콜

```python
def validate_dependencies_before_create(new_task, existing_tasks):
    """Task 생성 전 순환 의존성 검사"""

    # 1. 의존성 그래프 구축
    graph = build_dependency_graph(existing_tasks)

    # 2. 새 Task 추가 시뮬레이션
    graph.add_node(new_task.id)
    for dep in new_task.depends_on:
        graph.add_edge(dep, new_task.id)

    # 3. 순환 감지
    if has_cycle(graph):
        cycle = find_cycle(graph)
        return {
            "valid": False,
            "error": "CIRCULAR_DEPENDENCY_DETECTED",
            "cycle": cycle,
            "suggestion": f"의존성 재구성 필요: {' → '.join(cycle)}"
        }

    # 4. 데드락 가능성 검사
    if can_deadlock(graph, new_task):
        return {
            "valid": False,
            "error": "POTENTIAL_DEADLOCK",
            "reason": "상호 대기 상태 발생 가능",
            "suggestion": "의존성 방향 재검토 필요"
        }

    return {"valid": True}


def has_cycle(graph):
    """DFS 기반 순환 감지"""
    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    for node in graph.nodes():
        if node not in visited:
            if dfs(node):
                return True
    return False
```

### 데드락 방지 출력

```
============================================
[DEADLOCK CHECK] 의존성 검증 결과
============================================

❌ 순환 의존성 감지됨!

🔄 감지된 순환:
TASK-003 → TASK-005 → TASK-007 → TASK-003

📋 현재 의존성:
• TASK-003: TASK-001, TASK-002에 의존
• TASK-005: TASK-003에 의존
• TASK-007: TASK-005에 의존
• TASK-003: TASK-007에 의존 ← 순환 발생!

🔧 권장 해결책:
1. TASK-003의 TASK-007 의존성 제거
2. 또는 TASK-007을 독립 Task로 분리

============================================
```

---

## ⏱️ Heartbeat & Timeout (하트비트 및 타임아웃)

> **"Heartbeat timeout releases task when agent crashes"** - 에이전트 크래시 대응

### 타임아웃 관리

```python
class TaskHeartbeat:
    """Task 실행 상태 모니터링"""

    TIMEOUT_THRESHOLDS = {
        "inner_loop": 300,      # 5분 (코드 수정)
        "middle_loop": 1800,    # 30분 (Task 구현)
        "outer_loop": 7200,     # 2시간 (설계/계획)
        "background": 3600      # 1시간 (백그라운드)
    }

    def __init__(self, task_id, loop_type):
        self.task_id = task_id
        self.loop_type = loop_type
        self.last_heartbeat = datetime.now()
        self.timeout = self.TIMEOUT_THRESHOLDS[loop_type]

    def beat(self):
        """하트비트 갱신"""
        self.last_heartbeat = datetime.now()
        update_task_heartbeat(self.task_id, self.last_heartbeat)

    def is_alive(self):
        """Task가 살아있는지 확인"""
        elapsed = (datetime.now() - self.last_heartbeat).seconds
        return elapsed < self.timeout

    def check_and_release(self):
        """타임아웃 시 Task 해제"""
        if not self.is_alive():
            release_task(self.task_id)
            return {
                "status": "released",
                "reason": "heartbeat_timeout",
                "last_heartbeat": self.last_heartbeat.isoformat(),
                "timeout_seconds": self.timeout,
                "action": "task_available_for_retry"
            }
        return {"status": "alive"}
```

### Worktree에 하트비트 기록

```json
{
  "current_task": "TASK-003",
  "heartbeat": {
    "task_id": "TASK-003",
    "last_beat": "2024-01-15T10:30:00Z",
    "loop_type": "middle_loop",
    "timeout_at": "2024-01-15T11:00:00Z",
    "status": "alive"
  },
  "stale_tasks": [
    {
      "task_id": "TASK-002",
      "last_beat": "2024-01-15T08:00:00Z",
      "status": "released",
      "reason": "heartbeat_timeout"
    }
  ]
}
```

### 타임아웃 복구 출력

```
============================================
[HEARTBEAT] Task 상태 체크
============================================

⚠️ TASK-002 타임아웃 감지

• 마지막 하트비트: 2024-01-15T08:00:00Z
• 타임아웃 임계값: 30분
• 경과 시간: 2시간 30분

🔧 자동 복구 조치:
1. TASK-002 상태 → "released"
2. 작업 잠금 해제
3. 재시도 대기열 추가

📋 권장 액션:
• /restore로 마지막 체크포인트에서 재개
• 또는 TASK-002 수동 재시작

============================================
```

---

## 🛡️ Proactive Interruption Management (선제적 중단 관리)

> **"Minimize disruption to user flow"** - 사용자 흐름 방해 최소화

### 중단 유형 및 대응

| 중단 유형 | 심각도 | 대응 전략 | 사용자 알림 |
|----------|--------|----------|------------|
| **빌드 실패** | Medium | 자동 수정 시도 → 실패 시 알림 | 5개+ 오류만 |
| **테스트 실패** | Low | 백그라운드 재시도 → 요약만 | 요약 형태 |
| **외부 API 오류** | High | 재시도 + 폴백 → 지속 시 알림 | 즉시 알림 |
| **세션 Compact** | Critical | 자동 체크포인트 → 복구 안내 | /restore 안내 |

### 중단 최소화 프로토콜

```python
def handle_interruption(interruption_type, context):
    """중단 발생 시 사용자 방해 최소화"""

    INTERRUPTION_HANDLERS = {
        "build_error": {
            "auto_retry": True,
            "max_silent_retries": 3,
            "escalate_threshold": 5,  # 5개 이상 오류 시 사용자 알림
            "handler": "build-error-resolver"
        },
        "test_failure": {
            "auto_retry": True,
            "max_silent_retries": 2,
            "escalate_threshold": 3,
            "handler": "reinforcer"
        },
        "external_api": {
            "auto_retry": True,
            "backoff": "exponential",
            "max_retries": 3,
            "fallback": "cache_or_mock"
        },
        "context_loss": {
            "auto_retry": False,
            "immediate_save": True,
            "handler": "/restore"
        }
    }

    handler_config = INTERRUPTION_HANDLERS.get(interruption_type)

    if handler_config["auto_retry"]:
        # 조용히 재시도
        for attempt in range(handler_config["max_silent_retries"]):
            result = retry_silently(context, attempt)
            if result.success:
                return {"status": "resolved_silently", "attempts": attempt + 1}

        # 임계값 초과 시만 사용자에게 알림
        if context.error_count >= handler_config.get("escalate_threshold", 1):
            return {
                "status": "escalated",
                "notify_user": True,
                "summary": generate_error_summary(context)
            }

    return {"status": "requires_user_action", "handler": handler_config["handler"]}


def generate_minimal_notification(errors):
    """최소한의 알림 생성 (방해 최소화)"""

    if len(errors) == 1:
        return None  # 단일 오류는 조용히 처리

    return f"""
    ⚠️ {len(errors)}개 이슈 발생 (자동 처리 중)
    • 주요 이슈: {errors[0].summary}
    • 예상 해결 시간: ~{estimate_fix_time(errors)}

    [무시] [상세 보기]
    """
```

### 중단 요약 출력 (배치)

```
============================================
[INTERRUPTION SUMMARY] 작업 중 발생 이슈 요약
============================================

📊 발생 이슈: 7건
━━━━━━━━━━━━━━━━━━
✅ 자동 해결: 5건
⚠️ 주의 필요: 2건

🔧 자동 해결된 항목:
• TypeScript 오류 3건 → reinforcer가 수정
• 린트 경고 2건 → 자동 포맷팅

⚠️ 주의 필요 항목:
1. [TASK-003] 외부 API 타임아웃 (재시도 중...)
2. [TASK-004] 타입 정의 누락 (확인 필요)

💡 권장 액션:
현재 작업 계속 진행 가능합니다.
위 항목은 백그라운드에서 처리 중입니다.

============================================
```
