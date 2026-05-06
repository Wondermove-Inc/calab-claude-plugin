# Quality Gate 프로세스

> discovery / build 스킬이 참조합니다. 실행 상세(AskUserQuestion 파라미터, 분기 처리)는 각 SKILL.md에 정의되어 있습니다.

## Gate 개요

워크플로우는 **discovery**(대화형 탐색)와 **build**(구현) 두 단계로 분리되며, 각 단계 종료 시점에 사용자 승인 게이트를 둡니다.

```
[discovery] 대화 루프 (라운드 무제한) → Discovery Gate → (이슈 생성 / 미생성) 종료
                                                              ↓ 이슈 생성 시
[build] Worker 실행 → 검증 → 리뷰 루프 → Completion Gate → close
```

| Gate | 검증 대상 | 시점 | 주체 | 정의 위치 |
|------|----------|------|------|----------|
| **Discovery Gate** | 산출물 분기 (이슈 생성 / 미생성 / 더 진행) | 사용자 종료 신호 시 | 메인 Claude (산출물 판단) + 사용자 (승인) | `skills/discovery/SKILL.md` 3 |
| **설계 리스크 노출** (조건부) | architect 종합 호출의 리스크 분석 | 🔴 리스크 1건 이상 | architect 응답 기반 메인 Claude 판단 | `skills/discovery/SKILL.md` 4-3 |
| **Completion Gate** | 최종 완료 검토 + user-decision | 리뷰 루프 종료 후 | 메인 Claude | `skills/build/SKILL.md` 7 |

- discovery는 사용자 주도 라운드 무제한 대화. **Discovery Gate는 종료 시점에만 한 번** 등장 (반복 대화 도중 게이트 없음)
- 산출물 미생성 종료도 정상 (단순 탐색·아이데이션·결정 보류)
- Completion Gate는 자동 통과 조건 충족 시 스킵 가능 (user-decision 0건 + 모든 리뷰 PASS + AC 1:1 충족)
- 모든 Gate는 메인 Claude가 주체. 서브에이전트(architect, worker, reviewer)는 Gate에 관여하지 않음

## 강제 중단 보장

`AskUserQuestion` 호출 후 **반드시**:
1. 즉시 메시지 종료 (추가 도구 호출/텍스트 출력 금지)
2. 사용자 응답까지 대기
3. "Other" 선택 시 입력 내용 분석하여 분기 결정

## Gate 거부/수정 시 처리

| Gate | 옵션 | 처리 |
|------|------|------|
| Discovery Gate | 이슈 생성하고 종료 | 4단계 진행 (architect 종합 호출 → task/epic 산출 → 이슈 생성) |
| Discovery Gate | 이슈 없이 종료 | 5-B 단순 종료 보고 (bd 기록 없음, 보강 모드는 comment 1줄) |
| Discovery Gate | 더 진행 | 2단계 대화 루프 복귀 (라운드 횟수 제한 없음) |
| Discovery Gate | 그래도 이슈 생성 (산출물 없음 판단 시) | 4단계 진행 (사용자가 산출물 있다고 판단) |
| 설계 리스크 노출 | 그대로 진행 | 4-4 이슈 생성으로 진행 |
| 설계 리스크 노출 | 다시 논의 | 2단계 대화 루프 복귀 |
| 설계 리스크 노출 | 이슈 없이 종료 | 5-B 단순 종료 |
| Completion Gate | 완료 (user-decision 0건 도달 후) | task close + 결과 보고. Epic 자식이면 다음 task 안내 |
| Completion Gate | user-decision 항목별 "반영" / "그래도 적용" | 결정 누적 → worker 재호출 → 4·5·6 재진행 → Gate 재진입 |
| Completion Gate | user-decision 항목별 "Worker 반려 인정" | 반려 사유 comment 기록 후 잔여 목록에서 제외 (PR 미반영) |
| Completion Gate | user-decision 항목별 "이번 PR 무시" | 사용자 사유 필수 입력 → comment 기록 후 잔여 목록에서 제외 |
| Completion Gate | 취소 | 이슈 in_progress 유지, 변경사항 수동 처리 안내 (자동 revert 없음) |

## 리뷰 이슈 처리 원칙 (이번 PR 내 전수 처리)

리뷰에서 도출된 모든 항목은 **이번 PR 안에서 종결**되어야 합니다. 미결 상태로 close하지 않습니다.

### 3-way 분류

| 분류 | 정의 | 처리 |
|------|------|------|
| **auto-fix** | 명백한 개선 (등급 무관) | Worker가 1라운드부터 전수 적용. Critical/Major/Minor/Suggestion 모두 동일 |
| **user-decision** | 트레이드오프가 명확하여 작성자만으로 판단 불가 (옵션 A/B 양자택일, 정책·범위 결정, 리뷰어 간 의견 충돌) | Completion Gate 7-2-A에서 항목별 결정 |
| **Worker 반려** | Worker가 auto-fix 시도 중 false positive·컨텍스트 부족·상충 충돌·AC 위반으로 부적절 판단한 항목 | Completion Gate 7-2-B에서 사용자가 반려 인정 / 그래도 적용 / 무시 / 취소 결정 |

| 등급 | 1라운드 | 2~3라운드 |
|------|---------|-----------|
| **Critical** | auto-fix | auto-fix (반복) |
| **Major** | auto-fix | auto-fix (반복) |
| **Minor** | auto-fix | auto-fix (반복) |
| **Suggestion** | auto-fix | auto-fix (반복) |

3라운드 초과 시 잔여 항목은 user-decision으로 자동 승격되며, **승격된 항목과 Worker 반려 항목 모두 Completion Gate 7-2에서 항목별 처리 결정이 강제**됩니다.

### Worker 반려 권한 (false positive 방지)

리뷰어 피드백이 항상 옳지는 않으므로 Worker는 false positive·컨텍스트 부족·상충 충돌·AC 위반 시 적용을 거부할 권한을 가집니다. 사유 정의·반려 보고 포맷은 [`agents/worker.md`](../agents/worker.md) §리뷰 auto-fix 모드가 정전.

반려 시 Worker는 항목ID + 근거 코드 위치를 사유에 포함해야 하며, team-lead는 이를 user-decision으로 승격하여 7-2-B에서 사용자 최종 결정에 부칩니다.

## Completion Gate의 user-decision 처리 (항목별 강제)

user-decision 잔여(원래의 트레이드오프 + Worker 반려 + 3라운드 초과 승격분)가 1건 이상이면 **항목별로** `AskUserQuestion`을 호출합니다. "보류한 채 완료"는 허용하지 않습니다.

### 7-2-A. 일반 user-decision 선택지

| 선택 | 처리 |
|------|------|
| 옵션 X 반영 | 결정 누적 → 모든 항목 결정 후 worker 재호출(6-2) → 4·5·6 재진행 → Gate 재진입 |
| 이번 PR 무시 | 사용자 자유 입력으로 사유 필수 → `[Build Gate] 무시 사유` comment 기록 → 잔여 목록에서 제외 |
| 취소 | Gate 취소 분기 (close 안 함, in_progress 유지) |

### 7-2-B. Worker 반려 항목 선택지

| 선택 | 처리 |
|------|------|
| Worker 반려 인정 | `[Build Gate] 반려 인정` comment 기록 후 잔여 목록에서 제외 (PR에 반영 안 함) |
| 그래도 적용 | 반려 사유를 무력화하는 명시 지시와 함께 worker 재호출. Gate 재진입 |
| 이번 PR 무시 | 7-2-A의 무시와 동일 처리 |
| 취소 | 7-2-A의 취소와 동일 처리 |

처리 결정은 누적 후 일괄 반영(라운드 절약). "반영" 또는 "그래도 적용" 결정이 1건 이상이면 worker 재호출 필수.

user-decision 잔여가 0건이 되면 최종 분기(`["완료" / "취소"]`)로 진입합니다. **자동 통과 조건**(user-decision 0건 + 모든 리뷰 PASS + AC 1:1 충족)에서는 Gate 전체 스킵 가능.

## 증거 기반 완료 검증

Completion Gate에서 메인 Claude는 자동 주장이 아닌 **실행 결과로** 검증합니다:

- [ ] 이슈 AC 1:1 대조 — 모든 항목 충족
- [ ] 전체 테스트 직접 실행 — PASS
- [ ] 빌드 명령 직접 실행 — 성공
- [ ] `git status` / `git diff --name-only`로 변경 파일 확인
- [ ] auto-fix 항목 전수 반영 여부 — 리뷰 라운드 결과 대조

worker의 "PASS 보고"를 그대로 신뢰하지 않고 메인 Claude가 재검증하는 이유: 에이전트 보고 신뢰성 문제(허위/착오 보고 방지).

## 이슈 라이프사이클 (discovery ↔ build 협력)

discovery 종료 분기에 따라 세 가지 경로가 있습니다.

### A. task 단일 케이스 (이슈 생성 + 단일 모듈)

| 시점 | 상태 변화 | 주체 |
|------|----------|------|
| discovery 4-4 | task 1개 생성 (open) | discovery |
| discovery 5-A | 결과 보고 + 인계 안내 | discovery |
| build 1-A | task in_progress 전환 | build |
| build 8단계 | Completion Gate 통과 후 task close | build |

### B. epic + 자식 task 케이스 (이슈 생성 + 다중 모듈)

| 시점 | 상태 변화 | 주체 |
|------|----------|------|
| discovery 4-4 | Epic 생성 (open → in_progress) + 자식 task N개 생성 (open) | discovery |
| discovery 5-A | 결과 보고 + 인계 안내 | discovery |
| build 1-A | 자식 task 1개 in_progress 전환 | build |
| build 8단계 | 자식 task close | build |
| build 8단계 후속 | 모든 자식 close 시 Epic close 사용자 확인 | build |

### C. 산출물 미생성 케이스 (이슈 없이 종료)

| 시점 | 상태 변화 | 주체 |
|------|----------|------|
| discovery 5-B | 단순 종료 보고 | discovery |
| (신규 모드) | bd 기록 없음 | — |
| (보강 모드) | epic에 `[Discovery] 보강 종료 — 산출물 없음` comment 1줄 | discovery |

**close는 항상 사용자 승인 후**. discovery/build 모두 자동 close하지 않습니다.

## comment 키 (이슈 영속 기록)

이 표가 정전(canonical)입니다. discovery/SKILL.md, build/SKILL.md의 comment 표는 사용 키만 부분 발췌하여 참조합니다.

| 단계 | 키 | 의미 |
|------|-----|------|
| discovery | `[Discovery] 보강 시작` | 1단계 보강 모드 진입 (보강 모드 한정) |
| discovery | `[Discovery] 진입` | 4-4 이슈 생성 시 (라운드 N, Work 수, 리스크 통합 기록) |
| discovery | `[Discovery] 보강 종료 — 산출물 없음` | 5-B 보강 모드에서 이슈 미생성 종료 |
| discovery | `[Discovery] build 인계` | 5-A 결과 보고 직후 |
| build | `[Build] 시작` | 진입 (Epic 자식인 경우 Epic ID 표기) |
| build | `[Build 검증]` | Worker 검증 통과 |
| build | `[Build 검증실패]` | Worker 검증 실패 (선택) |
| build | `[Build 리뷰 #N]` | 라운드별 취합 결과 (auto-fix/user-decision/reject-후보) |
| build | `[Build 리뷰 종료]` | 리뷰 루프 종료 (전부 통과 / 3라운드 초과 — Gate에서 전수 처리) |
| build | `[Build Gate] user-decision 처리` | 항목별 반영/반려 인정/무시 결정 합계 |
| build | `[Build Gate] 반려 인정` | 항목별 Worker 반려 사유 (적용 안 함 결정 시) |
| build | `[Build Gate] 무시 사유` | 항목별 사용자 명시 사유 |
| build | `[Build Gate]` | 완료 / 취소 / 자동 통과 |
| build | `[Build] 완료` | task close 직전 |
| build | `[Build] 사용자 취소` | Gate 취소 시 (close 안 함) |
| build | `[Build] Epic 완료` | Epic close 직전 (Epic 이슈 측) |
