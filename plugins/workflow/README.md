# workflow 플러그인

> Single/Teams 두 가지 모드를 제공하는 멀티 에이전트 워크플로우 (v4.0.0)

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/workflow:single` | 단일 Worker (중/소규모) |
| `/workflow:teams` | Agent Teams (대규모/복잡) |
| `/workflow:compound` | 회고 분석 |
| `/workflow:help` | 상세 도움말 |

## 구조

```
plugins/workflow/
├── agents/           # 5개 에이전트 (worker, planner, team-worker, team-reviewer, compound)
├── skills/           # 4개 스킬 (single, teams, help, compound)
├── guides/           # 공통 가이드 (TDD, 코딩 표준, 아키텍처, Gate, beads)
└── templates/        # 설계 문서 템플릿
```

상세 사용법은 `/workflow:help`를 참조하세요.
