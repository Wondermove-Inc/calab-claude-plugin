---
name: workflow:help
description: workflow 플러그인의 명령어와 에이전트 사용법을 안내합니다.
allowed-tools: Read
disable-model-invocation: true
---

# workflow 플러그인 도움말

Plan → Work → Review → Compound 루프 기반 멀티 에이전트 워크플로우입니다.

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/workflow:start <요청>` | 워크플로우 시작 (오케스트레이터) |
| `/workflow:start --resume <epic-id>` | 중단된 워크플로우 재개 |
| `/workflow:compound` | 최근 1주일 워크플로우 회고 분석 및 복리화 |
| `/workflow:help` | 도움말 표시 |

## 에이전트 목록 (3+1)

| 에이전트 | 역할 | 산출물 | 모델 | 색상 |
|----------|------|--------|------|------|
| `planner` | 요청 분석, 요구사항 명확화, 설계 | 이슈 (요구사항, 스펙, 설계) | opus | 파랑 |
| `worker` | TDD 기반 테스트 작성 + 코드 구현 | 이슈 (작업 내용, 테스트 결과), 코드 | sonnet | 초록 |
| `reviewer` | 코드/설계 리뷰, 품질 검증 | 이슈 (코드 리뷰) | opus | 빨강 |
| `compound` | 워크플로우 회고 분석 (수동 호출만) | compound.md | opus | 금색 |

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
    ├─ 수정필요 → Worker 재작업 ⟲ (최대 3회 자동)
    └─ 승인 ↓
    Completion Gate: 최종 완료 검토 (사용자 승인)
    ├─ 완료 → 워크플로우 종료
    └─ 수정 → Reviewer 수정 계획 → Worker 재작업
```

## Quality Gates (2개)

| Gate | 검증 대상 | 시점 |
|------|----------|------|
| Plan Gate | 요구사항 + 설계 (Planner 이슈) | Planner 완료 후 |
| Completion Gate | 최종 완료 검토 (Reviewer 승인 후) | Reviewer 승인 시 |

**자동 반복 로직**: Reviewer 수정필요 시 Worker 자동 재작업 (최대 3회, 사용자 개입 없음)

## 산출물

모든 산출물은 beads 이슈에 작성됩니다:

```
Epic (Planner): 요구사항, 기능 스펙, 설계
├── Worker 이슈: 상세 작업 내용, 테스트 결과
└── Reviewer 이슈: 코드 리뷰
```

## 사용 예시

### 새 기능 개발
```
/workflow:start 사용자 알림 기능 추가
```
Planner(이슈) → Plan Gate → Worker(TDD) → Reviewer(이슈) ⟲ (자동 반복 최대 3회) → Completion Gate → 완료

### 버그 수정
```
/workflow:start 로그인 실패 시 에러 메시지 표시 안됨
```
Planner(간소) → Worker(TDD) → Reviewer → 완료

### 리팩토링
```
/workflow:start 인증 모듈 클린 아키텍처로 리팩토링
```
Planner(설계 포함) → Worker(TDD) → Reviewer → 완료

### 워크플로우 회고
```
/workflow:compound
```
최근 1주일 워크플로우 전체 분석 → compound.md

## 코딩 가이드

`guides/language-guide.md`에서 다음 원칙들을 참조합니다:

| 언어 | 핵심 원칙 |
|------|-----------|
| **Go** | Accept interfaces, return structs / 작은 인터페이스 / 명시적 에러 처리 |
| **TypeScript** | strict 모드 필수 / any 금지 / 타입 가드 활용 |
| **React** | 단일 책임 컴포넌트 / Props drilling 지양 / Custom Hooks |
| **Python** | 타입 힌트 100% / Pydantic 검증 / async/await |

## beads 이슈 관리

상세 가이드는 `guides/beads-issue-guide.md`를 참조하세요.
- `/workflow:start` 실행 시 자동으로 Epic + Sub-task 생성
- 에이전트별 라벨 자동 지정
- 진행 상황 실시간 업데이트
