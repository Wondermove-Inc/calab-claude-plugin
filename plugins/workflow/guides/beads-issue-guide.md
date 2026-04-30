# beads 이슈 작성 가이드라인

> discovery / build 워크플로우에서 이슈를 생성할 때 참조합니다. 메인 Claude가 discovery(설계)과 build(구현) 단계의 오케스트레이터로 동작하며, 두 스킬이 bd 이슈로 인계됩니다.

## 워크플로우 이슈 계층

discovery는 작업 사이즈에 따라 두 가지 산출물 형태 중 하나를 만듭니다 (보수적 판단, 기본은 task).

### A. task 단일 (단일 모듈, 단일 책임)

```
Task (discovery 5단계 생성, build가 in_progress 전환·close)
```

### B. epic + 자식 task (다중 모듈, 분할 명백)

```
Epic (discovery 메인 Claude 생성, 또는 사용자가 보강 모드로 전달)
├── Task #1 (discovery 5단계 생성, build가 in_progress 전환·close)
├── Task #2
├── ...
└── Task #N
```

> 리뷰 피드백은 이슈로 관리하지 않습니다. reviewer들의 피드백은 SendMessage로 메인 Claude에 직접 보고하고, build 메인 Claude가 task comment에 주요 사항을 기록합니다.

### 이슈 주체 매트릭스

| 이슈 | 생성 주체 | 상태 전환 | close 주체 |
|------|----------|----------|-----------|
| **단일 Task (task 단일 케이스)** | discovery 메인 Claude (5단계) | open → in_progress(build, 1-A) → closed(build, 8단계) | build 메인 Claude (Completion Gate 통과 후) |
| **Epic** | discovery 메인 Claude (5단계) 또는 사용자 전달 | open → in_progress(discovery, 5단계) → closed(build) | build 메인 Claude (모든 자식 close 후 사용자 승인 시) |
| **자식 Task (epic 케이스)** | discovery 메인 Claude (5단계) | open → in_progress(build, 1-A) → closed(build, 8단계) | build 메인 Claude (Completion Gate 통과 후) |

Discovery는 architect가 단발 Agent 호출로 설계 초안을 반환하면, discovery 메인 Claude가 검토·확정한 뒤 5단계에서 산출물 형태(task 단일 vs epic+task)를 결정합니다. 별도 Discovery 이슈는 생성하지 않으며, **단일 Work + 단일 모듈 + 의존성 없음이면 task 1개**, 그 외(Work 2개 이상 / 다중 모듈)는 epic + 자식 task 계층을 만듭니다.

## 버전 표기 규칙

- **형식**: `YY.Q.N` (연도.분기.빌드번호)
- **예시**: `26.2.1` = 2026년 2분기 1번째 빌드

## 제목 형식

| 이슈 | 형식 | 예시 |
|------|------|------|
| Epic | `[YY.Q.N][영역] 기능명` | `[26.2.1][Azure] AKS 클러스터 통합` |
| Task (epic 자식) | `Work #N: {담당 모듈}` | `Work #1: 도메인 모델` |

## Epic 생성 (discovery 메인 Claude가 5단계에서 수행)

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
{Discovery 요점 — 스킵 시 "Discovery 스킵 (요청이 충분히 구체적)"}

## 실행 구조
- discovery 메인 Claude: Discovery + architect 호출 + Discovery Gate (설계 단계)
- architect: 설계 + 작업 분할 + 리스크 (단발 Agent 호출)
- build 메인 Claude: Worker 호출 + 검증 + 리뷰 취합 + Completion Gate (구현 단계)
- worker: TDD 구현 (단발 Agent 호출)
- security/performance/logic-reviewer: 병렬 리뷰 (TeamCreate)
EOF
)" \
  --acceptance "$(cat <<'EOF'
- [ ] AC1: 조건 1
- [ ] AC2: 조건 2
EOF
)"
```

> **필드 구성**: Epic은 `--description`과 `--acceptance`만 사용합니다. 설계 내용은 architect가 작성하고 discovery 메인 Claude가 task description에 분산 기록합니다.

## task 생성 (discovery 메인 Claude가 5단계에서 수행)

architect의 작업 분할 draft에 따라 Work 1개당 task 1개 생성. open 상태로 유지 (in_progress 전환은 build가 수행).

```bash
bd create "Work #<N>: {담당 모듈}" \
  --parent <epic-id> \
  --type task \
  --priority 2 \
  --labels "build,worker" \
  --description "$(cat <<'EOF'
## 담당
- 모듈/파일: {파일 경로 목록}

## 작업 내용
{구체적 구현 범위}

## 설계 참조
{아키텍처, 인터페이스 정의, 데이터 흐름 — Mermaid 다이어그램 포함 가능}

## 의존성
- 선행 작업: {다른 task ID 또는 "없음"}
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

## task 완료 기록 (build 메인 Claude가 8단계에서 수행)

build 메인 Claude가 Completion Gate 통과 후 close합니다. worker는 close 권한 없음.

```bash
bd comments add <worker-task-id> "$(cat <<'EOF'
## [Build] 완료

### 변경 내역
| 파일 | 변경 내용 |
|------|----------|
| ... | ... |

### 테스트 결과
- 단위 테스트: PASS (N건)
- 빌드: 성공
- 리뷰 라운드: N회

### Gate
- 사용자 승인 (또는 자동 통과)
EOF
)"

bd close <worker-task-id>
```

## 피드백 분류 기준

| 분류 | 조건 | 예시 |
|------|------|------|
| **auto-fix** | 객관적 기준 위반, 답이 하나 | SOLID 위반, 타입 오류, 의존성 역전, null check, 커버리지 부족, 네이밍 컨벤션, 보안 취약점, N+1 쿼리 |
| **user-decision** | 트레이드오프, 사용자 선호 개입 | 스코프 변경, 설계 방향, 성능 vs 가독성, API 이름, 기능 추가 제안, 보안-편의성 균형 |

분류는 **build 메인 Claude가 3명 reviewer(security/performance/logic)의 피드백을 취합 후 직접 확정**합니다.

심각도 자동 승격 규칙(1라운드 후 Minor/Suggestion → user-decision)은 [`gate-process.md`](gate-process.md) §심각도 자동 승격 규칙 참조.

## 심각도 등급 (분류와 별개)

| 등급 | 의미 |
|------|------|
| Critical | 아키텍처 위반, 로직 오류, 즉시 악용 가능 취약점, 프로덕션 장애 유발 |
| Major | SOLID 위반, 설계 불일치, N+1 쿼리, 에러 처리 누락 |
| Minor | 패턴/네이밍 일관성, 최적화 기회 |
| Suggestion | 개선 제안, 모범 사례 |

## 라벨 컨벤션

### 영역별 (선택)
`backend`, `frontend`, `agent`, `infrastructure`

### 타입별 (선택)
`feature`, `improvement`, `refactoring`, `patch`, `hotfix`

### 워크플로우 역할별
- `build,worker` (task 라벨)

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
Epic/기존 티켓:  → in_progress (discovery, 5단계) → closed (build, 모든 자식 close 후 사용자 승인)

Task:            open(discovery 5단계) → in_progress (build 1-A) → closed (build 8단계)
              ↑                                              │
              └───────────────── 재작업 (리뷰 피드백) ─────────┘
              (bd update <id> --status in_progress)
```

### 재작업 경로 (task)

리뷰 피드백 반영 시 closed → in_progress로 직접 전환합니다. beads는 `bd update <id> --status in_progress`로 closed 이슈를 다시 진행 상태로 되돌리는 것을 지원합니다. 다만 build 워크플로우는 일반적으로 close 전에 Completion Gate에서 모든 피드백을 반영하므로 재open은 사용자 결정에 따른 예외 경로입니다.

### 코멘트 키

전체 키 목록과 시점 정의는 [`gate-process.md`](gate-process.md) §comment 키를 정전(canonical)으로 참조합니다. 요약: `[Discovery] 진입` / `[Discovery Gate]` / `[Discovery] build 인계` / `[Build] 시작` / `[Build 검증]` / `[Build 리뷰 #N]` / `[Build Gate]` / `[Build] 완료` / `[Build] Epic 완료`.

### 필수 규칙

- **build 메인 Claude**: task의 in_progress 전환·close, Epic의 close 모두 build가 수행. worker는 코드 변경만 담당하고 이슈 상태 전환 권한 없음.
- **discovery 메인 Claude**: Epic 생성·in_progress 전환, task 생성(open). 자체적으로 close하지 않음 (예외: 설계 리스크 중단 시 Epic close).
- **취소 시**: `bd list --parent <epic-id> --status open`으로 남은 하위 이슈를 일괄 close하기 전에 사용자에게 확인.

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

- `skills/discovery/SKILL.md`: Discovery + 설계 + 작업 분할 (task 또는 epic+task 생성)
- `skills/build/SKILL.md`: 단일 Worker 구현 + 리뷰 + Completion Gate
- `agents/architect.md`: 설계 전담 (discovery 단발 호출)
- `agents/worker.md`: TDD 구현 (build 단발 호출)
- `agents/security-reviewer.md`: 보안 전문 리뷰
- `agents/performance-reviewer.md`: 성능 전문 리뷰
- `agents/logic-reviewer.md`: 로직 + 아키텍처/SOLID 통합 리뷰
- `references/agent-common.md`: 에이전트 공통 규칙
- `guides/gate-process.md`: Discovery / Completion Gate 정책
