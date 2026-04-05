# beads 이슈 작성 가이드라인

> teams 워크플로우에서 이슈를 생성할 때 참조합니다. team-lead(메인 Claude)가 전 생명주기를 소유하는 구조에서의 이슈 계층을 정의합니다.

## 워크플로우 이슈 계층

```
Epic (team-lead / 메인 Claude 생성)
├── Worker Task #1 (team-lead 생성, team-worker-1에 할당)
├── Worker Task #2 (team-lead 생성, team-worker-2에 할당)
├── ...
├── Review Task #1 (team-reviewer 생성, 리뷰 라운드 #1)
├── Review Task #2 (team-reviewer 생성, 리뷰 라운드 #2, auto-fix 루프 시)
└── ...
```

### 이슈 주체 매트릭스

| 이슈 | 생성 주체 | 상태 전환 | close 주체 |
|------|----------|----------|-----------|
| **Epic** | team-lead (메인 Claude, 2단계) | open → closed | team-lead (Completion Gate 최종 승인) |
| **Worker Task** | team-lead (Plan 후 6단계) | open → in_progress(worker) → closed(worker) | team-worker (작업 완료 시) |
| **Review Task** | team-reviewer (리뷰 시작 시, 라운드마다) | open → closed | team-reviewer (변경점 확인 후) |

Plan은 team-lead가 직접 수행하며, 결과는 Epic description과 Worker Task description에 분산 기록됩니다. 별도 Plan 이슈는 생성하지 않습니다.

## 버전 표기 규칙

- **형식**: `YY.Q.N` (연도.분기.빌드번호)
- **예시**: `26.2.1` = 2026년 2분기 1번째 빌드

## 제목 형식

| 이슈 | 형식 | 예시 |
|------|------|------|
| Epic | `[YY.Q.N][영역] 기능명` | `[26.2.1][Azure] AKS 클러스터 통합` |
| Worker Task | `Work #N: {담당 모듈}` | `Work #1: 도메인 모델` |
| Review Task | `Review #<라운드>: {기능명}` | `Review #1: AKS 클러스터 통합` |

## Epic 생성 (team-lead / 메인 Claude가 2단계에서 수행)

```bash
bd create "[YY.Q.N][영역] 기능명" \
  --type epic \
  --priority 2 \
  --description "$(cat <<'EOF'
## 요청 분석
- **원본 요청**: {사용자 요청}
- **작업 유형**: [새 기능 / 버그 수정 / 리팩토링 / 성능 개선 / 문서]
- **복잡도**: [단순 / 중간 / 복잡]

## Discovery 요약
{Phase 3 요약 전문 — Discovery 스킵 시 "Discovery 스킵 (요청이 충분히 구체적)"}

## 실행 구조
- team-lead: Discovery + Plan + 이슈 생성 + 조율 + 리뷰 루프 + Completion Gate (전 생명주기 소유)
- team-worker ×N: 할당받은 Worker Task 수행 (worktree isolation, TDD)
- team-reviewer: Review Task 생성·관리, 피드백 분류, 변경점 확인 후 close
EOF
)" \
  --acceptance "$(cat <<'EOF'
- [ ] AC1: 조건 1
- [ ] AC2: 조건 2
EOF
)"
```

> **필드 구성**: Epic은 `--description`과 `--acceptance`만 사용합니다. 설계 내용은 team-lead가 Worker Task description에 분산 기록합니다.

## Worker Task 생성 (team-lead / 메인 Claude가 Plan 후 수행)

워커 1명당 1개 생성. team-lead가 플랜 결과에 따라 분할합니다.

```bash
bd create "Work #<N>: {담당 모듈}" \
  --parent <epic-id> \
  --type task \
  --priority 2 \
  --labels "implementation,worker,teams" \
  --description "$(cat <<'EOF'
## 담당
- 워커: team-worker-<N>
- 모듈/파일: {파일 경로 목록}

## 작업 내용
{구체적 구현 범위}

## 설계 참조
{아키텍처, 인터페이스 정의, 데이터 흐름 — Mermaid 다이어그램 포함 가능}

## 의존성
- 선행 작업: {다른 Worker Task ID 또는 "없음"}
- 공유 인터페이스: {타입/포트 정의}

## TDD 계획
| 단계 | 대상 | 유형 |
|------|------|-----|
| RED | ... | 단위/통합 |
| GREEN | ... | - |

## 파일 경계
- 수정 허용: {파일 목록}
- 읽기 전용: {파일 목록}
EOF
)" \
  --acceptance "$(cat <<'EOF'
- [ ] 테스트 통과
- [ ] 빌드 성공
- [ ] 담당 파일 경계 준수
- [ ] AC1: ...
EOF
)"
```

의존성이 있는 경우:
```bash
bd update <worker-task-id> --blocked-by <dependency-task-id>
```

## Worker Task 완료 기록 (team-worker가 수행)

작업 완료 시 comment로 결과를 기록하고 close합니다.

```bash
bd comments add <worker-task-id> "$(cat <<'EOF'
## [team-worker-N] 작업 완료

### 변경 내역
| 파일 | 변경 내용 |
|------|----------|
| ... | ... |

### 테스트 결과
- 단위 테스트: PASS (N건)
- 커버리지: ...

### Worktree
- 브랜치: {branch-name}
- 경로: {worktree-path}
EOF
)"

bd close <worker-task-id>
```

## Review Task 생성 (team-reviewer가 리뷰 라운드마다 수행)

```bash
bd create "Review #<라운드>: {기능명}" \
  --parent <epic-id> \
  --type task \
  --priority 2 \
  --labels "review,reviewer,teams" \
  --description "$(cat <<'EOF'
## 리뷰 범위
- 라운드: #<N>
- 반영된 파일: {목록}
- 연관 Worker Task: bd-<task-id-1>, bd-<task-id-2>

## 체크 항목
- [ ] 아키텍처 (SOLID, 의존성 방향)
- [ ] 통합 (인터페이스 일관성, 모듈 경계)
- [ ] 코드 품질 (보안, 성능, 에러 처리)
- [ ] 테스트 (커버리지, 경계값)
- [ ] 문서/리네이밍 (해당 시)
EOF
)"
```

### Review Task 피드백 기록 (comment)

피드백은 auto-fix / user-decision으로 분류되어 comment에 기록됩니다:

```bash
bd comments add <review-task-id> "$(cat <<'EOF'
## [피드백 - 라운드 #N]

### auto-fix (N건)
1. [Critical] path/to/file:42 — {설명} → 담당: team-worker-1
2. [Major] path/to/file:78 — {설명} → 담당: team-worker-2
3. [Minor] path/to/file:103 — {설명} → 담당: team-worker-1

### user-decision (N건)
1. [Major] path/to/file:55 — {설명}
   - 옵션 A: ...
   - 옵션 B: ...
   - 내 의견: 옵션 A 권장 (이유: ...)
EOF
)"
```

### Review Task close (team-reviewer가 수행)

```bash
bd comments add <review-task-id> "$(cat <<'EOF'
## [최종 확인 완료]
- auto-fix: N건 전부 반영
- user-decision: N건 보류 (Completion Gate 판단)
- 변경점 최종 확인: ✅
- 추가 이슈 없음
EOF
)"

bd close <review-task-id>
```

## 피드백 분류 기준

| 분류 | 조건 | 예시 |
|------|------|------|
| **auto-fix** | 객관적 기준 위반, 답이 하나 | SOLID 위반, 타입 오류, 의존성 역전, null check, 커버리지 부족, 네이밍 컨벤션 |
| **user-decision** | 트레이드오프, 사용자 선호 개입 | 스코프 변경, 설계 방향, 성능 vs 가독성, API 이름, 기능 추가 제안 |

분류는 **team-reviewer가 draft → team-lead와 협의 → 확정**의 순서로 진행됩니다.

## 심각도 등급 (분류와 별개)

| 등급 | 의미 |
|------|------|
| Critical | 아키텍처 위반, 로직 오류 |
| Major | SOLID 위반, 설계 불일치 |
| Minor | 패턴/네이밍 일관성 |
| Suggestion | 개선 제안 |

## 라벨 컨벤션

### 영역별 (선택)
`backend`, `frontend`, `agent`, `infrastructure`

### 타입별 (선택)
`feature`, `improvement`, `refactoring`, `patch`, `hotfix`

### 워크플로우 역할별
- `implementation,worker,teams` (Worker Task)
- `review,reviewer,teams` (Review Task)

## 우선순위 매핑

| 우선순위 | 의미 | 적용 기준 |
|---------|------|----------|
| `--priority 0` (P0) | Critical | 릴리즈 블로커 |
| `--priority 1` (P1) | High | 핵심 기능 미동작 |
| `--priority 2` (P2) | Medium | 기본값 |
| `--priority 3` (P3) | Low | UI 개선, 문서 오타 |

## 상태 관리

### 상태 흐름

```
Epic:         open → (team-lead 작업 중) → closed (Completion Gate 최종 승인)

Worker Task:  open → in_progress (worker 시작) → closed (worker 완료)
              ↑                                    │
              └────── 재작업 (리뷰 피드백) ─────────┘
              (bd update <id> --status in_progress)

Review Task:  open → closed (reviewer 변경점 확인 후) | (승격 close — 3회 루프 초과)
              ※ 라운드마다 새 Review Task 생성 (재open하지 않음)
```

### 재작업 경로 (Worker Task)

리뷰 피드백 반영 시 closed → in_progress로 직접 전환합니다. beads는 `bd update <id> --status in_progress`로 closed 이슈를 다시 진행 상태로 되돌리는 것을 지원합니다.

### Epic 코멘트 키

| 키 | 시점 | 주체 |
|----|------|------|
| `[Workflow] 시작` | Epic 생성 직후 | team-lead |
| `[Workflow] 완료` | 최종 승인 직전 Epic close | team-lead |
| `[Workflow] 사용자 취소` | 사용자 취소 시 | team-lead |
| `[Workflow] 설계 리스크로 중단` | 설계 리스크 중단 시 | team-lead |

### 필수 규칙

- **team-worker**: 작업 시작 시 `bd update <id> --status in_progress`, 완료 시 `bd close <id>`. 재작업 시 동일 명령으로 재open.
- **team-reviewer**: 리뷰 라운드마다 새 Review Task 생성. 라운드 #2 이상이면 description에 `이전 라운드: bd-<prev-id>` 필수 기록.
- **team-lead**: Worker Task 생성·할당만 수행. Worker Task 상태 전환은 워커에 위임. Epic은 Completion Gate 최종 승인/취소/설계 리스크 중단 시에만 close. 취소 시 `bd list --parent <epic-id> --status open`으로 남은 하위 이슈를 일괄 close.

## 계층 관리 명령어

```bash
# 자식 이슈 조회
bd children <epic-id>

# 트리 형태로 조회
bd list --parent <epic-id> --tree

# 의존성 그래프 시각화
bd graph <epic-id>

# Epic 완료 상태 확인
bd epic status
```

## 참조

- `skills/teams/SKILL.md`: 전체 워크플로우 오케스트레이션 (team-lead = 메인 Claude가 주도)
- `agents/team-worker.md`: 구현 + 이슈 상태 전환
- `agents/team-reviewer.md`: Review Task 소유·관리
- `guides/context-management.md`: 이슈 기반 컨텍스트 관리
- `guides/gate-process.md`: Discovery Gate + Completion Gate
