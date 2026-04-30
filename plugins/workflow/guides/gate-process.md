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
| Completion Gate | 완료 | task close + 결과 보고. Epic 자식이면 다음 task 안내 |
| Completion Gate | 수정 필요 | 사용자 결정에 따라 Worker 재호출 → 4·5·6 재진행 → Gate 재진입 |
| Completion Gate | 취소 | 이슈 in_progress 유지, 변경사항 수동 처리 안내 (자동 revert 없음) |

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

3명 리뷰어의 피드백에서 메인 Claude가 취합한 **user-decision 목록**을 사용자에게 명시적으로 제시:

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

사용자가 옵션을 선택하면 메인 Claude는 결과를 메모리로 저장한 뒤 "수정 필요" 분기에서 worker 재호출(6-2 패턴)에 반영. Completion Gate "완료/수정 필요/취소" 자체는 `AskUserQuestion` 분기입니다.

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
| build | `[Build 리뷰 #N]` | 라운드별 취합 결과 |
| build | `[Build 리뷰 종료]` | 리뷰 루프 종료 (전부 통과 / 3라운드 초과) |
| build | `[Build Gate]` | 완료 / 수정 필요 / 취소 / 자동 통과 |
| build | `[Build] 완료` | task close 직전 |
| build | `[Build] 사용자 취소` | Gate 취소 시 (close 안 함) |
| build | `[Build] Epic 완료` | Epic close 직전 (Epic 이슈 측) |
