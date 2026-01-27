---
# 원본: claude-monitoring-main
# 적용: calab-claude-plugin v2.3.0+
name: best-practices
description: 기술별 코딩 베스트 프랙티스. TypeScript, React, Python, Go, Rust의 검증된 패턴과 안티패턴을 제공합니다.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Best Practices

기술별 코딩 베스트 프랙티스 가이드. 코드 작성 시 자동으로 적용되며, QA 검증 시 참조됩니다.

## 지원 기술

| 기술 | 파일 수 | 주요 카테고리 |
|------|--------|--------------|
| **TypeScript** | 26개 | 타입 시스템, 검증, 에러 처리, 비동기, Next.js |
| **React** | 43개 | 비동기, 번들 최적화, Server Components, 상태 관리, 리렌더링 |
| **Python** | 19개 | 타입 힌트, Pythonic, 컨텍스트 매니저, 에러 처리 |
| **Go** | 20개 | 에러 처리, 동시성, 인터페이스, 안티패턴 |
| **Rust** | 20개 | 소유권, 에러 처리, 패턴 매칭, 메모리 안전성 |

## 규칙 구조

```
rules/
├── _sections.md          # 전체 섹션 인덱스
├── _template.md          # 규칙 작성 템플릿
├── ts-*.md              # TypeScript 규칙
├── react-*.md           # React 규칙
├── py-*.md              # Python 규칙
├── go-*.md              # Go 규칙
└── rust-*.md            # Rust 규칙
```

## 규칙 파일 형식

각 규칙 파일은 다음 구조를 따릅니다:

```markdown
---
title: 규칙 제목
impact: CRITICAL | HIGH | MEDIUM | LOW
tags: [관련, 태그]
---

# 규칙 제목

## Problem
해결하려는 문제 설명

## Solution
권장 해결 방법

## Example
### Before (Bad)
잘못된 코드 예시

### After (Good)
올바른 코드 예시

## Why It Matters
이 규칙이 중요한 이유
```

## 자동 적용 시점

| 상황 | 적용되는 규칙 |
|------|-------------|
| 새 기능 구현 | 해당 기술의 전체 규칙 |
| 버그 수정 | 에러 처리, 안티패턴 규칙 |
| 코드 리뷰 | 전체 규칙 (체크리스트) |
| QA 검증 | CRITICAL, HIGH 영향도 규칙 |

## 영향도 기준

```
  영향도    설명                              예시
  ────────  ────────────────────────────────  ──────────────────────────
  CRITICAL  보안, 성능, 안정성에 심각한 영향  타입 any 남용, Goroutine 누수
  HIGH      버그 발생 가능성 높음             에러 미처리, 메모리 누수
  MEDIUM    유지보수성, 가독성 저하           네이밍 규칙, 코드 구조
  LOW       스타일, 미세 최적화               포맷팅, 미세 성능 개선
  ────────  ────────────────────────────────  ──────────────────────────
```

## 기술별 규칙 요약

### TypeScript (ts-*)

| 카테고리 | 접두사 | 설명 |
|---------|--------|------|
| Type System | ts-types-* | any 회피, 유니온, 제네릭, const assertion |
| Validation | ts-validation-* | Zod 스키마 검증 |
| Error Handling | ts-error-* | 커스텀 에러, Result 패턴 |
| Async | ts-async-* | Promise.allSettled, retry, batch |
| Next.js | ts-nextjs-* | API 라우트 타이핑 |
| Organization | ts-org-* | interface vs type, barrel exports |
| Anti-patterns | ts-anti-* | 타입 단언 남용, @ts-ignore |

### React (react-*)

| 카테고리 | 접두사 | 설명 |
|---------|--------|------|
| Async | react-async-* | Waterfall 제거, 병렬 fetch |
| Bundle | react-bundle-* | 동적 import, tree shaking |
| Server | react-server-* | RSC, 스트리밍 |
| Components | react-components-* | 컴포넌트 패턴 |
| State | react-state-* | 상태 관리, derived state |
| Re-render | react-rerender-* | useMemo, useCallback |
| Effects | react-effects-* | useEffect 최적화 |
| JS Perf | react-js-* | JavaScript 성능 |

### Python (py-*)

| 카테고리 | 접두사 | 설명 |
|---------|--------|------|
| Types | py-types-* | 타입 힌트, 제네릭, Protocol |
| Pythonic | py-pythonic-* | 컴프리헨션, 제너레이터, 언패킹 |
| Context | py-context-* | with문, 커스텀 매니저 |
| Error | py-error-* | 예외 계층, Result 패턴 |
| Anti-patterns | py-anti-* | bare except, mutable defaults |

### Go (go-*)

| 카테고리 | 접두사 | 설명 |
|---------|--------|------|
| Error | go-error-* | 명시적 반환, 래핑, defer |
| Concurrency | go-concurrency-* | goroutine, channel, context |
| Interface | go-interface-* | 작은 인터페이스, 분리 |
| Organization | go-org-* | 패키지 구조, internal |
| Anti-patterns | go-anti-* | goroutine 누수, 에러 무시 |

### Rust (rust-*)

| 카테고리 | 접두사 | 설명 |
|---------|--------|------|
| Ownership | rust-ownership-* | 소유권 이전, 빌림, 라이프타임 |
| Error | rust-error-* | Result, Option, ? 연산자 |
| Match | rust-match-* | 패턴 매칭, if let, guard |
| Memory | rust-memory-* | null 없음, 데이터 레이스 방지 |
| Anti-patterns | rust-anti-* | 불필요한 clone, unwrap 남용 |

## 사용 방법

### 특정 기술 규칙 조회

```
# TypeScript 규칙 목록
Glob: rules/ts-*.md

# React 비동기 패턴
Glob: rules/react-async-*.md

# 안티패턴 모음
Grep: "Anti-patterns" rules/
```

### 특정 영향도 규칙 조회

```
# CRITICAL 규칙만
Grep: "impact: CRITICAL" rules/

# HIGH 이상
Grep: "impact: (CRITICAL|HIGH)" rules/
```

## 기존 가이드와의 관계

| 위치 | 용도 | 상세도 |
|------|------|--------|
| `.claude/best-practices/*.md` | 일반 가이드라인 | 개요 수준 |
| `.claude/skills/best-practices/rules/*.md` | 상세 규칙 | 구체적 패턴/안티패턴 |

두 디렉토리는 상호 보완적:
- **일반 가이드**: 기술 전반의 철학과 원칙
- **상세 규칙**: 구체적인 코드 패턴과 예시

## 관련 스킬

- `code-quality`: 코드 스멜 탐지, 리팩토링 가이드
- `clean-architecture`: 레이어 분리, 의존성 규칙
- `problem-solving`: 버그 해결 방법론
