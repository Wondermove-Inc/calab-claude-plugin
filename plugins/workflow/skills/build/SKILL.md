---
name: workflow:build
description: 단일 Worker 구현 워크플로우. 이슈 또는 사용자 요청을 기반으로 Worker를 실행하고, 병렬 리뷰·Completion Gate까지 수행합니다. 중/소규모 작업용.
allowed-tools: Agent, Bash, AskUserQuestion, Read, Grep, Glob, TeamCreate, TeamDelete, SendMessage
---

# /workflow:build 커맨드

이슈 ID 또는 사용자 자유 요청을 받아 단일 Worker를 실행합니다. 설계가 필요한 작업은 먼저 `/workflow:discovery`으로 task 또는 epic+task를 생성한 뒤 build로 인계하세요.

```
/workflow:build bd-abc123                          # 단일 task 모드 (task 타입)
/workflow:build bd-epic-xxx                        # Epic 하이브리드 모드 (epic 타입)
/workflow:build 로그인 API에 rate limiting 추가해줘   # 자유 요청 모드 (이슈 자동 생성)
```

## 모드 판별

| 입력 | 모드 |
|------|------|
| `bd-` 접두사 + type=task | **단일 task 모드** — 곧장 구현 |
| `bd-` 접두사 + type=epic | **Epic 하이브리드 모드** — 자식 Task 목록 노출 → 시작 task 선택 → 단일 task 모드 진입 |
| 자유 텍스트 | **요청 모드** — task 자동 생성 |

## 핵심 원칙

1. **요구사항 명확화**: 복잡한 요청만 사용자에게 질문, 단순 요청은 바로 실행
2. **설계 단계 없음**: Worker가 바로 구현, 리뷰는 전문 리뷰어 3명 병렬
3. **TDD 필수**: RED → GREEN → REFACTOR
4. **증거 기반 검증**: Worker 보고를 오케스트레이터가 테스트 재실행으로 교차 검증
5. **리뷰 이슈 전수 처리(이번 PR 내)**: 등급 무관 모든 리뷰 항목은 ① 코드 반영, ② Worker 반려(사유 + 사용자 확인), ③ 사용자 명시적 무시(사유 필수) 중 하나로 close 전 종결. 미결 상태로 close 금지.
6. **Completion Gate**: close 직전 사용자 승인 게이트 통과 필수. user-decision/Worker 반려 항목이 있으면 항목별 처리 결정 강제.
7. **이슈 comment 영속 기록**: 시작/검증/라운드별 리뷰 취합/게이트 결정/완료를 모두 bd comments에 기록

> 공통 규칙(금지 사항, 합리화 경고, 신뢰 수준, 혼란 관리): [`references/agent-common.md`](../../references/agent-common.md)

## 워크플로우

```
사용자 입력 → [1] 입력 판별/이슈 확보
            → [2] 요구사항 명확화 (복잡한 요청만)
            → [3] Worker 호출 (단일 또는 병렬)
            → [4] 증거 기반 검증 (테스트 재실행)
            → [5] 병렬 리뷰 (보안 + 성능 + 로직)
            → [6] 피드백 취합 + auto-fix 루프 (최대 3회)
            → [7] Completion Gate (사용자 승인)
            → [8] 결과 보고 + 이슈 완료
```

## 1단계: 입력 판별 + 이슈 확보

### 1-A. `bd-` 접두사 입력 — 타입 확인

```bash
bd show <issue-id>
# type 필드를 확인하여 분기
```

#### type=task → 단일 task 모드

```bash
bd update <issue-id> --status in_progress && bd comments add <issue-id> "[Build] 시작"
```

#### type=epic → Epic 하이브리드 모드

자식 task 목록을 사용자에게 노출하고 시작할 task를 선택받습니다:

```bash
bd list --parent <epic-id> --status open  # 미완료 자식 task 목록
```

```
AskUserQuestion:
  question: "Epic bd-<epic-id>의 미완료 task 목록입니다. 어떤 task부터 시작할까요?"
  options:
    - "bd-<task-id-1> — <제목 1>"
    - "bd-<task-id-2> — <제목 2>"
    - ...
    - "Epic 진행 상황만 확인 (실행 안 함)"
```

선택된 task ID를 단일 task 모드로 진입시킵니다:

```bash
bd update <선택된-task-id> --status in_progress
bd comments add <선택된-task-id> "[Build] 시작 — Epic bd-<epic-id> 자식 작업"
```

> Epic 자체는 in_progress 유지 (이미 discovery에서 전환됨). 모든 자식 task가 완료되면 8단계 종료 직후 Epic close 여부를 사용자에게 묻습니다.

### 1-B. 자유 텍스트 입력 — 요청 모드

```bash
bd create "<요청 요약>" --type task --priority 2
bd update <생성된-id> --description "<요청 정리>" --acceptance "<완료 조건>"
bd update <생성된-id> --status in_progress && bd comments add <생성된-id> "[Build] 시작"
```

### 1-C. blocked_by 검사 (Epic 모드에서)

선택된 task에 `blocked_by`가 있고 선행 task가 미완료(open/in_progress)면 사용자에 안내:

```
"이 task는 bd-<선행>에 의존합니다. 선행 task부터 진행하시겠습니까?"
options: ["선행 task로 변경" / "그대로 진행 (강제)" / "취소"]
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

검증 통과 후 comment 기록:

```bash
bd comments add <issue-id> "[Build 검증] 변경 파일 N개, 테스트 N개 PASS, 빌드 성공"
```

검증 실패 후 사용자 판단 요청 시에도 사유 기록:

```bash
bd comments add <issue-id> "[Build 검증실패] 사유: <테스트 N개 FAIL / 파일 불일치 / Worker CONFUSION>"
```

## 5단계: 병렬 리뷰 (3명 리뷰어)

Worker 검증 통과 후 3명 리뷰어를 팀으로 생성하여 병렬 리뷰:

```
TeamCreate(
  name: "build-reviewers",
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

### 6-1. 취합 (3-way 분류)

- **중복 제거**: 같은 file:line은 더 높은 심각도 기준
- **분류 확정**: team-lead가 다음 3가지로 최종 확정
  - **auto-fix**: 명백한 개선. 등급 무관 전수 적용 대상
  - **user-decision**: 트레이드오프가 명확하여 사용자 결정이 필요 (옵션 A/B, 정책 결정, 리뷰어 간 의견 충돌)
  - **reject 후보**: team-lead 판단으로도 false positive·컨텍스트 부족이 의심되는 항목 → Worker 검토 후 사유와 함께 7-2로 승격
- **comment 영속 기록**: 라운드별 취합 결과를 반드시 bd에 기록

```bash
bd comments add <issue-id> "[Build 리뷰 #N] auto-fix N건 / user-decision M건 / reject-후보 K건 — 핵심: <2~3줄 요약>"
# 예) [Build 리뷰 #1] auto-fix 3건 / user-decision 1건 / reject-후보 1건 — 핵심: SQL 인젝션 1건(Critical), 캐싱 정책 1건, 보안 false-positive 의심 1건
```

### 6-2. auto-fix 반영 + Worker 반려 권한

auto-fix 대상은 등급 무관 전수 적용. Worker는 false positive·컨텍스트 부족·상충 충돌·AC 위반 시 적용을 거부하고 반려 사유를 보고할 권한이 있음. 사유 정의·반려 보고 포맷은 [`agents/worker.md`](../../agents/worker.md) §리뷰 auto-fix 모드 참조.

```
Agent(
  subagent_type: "workflow:worker",
  model: "opus",
  run_in_background: false,
  description: "리뷰 auto-fix 반영",
  prompt: "bd-<issue-id> auto-fix 반영.\n수정 항목 (등급 무관 전수):\n{auto-fix 목록}\n\n반려 권한 행사 시 worker.md §리뷰 auto-fix 모드의 반려 보고 포맷 사용. 기존 테스트 비파괴 주의."
)
```

team-lead는 Worker 반려 항목을 6-1의 reject-후보와 합쳐 **user-decision으로 자동 승격**시키고 7-2-B로 보냅니다.

### 6-3. 재검증 (4단계 반복)

Worker 재작업 후 다시 테스트·빌드 직접 재실행하여 교차 검증.

### 6-4. 재리뷰 (이슈 제기 리뷰어에게만)

```
SendMessage(to: "<이슈 제기 리뷰어>",
  message: "재리뷰 요청 — 이슈 bd-<id>, 수정 파일 {목록}, 라운드 #N")
```

이전 라운드 "이슈 없음"이었던 리뷰어는 스킵.

재리뷰 결과도 comment에 기록:

```bash
bd comments add <issue-id> "[Build 리뷰 #N] auto-fix N건 (재리뷰 통과 / 잔여 N건)"
```

### 6-5. 루프 종료 조건

- 모든 리뷰어가 "이슈 없음" → 7단계
- 최대 3라운드 초과 → 남은 항목을 user-decision으로 승격, comment에 승격 사유 기록 후 7단계 (Gate에서 항목별 처리 강제)
- 새 항목 발견(등급 무관) → 6-1부터 반복

```bash
bd comments add <issue-id> "[Build 리뷰 종료] 라운드 N회 종료 — 잔여 user-decision M건 (Gate에서 전수 처리)"
```

### 6-6. 팀 해산

```
TeamDelete(name: "build-reviewers")
```

## 7단계: Completion Gate (사용자 승인)

close 직전 **사용자에게 최종 변경사항을 노출하고 승인을 받습니다**. **리뷰에서 도출된 모든 이슈는 이번 PR 안에서 종결되어야 하며**, user-decision 잔여 항목이 있으면 항목별로 처리 결정을 강제합니다.

### 7-1. 게이트 보고 (사용자 노출)

```markdown
## Build 완료 보고 (Gate)

### 구현 요약
{핵심 변경 2~4줄}

### 변경 파일
- ...

### 완료 검증 (증거 기반)
- [ ] 모든 AC 구현 (1:1 대조)
- [ ] 테스트 PASS (오케스트레이터 직접 실행 결과)
- [ ] 빌드 성공 (오케스트레이터 직접 실행 결과)
- [ ] 리뷰 auto-fix 전수 반영
- [ ] user-decision 잔여 0건 (또는 7-2 처리 후 0건)

### 리뷰 결과
- 라운드: N회 / auto-fix: N건 / user-decision: M건
- 리뷰어별: security N건 / performance N건 / logic N건

### ⚠️ 사용자 판단 필요 항목 (있을 때만)
1. [항목 1] — {설명} (옵션 A/B + reviewer 의견)
```

### 7-2. user-decision 항목별 처리 (M ≥ 1인 경우 필수)

user-decision 잔여(6-1 트레이드오프 + 6-2 Worker 반려 + 3라운드 초과 승격분)가 한 건이라도 있으면 **항목별로** `AskUserQuestion`을 호출. "보류한 채 완료"는 허용하지 않습니다.

분기 표(7-2-A 일반 user-decision / 7-2-B Worker 반려 항목)와 선택지별 처리 정의는 [`guides/gate-process.md`](../../guides/gate-process.md) §Completion Gate의 user-decision 처리를 참조.

#### AskUserQuestion 호출 패턴

```
# 7-2-A 일반 user-decision (트레이드오프)
AskUserQuestion:
  question: "[Build Gate] user-decision 항목 N/M:\n{항목 설명}\n출처: {reviewer}\n옵션: {A / B / 트레이드오프}"
  options: ["옵션 A 반영", "옵션 B 반영", "이번 PR 무시 (사유 필수)", "취소 (close 안 함)"]

# 7-2-B Worker 반려 항목
AskUserQuestion:
  question: "[Build Gate] Worker 반려 항목 N/M:\n리뷰 피드백: {원 피드백}\n출처: {reviewer}\nWorker 반려 사유: {사유 + 코드 근거}"
  options: ["Worker 반려 인정 (적용 안 함)", "그래도 적용 (Worker 반려 거부)", "이번 PR 무시 (사유 필수)", "취소 (close 안 함)"]
```

처리 결정 누적 후 일괄 반영 권장. "반영" 또는 "그래도 적용" 결정이 1건 이상이면 worker 재호출 필수(6-2 패턴 → 4·5·6 재진행 → 7 재진입).

```bash
bd comments add <issue-id> "[Build Gate] user-decision 처리 — 반영 N건 / Worker 반려 인정 K건 / 무시 M건"
bd comments add <issue-id> "[Build Gate] 반려 인정 — {항목명}: {Worker 사유}"   # 반려 인정 항목별
bd comments add <issue-id> "[Build Gate] 무시 사유 — {항목명}: {사용자 사유}"   # 무시 항목별
```

### 7-3. 최종 분기 (user-decision 잔여 0건 도달 후)

user-decision이 0건이거나 7-2 처리로 0건이 되면:

```
AskUserQuestion:
  question: "[Build Gate] 모든 리뷰 이슈가 처리되었습니다. 완료할까요?"
  options: ["완료" / "취소"]
```

**자동 통과 조건** (게이트 스킵 가능): user-decision 0건 + 모든 리뷰 PASS + AC 1:1 모두 충족인 경우, 7-2·7-3을 스킵하고 바로 8단계 진행해도 됩니다. comment에는 `[Build Gate] 자동 통과` 기록.

**완료** — 8단계 진행:

```bash
bd comments add <issue-id> "[Build Gate] 사용자 승인 — 완료"
```

**취소** — close하지 않음, 변경사항 처리는 사용자에게 위임:

```bash
bd comments add <issue-id> "[Build] 사용자 취소 — 변경사항 처리는 수동"
# 이슈는 in_progress 유지 (사용자가 수동 close하거나 후속 처리)
```

오케스트레이터는 변경사항을 자동 revert/stash하지 않습니다. 사용자에게 `git status` 결과만 보여주고 종료.

## 8단계: 결과 보고 + 이슈 완료

### 성공 시

```bash
bd update <issue-id> \
  --description "<작업 요약: 변경 파일, 주요 내용>" \
  --acceptance "<AC 체크리스트>"
bd comments add <issue-id> "[Build] 완료" && bd close <issue-id>
```

### 결과 보고 포맷 (Gate 통과 후 최종)

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
| Gate | 사용자 승인 (또는 자동 통과) |

`bd show <issue-id>`
```

**필수 규칙**: 통계 표를 2번 이상 출력하지 말 것. 7단계 게이트 보고와 8단계 최종 보고가 중복되지 않도록 8단계는 표 1개만 출력.

### Epic 하이브리드 모드 후속 안내

이번 task가 Epic의 자식이었다면 (1-A에서 Epic 모드로 진입), close 직후 Epic의 잔여 자식 task 상태를 확인하여 안내합니다:

```bash
bd list --parent <epic-id> --status open  # 미완료 자식 task
```

| 결과 | 처리 |
|------|------|
| 미완료 자식 task 1개 이상 | 사용자에게 "다음 task: bd-<id> — 계속 진행하시겠습니까?" 안내. 승인 시 build 재호출 (1-A Epic 모드 재진입) |
| 미완료 자식 task 0개 | "Epic의 모든 task가 완료되었습니다. Epic을 close 할까요?" 사용자 확인 후 `bd close <epic-id>` + `bd comments add <epic-id> "[Build] Epic 완료 — 자식 task N개 close"` |

> Epic close는 항상 사용자 승인 후 수행. build가 자동 close하지 않습니다.

## 이슈 comment 기록 표준 (영속 기록)

이슈에 남기는 comment 식별자는 다음을 사용합니다. 라이프사이클 추적·중단 후 재개·감사 용도.

| 시점 | 식별자 | 내용 |
|------|--------|------|
| 시작 | `[Build] 시작` | 워크플로우 진입 (Epic 자식인 경우 Epic ID 표기) |
| Worker 검증 통과 | `[Build 검증]` | 변경 파일 수, 테스트/빌드 결과 |
| Worker 검증 실패 | `[Build 검증실패]` | 실패 사유 (선택) |
| 리뷰 라운드별 | `[Build 리뷰 #N]` | auto-fix/user-decision/reject-후보 건수, 핵심 요약 |
| 리뷰 종료 | `[Build 리뷰 종료]` | 종료 사유 (전부 통과 / 3라운드 초과 — Gate에서 전수 처리) |
| Gate user-decision 처리 | `[Build Gate] user-decision 처리` | 항목별 반영/Worker 반려 인정/무시 결정 합계 |
| Gate 반려 인정 | `[Build Gate] 반려 인정` | 항목별 Worker 반려 사유 (적용 안 함 결정 시) |
| Gate 무시 사유 | `[Build Gate] 무시 사유` | 항목별 사용자 명시 사유 (반영 안 함 결정 시) |
| Gate 결정 | `[Build Gate]` | 사용자 승인 / 취소 / 자동 통과 |
| 완료 | `[Build] 완료` | close 직전 |
| 취소 | `[Build] 사용자 취소` | close 안 함, 사유 기록 |
| Epic 완료 | `[Build] Epic 완료` | Epic close 시 (Epic 이슈 측에 기록) |

## 에러 핸들링

| 상황 | 처리 |
|------|------|
| 이슈 없음 | "이슈를 찾을 수 없습니다" 보고 후 종료 |
| Worker 실패 | 사용자에게 재시도/종료 선택 요청 |
| Worker 보고-실제 불일치 | Worker 재호출 (범위 준수 지시) |
| 병렬 Worker 일부 실패 | 성공분 유지, 실패 내용 보고 후 사용자 판단 |
| Worker가 CONFUSION 출력 | 혼란 내용·옵션을 사용자에게 전달 |
| 리뷰어 무응답 | 해당 리뷰어 스킵 후 사용자 보고 |
| 리뷰 3라운드 초과 | 남은 항목을 user-decision으로 승격 후 7단계 Gate (항목별 처리 강제) |
| Worker가 auto-fix 반려 | 6-1 reject-후보와 합쳐 user-decision 자동 승격 → 7-2-B에서 사용자 결정 |
| Gate user-decision 잔여 | 항목별 `AskUserQuestion`로 반영/반려 인정/무시(사유 필수)/취소 강제 |
| Gate 취소 | 이슈 in_progress 유지, 변경사항 수동 처리 안내 |

## 호출 규칙 요약

- 단일 Worker: `Agent(run_in_background: false)` — 포그라운드 차단
- 병렬 Worker: `Agent(run_in_background: true)` 동시 호출 → 자동 완료 메시지 수신
- Worker에게 이슈 ID만 전달 (토큰 효율화)
- 리뷰 필수: Worker 완료 후 반드시 4~6단계 수행
- Completion Gate 필수: close 직전 7단계 통과 후에만 8단계 close 진행 (자동 통과 조건 제외)

## 지금 시작하세요

위 프로세스에 따라 워크플로우를 실행합니다.
