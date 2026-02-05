---
name: dev:help
description: dev 플러그인의 명령어와 에이전트 사용법을 안내합니다.
user-invocable: true
---

# dev 플러그인 도움말

멀티 에이전트 오케스트레이션 시스템으로 체계적인 개발 워크플로우를 제공합니다.

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/dev:workflow <요청>` | 멀티 에이전트 워크플로우 시작 |
| `/dev:help` | 도움말 표시 |

> **참고**: 코드 리뷰와 커밋은 `/toolkit:code-review`, `/toolkit:code-commit`으로 이동했습니다.

## 에이전트 목록

| 에이전트 | 역할 | 색상 |
|----------|------|------|
| `planner` | 워크플로우 오케스트레이터, 작업 분석 및 에이전트 조율 | 파랑 |
| `interviewer` | 요구사항 명확화, 스펙 문서 작성 | 청록 |
| `architect` | 아키텍처 설계, 기술 스펙 정의 | 보라 |
| `designer` | UX/UI 디자인, shadcn/ui 활용 | 분홍 |
| `coder` | 코드 구현, 수정, 리팩토링 | 초록 |
| `tester` | 테스트 코드 작성, 커버리지 관리 | 노랑 |
| `reviewer` | 코드/설계 리뷰, 품질 평가 | 빨강 |
| `writer` | 문서 품질 검토, 일관성 보장 | 주황 |

## 코딩 가이드

`guides/language-guide.md`에서 다음 원칙들을 참조합니다:

### 공통 원칙
- **SOLID**: 단일 책임, 개방-폐쇄, 리스코프 치환, 인터페이스 분리, 의존성 역전
- **DRY/KISS**: 중복 제거, 단순함 우선
- **보안**: 입력 검증, 민감 정보 관리, 최소 권한

### 언어별 주요 원칙

| 언어 | 핵심 원칙 |
|------|-----------|
| **Go** | Accept interfaces, return structs / 작은 인터페이스 / 명시적 에러 처리 |
| **TypeScript** | strict 모드 필수 / any 금지 / 타입 가드 활용 |
| **React** | 단일 책임 컴포넌트 / Props drilling 지양 / Custom Hooks |
| **Python** | 타입 힌트 100% / Pydantic 검증 / async/await |

## 워크플로우 흐름

```
사용자 요청
    ↓
┌─────────────┐
│   Planner   │  ← 요청 분석, 계획 수립
└─────────────┘
    ↓ Gate 0: 계획 승인
┌─────────────┐
│ Interviewer │  ← 요구사항 명확화 (필수)
└─────────────┘
    ↓ Gate 1: 요구사항 검증
┌─────────────────────┐
│ Architect │ Designer│  ← 설계 (조건부)
└─────────────────────┘
    ↓ Gate 2: 설계 검증
┌─────────────────────────────┐
│ Tester → Coder → Reviewer   │  ← TDD (RED→GREEN)
└─────────────────────────────┘
    ↓ Gate 3: 최종 검증
    완료
```

## 산출물

| 단계 | 문서 | 위치 |
|------|------|------|
| 요구사항 | spec.md | `docs/{앱}/{기능}/spec.md` |
| UX 설계 | ux-scenario.md | `docs/{앱}/{기능}/ux-scenario.md` |
| 기술 설계 | design.md | `docs/{앱}/{기능}/design.md` |
| 테스트 | test.md | `docs/{앱}/{기능}/test.md` |

## 사용 예시

### 새 기능 개발
```
/dev:workflow 사용자 알림 기능 추가
```

### 버그 수정
```
/dev:workflow 로그인 실패 시 에러 메시지 표시 안됨
```

### 리팩토링
```
/dev:workflow 인증 모듈 클린 아키텍처로 리팩토링
```

## Quality Gates

각 단계 완료 시 사용자 승인을 요청합니다:

- **Gate 0**: 작업 계획 승인
- **Gate 1**: 요구사항 스펙 검증
- **Gate 2**: 설계 문서 검증
- **Gate 3**: 최종 결과물 검증

## beads 연동

모든 작업은 beads 이슈로 추적됩니다:
- Epic + Sub-task 구조
- 에이전트별 라벨 자동 지정
- 진행 상황 실시간 업데이트
