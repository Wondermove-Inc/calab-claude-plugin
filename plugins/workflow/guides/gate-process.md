# Quality Gate 프로세스

> 이 문서는 start 스킬(오케스트레이터)이 참조합니다.

## Gate 개요

2개의 Gate로 워크플로우 품질을 관리합니다.

```
Planner → 이슈 (요구사항, 설계)
    ↓
Plan Gate: 요구사항 + 설계 통합 검증
    ↓
Worker → 코드, 이슈 (작업 내용, 테스트 결과)
    ↓ (자동 전환)
Reviewer → 이슈 (코드 리뷰)
    ↓
Review Gate: 사용자 판단 (승인 / Worker 재작업 / Reviewer 재리뷰)
```

## Gate 적용 원칙

**해당 단계가 실행된 경우에만 Gate 검증**

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

### Review Gate: 사용자 판단

> Reviewer 완료 시 **항상** 사용자 판단을 거칩니다.

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

사용자 선택에 따라 기존 이슈를 **reopen**하여 Worker/Reviewer를 재호출하고, 완료 후 **다시 Review Gate로 복귀**합니다.
새로운 이슈를 생성하지 않으며, 재작업 이력은 이슈 코멘트로 추적합니다.

## Gate 거부 시 처리

| Gate | 처리 |
|------|------|
| Plan Gate | Planner 재호출, 이슈 수정 |
| Review Gate (Worker 재작업) | 기존 이슈 reopen → Worker → Reviewer → Review Gate 복귀 |
| Review Gate (Reviewer 재리뷰) | 기존 이슈 reopen → Reviewer → Review Gate 복귀 |

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
