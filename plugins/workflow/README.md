# workflow 플러그인

> Single/Teams 두 가지 모드를 제공하는 멀티 에이전트 워크플로우

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/workflow:single` | 단일 Worker + 리뷰어 3명 (중/소규모) |
| `/workflow:teams` | Agent Teams (대규모/복잡) |
| `/workflow:teams --resume <epic-id>` | 중단 워크플로우 재개 |
| `/workflow:compound` | 회고 분석 |
| `/workflow:help` | 상세 도움말 |

## 구조

```
plugins/workflow/
├── agents/           # 8개 에이전트 (worker/architect/builder/3×reviewer/scribe/compound)
├── skills/           # 4개 스킬 (single, teams, help, compound)
├── guides/           # TDD, 코딩 표준, 아키텍처, Gate, beads, 비용, hooks, 재개
├── references/       # 에이전트 공통 규칙, 리뷰 체크리스트, 신뢰 수준
└── templates/        # 설계 문서 템플릿
```

## 에이전트 (총 8명)

| 에이전트 | 모드 | 역할 | 모델 |
|----------|------|------|------|
| worker | Single | TDD 구현 | opus |
| architect | Teams | 설계 전담 (아키텍처 리뷰 제외) | opus |
| builder | Teams | TDD 구현 (worktree isolation) | sonnet |
| security-reviewer | Single+Teams | 보안 리뷰 (OWASP, 인증/인가) | opus |
| performance-reviewer | Single+Teams | 성능 리뷰 (N+1, 메모리, I/O) | opus |
| logic-reviewer | Single+Teams | 로직 + 아키텍처/SOLID 통합 리뷰 | opus |
| scribe | Teams (선택) | 문서 생성 (on-demand) | sonnet |
| compound | 독립 | 회고 분석 | opus |

## 에이전트 공통 규칙

모든 구현·리뷰·설계 에이전트에 적용되는 규칙은 [`references/agent-common.md`](references/agent-common.md) 한 곳에 정의되어 있습니다:

- Anti-Rationalization 합리화 경고
- 금지 사항 (팀원 직접 지시, 이슈 생성 등)
- 신뢰 수준 (Trusted/Verify/Untrusted)
- 혼란 관리 프로토콜 (CONFUSION 옵션 표면화)
- 가정 표면화 (ASSUMPTIONS)
- NOTICED BUT NOT TOUCHING (범위 외 발견)
- 증거 기반 완료 검증 체크리스트
- SendMessage 보고 통신 규칙 (자연어)

각 에이전트 파일은 역할 특화 내용만 기술합니다.

## 모드 선택 기준

- **버그 수정·설정 변경·단일 모듈 (1~2 파일)** → `/workflow:single`
- **다중 모듈·새 기능·대규모 리팩토링 (3+ 모듈)** → `/workflow:teams`
- **단순 문서·주석·오타** → 직접 수정 (스킬 불필요)

대부분의 작업은 Single로 충분합니다. 상세 사용법은 `/workflow:help`를 참조하세요.
