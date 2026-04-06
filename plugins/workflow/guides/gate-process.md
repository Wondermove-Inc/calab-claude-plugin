# Quality Gate 프로세스

> teams 스킬이 참조합니다. 실행 상세(AskUserQuestion 파라미터, SendMessage 포맷)는 `skills/teams/SKILL.md`에 정의되어 있습니다.

## Gate 개요

**2개의 Gate**로 워크플로우 품질을 관리합니다. Plan은 architect가 설계 초안을 작성하고 team-lead(메인 Claude)가 검토·확정합니다. **설계 리스크**는 architect의 보고를 기반으로 team-lead가 판단하며, 중대 리스크 발견 시에만 사용자에게 `AskUserQuestion`을 노출합니다.

```
Discovery Gate → (Epic 생성 → 팀 spawn → architect 설계 → 설계 리스크 점검) → Completion Gate
```

| Gate | 검증 대상 | 시점 | 주체 |
|------|----------|------|------|
| **Discovery Gate** | 요점 정리 (What) | Discovery 완료 후 | 메인 Claude (= team-lead) |
| **설계 리스크 노출** (조건부) | architect의 리스크 분석 | 중대 리스크 탐지 시 | architect 보고 기반 메인 Claude 판단 |
| **Completion Gate** | 최종 완료 검토 + user-decision 판단 | 문서 생성 완료 후 | 메인 Claude |

- Discovery 스킵 시 Discovery Gate도 생략
- Gate 없이 워크플로우가 자동 완료되는 것은 허용하지 않음
- 모든 Gate는 메인 Claude가 주체. 서브에이전트는 Gate에 관여하지 않음

## 강제 중단 보장

AskUserQuestion 호출 후 **반드시**:
1. 즉시 메시지 종료 (추가 도구 호출/텍스트 출력 금지)
2. 사용자 응답까지 대기
3. "Other" 선택 시 입력 내용 분석하여 분기 결정

## Gate 거부/수정 시 처리

| Gate | 옵션 | 처리 |
|------|------|------|
| Discovery Gate | 수정 필요 | Discovery Phase 1 복귀 |
| Discovery Gate | 취소 | 즉시 종료 (Epic/팀 미존재, beads 기록 없음) |
| 설계 리스크 노출 | 계속 | 그대로 6단계 진행 |
| 설계 리스크 노출 | 설계 수정 | architect에 `[설계 수정 요청]` 재전달 후 재검증 |
| 설계 리스크 노출 | 중단 | 전원 shutdown → `TeamDelete` + `[Workflow] 설계 리스크로 중단` + Epic close |
| Completion Gate | 수정 필요 | 메인 Claude가 사용자 결정을 분석하여 해당 builder에 `[재작업 요청]` → 리뷰 루프 재진입. 팀 유지 |
| Completion Gate | 취소 | 전원 shutdown → `TeamDelete` + 하위 이슈 일괄 close + `[Workflow] 사용자 취소` + Epic close |

## Completion Gate의 user-decision 처리

4명 리뷰어의 피드백에서 team-lead가 취합한 **user-decision 목록**을 사용자에게 명시적으로 제시:

```markdown
## ⚠️ 사용자 판단 필요 항목 (user-decision)
1. [항목 1] — {설명} (출처: {리뷰어 이름})
   - 옵션 A: ...
   - 옵션 B: ...
   - reviewer 의견: ...
2. [항목 2] — ...
```

사용자가 옵션을 선택하면 메인 Claude는 내부 상태로 저장한 뒤, 수정 필요 분기에서 해당 builder에 SendMessage로 지시를 전달합니다. (Completion Gate "수정/완료/취소" 자체는 `AskUserQuestion` 분기이며 SendMessage가 아닙니다.)

## 완료 / 취소 / 중단 시 처리

실행 절차(전원 shutdown → `TeamDelete` → Epic 기록·close, 취소 시 남은 하위 이슈 일괄 close)는 **`skills/teams/SKILL.md`의 15-2(완료), 15-3(취소), 5단계(설계 리스크 중단) 섹션**에 정의되어 있습니다. 이 가이드는 정책만 정의합니다.

정책:
- Worker Task는 builder가 이미 close. 메인 Claude는 **Epic만 close**.
- 취소·중단 시에는 팀 해산 전 `bd list --parent <epic-id> --status open`으로 남은 하위 이슈를 **일괄 close**(sanity check).
- Epic comment 키는 `[Workflow] 완료` / `[Workflow] 사용자 취소` / `[Workflow] 설계 리스크로 중단` 중 하나.

## 세션 중단/재개

`/workflow:teams --resume <epic-id>` — 절차는 `guides/context-management.md` "재개 워크플로우" 섹션 참조.
