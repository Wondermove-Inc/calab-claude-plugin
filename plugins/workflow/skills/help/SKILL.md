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
| `/workflow:teams <요청>` | Agent Teams 실행 (대규모/복잡 작업) |
| `/workflow:teams --resume <epic-id>` | 중단된 Teams 워크플로우 재개 |
| `/workflow:compound` | 최근 1주일 워크플로우 회고 분석 |
| `/workflow:help` | 도움말 표시 |

## 실행 모드

| 모드 | 적합한 작업 | 흐름 |
|------|------------|------|
| **Single** | 버그 수정, 설정 변경, 단일 모듈 | 요청 → Worker(TDD) → 완료 |
| **Teams** | 다중 모듈, 새 기능, 대규모 리팩토링 | Discovery → Planner → Agent Teams → Completion Gate |

## 에이전트

| 에이전트 | 모드 | 역할 | 모델 |
|----------|------|------|------|
| `worker` | Single | TDD 구현 | opus |
| `planner` | Teams | 설계, 작업 분할 | opus |
| `team-lead` | Teams | captain (팀 조율, 머지, 리뷰 조율) | opus |
| `team-worker` | Teams | TDD 구현 (worktree) | sonnet |
| `team-reviewer` | Teams | 통합 리뷰 | opus |
| `compound` | 공용 | 회고 분석 (수동) | opus |

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
| 아키텍처 | `guides/architecture/` |
