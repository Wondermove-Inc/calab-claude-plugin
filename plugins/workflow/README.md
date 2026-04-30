# workflow 플러그인

> Discovery(대화형 탐색) → Build(구현) 분리형 멀티 에이전트 워크플로우

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/workflow:discovery` | 사용자-Claude 대화형 탐색 (라운드 무제한). 종료 시 task/epic 산출 또는 산출물 없이 종료 |
| `/workflow:build` | 단일 Worker + 리뷰어 3명 + Completion Gate (Epic/단일 task 모드) |

## 작업 흐름

```
사용자
  │
  ▼
/workflow:discovery <주제>      ──→  사용자-Claude 대화 루프 (라운드 무제한)
                                · 매 라운드 정리·명확화·옵션 제시
                                · 필요 시 architect 자동 호출 (코드 분석 보조)
                                · 사용자 종료 신호 시 Discovery Gate
  │                                    ↓
  │                              ┌─────┴──────────────────┐
  │                              ↓                        ↓
  │                       이슈 생성하고 종료          이슈 없이 종료
  │                       (architect 종합 호출)      (단순 종료, bd 기록 없음)
  │                       · 단일 Work → task 1개
  │                       · Work N개 → epic + 자식 task N개
  │
  ▼ (이슈 생성 시, 사용자가 직접 호출)
/workflow:build bd-<task-id>   ──→  단일 task 모드: 곧장 구현
/workflow:build bd-<epic-id>   ──→  Epic 하이브리드 모드 (자식 선택 → 구현)

또는 discovery 스킵:
/workflow:build <자유 텍스트>      ←── 짧은 변경은 바로 구현
```

> discovery는 **사용자 주도 대화 프로세스**입니다. 라운드 수 제한 없이 사용자가 종료할 때까지 진행하며, 결과물 없이 끝나도 정상입니다.
> 산출물 결정은 보수적 — **task가 기본**, epic은 분할이 명백한 경우에만.

## 구조

```
plugins/workflow/
├── agents/           # 5개 에이전트 (worker/architect/3×reviewer)
├── skills/           # 2개 스킬 (discovery, build)
├── guides/           # TDD, 코딩 표준, 아키텍처, Gate, beads, hooks
├── references/       # 에이전트 공통 규칙, 리뷰 체크리스트, 신뢰 수준
└── templates/        # 설계 문서 템플릿
```

## 에이전트 (총 5명)

| 에이전트 | 호출 위치 | 역할 | 모델 |
|----------|----------|------|------|
| architect | discovery | 코드 분석·작업 분할·리스크 (대화 중 자동 호출 + 종합 호출) | opus |
| worker | build | TDD 구현 | opus |
| security-reviewer | build | 보안 리뷰 (OWASP, 인증/인가) | opus |
| performance-reviewer | build | 성능 리뷰 (N+1, 메모리, I/O) | opus |
| logic-reviewer | build | 로직 + 아키텍처/SOLID 통합 리뷰 | opus |

> architect/worker는 **단발 Agent 호출** (discovery에서는 라운드 도중 반복 호출 가능), reviewer 3명은 **TeamCreate 병렬** 패턴.

## 에이전트 공통 규칙

모든 서브에이전트에 적용되는 규칙은 [`references/agent-common.md`](references/agent-common.md) 한 곳에 정의되어 있습니다:

- Anti-Rationalization 합리화 경고
- 공통 금지 사항 (이슈 임의 생성, 베이스 브랜치 직접 push 등)
- 신뢰 수준 (Trusted/Verify/Untrusted)
- 혼란 관리 프로토콜 (CONFUSION 옵션 표면화)
- 가정 표면화 (ASSUMPTIONS)
- NOTICED BUT NOT TOUCHING (범위 외 발견)
- 증거 기반 완료 검증 체크리스트

각 에이전트 파일은 역할 특화 내용만 기술합니다.

## 스킬 선택 기준

| 상황 | 스킬 | 비고 |
|------|------|------|
| 주제 탐색·문제 파악·아이데이션·설계 협의 | `/workflow:discovery <주제>` | 결과: task/epic 산출 또는 산출물 없이 종료 |
| 이슈가 이미 있고 구현만 필요 | `/workflow:build bd-<task-id>` 또는 `bd-<epic-id>` | Epic 하이브리드 모드 또는 단일 task 모드 |
| 짧은 변경 (버그 수정, 설정, 단일 모듈) | `/workflow:build <자유 텍스트>` | discovery 스킵, 즉시 구현 |
| 단순 문서·주석·오타 | 직접 수정 | 스킬 불필요 |

discovery는 사용자가 함께 깊이 탐색해야 할 주제일 때 적합합니다. 짧은 작업은 build만으로 충분합니다.
