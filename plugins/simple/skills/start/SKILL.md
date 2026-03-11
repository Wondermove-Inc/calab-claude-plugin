---
name: simple:start
description: 심플 워크플로우를 시작합니다. 이슈 또는 사용자 요청을 기반으로 Worker를 실행합니다.
disable-model-invocation: true
---

# /simple:start 커맨드

이슈 ID 또는 사용자의 자유 요청을 받아 Worker를 실행합니다.

## 사용법

```
/simple:start <issue-id>           # 기존 이슈 기반
/simple:start <자유 요청 텍스트>     # 사용자 요청 기반

예시:
/simple:start bd-abc123
/simple:start 로그인 API에 rate limiting 추가해줘
```

## 입력 판별

인자가 `bd-` 접두사로 시작하면 **이슈 모드**, 그 외는 **요청 모드**로 동작합니다.

| 모드 | 입력 형태 | 이슈 관리 |
|------|----------|----------|
| 이슈 모드 | `bd-xxx` | 기존 이슈 조회 → 업데이트 → close |
| 요청 모드 | 자유 텍스트 | 이슈 자동 생성 → 업데이트 → close |

## 핵심 원칙

1. **이슈 또는 요청**: 기존 이슈를 받거나, 자유 요청을 이슈로 변환하여 진행
2. **요구사항 명확화 우선**: 불명확한 점이 있으면 반드시 사용자에게 질문
3. **Worker만 실행**: Planner/Reviewer 없음, Gate 없음
4. **병렬 실행**: 독립 작업 단위가 있으면 Worker를 병렬 호출
5. **이슈 1개**: 이슈 하나에 모든 결과 기록
6. **TDD 필수**: Worker는 RED → GREEN → REFACTOR 사이클 준수

## 워크플로우 흐름

```
사용자: /simple:start <issue-id 또는 요청>
    ↓
┌──────────────────────────────────┐
│  1. 입력 판별 (이슈 / 요청)      │
│  2. 요구사항 확보 & 명확화        │
│  3. 병렬 여부 판단               │
│  4. Worker 호출                  │
│  5. 이슈 업데이트 & close        │
└──────────────────────────────────┘
```

## 오케스트레이션 프로세스

### 1단계: 입력 판별 및 요구사항 확보

#### A. 이슈 모드 (`bd-` 접두사)

```bash
bd show <issue-id>
bd update <issue-id> --status in_progress && bd comments add <issue-id> "[Simple] 워크플로우 시작"
```

이슈의 description과 acceptance를 분석하여:
- **작업 범위** 파악
- **요구사항 명확성** 검증
- **병렬 분해 가능 여부** 판단

#### B. 요청 모드 (자유 텍스트)

사용자 요청을 분석하여 이슈를 생성합니다:

```bash
bd create "<요청 요약>" --type task --priority 2
bd update <생성된-id> \
  --description "<사용자 요청 내용 정리>" \
  --acceptance "<요청에서 도출한 완료 조건>"
bd update <생성된-id> --status in_progress && bd comments add <생성된-id> "[Simple] 워크플로우 시작"
```

이후 이슈 모드와 동일하게 진행합니다.

### 2단계: 요구사항 명확화 (조건부)

요구사항(이슈 description/acceptance 또는 사용자 요청)을 검토하여 **아래 항목 중 하나라도 해당**하면 AskUserQuestion으로 사용자에게 질문합니다.

| 불명확 유형 | 예시 |
|------------|------|
| acceptance 없음 | 완료 조건이 정의되지 않음 |
| 모호한 요구사항 | "성능 개선", "UI 수정" 등 구체성 부족 |
| 구현 방향 복수 | 여러 접근법이 가능하여 선택 필요 |
| 영향 범위 불명확 | 어디까지 수정해야 하는지 판단 불가 |

**AskUserQuestion 호출**:
```
question: "요구사항을 확인했습니다. 아래 항목이 불명확합니다:\n\n[불명확 항목 나열]\n\n진행 방향을 선택해주세요."
header: "요구사항"
options:
  - label: "보완 후 진행", description: "불명확한 부분을 답변하여 보완합니다"
  - label: "그대로 진행", description: "현재 내용으로 최선의 판단으로 진행합니다"
```

- **"보완 후 진행"** 선택 시: 사용자 답변을 반영하여 **이슈 업데이트 후** 작업 진행
- **"그대로 진행"** 선택 시: 현재 내용 기반으로 최선의 판단으로 진행

#### 이슈 업데이트 (보완 시)

사용자 답변을 바탕으로 이슈의 description/acceptance를 보완합니다:

```bash
bd update <issue-id> \
  --description "<기존 내용 + 보완된 요구사항>" \
  --acceptance "<기존 AC + 보완된 AC>"
bd comments add <issue-id> "[Simple] 요구사항 보완 완료"
```

**보완 원칙**:
- 기존 이슈 내용을 덮어쓰지 않고 **보완/추가**
- acceptance가 없었으면 사용자 답변 기반으로 **새로 작성**
- 보완된 이슈가 Worker의 Single Source of Truth가 됨

**요구사항이 명확하면 이 단계를 건너뛰고 3단계로 진행합니다.**

### 3단계: 병렬 분해 판단

기본은 **단일 Worker 실행**입니다. 이슈의 description에 명확히 독립적인 작업 단위가 복수 존재할 때만 병렬을 고려합니다.

#### 병렬 실행 조건 (모두 충족 시)

- 서로 다른 파일/모듈을 수정
- 공유 인터페이스 없이 완전 독립
- 이슈에 독립 단위가 명시적으로 나열됨

### 4단계: Worker 호출

#### 단일 실행 (기본)

```
Task (subagent_type: simple:worker, model: sonnet, run_in_background: true):
"bd-<issue-id> 구현. bd show로 상세 확인."
```

```
TaskOutput(task_id, block: true, timeout: 600000)
```

#### 병렬 실행

각 Worker에게 **담당 영역**을 명시합니다.

```
# 병렬 Worker 호출 (최대 5개)
Task (subagent_type: simple:worker, model: sonnet, run_in_background: true):
"bd-<issue-id> 구현. 담당: <영역N 설명>. bd show로 상세 확인."
```

모든 Worker 완료 대기:
```
TaskOutput(task_id_N, block: true, timeout: 600000)
```

### 5단계: 이슈 업데이트 및 완료

모든 Worker 완료 후 이슈 필드를 업데이트합니다.

#### description (작업 결과)

```markdown
## 작업 요약
- Worker 수: N개 (단일/병렬)
- 변경 파일: N개
- 신규 파일: N개

## 변경 내역
| 파일 | 변경 내용 |
|------|----------|
| path/to/file | [변경 내용] |

(병렬 실행 시 Worker별 결과 테이블 추가)
| Worker | 담당 | 파일 | 테스트 | 빌드 |
|--------|------|------|--------|------|
| #1 | 영역1 | N개 | N PASS | 성공 |

## 테스트 결과
| 구분 | 전체 | 통과 | 실패 |
|------|------|------|------|
| 단위 테스트 | N | N | 0 |

## 빌드
- 상태: 성공
```

#### acceptance (달성 상태)

이슈의 기존 acceptance를 체크리스트로 업데이트:

```markdown
- [x] AC1: [달성한 조건]
- [x] AC2: [달성한 조건]
- [ ] AC3: [미달성 조건 — 사유]
```

#### 이슈 업데이트 명령어

```bash
bd update <issue-id> \
  --description "<작업 결과>" \
  --acceptance "<AC 달성 상태>"
bd comments add <issue-id> "[Simple] 완료" && bd close <issue-id>
```

### 결과 보고

사용자에게 간결한 결과를 보고합니다:

```markdown
완료: <issue-id>

| 항목 | 결과 |
|------|------|
| Worker | N개 (단일/병렬) |
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
| Worker 실패 | 에러 내용을 이슈 코멘트에 기록, 사용자에게 보고 |
| 병렬 Worker 일부 실패 | 성공한 Worker 결과는 유지, 실패 내용 보고 |
| timeout (10분) | 사용자에게 상태 보고 |

## 에이전트 호출 규칙

- 모든 Task 호출 시 `run_in_background: true` 사용
- Worker에게 이슈 ID만 전달 (토큰 효율화)
- 병렬 Worker는 담당 영역을 명시

## 지금 시작하세요

위 오케스트레이션 프로세스에 따라 워크플로우를 실행합니다.
