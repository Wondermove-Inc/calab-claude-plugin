---
name: workflow:help
description: workflow 플러그인의 명령어와 에이전트 사용법을 안내합니다.
allowed-tools: Read
disable-model-invocation: true
---

# workflow 플러그인 도움말

두 가지 실행 모드를 제공하는 멀티 에이전트 워크플로우입니다. 공식 Claude Code Agent Teams 위에 구축되었으며, 리뷰어 3명 체제·심각도 자동 승격·증거 기반 검증을 특징으로 합니다.

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/workflow:single <요청 또는 이슈ID>` | 단일 Worker 실행 (중/소규모 작업) |
| `/workflow:teams <요청>` | Agent Teams 실행 (대규모/복잡 작업, team-lead = 메인 Claude) |
| `/workflow:teams --resume <epic-id>` | 중단된 Teams 워크플로우 재개 |
| `/workflow:compound` | 최근 워크플로우 회고 분석 (독립 스킬) |
| `/workflow:help` | 도움말 표시 |

## 실행 모드 비교

| 모드 | 적합한 작업 | 팀 구성 |
|------|------------|---------|
| **Single** | 버그 수정, 설정 변경, 단일 모듈 (1~2 파일) | Worker 1 + reviewer 3 |
| **Teams** | 다중 모듈, 새 기능, 대규모 리팩토링 (3+ 모듈) | team-lead + architect + builder ×N + reviewer ×3 + scribe (선택) |

> **대부분의 작업은 Single로 충분합니다.** 멀티 에이전트 병렬화 비용이 단축 이득을 넘는 작업은 소수입니다. Teams 선택은 신중히.

## 에이전트 (총 8명)

| 에이전트 | 모드 | 역할 | 모델 |
|----------|------|------|------|
| `worker` | Single | TDD 구현 | opus |
| `architect` | Teams | 설계 전담 (아키텍처 리뷰 제외) | opus |
| `builder` | Teams | 구현원 (worktree, TDD, 이슈 전환) | sonnet |
| `security-reviewer` | Single+Teams | 보안 전문 리뷰 (OWASP, 인증/인가) | opus |
| `performance-reviewer` | Single+Teams | 성능 전문 리뷰 (N+1, 메모리, I/O) | opus |
| `logic-reviewer` | Single+Teams | **로직 + 아키텍처/SOLID 통합 리뷰** | opus |
| `scribe` | Teams (선택) | 문서 생성 (on-demand) | sonnet |
| `compound` | 독립 | 회고 분석 (수동 호출) | opus |

> Teams 모드에서 `team-lead` 역할은 메인 Claude가 직접 수행합니다 — 별도 에이전트 파일 없음 (`TeamCreate` 호출자가 자동 등록).

## 핵심 설계 결정

### 1. 리뷰어 3명 체제
- security + performance + logic 3명. logic-reviewer가 SOLID/레이어/인터페이스 일관성 통합 검증.
- **이유**: architect self-review 방지, 공식 권장 팀 크기(3-5명)에 부합, 리뷰 중복 제거.

### 2. 심각도 자동 승격
- 1라운드 auto-fix 이후 남은 **Minor/Suggestion**은 자동으로 user-decision 승격.
- Critical/Major만 auto-fix 루프 반복 (최대 3회).
- **이유**: 사소한 피드백 때문에 루프가 늘어나는 비용 절감.

### 3. 증거 기반 검증
- builder/worker의 "PASS 보고"를 team-lead가 직접 재실행으로 교차 검증.
- `git diff --name-only`로 보고된 파일 목록과 실제 변경 목록 대조.
- **이유**: 에이전트 보고 신뢰성 보장 (허위 보고 방지).

### 4. SendMessage 자연어 원칙
- 접두어 강제 없음. 자연어 본문.
- 다만 이슈 ID, 진행 상태, 테스트 결과, 변경 파일은 반드시 본문 포함.
- **이유**: 포멀리즘 감축, 유지보수 단순화.

## Teams 모드 핵심 개념

- **team-lead = 메인 Claude**: Discovery + 조율 + 피드백 취합 + Completion Gate 직접 수행
- **architect 설계 위임**: Plan을 architect에 위임, team-lead가 검토·확정. architect는 리뷰 미참여.
- **병렬 리뷰**: security + performance + logic 3명이 동시 리뷰
- **피드백 취합**: team-lead가 3명 피드백을 수신·중복 제거·분류 확정. 심각도 자동 승격 규칙 적용.
- **문서 생성**: on-demand (새 API/아키텍처/Breaking change 시만). 내부 리팩토링은 스킵.
- **팀 유지**: Completion Gate 수정 요청 시에도 같은 팀으로 재작업

## 사용 예시

```
/workflow:single 로그인 실패 시 에러 메시지 표시 안됨
/workflow:single bd-abc123
/workflow:teams 클러스터 알림 기능 추가
/workflow:teams --resume bd-epic-xxx
/workflow:compound
```

## 가이드 / 참조

| 문서 | 내용 |
|------|------|
| [`guides/tdd-workflow.md`](../../guides/tdd-workflow.md) | TDD 세부 규칙 |
| [`guides/coding-standards.md`](../../guides/coding-standards.md) | 코딩 표준 |
| [`guides/gate-process.md`](../../guides/gate-process.md) | Discovery/Completion Gate |
| [`guides/beads-issue-guide.md`](../../guides/beads-issue-guide.md) | beads 이슈 계층·템플릿 |
| [`guides/context-management.md`](../../guides/context-management.md) | 재개 프로세스 + 제한사항 |
| [`guides/rename-checklist.md`](../../guides/rename-checklist.md) | 리네이밍 체크리스트 |
| [`guides/hooks-integration.md`](../../guides/hooks-integration.md) | Hooks 통합 예시 |
| [`guides/architecture/`](../../guides/architecture/) | 아키텍처 참조 |
| [`references/agent-common.md`](../../references/agent-common.md) | 에이전트 공통 규칙 |
| [`references/trust-levels.md`](../../references/trust-levels.md) | 신뢰 수준 체계 |
| [`references/security-checklist.md`](../../references/security-checklist.md) | 보안 체크리스트 |
| [`references/performance-checklist.md`](../../references/performance-checklist.md) | 성능 체크리스트 |
