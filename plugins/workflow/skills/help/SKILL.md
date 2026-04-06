---
name: workflow:help
description: workflow 플러그인의 명령어와 에이전트 사용법을 안내합니다.
allowed-tools: Read
disable-model-invocation: true
---

# workflow 플러그인 도움말

두 가지 실행 모드를 제공하는 멀티 에이전트 워크플로우입니다.

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/workflow:single <요청 또는 이슈ID>` | 단일 Worker 실행 (중/소규모 작업) |
| `/workflow:teams <요청>` | Agent Teams 실행 (대규모/복잡 작업, team-lead=메인 Claude 주도) |
| `/workflow:teams --resume <epic-id>` | 중단된 Teams 워크플로우 재개 |
| `/workflow:compound` | 최근 1주일 워크플로우 회고 분석 (독립 스킬) |
| `/workflow:help` | 도움말 표시 |

## 실행 모드

| 모드 | 적합한 작업 | 흐름 |
|------|------------|------|
| **Single** | 버그 수정, 설정 변경, 단일 모듈 | 요청 → Worker(TDD) → 완료 |
| **Teams** | 다중 모듈, 새 기능, 대규모 리팩토링 | Discovery → Epic 생성 → 팀 spawn(7명) → architect 설계 → 구현·병렬 리뷰·문서 → Completion Gate |

## 에이전트

| 에이전트 | 모드 | 역할 | 모델 |
|----------|------|------|------|
| `worker` | Single | TDD 구현 | opus |
| `architect` | Teams | 설계 초안 + 아키텍처 리뷰 | opus |
| `builder` | Teams | 구현원 (worktree, TDD, 이슈 상태 전환) | sonnet |
| `security-reviewer` | Teams | 보안 전문 리뷰 (OWASP, 인증/인가) | opus |
| `performance-reviewer` | Teams | 성능 전문 리뷰 (N+1, 메모리, I/O) | opus |
| `logic-reviewer` | Teams | 로직/코드 품질 리뷰 (에러 처리, 테스트) | opus |
| `scribe` | Teams | 문서 생성 (API, 아키텍처, CHANGELOG) | sonnet |
| `compound` | 독립 | 회고 분석 (수동 호출) | opus |

> `planner` 에이전트는 수동 호출 전용입니다. 필요 시 `workflow:planner` subagent_type으로 호출하세요.
> Teams 모드에서 `team-lead` 역할은 메인 Claude가 직접 수행합니다 — 별도 에이전트 파일 없음 (프레임워크가 `TeamCreate` 호출자를 자동으로 `team-lead`로 등록).

## Teams 모드 핵심 개념

- **team-lead = 메인 Claude**: Discovery + 조율 + 피드백 취합 + Completion Gate 직접 수행
- **architect 설계 위임**: Plan을 architect에 위임, team-lead가 검토·확정
- **병렬 리뷰**: architect + security + performance + logic 4명이 동시 리뷰
- **이슈 주체**: Epic과 Worker Task는 team-lead(메인 Claude). 리뷰 피드백은 SendMessage로 보고 (이슈 미생성)
- **피드백 취합**: team-lead가 4명 피드백을 수신·중복 제거·분류 확정 후 auto-fix(최대 3회) / user-decision(Completion Gate 판단)
- **문서 생성**: 리뷰 완료 후 scribe가 `.workflow/docs/<epic-id>/`에 문서 생성
- **팀 유지**: Completion Gate 수정 요청 시에도 같은 팀으로 재작업

## 사용 예시

```
/workflow:single 로그인 실패 시 에러 메시지 표시 안됨
/workflow:single bd-abc123
/workflow:teams 클러스터 알림 기능 추가
/workflow:compound
```

## 가이드

| 가이드 | 파일 |
|--------|------|
| TDD 워크플로우 | `guides/tdd-workflow.md` |
| 코딩 표준 | `guides/coding-standards.md` |
| Quality Gate | `guides/gate-process.md` |
| beads 이슈 | `guides/beads-issue-guide.md` |
| 컨텍스트 관리 | `guides/context-management.md` |
| 리네이밍 체크리스트 | `guides/rename-checklist.md` |
| 아키텍처 | `guides/architecture/` |
