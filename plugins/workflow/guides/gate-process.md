# Quality Gate 프로세스

> 이 문서는 start 스킬(오케스트레이터)이 참조합니다.

## Gate 개요

2개의 Gate와 자동 반복 로직으로 워크플로우 품질을 관리합니다.

```
Planner → 이슈 (요구사항, 설계)
    ↓
Plan Gate: 계획 검토 (사용자 승인)
    ↓
Worker → 코드 구현
    ↓
Reviewer → 코드 리뷰
    ├─ 수정필요 → Worker 재작업 ⟲ (최대 3회 자동 반복)
    └─ 승인 ↓
Completion Gate: 최종 완료 검토 (사용자 승인)
    ├─ 완료 → 워크플로우 종료
    └─ 수정 → Reviewer가 수정 계획 업데이트 → Worker 재작업 → Completion Gate 복귀
```

## Gate 적용 원칙

**Gate는 무조건 실행하여 사용자 승인을 받아야 합니다.**
- 에이전트 스킵 여부와 관계없이 Plan Gate와 Completion Gate는 항상 실행
- Gate 없이 워크플로우가 자동 완료되는 것은 허용하지 않음

### 강제 중단 보장

Gate 텍스트를 출력한 후 **반드시 다음 규칙을 따릅니다:**
1. Gate 텍스트 출력 후 즉시 메시지를 종료 (추가 도구 호출이나 텍스트 출력 금지)
2. 사용자의 다음 메시지가 도착할 때까지 어떤 단계도 진행하지 않음
3. 사용자 응답이 "승인", "수정 필요", "완료", "취소" 중 하나에 매칭되지 않으면 재질문

## 자동 반복 로직 (Worker ↔ Reviewer)

Reviewer가 "수정필요" 판정 시 **사용자 개입 없이 자동으로** Worker 재작업을 수행합니다.

### 반복 제한
- **최대 3회** 자동 반복 (Worker → Reviewer)
- 3회 초과 시 Reviewer가 승인하더라도 Completion Gate에서 사용자에게 보고

### 반복 카운터 추적

Epic 코멘트로 추적하며, 오케스트레이터가 실시간으로 파싱합니다:

```bash
# 현재 반복 횟수 확인
iteration_count=$(bd show <epic-id> | grep -c "Worker-Reviewer 자동 반복")

# 코멘트 예시
[Workflow] Worker-Reviewer 자동 반복 (1/3)
[Workflow] Worker-Reviewer 자동 반복 (2/3)
[Workflow] Worker-Reviewer 자동 반복 (3/3) - 최대 도달
```

## Gate 상세

### Plan Gate: 계획 승인

> Planner가 작성한 이슈를 기반으로 승인을 요청합니다.

```
## Plan 검토

이슈: bd show <planner-subtask-id>

### 요약
- 유형: [새 기능 개발 / 버그 수정 / 리팩토링]
- 복잡도: [단순 / 중간 / 복잡]
- 주요 변경: [요약]

옵션:
- "승인": Worker 단계로 진행
- "수정 필요": Planner 재호출, 이슈 수정
- "취소": 작업 중단
```

### Completion Gate: 최종 완료 검토

> Reviewer가 **승인** 판정 시 사용자에게 최종 완료 검토를 요청합니다.

```
## 워크플로우 완료 검토

- Reviewer 결정: 승인
- 품질: N/10
- Critical: 0건, Major: N건
- 자동 반복: N/3회
- 리뷰 상세: bd show <reviewer-subtask-id>

옵션:
- "완료": 워크플로우 종료 및 모든 이슈 close
- "수정 필요": Reviewer가 수정 계획 업데이트 → Worker 재작업
- "취소": 작업 중단
```

#### 3회 자동 반복 도달 시 추가 옵션

자동 반복이 3/3회에 도달한 경우 Completion Gate에서 추가 옵션을 제공합니다:

```
⚠️ 자동 반복 최대 도달 (3/3회) - 품질 재검토 권장

추가 옵션:
- "완료": 현재 상태로 워크플로우 종료
- "수정 필요 (재시도)": 자동 반복 카운터를 초기화하고 Worker 재작업 (최대 3회 재시도)
- "수정 필요 (1회)": 카운터 초기화 없이 Worker 1회 재작업 후 Completion Gate 복귀
- "취소": 작업 중단
```

재시도 선택 시 Epic 코멘트 추가:
```
[Workflow] 자동 반복 카운터 초기화 (사용자 요청)
[Workflow] Worker-Reviewer 자동 반복 (1/3) - 2차 시도
```

#### 완료 선택 시
```bash
# 모든 Sub-task close
bd close <planner-subtask-id>
bd close <worker-subtask-id>
bd close <reviewer-subtask-id>

# Epic close
bd close <epic-id>
bd comments add <epic-id> "[Workflow] 완료"
```

#### 수정 필요 선택 시
1. Reviewer가 이슈 description에 **수정 계획** 작성
2. Worker Sub-task reopen → Worker 재작업
3. Reviewer 자동 리뷰
4. Reviewer 승인 시 **다시 Completion Gate 복귀**

## Gate 거부 시 처리

| Gate | 처리 |
|------|------|
| Plan Gate | Planner 재호출, 이슈 수정 |
| Completion Gate (수정) | Reviewer가 수정 계획 작성 → Worker 재작업 → Reviewer 리뷰 → Completion Gate 복귀 |

## 취소 시 처리

1. 진행 중인 에이전트 작업 중단
2. Epic 코멘트 추가: `[Workflow] 사용자 취소`
3. Epic close

## 세션 중단/재개

Gate 승인 대기 중 세션이 종료된 경우:

```
/workflow:start --resume <epic-id>
```

### 재개 지점 결정 (우선순위)

1. **Sub-task 상태** (주요 기준): `in_progress` → 해당 에이전트부터 재개
2. **Planner 이슈 상태** (스킵 판단): closed → Planner 스킵
3. **코멘트 상태** (보조 정보): `[Gate] 대기중` → 해당 Gate부터
