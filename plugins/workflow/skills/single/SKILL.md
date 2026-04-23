---
name: workflow:single
description: 단일 Worker 워크플로우. 이슈 또는 사용자 요청을 기반으로 Worker를 실행합니다. 중/소규모 작업용.
allowed-tools: Agent, Bash, AskUserQuestion, Read, Grep, Glob, TeamCreate, TeamDelete, SendMessage
disable-model-invocation: false
---

# /workflow:single 커맨드

이슈 ID 또는 사용자 자유 요청을 받아 단일 Worker를 실행합니다. 복잡한 작업은 `/workflow:teams`를 사용하세요.

```
/workflow:single bd-abc123                          # 기존 이슈 기반
/workflow:single 로그인 API에 rate limiting 추가해줘   # 사용자 요청 기반
```

## 모드 판별

`bd-` 접두사 → **이슈 모드**, 그 외 → **요청 모드** (이슈 자동 생성)

## 핵심 원칙

1. **요구사항 명확화**: 복잡한 요청만 사용자에게 질문, 단순 요청은 바로 실행
2. **설계 단계 없음**: Worker가 바로 구현, 리뷰는 전문 리뷰어 3명 병렬
3. **TDD 필수**: RED → GREEN → REFACTOR
4. **증거 기반 검증**: Worker 보고를 오케스트레이터가 테스트 재실행으로 교차 검증
5. **심각도 기반 루프 단축**: Minor/Suggestion은 자동 user-decision 승격 (Critical/Major만 auto-fix)

> 공통 규칙(금지 사항, 합리화 경고, 신뢰 수준, 혼란 관리): [`references/agent-common.md`](../../references/agent-common.md)

## 워크플로우

```
사용자 입력 → [1] 입력 판별/이슈 확보
            → [2] 요구사항 명확화 (복잡한 요청만)
            → [3] Worker 호출 (단일 또는 병렬)
            → [4] 증거 기반 검증 (테스트 재실행)
            → [5] 병렬 리뷰 (보안 + 성능 + 로직)
            → [6] 피드백 취합 + auto-fix 루프 (최대 3회)
            → [7] 결과 보고 + 이슈 완료
```

## 1단계: 입력 판별 + 이슈 확보

### 이슈 모드 (`bd-` 접두사)

```bash
bd show <issue-id>
bd update <issue-id> --status in_progress && bd comments add <issue-id> "[Single] 시작"
```

### 요청 모드 (자유 텍스트)

```bash
bd create "<요청 요약>" --type task --priority 2
bd update <생성된-id> --description "<요청 정리>" --acceptance "<완료 조건>"
bd update <생성된-id> --status in_progress && bd comments add <생성된-id> "[Single] 시작"
```

## 2단계: 요구사항 명확화 (조건부)

**단순 요청은 건너뜀**:
- 오타 수정, 설정 변경, 단일 함수 수정 → 건너뜀
- 새 기능, 아키텍처 변경, 다중 모듈 → 아래 체크 수행

복잡 요청에서 아래 중 하나라도 해당하면 `AskUserQuestion`:
- acceptance가 없거나 모호
- 구현 방향이 복수
- 영향 범위 불명확

```
question: "요구사항에 불명확한 항목이 있습니다: [나열]. 진행 방향을 선택해주세요."
options:
  - "보완 후 진행" — 답변 반영 후 이슈 업데이트
  - "그대로 진행" — 현재 내용 기반 최선 판단
```

### 가정 표면화

"그대로 진행" 또는 단순 요청에서 **암묵적 가정이 있으면** Worker 호출 전 `agent-common.md` §6 포맷으로 표면화. 암묵적 가정이 없는 명확한 요청은 생략.

## 3단계: Worker 호출

### 단일 실행 (기본) — 포그라운드

```
Agent(
  subagent_type: "workflow:worker",
  model: "opus",
  run_in_background: false,
  description: "단일 Worker 실행",
  prompt: "bd-<issue-id> 구현. bd show로 상세 확인."
)
```

### 병렬 실행 (독립 영역 명확한 경우만) — 백그라운드

파일 경계가 확실히 분리되는 경우에만 최대 5개 병렬:

```
# 한 메시지에서 동시 호출
Agent(
  subagent_type: "workflow:worker",
  run_in_background: true,
  description: "Worker 1",
  prompt: "bd-<issue-id> 구현. 담당: <영역 1>. bd show로 상세 확인."
)
Agent(
  subagent_type: "workflow:worker",
  run_in_background: true,
  description: "Worker 2",
  prompt: "bd-<issue-id> 구현. 담당: <영역 2>. bd show로 상세 확인."
)
```

> 확신 없으면 단일 실행. 병렬 Worker는 TeamCreate 없이 단순 백그라운드 subagent.

## 4단계: 증거 기반 검증 (Worker 보고 교차 검증)

Worker가 "테스트 PASS / 빌드 성공"을 보고한 경우에도 **오케스트레이터가 직접 재검증**합니다:

```bash
# 1. 실제 변경 파일 확인
git status --short
git diff --name-only

# 2. 보고된 파일 목록과 실제 변경 목록 비교
# 불일치 시: Worker가 범위 외 파일을 건드렸거나 누락한 가능성 → 재호출

# 3. 테스트 명령 직접 실행 (프로젝트별)
# 보고의 "PASS"와 실제 실행 결과 대조

# 4. 빌드 명령 직접 실행
```

| Worker 출력 | 검증 결과 | 처리 |
|-------------|----------|------|
| 완료 보고 | 테스트·빌드 실제 PASS | 5단계 진행 |
| 완료 보고 | 실제 실행 FAIL | "실패" 처리 → 사용자 판단 요청 |
| 완료 보고 | 파일 목록 불일치 | Worker에 재호출 (범위 준수 지시) |
| 실패 보고 / CONFUSION | — | 사용자 판단 요청 |

## 5단계: 병렬 리뷰 (3명 리뷰어)

Worker 검증 통과 후 3명 리뷰어를 팀으로 생성하여 병렬 리뷰:

```
TeamCreate(
  name: "single-reviewers",
  members: [
    {subagent_type: "workflow:security-reviewer", model: "opus",
     name: "security-reviewer",
     prompt: "보안 리뷰 요청 — 이슈 bd-<id>, 변경 파일 {목록}, 라운드 #1"},
    {subagent_type: "workflow:performance-reviewer", model: "opus",
     name: "performance-reviewer",
     prompt: "성능 리뷰 요청 — 이슈 bd-<id>, 변경 파일 {목록}, 라운드 #1"},
    {subagent_type: "workflow:logic-reviewer", model: "opus",
     name: "logic-reviewer",
     prompt: "로직/아키텍처 리뷰 요청 — 이슈 bd-<id>, 변경 파일 {목록}, 라운드 #1"}
  ]
)
```

3명의 피드백 보고 SendMessage를 모두 수신한 후 6단계 진행.

> logic-reviewer가 SOLID/레이어/인터페이스 일관성까지 통합 검증합니다.

## 6단계: 피드백 취합 + auto-fix 루프

### 6-1. 취합

- **중복 제거**: 같은 file:line은 더 높은 심각도 기준
- **분류 확정**: team-lead가 auto-fix/user-decision 최종 확정
- **심각도 자동 승격**: [`guides/gate-process.md`](../../guides/gate-process.md) §심각도 자동 승격 규칙

### 6-2. auto-fix 반영 (Critical/Major만)

```
Agent(
  subagent_type: "workflow:worker",
  model: "opus",
  run_in_background: false,
  description: "리뷰 auto-fix 반영",
  prompt: "bd-<issue-id> auto-fix 반영.\n수정 항목:\n{auto-fix 목록}\n기존 테스트 비파괴 주의."
)
```

### 6-3. 재검증 (4단계 반복)

Worker 재작업 후 다시 테스트·빌드 직접 재실행하여 교차 검증.

### 6-4. 재리뷰 (이슈 제기 리뷰어에게만)

```
SendMessage(to: "<이슈 제기 리뷰어>",
  message: "재리뷰 요청 — 이슈 bd-<id>, 수정 파일 {목록}, 라운드 #N")
```

이전 라운드 "이슈 없음"이었던 리뷰어는 스킵.

### 6-5. 루프 종료 조건

- 모든 리뷰어가 "이슈 없음" → 7단계
- 최대 3라운드 초과 → 남은 항목을 user-decision으로 승격, 사용자 판단
- 새 Critical/Major 발견 → 6-1부터 반복

### 6-6. user-decision 처리

```
AskUserQuestion:
  question: "리뷰어 피드백 중 사용자 판단 필요 항목: [나열]. 각 항목에 대해 선택해주세요."
```

사용자 결정 후 필요 시 Worker 재호출.

### 6-7. 팀 해산

```
TeamDelete(name: "single-reviewers")
```

## 7단계: 결과 보고 + 이슈 완료

### 성공 시

```bash
bd update <issue-id> \
  --description "<작업 요약: 변경 파일, 주요 내용>" \
  --acceptance "<AC 체크리스트>"
bd comments add <issue-id> "[Single] 완료" && bd close <issue-id>
```

### 결과 보고 포맷

```markdown
완료: <issue-id>

| 항목 | 결과 |
|------|------|
| Worker | N개 |
| 변경 파일 | N개 |
| 테스트 | N개 PASS (오케스트레이터 재검증) |
| 빌드 | 성공 |
| 리뷰 | 보안 PASS / 성능 PASS / 로직 PASS |
| 리뷰 라운드 | N회 |
| AC 달성 | N/N |

`bd show <issue-id>`
```

## 에러 핸들링

| 상황 | 처리 |
|------|------|
| 이슈 없음 | "이슈를 찾을 수 없습니다" 보고 후 종료 |
| Worker 실패 | 사용자에게 재시도/종료 선택 요청 |
| Worker 보고-실제 불일치 | Worker 재호출 (범위 준수 지시) |
| 병렬 Worker 일부 실패 | 성공분 유지, 실패 내용 보고 후 사용자 판단 |
| Worker가 CONFUSION 출력 | 혼란 내용·옵션을 사용자에게 전달 |
| 리뷰어 무응답 | 해당 리뷰어 스킵 후 사용자 보고 |
| 리뷰 3라운드 초과 | 남은 항목을 user-decision으로 승격 후 Completion Gate |

## 호출 규칙 요약

- 단일 Worker: `Agent(run_in_background: false)` — 포그라운드 차단
- 병렬 Worker: `Agent(run_in_background: true)` 동시 호출 → 자동 완료 메시지 수신
- Worker에게 이슈 ID만 전달 (토큰 효율화)
- 리뷰 필수: Worker 완료 후 반드시 4~6단계 수행 후 이슈 close

## 지금 시작하세요

위 프로세스에 따라 워크플로우를 실행합니다.
