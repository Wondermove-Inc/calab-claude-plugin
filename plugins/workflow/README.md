# workflow 플러그인

> Plan → Work → Review → Compound 루프 기반 멀티 에이전트 워크플로우 (v2.0.0)

---

## 구조

```
plugins/workflow/
├── agents/           # 4개 에이전트 정의
├── guides/           # 공통 가이드
│   ├── architecture/ # 아키텍처 가이드 (Clean, Hexagonal)
│   └── ...           # 코딩, TDD, Gate
├── templates/        # 설계 문서 템플릿
└── skills/           # 스킬 (start, help, compound)
```

---

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/workflow:start <요청>` | 워크플로우 시작 (오케스트레이터) |
| `/workflow:start --resume <epic-id>` | 중단된 워크플로우 재개 |
| `/workflow:compound` | 최근 1주일 워크플로우 회고 분석 |
| `/workflow:help` | 도움말 표시 |

---

## 에이전트 목록 (3+1)

| 에이전트 | 역할 | 산출물 | 모델 | 색상 |
|----------|------|--------|------|------|
| `planner` | 요청 분석, 요구사항 명확화, 설계 | 이슈 (요구사항, 스펙, 설계) | opus | 파랑 |
| `worker` | TDD 기반 테스트 작성 + 코드 구현 | 이슈 (작업 내용, 테스트 결과), 코드 | sonnet | 초록 |
| `reviewer` | 코드/설계 리뷰, 품질 검증 | 이슈 (코드 리뷰) | opus | 빨강 |
| `compound` | 워크플로우 회고 분석 (수동 호출만) | compound.md | opus | 금색 |

### 모델 선택 기준

| 기준 | opus | sonnet |
|------|------|--------|
| 용도 | 복잡한 판단, 설계, 리뷰 | 명확한 지시에 따른 구현 |
| 에이전트 | planner, reviewer, compound | worker |

---

## 워크플로우 흐름

```
사용자 요청
    ↓
┌─────────────┐
│   Planner   │  ← 요청 분석, 이슈에 계획 작성
└─────────────┘
    ↓ Plan Gate: 계획 승인
┌─────────────┐
│   Worker    │  ← TDD (RED→GREEN→REFACTOR)
└─────────────┘
    ↓ (자동 전환)
┌─────────────┐
│  Reviewer   │  ← 코드 리뷰, 이슈에 결과 작성
└─────────────┘
    ├─ 수정필요 → Worker 재작업 ⟲ (최대 3회 자동 반복)
    └─ 승인 ↓
Completion Gate: 최종 완료 검토 (사용자 승인)
    ├─ 완료 → 워크플로우 종료
    └─ 수정 → Reviewer가 수정 계획 업데이트 → Worker 재작업 → Completion Gate 복귀
```

---

## Quality Gates (2개)

| Gate | 검증 대상 | 참조 |
|------|----------|------|
| Plan Gate | 요구사항 + 설계 | Planner 이슈 |
| Completion Gate | 코드 품질 + 최종 완료 | Reviewer 이슈 |

### 자동 반복 로직 (Worker ↔ Reviewer)
- Reviewer가 "수정필요" 판정 시 **사용자 개입 없이 자동으로** Worker 재작업
- **최대 3회** 자동 반복 후 Reviewer 승인 시 Completion Gate로 이동
- Epic 코멘트로 반복 카운터 추적: `[Workflow] Worker-Reviewer 자동 반복 (1/3)`

---

## 산출물 구조

모든 산출물은 beads 이슈에 작성됩니다:

```
Epic (Planner): 요구사항, 기능 스펙, 설계
├── Worker 이슈: 상세 작업 내용, 테스트 결과
└── Reviewer 이슈: 코드 리뷰

.workflow/
└── compound/                # 회고 분석 (compound만 파일 산출)
    └── <epic-id>.md         # Compound 분석 보고서
```

---

## beads 연동

모든 작업은 beads 이슈로 추적됩니다:

### 이슈 구조
```
Epic: [epic] 기능명
├── Sub-task: Plan (planner)
├── Sub-task: Work (worker)
└── Sub-task: Review (reviewer)
```

### 라벨 컨벤션
| 라벨 | 담당 에이전트 |
|-----|--------------|
| `plan`, `planner` | planner |
| `implementation`, `worker` | worker |
| `test` | worker |
| `review`, `reviewer` | reviewer |
| `rework` | Worker→Reviewer 재작업 |

---

## 적응적 워크플로우

작업 복잡도에 따라 필요한 단계만 실행합니다:

| 작업 유형 | 실행 흐름 |
|----------|----------|
| 복잡 기능 | Planner → Worker → Reviewer |
| 중간 작업 | Planner(간소) → Worker → Reviewer |
| 단순 버그 | Worker만 |

---

## 가이드

### 아키텍처 가이드

| 가이드 | 파일 | 설명 |
|--------|------|------|
| Clean Architecture | `guides/architecture/clean-architecture.md` | 4-레이어 구조, 의존성 규칙 |
| Hexagonal Architecture | `guides/architecture/hexagonal-architecture.md` | Port/Adapter 패턴 |
| API 설계 | `guides/architecture/api-design.md` | RESTful API 설계 원칙 |
| 데이터베이스 | `guides/architecture/database.md` | 스키마 설계 원칙 |

### 공통 가이드

| 가이드 | 파일 | 설명 |
|--------|------|------|
| 코딩 가이드 | `guides/language-guide.md` | SOLID, DRY, KISS + Go, TypeScript, React, Python |
| TDD 워크플로우 | `guides/tdd-workflow.md` | RED-GREEN-REFACTOR 사이클 |
| Quality Gate | `guides/gate-process.md` | Plan/Completion Gate 프로세스 |
| 이슈 작성 | `guides/beads-issue-guide.md` | beads 이슈 계층 구조 및 템플릿 |
