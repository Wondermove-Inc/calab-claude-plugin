# Quality Gate 프로세스

> teams 스킬이 참조합니다. 실행 상세(AskUserQuestion 파라미터, SendMessage 포맷)는 `skills/teams/SKILL.md`에 정의되어 있습니다.

## Gate 개요

**2개의 주요 Gate + 1개 조건부 노출**로 워크플로우 품질을 관리합니다.

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
| 설계 리스크 노출 | 계속 | 그대로 2-3 (builder spawn) 진행 |
| 설계 리스크 노출 | 설계 수정 | architect에 SendMessage 재설계 요청 |
| 설계 리스크 노출 | 중단 | 전원 shutdown → `TeamDelete` + `[Workflow] 설계 리스크로 중단` + Epic close |
| Completion Gate | 수정 필요 | 메인 Claude가 사용자 결정을 분석하여 담당 builder에 재작업 요청 → 리뷰 루프 재진입. 팀 유지 |
| Completion Gate | 취소 | 전원 shutdown → `TeamDelete` + 하위 이슈 일괄 close + `[Workflow] 사용자 취소` + Epic close |

## 심각도 자동 승격 규칙

리뷰 라운드에서 발견된 항목의 처리 우선순위:

| 등급 | 1라운드 | 2~3라운드 |
|------|---------|-----------|
| **Critical** | auto-fix | auto-fix (반복) |
| **Major** | auto-fix | auto-fix (반복) |
| **Minor** | auto-fix 시도 | **자동 user-decision 승격** |
| **Suggestion** | auto-fix 시도 또는 스킵 | **자동 user-decision 승격** |

1라운드 auto-fix 반영 후에도 남은 Minor/Suggestion은 모두 Completion Gate에서 사용자 판단에 위임합니다. 3회 라운드 상한에 도달하지 않도록 루프를 단축합니다.

## Completion Gate의 user-decision 처리

3명 리뷰어의 피드백에서 team-lead가 취합한 **user-decision 목록**을 사용자에게 명시적으로 제시:

```markdown
## ⚠️ 사용자 판단 필요 항목 (user-decision)

### 리뷰어 제시 트레이드오프
1. [항목 1] — {설명} (출처: {리뷰어 이름})
   - 옵션 A: ...
   - 옵션 B: ...
   - reviewer 의견: ...

### 심각도 승격된 잔여 Minor/Suggestion
2. [Minor/승격] {설명}
   - 출처: {리뷰어}
   - 반영 권장도: 낮음 (시간/비용 vs 효과 판단 필요)
```

사용자가 옵션을 선택하면 메인 Claude는 내부 상태로 저장한 뒤, "수정 필요" 분기에서 해당 builder에 SendMessage로 지시 전달. Completion Gate "수정/완료/취소" 자체는 `AskUserQuestion` 분기이며 SendMessage가 아닙니다.

## 증거 기반 완료 검증

Completion Gate에서 team-lead는 자동 주장이 아닌 **실행 결과로** 검증합니다:

- [ ] Epic AC 1:1 대조 — 모든 항목 충족
- [ ] 통합 worktree에서 전체 테스트 직접 실행 — PASS
- [ ] 빌드 명령 직접 실행 — 성공
- [ ] `git log --oneline <base>..wf-<epic-id>` — 변경 커밋 목록 확인
- [ ] auto-fix 항목 전수 반영 여부 — 리뷰 라운드 결과 대조

builder의 "PASS 보고"를 그대로 신뢰하지 않고 team-lead가 재검증하는 이유: 에이전트 보고 신뢰성 문제 (허위/착오 보고 방지).

## 완료 / 취소 / 중단 시 처리

실행 절차(전원 shutdown → `TeamDelete` → Epic 기록·close, 취소 시 남은 하위 이슈 일괄 close)는 **`skills/teams/SKILL.md`의 4-3 (완료/취소), 2-2 (설계 리스크 중단) 섹션**에 정의되어 있습니다. 이 가이드는 정책만 정의합니다.

정책:
- Worker Task는 builder가 이미 close. 메인 Claude는 **Epic만 close**.
- 취소·중단 시에는 팀 해산 전 `bd list --parent <epic-id> --status open`으로 남은 하위 이슈를 **일괄 close**(sanity check).
- Epic comment 키: `[Workflow] 완료` / `[Workflow] 사용자 취소` / `[Workflow] 설계 리스크로 중단` 중 하나.

## 세션 중단/재개

`/workflow:teams --resume <epic-id>` — 절차 + **공식 제한사항**은 `guides/context-management.md` "재개 워크플로우" 섹션 참조.
