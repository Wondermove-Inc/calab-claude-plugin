# Quality Gate 프로세스

> 이 문서는 Planner 에이전트가 참조합니다.

## Gate 개요

각 단계 완료 시 사용자 승인을 요청합니다.

```
Gate 0: 계획 승인
    ↓
Gate 1: 요구사항 검증 (Interviewer 실행 시)
    ↓
Gate 2: 설계 검증 (Architect/Designer 실행 시)
    ↓
Gate 3: 최종 검증
```

## Gate 적용 원칙

**해당 단계가 실행된 경우에만 Gate 검증**

## Gate 상세

### Gate 0: 초기 계획 승인

> Epic description에 기록된 분석 내용을 기반으로 승인을 요청합니다.

```
## 워크플로우 실행 계획

Epic: <epic-id> (bd show <epic-id>로 상세 확인)

### 요약
- 유형: [새 기능 개발 / 버그 수정 / 리팩토링]
- 복잡도: [단순 / 중간 / 복잡]

### 실행 순서
(Epic description의 실행 계획 테이블 요약)

### 스킵 단계
(Epic description의 스킵 단계 요약)

옵션:
- "승인": 계획대로 진행
- "수정 필요": 피드백 반영 후 재계획
- "취소": 작업 중단
```

### Gate 1: 요구사항 검증

```
## 요구사항 스펙 검토

문서: .workflow/artifacts/{앱명}/{기능명}/spec.md

### 핵심 요구사항
1. [요구사항 1]
2. [요구사항 2]

옵션:
- "승인": 설계 단계로 진행
- "수정 필요": 요구사항 재검토
- "취소": 작업 중단
```

### Gate 2: 설계 검증

```
## 설계 문서 검토

### 산출물
- UX 시나리오: .workflow/artifacts/{앱명}/{기능명}/ux-scenario.md
- 기술 설계: .workflow/artifacts/{앱명}/{기능명}/design.md

### 주요 설계 결정
1. [결정 1]
2. [결정 2]

옵션:
- "승인": 구현 단계로 진행
- "수정 필요": 설계 재검토
- "취소": 작업 중단
```

### Gate 3: 최종 검증

```
## 최종 결과물 검토

### 구현 완료
- 변경 파일: N개
- 테스트: 통과/실패
- 리뷰: 승인/수정필요

### 커버리지 현황
| 패키지 | 커버리지 | 상태 |
|--------|----------|------|
| ... | 85% | OK |

### Reviewer 피드백
[피드백 요약]

옵션:
- "승인": 작업 완료
- "승인 + 테스트 보강": 커버리지 미달 보강
- "수정 필요": 피드백 반영
- "취소": 작업 중단
```

## 승인 거부 시 처리

| Gate | 처리 |
|------|------|
| Gate 0 | 사용자 피드백 반영하여 계획 재수립 |
| Gate 1 | Interviewer 재호출, spec.md 수정 |
| Gate 2 | Architect/Designer 재호출, 문서 수정 |
| Gate 3 | Coder 재호출, 피드백 반영 |

## 취소 시 처리

1. 진행 중인 에이전트 작업 중단
2. Epic 코멘트 추가: `[Workflow] 사용자 취소`
3. Epic 상태 업데이트: closed (사용자 취소)

---

## 세션 중단/재개 가이드

Gate 승인 대기 중 세션이 종료되거나 다른 작업을 진행해야 할 경우를 위한 가이드입니다.

### 코멘트 기록 형식

> 상세 형식 및 예시는 `agents/planner.md`의 "6단계: 진행 추적" 섹션 참조

### 세션 재개 방법

중단된 워크플로우를 재개하려면:

```
/workflow:start --resume <epic-id>
```

### 재개 지점 결정 (우선순위)

Planner는 다음 순서로 재개 지점을 결정합니다:

**1. Sub-task 상태 (주요 기준)**
```bash
bd list --parent <epic-id>
```
- `in_progress` Sub-task → 해당 에이전트부터 재개
- 모두 `open` → 처음부터 시작
- 일부 `closed` → 다음 `open` Sub-task부터

**2. 산출물 존재 여부 (스킵 판단)**
```bash
ls .workflow/artifacts/{앱명}/{기능명}/
```
- spec.md 존재 → Interviewer 스킵 가능
- design.md 존재 → Architect 스킵 가능

**3. 코멘트 상태 (보조 정보)**
```bash
bd comments <epic-id>
```
- `[Gate N] 대기중` → 해당 Gate 승인 요청부터

### 재개 불가능한 경우

다음 상황에서는 새 워크플로우를 시작하는 것을 권장합니다:
- Epic이 closed 상태인 경우
- 관련 문서나 코드가 삭제된 경우
- 요구사항이 크게 변경된 경우
