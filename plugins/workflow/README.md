# workflow 플러그인

> Single/Teams 두 가지 모드를 제공하는 멀티 에이전트 워크플로우 (v4.0.5)

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
├── agents/           # 9개 에이전트
├── skills/           # 4개 스킬 (single, teams, help, compound)
├── guides/           # 공통 가이드 (TDD, 코딩 표준, 아키텍처, Gate, beads)
├── references/       # 리뷰 체크리스트 (보안, 성능, 신뢰 수준)
└── templates/        # 설계 문서 템플릿
```

## 에이전트

| 에이전트 | 모드 | 역할 | MCP 도구 |
|----------|------|------|----------|
| worker | Single | TDD 구현 | Serena, graph |
| architect | Teams | 설계 + 아키텍처 리뷰 | Serena, graph |
| builder | Teams | TDD 구현 (worktree isolation) | Serena, graph |
| security-reviewer | Teams | 보안 리뷰 (OWASP, 인증/인가) | Serena, graph |
| performance-reviewer | Teams | 성능 리뷰 (N+1, 메모리, I/O) | Serena, graph |
| logic-reviewer | Teams | 로직/품질 리뷰 (에러 처리, 테스트) | Serena, graph |
| scribe | Teams | 문서 생성 (API, 아키텍처, CHANGELOG) | Serena |
| compound | 독립 | 회고 분석 | Serena |

## 에이전트 행동 패턴

모든 구현 에이전트(worker, builder)에 적용:

- **Anti-Rationalization**: 단계 스킵 합리화를 테이블로 방지
- **가정 표면화**: 구현 전 암묵적 가정을 명시적으로 나열
- **NOTICED BUT NOT TOUCHING**: 범위 외 발견사항을 기록만 하고 수정하지 않음
- **혼란 관리**: 스펙과 코드 충돌 시 임의 결정 금지, 옵션 표면화
- **신뢰 수준 체계**: Trusted/Verify/Untrusted 소스 구분
- **완료 검증 체크리스트**: 증거 기반 검증 (AC 대조, 테스트 결과, 빌드 확인)

상세 사용법은 `/workflow:help`를 참조하세요.
