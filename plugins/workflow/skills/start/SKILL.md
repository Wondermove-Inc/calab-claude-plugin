---
name: workflow:start
description: 워크플로우를 시작합니다. start 스킬이 오케스트레이터로서 Planner→Worker→Reviewer 흐름을 관리합니다.
disable-model-invocation: true
---

# /workflow:start 커맨드

워크플로우를 시작합니다. 이 스킬이 오케스트레이터 역할을 수행합니다.

## 사용법

### 새 워크플로우 시작
```
/workflow:start <작업 요청>

예시:
/workflow:start 클러스터 알림 기능 추가
/workflow:start 로그인 버그 수정
```

### 중단된 워크플로우 재개
```
/workflow:start --resume <epic-id>

예시:
/workflow:start --resume calab-claude-plugin-abc123
```

## 핵심 원칙

1. **start 스킬이 오케스트레이터**: Planner는 이슈에 계획을 작성하고, 흐름 제어는 이 스킬이 담당
2. **릴레이 방식**: 각 에이전트가 beads 이슈를 보고 독립적으로 이어받음
3. **beads가 Single Source of Truth**: 이슈 상태로 추적
4. **Work → Review 자동 진입**: Worker 완료 시 사용자 승인 없이 Reviewer로 전환
5. **Review Gate 필수**: Reviewer 완료 시 항상 사용자 승인을 거침 (승인/수정필요 모두)

## 워크플로우 흐름

```
사용자 요청
    ↓
┌─────────────┐
│   Planner   │  ← 요청 분석, 이슈에 계획 작성
└─────────────┘
    ↓ Plan Gate: 계획 승인
┌─────────────┐
│   Worker    │  ← TDD (RED→GREEN→REFACTOR)
└─────────────┘
    ↓ (자동 전환)
┌─────────────┐
│  Reviewer   │  ← 코드 리뷰, 이슈에 결과 작성
└─────────────┘
    ↓ Review Gate: 사용자 판단
    │
    ├─ 승인 → 완료
    ├─ Worker 재작업 → Worker → Reviewer → Review Gate
    └─ Reviewer 재리뷰 → Reviewer → Review Gate
```

## 오케스트레이션 프로세스

### 0단계: 이슈 생성

> **반드시 `guides/beads-issue-guide.md`를 읽고 계층 구조, 제목 형식, 템플릿을 준수합니다.**

**start 스킬은 Epic만 생성**합니다. Sub-task는 각 에이전트가 자기 작업 시작 시 직접 생성합니다.
재작업 시에는 기존 이슈를 reopen합니다.

| 이슈 | 생성 주체 | 시점 |
|------|----------|------|
| Epic | start 스킬 | 0단계 |
| Plan Sub-task | Planner 에이전트 | 1단계 시작 시 |
| Work Sub-task | Worker 에이전트 | 3단계 시작 시 |
| Review Sub-task | Reviewer 에이전트 | 4단계 시작 시 |

```bash
# Epic 생성 (워크플로우 Epic Description 템플릿 사용)
bd create "[YY.Q.N][영역] 기능명" --type epic --priority 2 \
  --description "$(cat <<'EOF'
## 요청 분석
- **원본 요청**: {사용자 요청}
- **작업 유형**: [새 기능 / 버그 수정 / 리팩토링]
- **복잡도**: [단순 / 중간 / 복잡]

## 실행 계획
| 순서 | 에이전트 | 작업 |
|------|---------|------|
| 1 | planner | 요청 분석, 설계 → 자기 이슈에 작성 |
| 2 | worker | TDD 구현 → 자기 이슈에 작업 내용 작성 |
| 3 | reviewer | 코드 리뷰 → 자기 이슈에 리뷰 결과 작성 |

## 완료 조건
- [ ] AC1: ...
- [ ] AC2: ...
EOF
)"

# 워크플로우 시작 코멘트
bd comments add <epic-id> "[Workflow] 시작"
```

### 1단계: Planner 호출

> Planner가 자기 Sub-task를 직접 생성합니다.

```
Task (subagent_type: workflow:planner, model: opus, run_in_background: true):
"Epic bd-<epic-id> 작업 수행. bd show로 상세 확인."
```

완료 대기:
```
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: 결과 확인 후 다음 단계
→ timeout: 사용자에게 "Planner 에이전트가 10분 내 완료되지 않았습니다" 알림, 재대기 또는 취소 선택
```

완료 시:
```bash
bd comments add <epic-id> "[Planner] 완료"
```

### 2단계: Plan Gate

`AskUserQuestion`으로 계획 승인 요청:

```
## Plan 검토

이슈: bd show <planner-subtask-id>

### 요약
- 유형: [작업 유형]
- 복잡도: [복잡도]
- 주요 변경: [요약]

옵션:
- "승인": Worker 단계로 진행
- "수정 필요": Planner 재호출
- "취소": 작업 중단
```

### 3단계: Worker 호출

> Worker가 자기 Sub-task를 직접 생성합니다.

```
Task (subagent_type: workflow:worker, model: sonnet, run_in_background: true):
"Epic bd-<epic-id> 작업 수행. bd show로 상세 확인."
```

완료 대기:
```
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: 결과 확인 후 다음 단계
→ timeout: 사용자에게 "Worker 에이전트가 10분 내 완료되지 않았습니다" 알림, 재대기 또는 취소 선택
```

완료 시:
```bash
bd comments add <epic-id> "[Worker] 완료"
```

### 4단계: Reviewer 호출

> Reviewer가 자기 Sub-task를 직접 생성합니다.

```
Task (subagent_type: workflow:reviewer, model: opus, run_in_background: true):
"Epic bd-<epic-id> 작업 수행. bd show로 상세 확인."
```

### 5단계: Review Gate

완료 대기:
```
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: 결과 확인 후 다음 단계
→ timeout: 사용자에게 "Reviewer 에이전트가 10분 내 완료되지 않았습니다" 알림, 재대기 또는 취소 선택
```

완료 시 **항상** `AskUserQuestion`으로 사용자 판단을 요청합니다:

```bash
bd comments add <epic-id> "[Reviewer] 완료"
```

```
## Review 완료

- 결정: [승인 / 수정필요]
- 품질: N/10
- Critical: N건, Major: N건
- 리뷰 상세: bd show <reviewer-subtask-id>

옵션:
- "승인": 워크플로우 완료
- "Worker 재작업": Worker가 수정 후 Reviewer 재리뷰
- "Reviewer 재리뷰": 코드 수정 없이 Reviewer만 재검토
- "취소": 작업 중단
```

#### Worker 재작업 선택 시

기존 Worker/Reviewer 이슈를 reopen하여 재사용합니다.

```bash
# 1. Worker 이슈 reopen
bd update <worker-subtask-id> --status in_progress
bd comments add <worker-subtask-id> "[Rework] 리뷰 피드백 반영 (N차)"
```

```
# 2. Worker 호출 (기존 이슈 ID 전달)
Task (subagent_type: workflow:worker, model: sonnet, run_in_background: true):
"bd-<worker-subtask-id> 재작업. 리뷰 피드백: bd show <reviewer-subtask-id> 참조."
```

```
# 3. Worker 완료 대기
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: 다음 단계
→ timeout: 사용자에게 알림, 재대기 또는 취소 선택
```

```bash
# 4. Worker 완료 → Reviewer 이슈 reopen
bd update <reviewer-subtask-id> --status in_progress
bd comments add <reviewer-subtask-id> "[Rework] 수정사항 검증 (N차)"
```

```
# 5. Reviewer 호출 (기존 이슈 ID 전달)
Task (subagent_type: workflow:reviewer, model: opus, run_in_background: true):
"bd-<reviewer-subtask-id> 재리뷰. bd show로 상세 확인."
```

```
# 6. Reviewer 완료 대기
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: 5단계(Review Gate)로 복귀
→ timeout: 사용자에게 알림, 재대기 또는 취소 선택
```

#### Reviewer 재리뷰 선택 시

기존 Reviewer 이슈를 reopen하여 재사용합니다.

```bash
# 1. Reviewer 이슈 reopen
bd update <reviewer-subtask-id> --status in_progress
bd comments add <reviewer-subtask-id> "[Rework] 재검토 (N차)"
```

```
# 2. Reviewer 호출 (기존 이슈 ID 전달)
Task (subagent_type: workflow:reviewer, model: opus, run_in_background: true):
"bd-<reviewer-subtask-id> 재리뷰. bd show로 상세 확인."
```

```
# 3. Reviewer 완료 대기
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: 5단계(Review Gate)로 복귀
→ timeout: 사용자에게 알림, 재대기 또는 취소 선택
```

### 6단계: 워크플로우 완료 — 티켓 일괄 close

Review Gate 승인 시, 모든 Sub-task와 Epic을 일괄 close합니다.

```bash
# 모든 Sub-task close
bd close <planner-subtask-id>
bd close <worker-subtask-id>
bd close <reviewer-subtask-id>

# Epic close
bd comments add <epic-id> "[Workflow] 완료"
bd close <epic-id>
```

사용자에게 결과 보고:
```
완료: <epic-id> | 상태: closed | 상세: bd show <epic-id>
```

## 재개 프로세스 (--resume)

```bash
# 1. Sub-task 상태 확인
bd list --parent <epic-id>

# 2. Epic 코멘트 확인
bd comments <epic-id>

```

**재개 지점 결정**:
- `in_progress` Sub-task → 해당 에이전트부터 재개
- 모두 `open` → 처음부터 시작
- 일부 `closed` → 다음 `open` Sub-task부터
- `[Gate N] 대기중` 코멘트 → 해당 Gate부터

## 적응적 워크플로우

작업 유형에 따라 에이전트 스킵이 가능합니다:

| 작업 유형 | 실행 흐름 |
|----------|----------|
| 복잡 기능 | Planner → Worker → Reviewer |
| 중간 작업 | Planner(간소) → Worker → Reviewer |
| 단순 버그/설정 | Worker만 (TDD 스킵 허용 시 코드만) |

### 에이전트 스킵 조건

| 에이전트 | 스킵 조건 |
|----------|----------|
| Planner | 3줄 미만 단순 수정, 설정 변경 |
| Worker (TDD) | 코드 로직 변경 없는 경우 (설정, 문서, 오타) |
| Reviewer | 3줄 미만 단순 수정 |

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
→ timeout: 사용자에게 "{에이전트명} 에이전트가 10분 내 완료되지 않았습니다" 알림
          AskUserQuestion으로 "재대기 / 취소" 선택 요청
```

**timeout 처리**:
- timeout 발생 시 반드시 사용자에게 알림
- `AskUserQuestion`으로 "재대기(10분 추가)" 또는 "취소" 선택
- 재대기 선택 시 동일한 task_id로 `TaskOutput` 재호출

## 토큰 효율성

### 핵심 원칙: 상세는 이슈에, 반환은 ID만

```mermaid
%%{init: {"flowchart": {"defaultRenderer": "elk"}}}%%
flowchart LR
    Agent[에이전트] -->|"완료: bd-abc<br/>(상세는 이슈에)"| Start[start 스킬]
    Start -->|"완료: bd-epic<br/>(상세: bd show)"| User[사용자]
```

## 에러 핸들링

| 상황 | 처리 |
|------|------|
| Plan Gate 거부 | Planner 재호출 |
| Review Gate: Worker 재작업 | Worker → Reviewer → Review Gate 복귀 |
| Review Gate: Reviewer 재리뷰 | Reviewer → Review Gate 복귀 |
| 에이전트 실패 | 최대 3회 재시도, 3회 실패 → 사용자 보고 |
| 대기 timeout (10분) | 사용자에게 알림 → 재대기 또는 취소 선택 |
| 사용자 취소 | Epic 코멘트 기록 후 close |

## 참조 문서

### 에이전트
- `agents/planner.md`: 요청 분석, 이슈에 계획 작성
- `agents/worker.md`: TDD 기반 테스트+구현
- `agents/reviewer.md`: 코드 리뷰, 이슈에 결과 작성
- `agents/compound.md`: 회고 분석 (수동 호출만)

### 가이드
- `guides/beads-issue-guide.md`: 이슈 계층 구조 및 작성 가이드
- `guides/gate-process.md`: Quality Gate 프로세스
- `guides/tdd-workflow.md`: TDD 워크플로우

## 지금 시작하세요

위 오케스트레이션 프로세스에 따라 워크플로우를 실행합니다.
