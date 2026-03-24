# Quality Gate 프로세스

> teams 스킬이 참조합니다. 실행 상세(AskUserQuestion 파라미터)는 `skills/teams/SKILL.md`에 정의되어 있습니다.

## Gate 개요

3개의 Gate로 워크플로우 품질을 관리합니다.

```
Discovery Gate → Plan Gate → (Agent Teams 실행) → Completion Gate
```

| Gate | 검증 대상 | 시점 |
|------|----------|------|
| **Discovery Gate** | 요점 정리 (What) | Discovery 완료 후 |
| **Plan Gate** | 설계 + 작업 분할 (How) | Planner 완료 후 |
| **Completion Gate** | 최종 완료 검토 | captain 완료 후 |

- Discovery 스킵 시 Discovery Gate도 생략
- Gate 없이 워크플로우가 자동 완료되는 것은 허용하지 않음

## 강제 중단 보장

AskUserQuestion 호출 후 **반드시**:
1. 즉시 메시지 종료 (추가 도구 호출/텍스트 출력 금지)
2. 사용자 응답까지 대기
3. "Other" 선택 시 입력 내용 분석하여 분기 결정

## Gate 거부/수정 시 처리

| Gate | 처리 |
|------|------|
| Discovery Gate (수정 필요) | Phase 1로 복귀 |
| Plan Gate (수정 필요) | Planner 재호출 |
| Completion Gate (수정 필요) | 같은 팀에 captain 재spawn → Completion Gate 복귀 |

## 취소 시 처리

1. 진행 중인 팀이 있으면 TeamDelete
2. Epic 코멘트: `[Workflow] 사용자 취소`
3. Epic close

## 완료 시 처리

```bash
# Sub-task close
bd close <planner-subtask-id>
bd close <worker-subtask-id>

# Epic close
bd comments add <epic-id> "[Workflow] 완료"
bd close <epic-id>
```

## 세션 중단/재개

```
/workflow:teams --resume <epic-id>
```

재개 지점: Sub-task 상태(`in_progress`) → 코멘트 상태(`[Teams] 완료`) → Planner 상태 순으로 판단
