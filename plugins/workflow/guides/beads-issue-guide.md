# beads 이슈 작성 가이드라인

> 이 문서는 Planner 에이전트가 beads 이슈를 생성할 때 참조합니다.

## 이슈 계층 구조

```
Initiative (이니셔티브) ── --type epic --labels initiative
  ↓
Epic (에픽) ── --type epic --parent <initiative-id>
  ↓
Task (작업) / Bug (버그) ── --type task|bug --parent <epic-id>
  ↓
Sub-task (하위 작업) ── --type task --parent <task-id>
```

### 계층별 특징

| 계층 | beads 타입 | 용도 | 기간 |
|------|-----------|------|------|
| Initiative | `epic` + 라벨 `initiative` | 버전별 릴리즈 목표 | 2-6주 |
| Epic | `epic` + `--parent` | 주요 기능 단위 | 4-5주 |
| Task | `task` + `--parent` | 개발 작업 단위 | 3-10일 |
| Sub-task | `task` + `--parent` | 최소 실행 단위 | 2-8시간 |
| Bug | `bug` + `--parent` | 결함 수정 | 상황별 |

## 버전 표기 규칙

- **형식**: `YY.Q.N` (연도.분기.빌드번호)
- **예시**: `26.1.2` = 2026년 1분기 2번째 빌드

## 제목 형식

| 계층 | 형식 | 예시 |
|------|------|------|
| Initiative | `[YY.Q.N] 릴리즈 주요 목표` | `[26.1.2] Azure/GCP 멀티 클라우드 지원` |
| Epic | `[YY.Q.N][영역] 기능명` | `[26.1.2][Azure] AKS 클러스터 통합` |
| Task | `[YY.Q.N][영역] 작업 내용` | `[26.1.2][Azure] Cost Management API 연동` |
| Sub-task | `[YY.Q.N] 구체적 작업 내용` | `[26.1.2] Azure Cost API 클라이언트 구현` |
| Bug | `[YY.Q.N][영역] 버그 현상` | `[26.1.2][Azure] 비용 수집 시 타임아웃 발생` |

## 생성 명령어

### Initiative 생성
```bash
bd create "[YY.Q.N] 릴리즈 목표" \
  --type epic \
  --priority 1 \
  --labels "initiative" \
  --description "$(cat <<'EOF'
## 배경
왜 이번 릴리즈가 필요한가?

## 목적
이번 릴리즈의 핵심 목표

## 주요 업무
### 카테고리 1
* 항목 1

## 기대효과
* 정량적 목표

## 비고
* 릴리즈 일정: YY년 Q분기
* 예상 개발 기간: N주
EOF
)"
```

### Epic 생성 (일반 — Initiative 하위 Epic)

> 워크플로우(`/workflow`) 실행 시에는 이 템플릿 대신 아래 "워크플로우 Description 템플릿" 섹션을 사용합니다.

```bash
bd create "[YY.Q.N][영역] 기능명" \
  --type epic \
  --parent <initiative-id> \
  --priority 2 \
  --labels "영역라벨" \
  --description "$(cat <<'EOF'
## 개요
기능에 대한 간단한 설명

## 배경
왜 필요한가?

## 주요 내용
### Backend
* 항목

### Frontend
* 항목

## 기술 스펙
기술적 세부사항

## 일정
* Week 1: 내용
* Week 2: 내용

## 성공 지표
* 지표 1
EOF
)"
```

### Task 생성
```bash
bd create "[YY.Q.N][영역] 작업 내용" \
  --type task \
  --parent <epic-id> \
  --priority 2 \
  --labels "영역라벨,담당에이전트" \
  --description "$(cat <<'EOF'
## 개요
작업 내용 1-2줄 요약

## 변경 대상
### 1. 컴포넌트/파일
* 변경 내용

## 기술 스펙
기술적 세부사항

## 참조
관련 문서
EOF
)"
```

### Sub-task 생성
```bash
bd create "[YY.Q.N] 구체적 작업 내용" \
  --type task \
  --parent <task-id> \
  --priority 2 \
  --labels "담당에이전트" \
  --description "$(cat <<'EOF'
## 설명
구체적으로 무엇을 구현할 것인가

## Acceptance Criteria
* AC1: 조건 1
* AC2: 조건 2

## 구현 위치
파일 경로

## 참조
관련 문서
EOF
)"
```

### Bug 생성
```bash
bd create "[YY.Q.N][영역] 버그 현상" \
  --type bug \
  --parent <epic-id> \
  --priority 1 \
  --labels "영역라벨" \
  --description "$(cat <<'EOF'
## 1. 현상 (What)
무엇이 잘못되었는가?

## 2. 재현 방법 (How to Reproduce)
1. 단계 1
2. 단계 2

## 3. 예상 동작 (Expected)
정상적으로 어떻게 되어야 하는가?

## 4. 실제 동작 (Actual)
실제로 어떻게 동작하는가?

## 5. 환경 (Environment)
* 버전:
* 발생 빈도:

## 6. RCA - 5 Whys 분석
### Why 1: 왜 문제가 발생했는가?
답변

### 근본 원인 (Root Cause)
5 Whys 분석을 통해 도출된 근본 원인

## 7. 해결 방안 (Solution)
### 즉시 수정 (Immediate Fix)
지금 당장 수정할 내용

### 재발 방지 (Prevention)
근본 원인 제거를 위한 장기적 개선

## 8. 영향 범위 (Impact)
* 영향 받는 버전:
* 우선순위:
* 임시 조치 (Workaround):
EOF
)"
```

## 라벨 컨벤션

### 클라우드별 (선택)
`aws`, `azure`, `gcp`, `oci`, `ncp`, `on-premise`

### 영역별 (선택)
`backend`, `frontend`, `agent`, `infrastructure`

### 타입별 (선택)
`feature`, `improvement`, `refactoring`, `patch`, `hotfix`

### 에이전트별 (워크플로우 전용)
`interviewer`, `requirements`, `architect`, `design`, `designer`, `ui`, `ux`, `coder`, `implementation`, `tester`, `test`, `reviewer`, `review`

## 우선순위 매핑

| beads 우선순위 | 의미 | 적용 기준 |
|---------------|------|----------|
| `--priority 0` (P0) | Critical | 릴리즈 블로커, 연동 불가 |
| `--priority 1` (P1) | High | 핵심 기능 미동작 |
| `--priority 2` (P2) | Medium | 부가 기능 오류 (기본값) |
| `--priority 3` (P3) | Low | UI 개선, 문서 오타 |

## 계층 관리 명령어

```bash
# 자식 이슈 조회
bd children <parent-id>

# 트리 형태로 조회
bd list --parent <id> --tree

# 의존성 그래프 시각화
bd graph <epic-id>

# Epic 완료 상태 확인
bd epic status
```

## 상태 관리

### 워크플로우

```
open (생성) → in_progress (작업 시작) → closed (완료)
```

### 필수 규칙
- **작업 시작 시**: `bd update <id> --status in_progress`
- **작업 완료 시**: `bd close <id>`
- **블로커 발생 시**: `bd update <id> --status blocked`

## 연결 관계 규칙

- Initiative는 최상위 (부모 없음)
- Epic은 Initiative에 연결 (`--parent`), 단순/중간 작업은 독립 Epic 허용
- Task는 반드시 Epic에 연결 (`--parent`)
- Sub-task는 반드시 Task에 연결 (`--parent`)
- Bug는 Epic 또는 Task에 연결 (발생 위치에 따라)

## 워크플로우 통합: 적응적 이슈 구조

작업 복잡도에 따라 이슈 구조가 달라집니다:

### 단순 작업 (버그 수정 등)
```
Epic
└── Sub-task: coder
```

### 중간 작업
```
Epic
├── Sub-task: tester
└── Sub-task: coder
```

### 복잡 작업 (새 기능 등)
```
Epic
├── Sub-task: interviewer (requirements)
├── Sub-task: architect (design)
├── Sub-task: designer (ux) ── 선택
├── Sub-task: tester (test)
├── Sub-task: coder (implementation)
├── Sub-task: reviewer (review)
└── Sub-task: writer (docs) ── 선택
```

### Initiative 포함 대규모 작업
```
Initiative
├── Epic: [영역1] 기능A
│   ├── Task: 작업1
│   │   ├── Sub-task: 세부작업1
│   │   └── Sub-task: 세부작업2
│   └── Task: 작업2
└── Epic: [영역2] 기능B
    └── Task: 작업3
```

## 워크플로우 Description 템플릿

> Planner가 이슈를 생성할 때 반드시 아래 템플릿을 사용하여 description을 작성합니다.
> Gate 0 분석 내용을 이슈에 기록하여 작업 맥락을 보존합니다.

### 워크플로우 Epic Description

```markdown
## 요청 분석
- **원본 요청**: 사용자의 원래 요청 내용
- **작업 유형**: [새 기능 / 버그 수정 / 리팩토링 / 성능 개선 / 문서]
- **복잡도**: [단순 / 중간 / 복잡]
- **영향 범위**: 변경이 미치는 범위 (컴포넌트, 패키지, 서비스 등)

## 배경 및 목적
왜 이 작업이 필요한가? 어떤 문제를 해결하는가?

## 주요 변경 사항
### 1. [변경 영역 1]
* 구체적 변경 내용

### 2. [변경 영역 2]
* 구체적 변경 내용

## 실행 계획
| 순서 | 에이전트 | 작업 | 산출물 |
|------|---------|------|--------|
| 1 | interviewer | 요구사항 명확화 | spec.md |
| 2 | architect | 기술 설계 | design.md |
| 3 | tester | 테스트 작성 (RED) | test code |
| 4 | coder | 구현 (GREEN) | implementation |
| 5 | reviewer | 코드 리뷰 | 피드백 |

### 스킵 단계
- [에이전트명]: [스킵 사유]

## 기술 고려사항
* 기존 코드와의 호환성, 의존성, 제약 등

## 완료 조건
* AC1: 조건 1
* AC2: 조건 2
```

### 워크플로우 Sub-task Description (에이전트별)

#### Interviewer (요구사항)
```markdown
## 목표
어떤 요구사항을 명확히 해야 하는가

## 맥락
* Epic에서 파악된 배경
* 불명확한 부분, 확인이 필요한 사항

## 기대 산출물
* spec.md (요구사항 스펙)

## Acceptance Criteria
* AC1: 핵심 요구사항이 정의됨
* AC2: 비기능 요구사항이 식별됨
* AC3: 엣지 케이스가 정리됨
```

#### Architect (설계)
```markdown
## 목표
어떤 아키텍처/설계를 수립해야 하는가

## 맥락
* 요구사항 스펙 참조: spec.md
* 기존 아키텍처와의 관계

## 기대 산출물
* design.md (기술 설계)

## Acceptance Criteria
* AC1: 컴포넌트 구조가 정의됨
* AC2: API 인터페이스가 설계됨
* AC3: 기존 코드와의 통합 방안이 명시됨
```

#### Designer (UX/UI)
```markdown
## 목표
어떤 화면/인터페이스를 설계해야 하는가

## 맥락
* 요구사항 스펙 참조: spec.md
* 기존 UI 패턴

## 기대 산출물
* ux-scenario.md (UX 시나리오)

## Acceptance Criteria
* AC1: 사용자 흐름이 정의됨
* AC2: 컴포넌트 구성이 설계됨
```

#### Tester (테스트)
```markdown
## 목표
어떤 테스트를 작성해야 하는가

## 맥락
* 설계 문서 참조: design.md
* 테스트 대상 범위

## 기대 산출물
* 테스트 코드 (TDD RED 단계)

## Acceptance Criteria
* AC1: 핵심 기능에 대한 테스트 케이스가 작성됨
* AC2: 엣지 케이스 테스트가 포함됨
* AC3: 테스트가 실패 상태 (RED)
```

#### Coder (구현)
```markdown
## 목표
어떤 코드를 구현해야 하는가

## 맥락
* 설계 문서 참조: design.md
* 테스트 코드 참조 (TDD GREEN 단계)

## 구현 범위
* 변경/생성할 파일과 컴포넌트

## 기대 산출물
* 구현 코드

## Acceptance Criteria
* AC1: 모든 테스트가 통과함 (GREEN)
* AC2: 설계 문서의 인터페이스를 준수함
```

#### Reviewer (리뷰)
```markdown
## 목표
어떤 관점에서 리뷰해야 하는가

## 맥락
* 설계 문서 참조: design.md
* 구현 코드 범위

## 리뷰 포인트
* SOLID 원칙 준수
* 기존 코드 스타일 일관성
* 에러 처리, 보안

## 기대 산출물
* 리뷰 피드백

## Acceptance Criteria
* AC1: 코드 품질 검증 완료
* AC2: 설계 일관성 확인
```

#### Writer (문서)
```markdown
## 목표
어떤 문서의 품질과 일관성을 검토/정제해야 하는가

## 맥락
* 검토 대상 문서 목록
* 문서 간 상호 참조 관계

## 기대 산출물
* 정제된 문서

## Acceptance Criteria
* AC1: 문서 간 용어/표현 일관성 확보
* AC2: 상호 참조가 정확함
```
