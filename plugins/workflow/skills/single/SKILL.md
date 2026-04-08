---
name: workflow:single
description: 단일 Worker 워크플로우. 이슈 또는 사용자 요청을 기반으로 Worker를 실행합니다. 중/소규모 작업용.
allowed-tools: Agent, Bash, AskUserQuestion, Read, Grep, Glob
disable-model-invocation: true
---

# /workflow:single 커맨드

이슈 ID 또는 사용자의 자유 요청을 받아 단일 Worker를 실행합니다.
복잡한 작업은 `/workflow:teams`를 사용하세요.

```
/workflow:single bd-abc123             # 기존 이슈 기반
/workflow:single 로그인 API에 rate limiting 추가해줘  # 사용자 요청 기반
```

## 입력 판별

`bd-` 접두사 → **이슈 모드**, 그 외 → **요청 모드**

| 모드 | 이슈 관리 |
|------|----------|
| 이슈 모드 | 기존 이슈 조회 → 업데이트 → close |
| 요청 모드 | 이슈 자동 생성 → 업데이트 → close |

## 핵심 원칙

1. **요구사항 명확화**: 복잡한 요청은 사용자에게 질문, 단순 요청은 바로 실행
2. **Worker만 실행**: Planner/Reviewer 없음
3. **TDD 필수**: Worker는 RED → GREEN → REFACTOR 사이클 준수
4. **결과 검증**: Worker 실패 시 이슈를 닫지 않고 사용자에게 판단 요청

## 자주 발생하는 합리화 (경고)

| 합리화 | 반론 |
|--------|------|
| "간단하니까 테스트 안 써도 돼" | 간단한 코드도 회귀한다. 2줄짜리 테스트라도 작성하라. |
| "한번에 다 하는 게 빠른데" | 500줄 중 어떤 줄이 원인인지 찾기 전까지만 빠르게 느껴진다. |
| "나중에 테스트 작성할게" | 사후 테스트는 구현을 검증하지 행위를 검증하지 않는다. |
| "이 정도는 명확화 없이 진행해도 돼" | acceptance 없이 시작하면 완료 기준이 사라진다. 2줄이라도 적어라. |
| "병렬로 나누면 빠를 텐데" | 확신 없는 병렬은 충돌로 되돌아온다. 기본은 단일 실행이다. |

## 워크플로우

```
사용자 입력
  ↓
1. 입력 판별 & 요구사항 확보
  ↓
2. 요구사항 명확화 (복잡한 요청만)
  ↓
3. 병렬 여부 판단
  ↓
4. Worker 호출
  ↓
5. 결과 검증 & 이슈 완료
```

## 오케스트레이션 프로세스

### 1단계: 입력 판별 및 요구사항 확보

#### A. 이슈 모드 (`bd-` 접두사)

```bash
bd show <issue-id>
bd update <issue-id> --status in_progress && bd comments add <issue-id> "[Single] 워크플로우 시작"
```

이슈의 description과 acceptance를 분석하여 작업 범위를 파악합니다.

#### B. 요청 모드 (자유 텍스트)

사용자 요청을 분석하여 이슈를 생성합니다:

```bash
bd create "<요청 요약>" --type task --priority 2
bd update <생성된-id> \
  --description "<사용자 요청 내용 정리>" \
  --acceptance "<요청에서 도출한 완료 조건>"
bd update <생성된-id> --status in_progress && bd comments add <생성된-id> "[Single] 워크플로우 시작"
```

이후 이슈 모드와 동일하게 진행합니다.

### 2단계: 요구사항 명확화 (조건부)

**단순 요청은 이 단계를 건너뜁니다.** 아래 기준으로 판단합니다:

| 복잡도 | 예시 | 명확화 |
|--------|------|--------|
| **단순** | 오타 수정, 설정 변경, 단일 함수 수정 | 건너뜀 → 3단계로 |
| **복잡** | 새 기능 추가, 아키텍처 변경, 다중 모듈 수정 | 아래 체크 수행 |

복잡한 요청에서 아래 항목 중 하나라도 해당하면 AskUserQuestion으로 질문합니다:

- acceptance가 없거나 모호함
- 구현 방향이 복수 존재
- 영향 범위가 불명확

```
question: "요구사항을 확인했습니다. 아래 항목이 불명확합니다:\n\n[불명확 항목 나열]\n\n진행 방향을 선택해주세요."
header: "요구사항"
options:
  - label: "보완 후 진행", description: "불명확한 부분을 답변하여 보완합니다"
  - label: "그대로 진행", description: "현재 내용으로 최선의 판단으로 진행합니다"
```

- **"보완 후 진행"**: 사용자 답변을 반영하여 이슈 description/acceptance 보완 후 진행
- **"그대로 진행"**: 현재 내용 기반으로 최선의 판단으로 진행

#### 가정 표면화

"그대로 진행"을 선택받았거나, 명확화를 건너뛴 단순 요청에서도 **암묵적 가정이 존재하면** Worker 호출 전에 표면화합니다:

```
ASSUMPTIONS:
1. {가정 1} (예: 기존 인증 미들웨어를 재사용한다)
2. {가정 2} (예: 데이터베이스 스키마 변경은 없다)
→ 다른 지시가 없으면 이대로 진행합니다.
```

암묵적 가정이 없는 명확한 요청(오타 수정, 단일 함수 수정 등)은 이 단계를 건너뜁니다.

### 3단계: 병렬 분해 판단

기본은 **단일 Worker 실행**입니다.

이슈에 독립 작업 단위가 명시적으로 나열되고, 서로 다른 파일/모듈을 수정하는 경우에만 병렬을 고려합니다. 확신이 없으면 단일 실행합니다.

### 4단계: Worker 호출

#### 단일 실행 (기본) — 포그라운드 차단

단일 Worker는 `Agent` 도구를 **포그라운드**(`run_in_background: false`)로 호출합니다. 메인 Claude는 Worker가 완료될 때까지 대기하고, Worker의 최종 출력이 그대로 반환됩니다.

```
Agent(
  subagent_type: "workflow:worker",
  model: "opus",
  run_in_background: false,
  description: "단일 Worker 실행",
  prompt: "bd-<issue-id> 구현. bd show로 상세 확인."
)
```

#### 병렬 실행 — 백그라운드 + 자동 완료 수신

병렬 Worker (최대 5개)는 `run_in_background: true`로 동시 spawn. 각 Worker가 완료하면 `<teammate-message>`로 결과가 자동 전달됩니다. 모든 Worker의 완료 메시지를 수신한 후 5단계로 진행.

```
# 병렬 Worker N개를 한 메시지에서 동시 호출
Agent(
  subagent_type: "workflow:worker",
  model: "opus",
  run_in_background: true,
  description: "Worker 1",
  prompt: "bd-<issue-id> 구현. 담당: <영역 설명 1>. bd show로 상세 확인."
)

Agent(
  subagent_type: "workflow:worker",
  model: "opus",
  run_in_background: true,
  description: "Worker 2",
  prompt: "bd-<issue-id> 구현. 담당: <영역 설명 2>. bd show로 상세 확인."
)
```

병렬 Worker는 **팀 소속이 아닙니다** (TeamCreate 없음). 단순 백그라운드 subagent 실행이며, 완료 시 각자의 출력이 자동으로 대화 턴으로 도착합니다.

### 5단계: 결과 검증 및 완료

#### Worker 출력 검증

Worker 출력을 파싱하여 성공/실패를 판단합니다. **Worker가 성공을 보고한 경우에도** 아래 항목을 오케스트레이터가 재확인합니다:

- [ ] AC 항목과 Worker 보고가 1:1 매핑됨
- [ ] 테스트 PASS가 보고됨
- [ ] 빌드 성공이 보고됨
- [ ] 변경 파일 수가 요청 범위와 합리적으로 일치

확인 후:

| Worker 출력 | 처리 |
|-------------|------|
| `완료: ... 빌드 성공` | 성공 → 이슈 업데이트 및 close |
| `완료: ... 빌드 실패` 또는 오류 보고 | 실패 → 사용자에게 판단 요청 |
| 병렬 Worker 일부 실패 | 성공한 결과 유지, 실패 내용 보고 후 사용자 판단 |

**실패 시 AskUserQuestion**:
```
question: "Worker 실행 결과 문제가 발생했습니다:\n\n[실패 내용]\n\n진행 방향을 선택해주세요."
header: "Worker 결과"
options:
  - label: "재시도", description: "Worker를 다시 실행합니다"
  - label: "종료", description: "현재 상태로 이슈를 남깁니다"
```

#### 이슈 업데이트 (성공 시)

```bash
bd update <issue-id> \
  --description "<작업 요약: 변경 파일, 주요 변경 내용>" \
  --acceptance "<AC 체크리스트: [x] 달성 / [ ] 미달성>"
bd comments add <issue-id> "[Single] 완료" && bd close <issue-id>
```

description 예시:
```markdown
## 작업 요약
- Worker: 1개 (단일)
- 변경: auth/middleware.go, auth/middleware_test.go

## 변경 내역
- rate limiting 미들웨어 추가 (토큰 버킷 알고리즘)
- 단위 테스트 5개 추가, 전체 PASS
- 빌드 성공
```

### 결과 보고

사용자에게 간결한 결과를 보고합니다:

```markdown
완료: <issue-id>

| 항목 | 결과 |
|------|------|
| Worker | N개 |
| 변경 파일 | N개 |
| 테스트 | N개 PASS |
| 빌드 | 성공 |
| AC 달성 | N/N |

`bd show <issue-id>`
```

## 에러 핸들링

| 상황 | 처리 |
|------|------|
| 이슈 없음 | "이슈를 찾을 수 없습니다" 보고 후 종료 |
| Worker 실패 | 사용자에게 재시도/종료 선택 요청 |
| 백그라운드 Worker 무응답 | 사용자에게 상태 보고 후 판단 |
| Worker가 CONFUSION 보고 | 혼란 내용과 옵션을 사용자에게 전달, 판단 후 Worker 재실행 |

## 에이전트 호출 규칙

- 단일 Worker: `Agent(run_in_background: false)` — 포그라운드 차단 + 결과 직접 반환
- 병렬 Worker (2개 이상): `Agent(run_in_background: true)` 동시 호출 → 자동 완료 메시지 수신
- Worker에게 이슈 ID만 전달 (토큰 효율화)
- 병렬 Worker는 담당 영역을 명시

## 지금 시작하세요

위 오케스트레이션 프로세스에 따라 워크플로우를 실행합니다.
