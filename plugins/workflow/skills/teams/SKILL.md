---
name: workflow:teams
description: Agent Teams 워크플로우. Discovery→Plan→Agent Teams(병렬 구현+리뷰) 흐름을 관리합니다. 대규모/복잡 작업용.
allowed-tools: Bash, Task, TaskOutput, AskUserQuestion, Read, Grep, Glob, TeamCreate, TeamDelete, SendMessage
disable-model-invocation: true
---

# /workflow:teams 커맨드

워크플로우를 시작합니다. 이 스킬이 오케스트레이터 역할을 수행합니다.
Agent Teams를 활용하여 병렬 구현 + 팀 내 리뷰를 수행합니다.

> 단순 작업(버그 수정, 설정 변경 등)은 `/workflow:single`를 사용하세요.

## 사용법

### 새 워크플로우 시작
```
/workflow:teams <작업 요청>

예시:
/workflow:teams 클러스터 알림 기능 추가
/workflow:teams API 응답 성능 최적화
```

### 중단된 워크플로우 재개
```
/workflow:teams --resume <epic-id>

예시:
/workflow:teams --resume calab-claude-plugin-abc123
```

## 용어 정리

| 용어 | 정의 |
|------|------|
| **Discovery** | 사용자 주도 탐색 → AI 보완 질문 → 요점 정리의 구체화 단계 |
| **Agent Teams** | team-lead + team-worker(N) + team-reviewer로 병렬 구현 + 리뷰 |
| **worktree isolation** | 각 team-worker가 독립 git worktree에서 작업, 충돌 방지 |

## 핵심 원칙

1. **teams 스킬이 오케스트레이터**: Discovery 대화, 흐름 제어, Gate 관리를 이 스킬이 담당
2. **Discovery는 사용자 주도**: 사용자가 질문/확인을 먼저 하고, AI는 요청에 응답
3. **항상 Agent Teams 모드**: Planner가 작업을 분할하고, team-lead가 팀을 조율
4. **beads가 Single Source of Truth**: 이슈 상태로 추적
5. **팀 내 리뷰**: team-reviewer가 머지된 코드를 리뷰 (최대 3라운드)
6. **Completion Gate**: team-lead 완료 후 사용자 최종 검토

## 워크플로우 흐름

```
사용자 요청 (모호/구체적)
    ↓ (구체적이면 Discovery 스킵)
┌──────────────────────────────┐
│  Discovery (teams 스킬 직접)  │  ← 사용자 주도 대화로 요구사항 구체화
│  Phase 1: 사용자 질문/탐색    │
│  Phase 2: AI 보완 질문        │
│  Phase 3: 요점 정리           │
└──────────────────────────────┘
    ↓ Discovery Gate: 요점 승인
┌─────────────┐
│   Planner   │  ← 설계 + 작업 분할 계획
└─────────────┘
    ↓ Plan Gate: 계획 승인
┌──────────────────────────────┐
│  Agent Teams                  │
│  team-lead (조율/머지/정리)    │
│  ├ team-worker-1 ◈           │  ◈ = worktree isolation
│  ├ team-worker-2 ◈           │
│  ├ ...                        │
│  └ team-reviewer              │
│  구현 → 머지 → 리뷰 → 정리    │
└──────────────────────────────┘
    ↓
    Completion Gate: 최종 완료 검토 (사용자 승인)
    ├─ 완료 → 워크플로우 종료
    └─ 수정 → team-lead 재호출
```

## 오케스트레이션 프로세스

### 0단계: Discovery — 요구사항 구체화

> Discovery는 별도 에이전트가 아니라 **teams 스킬(메인 스레드)이 직접 수행**합니다.
> 사용자가 주도하여 질문/탐색을 진행하고, AI는 요청에 응답합니다.

#### 자동 스킵 판단

사용자 요청이 아래 조건을 **모두** 만족하면 Discovery를 스킵하고 1단계(Epic 생성)로 진행:
- 구현 대상이 명확 (무엇을 만들/수정할지 특정됨)
- Acceptance Criteria를 바로 작성할 수 있는 수준
- 범위(In/Out-of-Scope)가 분명

**스킵 시**: "요청이 충분히 구체적이므로 Discovery를 스킵하고 바로 진행합니다." 를 표시

#### Phase 1: 사용자 주도 탐색

**주도권: 사용자**. AI는 능동적으로 질문하지 않고, 사용자의 요청에 응답합니다.

사용자가 할 수 있는 것:
- 자유로운 질문: "이 코드 어떤 구조야?", "이 기능 어떻게 동작해?"
- 코드 탐색 요청: "이 파일 보여줘", "이 함수 찾아줘"
- 확인 요청: "이렇게 하면 되나?", "이 방식이 맞아?"
- 아이디어 논의: "이런 식으로 만들면 어때?"

AI 행동:
- 사용자 질문에 답변 (코드 탐색 시 Read, Grep, Glob 도구 활용)
- 요청된 정보를 제공
- **능동적으로 질문하지 않음** — 사용자가 이끌어감

#### Phase 1 → Phase 2 전환

사용자가 **구체적 작업 지시**를 하면 Phase 2로 전환:
- "이걸 만들어줘", "이거 해줘", "이렇게 수정해줘"
- "자, 이제 X를 구현하자"
- 명확한 구현/수정 대상을 지정하는 발언

#### Phase 2: AI 보완 질문

**주도권: AI**. Planner에게 넘기기 전에 부족한 정보를 질문합니다.

보완 질문 대상:
- 범위가 불명확한 부분 (In-Scope / Out-of-Scope)
- 기술적 제약이나 선호사항
- 우선순위/트레이드오프 결정이 필요한 부분
- 예외 케이스나 엣지 케이스 처리 방향

**AskUserQuestion으로 질문**:
```
question: "[Discovery] {구체적 질문 내용}"
header: "Discovery"
```

- 질문이 여러 개이면 **한 번에 모아서** 질문 (AskUserQuestion 1회)
- 사용자 답변 후 추가 질문이 필요하면 1회 더 가능 (최대 2라운드)
- 사용자가 "됐어/진행해"라고 하면 즉시 Phase 3로

#### Phase 3: 요점 정리 + Discovery Gate

AI가 지금까지의 대화를 구조화하여 요점을 정리합니다.

**요점 정리 형식**:
```markdown
## Discovery 요약

### 배경/동기
왜 이 작업이 필요한가

### 구체화된 요구사항
- 요구사항 1
- 요구사항 2

### 범위
- **In-Scope**: 이번에 구현할 것
- **Out-of-Scope**: 이번에는 하지 않을 것

### 제약 조건
- 기술적 제약, 선호사항 등

### 사용자 결정 사항
- Q: 질문 → A: 답변
```

요점 정리를 텍스트로 표시한 후 **Discovery Gate**:

```
question: "[Discovery Gate] 위 내용으로 계획 단계(Planner)를 진행할까요?"
header: "Discovery"
options:
  - label: "승인", description: "Planner 단계로 진행합니다"
  - label: "수정 필요", description: "Discovery를 계속합니다"
  - label: "취소", description: "작업을 중단합니다"
multiSelect: false
```

- **승인**: 1단계(Epic 생성 + Planner)로 진행
- **수정 필요**: Phase 1로 복귀 (사용자가 추가 탐색/질문)
- **취소**: 워크플로우 종료

**강제 중단**: AskUserQuestion 호출 후 즉시 메시지를 종료합니다.

### 1단계: 이슈 생성

> **반드시 `guides/beads-issue-guide.md`를 읽고 계층 구조, 제목 형식, 템플릿을 준수합니다.**

**teams 스킬은 Epic + Work Sub-task를 생성**합니다. Plan Sub-task는 Planner가 직접 생성합니다.

| 이슈 | 생성 주체 | 시점 |
|------|----------|------|
| Epic | teams 스킬 | 1단계 |
| Plan Sub-task | Planner 에이전트 | 2단계 시작 시 |
| Work Sub-task | teams 스킬 | 4단계 시작 시 (team-lead가 결과 기록) |

```bash
# Epic 생성 (워크플로우 Epic 필드 사용법 참조)
bd create "[YY.Q.N][영역] 기능명" --type epic --priority 2 \
  --description "$(cat <<'EOF'
## 요청 분석
- **원본 요청**: {사용자 요청}
- **작업 유형**: [새 기능 / 버그 수정 / 리팩토링]
- **복잡도**: [복잡]

## Discovery 요약
{Phase 3에서 정리한 요점 전문 — Discovery 스킵 시 이 섹션 생략}

## 실행 계획
| 순서 | 에이전트 | 작업 |
|------|---------|------|
| 1 | planner | 요청 분석, 설계, 작업 분할 → 이슈에 작성 |
| 2 | team-lead | 팀 구성 → 병렬 구현 → 머지 → 리뷰 → 정리 |
EOF
)" \
  --acceptance "$(cat <<'EOF'
- [ ] AC1: ...
- [ ] AC2: ...
EOF
)"

# 워크플로우 시작 코멘트
bd comments add <epic-id> "[Workflow] 시작"
```

### 2단계: Planner 호출

> Planner가 자기 Sub-task를 직접 생성합니다.
> **Discovery 결과는 Epic의 description에 기록되어 있으므로**, Planner는 `bd show`로 확인합니다.

```
Task (subagent_type: workflow:planner, model: opus, run_in_background: true):
"Epic bd-<epic-id> 작업 수행. bd show로 상세 확인. Discovery 요약이 Epic description에 포함되어 있음."
```

완료 대기:
```
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: 결과 확인 후 다음 단계
→ timeout: AskUserQuestion으로 재대기 또는 취소 선택 요청
```

완료 시:
```bash
bd comments add <epic-id> "[Planner] 완료"
```

### 3단계: Plan Gate

요약을 텍스트로 표시한 후 AskUserQuestion 도구로 사용자 승인을 요청합니다.

**`[판단 필요]` 마커 처리:**
- Planner 결과에서 `[판단 필요]` 텍스트가 포함된 항목을 검출하여 요약에 별도 나열
- 해당 항목이 1개 이상이면 "⚠️ 판단 필요 항목" 섹션을 반드시 표시
- 항목이 없으면 이 섹션을 생략

**아래 파라미터로 AskUserQuestion 도구를 호출합니다:**
```
question: "[Plan Gate] Planner가 작성한 계획을 검토해주세요. 어떻게 진행하시겠습니까?"
header: "Plan Gate"
options:
  - label: "승인", description: "Agent Teams 단계로 진행합니다"
  - label: "수정 필요", description: "Planner를 재호출하여 이슈를 수정합니다"
  - label: "취소", description: "작업을 중단합니다"
multiSelect: false
```

**강제 중단**: AskUserQuestion 호출 후 즉시 메시지를 종료합니다. 추가 도구 호출이나 텍스트 출력 없이 사용자의 응답을 기다립니다.

### 4단계: Agent Teams 실행

> teams 스킬이 TeamCreate → team-lead spawn → 완료 대기를 수행합니다.
> 팀 내부 조율(팀원 spawn, 작업 할당, 머지, 리뷰)은 team-lead가 담당합니다.

#### 4-1. Work Sub-task 생성

```bash
# teams 스킬이 Work Sub-task를 생성 (team-lead가 결과를 기록할 대상)
bd create "Work: {기능명}" --parent <epic-id> --labels "implementation,worker,teams"
bd update <worker-subtask-id> --status in_progress
```

#### 4-2. TeamCreate

```
TeamCreate(team_name: "wf-<epic-id>", description: "워크플로우 Teams: {기능명}")
```

#### 4-3. Team Lead Spawn

```
Agent (subagent_type: workflow:team-lead, team_name: "wf-<epic-id>", name: "team-lead", model: opus, run_in_background: true):
"Epic bd-<epic-id> Teams 모드 실행.
- Worker Sub-task: bd-<worker-subtask-id> (작업 결과 기록용)
- Planner 이슈에서 작업 분할 계획, 공유 인터페이스, 파일 경계를 확인.
- bd show <planner-subtask-id> 참조.
- 팀원 spawn → 작업 할당 → 머지 → 리뷰 → 정리 수행."
```

#### 4-4. 완료 대기

```
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: team-lead 결과 확인
→ timeout: AskUserQuestion으로 재대기 또는 취소 선택 요청
```

완료 시:
```bash
bd comments add <epic-id> "[Teams] 완료 (팀원: N명, 리뷰: N라운드)"
```

#### 4-5. 팀 정리

```
TeamDelete()
```

### 5단계: Completion Gate — 최종 완료 검토

team-lead 완료 후 요약을 텍스트로 표시한 후 AskUserQuestion 도구로 사용자 승인을 요청합니다.

**아래 파라미터로 AskUserQuestion 도구를 호출합니다:**
```
question: "[Completion Gate] 워크플로우를 완료하시겠습니까?"
header: "Completion"
options:
  - label: "완료", description: "워크플로우 종료 및 모든 이슈 close"
  - label: "수정 필요", description: "team-lead를 재호출하여 수정합니다"
  - label: "취소", description: "작업을 중단합니다"
multiSelect: false
```

**강제 중단**: AskUserQuestion 호출 후 즉시 메시지를 종료합니다. 추가 도구 호출이나 텍스트 출력 없이 사용자의 응답을 기다립니다.

#### 완료 선택 시

모든 Sub-task와 Epic을 일괄 close합니다.

```bash
# 모든 Sub-task close
bd close <planner-subtask-id>
bd close <worker-subtask-id>

# Epic close
bd comments add <epic-id> "[Workflow] 완료"
bd close <epic-id>
```

**사용자에게 간결한 결과 보고**:

```markdown
워크플로우 완료

| 단계 | 에이전트 | 토큰 | 시간 | 결과 |
|------|---------|------|------|------|
| Plan | Planner | {tokens} | {time} | ✅ |
| Teams | team-lead | {tokens} | {time} | ✅ |
|  | team-worker-1 | {tokens} | {time} | ✅ |
|  | team-worker-2 | {tokens} | {time} | ✅ |
|  | team-reviewer | {tokens} | {time} | {decision} |
| **총계** | | **{total}** | **{total}** | |

Epic: {epic-id} (CLOSED) | `bd show {epic-id}`
```

**필수 규칙**:
- **절대로** 통계 표를 2번 이상 출력하지 말 것
- **절대로** 타임라인, 주요 성과, 완료된 이슈, 산출물 등 추가 요약을 작성하지 말 것
- **오직** 위 표 하나만 출력

#### 수정 필요 선택 시

사용자 피드백을 반영하여 team-lead를 재호출합니다.

```bash
# 1. Work Sub-task reopen
bd update <worker-subtask-id> --status in_progress
bd comments add <worker-subtask-id> "[Completion-Rework] Gate 피드백 반영"
```

```
# 2. TeamCreate (새 팀)
TeamCreate(team_name: "wf-<epic-id>-rework", description: "워크플로우 재작업: {피드백 요약}")
```

```
# 3. Team Lead 재호출
Agent (subagent_type: workflow:team-lead, team_name: "wf-<epic-id>-rework", name: "team-lead", model: opus, run_in_background: true):
"Epic bd-<epic-id> 재작업.
- 사용자 피드백: {피드백 내용}
- Worker Sub-task: bd-<worker-subtask-id>
- Planner 이슈: bd show <planner-subtask-id>
- 수정 범위만 팀원에게 할당."
```

```
# 4. 완료 대기 → TeamDelete → Completion Gate 복귀
```

### 6단계: 워크플로우 종료

## 재개 프로세스 (--resume)

```bash
# 1. Sub-task 상태 확인
bd list --parent <epic-id>

# 2. Epic 코멘트 확인
bd comments <epic-id>
```

**재개 지점 결정**:
- `in_progress` Sub-task → 해당 단계부터 재개
- 모두 `open` → 처음부터 시작
- `[Teams] 완료` 코멘트 → Completion Gate부터
- `[Gate] 대기중` 코멘트 → 해당 Gate부터

## 에이전트 호출 규칙

- 모든 Task 호출 시 `run_in_background: true` 사용
- 에이전트 호출 시 이슈 ID만 전달 (토큰 효율화)

### 완료 대기 패턴

```
# 1. 에이전트 호출 (background)
Task (run_in_background: true) → task_id 획득

# 2. 완료 대기 (최대 10분, 완료 시 즉시 반환)
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: 결과 처리, 다음 단계 진행
→ timeout: 사용자에게 알림 후 응답 대기
```

**timeout 처리:**
- timeout 발생 시 아래 파라미터로 AskUserQuestion 도구를 호출합니다:
```
question: "{에이전트명} 에이전트가 10분 내 완료되지 않았습니다. 어떻게 하시겠습니까?"
header: "Timeout"
options:
  - label: "재대기", description: "10분 추가 대기합니다"
  - label: "취소", description: "작업을 중단합니다"
multiSelect: false
```
- 재대기 선택 시 동일한 task_id로 `TaskOutput` 재호출

## 토큰 효율성

### 핵심 원칙: 상세는 이슈에, 반환은 ID만

```mermaid
%%{init: {"flowchart": {"defaultRenderer": "elk"}}}%%
flowchart LR
    Agent[에이전트] -->|"완료: bd-abc<br/>(상세는 이슈에)"| Start[teams 스킬]
    Start -->|"완료: bd-epic<br/>(상세: bd show)"| User[사용자]
```

## 에러 핸들링

| 상황 | 처리 |
|------|------|
| Plan Gate 거부 | Planner 재호출 |
| Completion Gate (수정 필요) | team-lead 재호출 (새 팀 구성) |
| 에이전트 실패 | 최대 3회 재시도, 3회 실패 → 사용자 보고 |
| 대기 timeout (10분) | AskUserQuestion으로 재대기 또는 취소 선택 요청 |
| 사용자 취소 | Epic 코멘트 기록 후 close |

## 참조 문서

### 에이전트
- `agents/planner.md`: 요청 분석, 작업 분할, 이슈에 계획 작성
- `agents/team-lead.md`: 팀 리더 (팀원 조율, worktree 머지, 정리)
- `agents/team-worker.md`: 팀 구현원 (worktree isolation, TDD)
- `agents/team-reviewer.md`: 팀 리뷰어 (통합 리뷰)
- `agents/compound.md`: 회고 분석 (수동 호출만)

### 가이드
- `guides/beads-issue-guide.md`: 이슈 계층 구조 및 작성 가이드
- `guides/gate-process.md`: Quality Gate 프로세스
- `guides/tdd-workflow.md`: TDD 워크플로우

## 지금 시작하세요

위 오케스트레이션 프로세스에 따라 워크플로우를 실행합니다.
