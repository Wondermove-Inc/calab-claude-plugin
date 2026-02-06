---
name: verify-agents
description: |
  에이전트 출력 감사. 병렬 작업 에이전트의 산출물을 계획과 체계적으로 비교 검증합니다.
  SubagentStop 훅에서 병렬 에이전트 완료 감지 시 자동 트리거됩니다.
user-invocable: false
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, Task]
skills: [project-rules, clarification-protocol]
agents:
  primary: agent-verifier
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# verify-agents - 에이전트 출력 자동 감사 (패시브)

> **병렬 작업 에이전트 완료 시 자동 트리거되어 산출물을 검증**

---

## 트리거 조건

| 조건 | 설명 |
|------|------|
| 병렬 에이전트 2개+ 완료 | `subagent_tracker.py`에서 running → 0 전환 감지 |
| Wave 완료 | 같은 Wave의 모든 Task 에이전트 종료 |

> `subagent_tracker.py` SubagentStop에서 자동 감지 → stdout으로 검증 지시를 Claude 컨텍스트에 주입

---

## 자동 검증 지시 (주입되는 메시지)

> **이 메시지가 Claude 컨텍스트에 주입되면, 반드시 `run_in_background=True`로 실행하세요.**
> **사용자 작업을 절대 차단하지 마세요.**

```python
Task(
    subagent_type="calab-plugin:agent-verifier",
    description="병렬 에이전트 출력 자동 감사",
    run_in_background=True,
    model="haiku",
    prompt="""
[Role] 에이전트 출력 검증 전문가 (읽기 전용)
[Goal] 방금 완료된 병렬 에이전트의 산출물 완전성 검증
[Scope] 최근 완료된 에이전트 (running → 0 전환 시점 기준)

## 검증 절차

### Step 1: 에이전트 실행 이력 수집
- `.claude-state/subagent_stats.json` 읽기 (에이전트 호출 통계)
- `.claude-state/subagent.log` 읽기 (최근 50줄)
- `.claude-state/artifact_check.log` 읽기 (이전 검증 결과)

### Step 2: 기대 산출물 목록 생성
- AGENT_ARTIFACTS 정의 대조 (post_skill_artifact_check.py 기반)
- 각 에이전트별 필수 산출물 경로 확인

### Step 3: 5단계 검증
1. 파일 존재 확인 (Glob)
2. 비어있지 않은 내용 확인 (Read + 10줄 이상)
3. export/import 유효성 확인 (Grep)
4. tsc --noEmit 타입 체크 (TypeScript 프로젝트인 경우)
5. 계획 대비 누락 파일 식별

### Step 4: 체크리스트 출력
- 각 에이전트별: 기대 산출물 vs 실제 산출물

### Step 5: 미달 항목 보고 (stdout 출력)
- 빈 파일 / 누락 파일 목록
- 권장 조치 제시
- ❌ 항목이 있으면 메인 오케스트레이터에게 수정 요청

[Output] stdout 체크리스트 (읽기 전용 에이전트 — 파일 쓰기 없음)
"""
)
```

---

## 검증 유형

| 옵션 | 검증 범위 |
|------|----------|
| `--all` | 현재 feature의 모든 에이전트 산출물 |
| `--recent` | 최근 30분 이내 완료된 에이전트만 |
| `--wave N` | 특정 Wave 번호에 속한 에이전트만 |
| (기본) | `--recent`와 동일 |

---

## 데이터 소스

### 상태 파일

| 파일 | 용도 |
|------|------|
| `.claude-state/subagent_stats.json` | 에이전트 호출 통계 (타입, 횟수, 평균 실행 시간) |
| `.claude-state/subagent.log` | JSONL 이벤트 로그 (SubagentStart/Stop) |
| `.claude-state/artifact_check.log` | 산출물 검증 결과 JSONL |
| `.claude-state/artifact_stats.json` | 에이전트별 검증 통과/실패 통계 |
| `.claude-state/worktree.json` | Wave/Task 매핑 정보 |

### subagent_stats.json 구조

```json
{
  "agents": {
    "calab-plugin:planner-phase": {
      "total_invocations": 3,
      "last_invoked": "2026-02-06T10:30:00",
      "avg_duration": 45.2
    }
  },
  "running": {},
  "total_starts": 150,
  "total_stops": 148
}
```

### 에이전트별 기대 산출물 (23개 에이전트)

| 에이전트 | 필수 산출물 |
|----------|-----------|
| `planner-phase` | `01-brainstorm.md`, `02-PRD.md` |
| `design` | `03-architecture.md`, `04-ERD.md` |
| `planner-task` | `05-tasks.md`, `worktree.json` |
| `dev-executor` | `implementation-report.md` |
| `validator` | `validation-report.md` |
| `reinforcer` | `reinforcer-report.md` |
| `code-reviewer` | `code-review.md` |
| `security-reviewer` | `security-review.md` |
| `qa` | `qa-report.md` |
| `build-error-resolver` | `build-error-report.md` |
| `task-validator` | `task-validation.md` |
| `project-onboarder` | `PROJECT_SUMMARY.md` 외 3개+ |
| `root-cause-finder` | `analysis.md` / `report.md` |
| `bug-fixer` | `fix-report.md` |
| `deep-researcher` | `.claude/research/*.md` |
| `web-researcher` | `.claude/research/*.md` |
| `doc-updater` | `doc-update-report.md` |
| `docs-generator` | `generated-docs.md` |
| `e2e-runner` | `e2e-report.md` |
| `jira-connector` | `jira-sync.md` |
| `project-guardian` | `guardian-report.md` |
| `refactor-cleaner` | `refactor-report.md` |
| `dev-workflow` | `workflow-log.md` |

---

## 5단계 검증 프로토콜

### Step 1: 파일 존재 (Existence)

```
Glob(".claude/docs/active/{feature}/*.md")
Glob(".claude-state/*.json")
→ 에이전트별 기대 파일 vs 실제 파일 대조
```

### Step 2: 내용 충분성 (Substantive)

```
각 파일 Read → 10줄 이상인지 확인
빈 파일 또는 스텁(placeholder)만 있는 파일 탐지
```

### Step 3: 연결 유효성 (Wired)

```
TypeScript 파일: import/export 검증
JSON 파일: JSON.parse 유효성
Markdown 파일: 필수 섹션 존재 확인
```

### Step 4: 타입 안전성 (Type Safety)

```bash
# TypeScript 프로젝트인 경우
tsc --noEmit
# 타입 오류 → 파일별 분류 → 수정 또는 위임
```

### Step 5: 계획 정합성 (Plan Alignment)

```
worktree.json의 Task 목록 vs 실제 구현 파일
각 Task의 expected_files vs 실제 파일 존재
누락된 파일 식별 + 보고
```

---

## 출력 형식

### 검증 통과

```
============================================
[VERIFY-AGENTS] 에이전트 출력 감사 완료
============================================

📊 검증 범위: 최근 30분 / 에이전트 5개
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 planner-phase (12:30:15)
  ✅ 01-brainstorm.md (142줄)
  ✅ 02-PRD.md (259줄)

🤖 design (12:35:22)
  ✅ 03-architecture.md (180줄)
  ✅ 04-ERD.md (95줄)

🤖 planner-task (12:40:10)
  ✅ 05-tasks.md (320줄)
  ✅ worktree.json (유효한 JSON)

🤖 dev-executor (12:50:33)
  ✅ src/auth/login.ts (245줄, tsc OK)
  ✅ src/auth/__tests__/login.test.ts (180줄)
  ✅ implementation-report.md (45줄)

🤖 validator (12:55:00)
  ✅ validation-report.md (68줄)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 결과: 5/5 에이전트 통과 | 12/12 파일 검증됨
✅ 타입 체크: tsc --noEmit 통과
============================================
```

### 검증 실패

```
============================================
[VERIFY-AGENTS] 에이전트 출력 감사 ⚠️
============================================

📊 검증 범위: Wave 2 / 에이전트 3개
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 dev-executor [TASK-003] (13:10:22)
  ✅ src/api/users.ts (310줄)
  ❌ src/api/__tests__/users.test.ts (0줄 - 빈 파일)
  ❌ implementation-report.md (미생성)

🤖 dev-executor [TASK-004] (13:12:45)
  ✅ src/api/auth.ts (280줄)
  ✅ src/api/__tests__/auth.test.ts (200줄)
  ⚠️ implementation-report.md (5줄 - 내용 부족)

🤖 code-reviewer (13:20:00)
  ❌ code-review.md (미생성)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 결과: 1/3 에이전트 통과 | 4/8 파일 검증됨
❌ 문제 4건: 빈 파일 1건, 미생성 2건, 내용 부족 1건

🔧 자동 수정 시도:
  → users.test.ts: 재생성 필요 (dev-executor 재호출)
  → implementation-report.md: 재생성 필요
  → code-review.md: code-reviewer 재호출 필요
============================================
```

---

## 산출물 (필수)

| 산출물 | 경로 |
|--------|------|
| 검증 보고서 | `.claude/docs/active/{feature}/agent-verification-report.md` |

### 보고서 형식

```markdown
# Agent Verification Report

## Summary
- 검증 시각: {timestamp}
- 검증 범위: {--all|--recent|--wave N}
- 에이전트 수: {total}
- 통과: {passed} / 실패: {failed}
- 파일 수: {total_files}
- 검증됨: {verified} / 누락: {missing} / 빈 파일: {empty}

## Agent Details
### {agent_type} ({timestamp})
| 파일 | 상태 | 줄 수 | 비고 |
|------|------|-------|------|
| {file} | ✅/❌/⚠️ | {lines} | {note} |

## Type Check (tsc --noEmit)
- 결과: PASS / FAIL
- 오류: {error_count}건
- 오류 목록: [...]

## Missing/Broken Files
1. {file} - {reason}

## Auto-Fix Actions
1. {action} - {result}

## Recommendations
- [...]
```

---

## 다음 단계 선택 (필수)

| 결과 | 권장 |
|------|------|
| 전체 통과 | 작업 계속 / 다음 Wave |
| 빈 파일/누락 발견 | 해당 에이전트 재호출 |
| 타입 오류 발견 | `build-error-resolver` 실행 |
| 심각한 누락 | `/solve` 에스컬레이션 |

> **작업 완료 후 반드시 AskUserQuestion 호출**
>
> 검증이 완료되면 현재 상황을 분석하여 AskUserQuestion으로 다음 단계 선택지를 제시하세요.
> - 검증 결과 요약
> - 누락 파일 재생성 옵션 (권장 표시, 이슈 있는 경우)
> - 다음 Wave/Task 진행 옵션
> - 추가 검증 옵션
> - 종료 옵션
