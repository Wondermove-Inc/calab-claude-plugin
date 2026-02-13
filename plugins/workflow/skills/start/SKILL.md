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

## 용어 정리

| 용어 | 정의 | 카운터 방식 |
|------|------|------------|
| **자동 반복** | Reviewer 수정필요 시 자동 Worker 재작업 (최대 3회) | Epic 코멘트 파싱: `grep -c "Worker-Reviewer 자동 반복"` |
| **재작업 차수** | Completion Gate 피드백 포함 총 재작업 횟수 (무제한) | Worker 이슈 코멘트: `[Auto-Rework]`, `[Completion-Rework]` |

## 핵심 원칙

1. **start 스킬이 오케스트레이터**: Planner는 이슈에 계획을 작성하고, 흐름 제어는 이 스킬이 담당
2. **릴레이 방식**: 각 에이전트가 beads 이슈를 보고 독립적으로 이어받음
3. **beads가 Single Source of Truth**: 이슈 상태로 추적
4. **Work → Review 자동 진입**: Worker 완료 시 사용자 승인 없이 Reviewer로 전환
5. **자동 반복 로직**: Reviewer 수정필요 시 Worker 자동 재작업 (최대 3회)
6. **Completion Gate**: Reviewer 승인 시에만 사용자 최종 검토

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
    ├─ 수정필요 → Worker 재작업 ⟲ (최대 3회 자동)
    └─ 승인 ↓
    Completion Gate: 최종 완료 검토 (사용자 승인)
    ├─ 완료 → 워크플로우 종료
    └─ 수정 → Reviewer 수정 계획 → Worker 재작업
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

### 5단계: Reviewer 완료 후 자동 반복 로직

완료 대기:
```
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: Reviewer 결과 확인
→ timeout: 사용자에게 "Reviewer 에이전트가 10분 내 완료되지 않았습니다" 알림, 재대기 또는 취소 선택
```

#### Reviewer 결과 분석

Reviewer 이슈의 description에서 결정 확인:
```bash
bd show <reviewer-subtask-id> | grep "결정:"
```

**반복 카운터 관리**: Epic 코멘트에서 실시간 파싱
```bash
# Epic 생성 시 초기화
max_iterations=3

# 현재 반복 횟수 확인 (코멘트 파싱, 실패 시 0으로 fallback)
iteration_count=$(bd show <epic-id> | grep -c "Worker-Reviewer 자동 반복" || echo "0")
```

#### Case 1: 수정필요 판정 (자동 반복)

반복 제한 확인:
```bash
# 최대 반복 도달 여부 확인
if [ "$iteration_count" -lt "$max_iterations" ]; then
    # 자동 Worker 재작업
    new_iteration=$((iteration_count + 1))
else
    # Completion Gate 진입 (최대 반복 도달 경고)
    # Case 2로 분기
fi
```

**자동 Worker 재작업**:
```bash
# 1. 반복 카운터 기록
bd comments add <epic-id> "[Workflow] Worker-Reviewer 자동 반복 (${new_iteration}/3)"

# 2. Worker 이슈 reopen
bd update <worker-subtask-id> --status in_progress
bd comments add <worker-subtask-id> "[Auto-Rework] Reviewer 피드백 반영 (${new_iteration}차)"
```

```
# 3. Worker 호출
Task (subagent_type: workflow:worker, model: sonnet, run_in_background: true):
"bd-<worker-subtask-id> 재작업. Reviewer 피드백: bd show <reviewer-subtask-id> 참조."
```

```
# 4. Worker 완료 대기
TaskOutput(task_id, block: true, timeout: 600000)
→ 완료: 다음 단계
→ timeout: 사용자에게 알림
```

```bash
# 5. Reviewer 이슈 reopen
bd update <reviewer-subtask-id> --status in_progress
bd comments add <reviewer-subtask-id> "[Auto-Review] 수정사항 검증 (${new_iteration}차)"
```

```
# 6. Reviewer 호출
Task (subagent_type: workflow:reviewer, model: opus, run_in_background: true):
"bd-<reviewer-subtask-id> 재리뷰. Worker 수정사항 검증."
```

```
# 7. 5단계로 복귀 (재귀)
→ Reviewer 결과 분석
```

#### Case 2: 승인 판정 (Completion Gate 진입)

```bash
bd comments add <epic-id> "[Reviewer] 승인 - Completion Gate 진입"
```

→ **6단계(Completion Gate)로 진행**

### 6단계: Completion Gate — 최종 완료 검토

Reviewer 승인 시 사용자에게 최종 완료 검토를 요청합니다.

```
## 워크플로우 완료 검토

- Reviewer 결정: 승인
- 품질: N/10
- Critical: 0건, Major: N건
- 자동 반복: ${iteration_count}/3회
- 리뷰 상세: bd show <reviewer-subtask-id>

옵션:
- "완료": 워크플로우 종료 및 모든 이슈 close
- "수정 필요": Reviewer가 수정 계획 업데이트 → Worker 재작업
- "취소": 작업 중단
```

**3회 자동 반복 도달 시 추가 경고**:
```
⚠️ 자동 반복 최대 도달 (3/3회) - 품질 재검토 권장

추가 옵션:
- "완료": 현재 상태로 워크플로우 종료
- "수정 필요 (재시도)": 자동 반복 카운터 초기화 후 Worker 재작업 (최대 3회)
- "수정 필요 (1회)": 카운터 초기화 없이 Worker 1회 재작업
- "취소": 작업 중단
```

#### 완료 선택 시

모든 Sub-task와 Epic을 일괄 close합니다.

```bash
# 모든 Sub-task close
bd close <planner-subtask-id>
bd close <worker-subtask-id>
bd close <reviewer-subtask-id>

# Epic close
bd comments add <epic-id> "[Workflow] 완료"
bd close <epic-id>
```

**사용자에게 간결한 결과 보고** (불필요한 중복 제거):

```markdown
🎯 워크플로우 완료

## 전체 에이전트 실행 통계
| 에이전트 | 실행 | 토큰 사용 | 소요 시간 | 도구 사용 | 결과 |
|---------|------|----------|----------|----------|------|
| Planner | 1회 | {tokens} | {time} | {tools}회 | ✅ 완료 |
| Worker (1차) | 1회 | {tokens} | {time} | {tools}회 | ✅ 완료 |
| Reviewer (1차) | 1회 | {tokens} | {time} | {tools}회 | ✅ {decision} |
| Worker (재작업) | N회 | {tokens} | {time} | {tools}회 | ✅ 피드백 반영 |
| Reviewer (재리뷰) | N회 | {tokens} | {time} | {tools}회 | ✅ {score}/10점 |
| **총계** | **N회** | **~{total_tokens}** | **~{total_time}** | **{total_tools}회** | **✅ 100%** |

Epic: {epic-id} (CLOSED)
상세: bd show {epic-id}
```

**주의사항**:
- 위 통계 표만 출력 (다른 요약, 타임라인, 산출물 목록 등은 생략)
- 재작업이 없었다면 해당 행 제외
- 토큰/시간/도구 사용은 실제 값으로 대체

#### 수정 필요 선택 시

Reviewer가 수정 계획을 작성하고 Worker가 재작업합니다.

```bash
# 1. Reviewer가 수정 계획 작성 (수동 또는 재호출)
bd update <reviewer-subtask-id> --description "$(cat <<'EOFD'
[Completion Gate 피드백 반영]

## 사용자 피드백
[사용자가 요청한 수정 사항]

## 수정 계획
| # | 파일 | 수정 내용 | 우선순위 |
|---|------|----------|----------|
| 1 | path/to/file | [구체적 수정 계획] | High |

Worker 재작업 지시.
EOFD
)"

# 2. Worker 이슈 reopen
bd update <worker-subtask-id> --status in_progress
bd comments add <worker-subtask-id> "[Completion-Rework] Gate 피드백 반영"
```

```
# 3. Worker 호출
Task (subagent_type: workflow:worker, model: sonnet, run_in_background: true):
"bd-<worker-subtask-id> 재작업. Completion Gate 피드백: bd show <reviewer-subtask-id> 참조."
```

```
# 4. Worker 완료 대기
TaskOutput(task_id, block: true, timeout: 600000)
```

```bash
# 5. Reviewer 이슈 reopen
bd update <reviewer-subtask-id> --status in_progress
bd comments add <reviewer-subtask-id> "[Completion-Review] Gate 피드백 검증"
```

```
# 6. Reviewer 호출
Task (subagent_type: workflow:reviewer, model: opus, run_in_background: true):
"bd-<reviewer-subtask-id> 재리뷰. Completion Gate 피드백 검증."
```

```
# 7. Reviewer 승인 시 Completion Gate 복귀
→ 6단계로 복귀
```

### 7단계: 워크플로우 종료

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
| Completion Gate (수정 필요) | Reviewer 수정 계획 → Worker 재작업 → Completion Gate 복귀 |

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
