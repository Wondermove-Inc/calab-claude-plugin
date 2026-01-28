# Best Practices Sections

> **버전**: calab-claude-plugin v2.4.0+
> **총 파일**: 147개

---

## 폴더 구조

```
skills/best-practices/references/
├── _sections.md          # 이 파일 - 전체 섹션 정의
├── _template.md          # 새 규칙 템플릿
│
├── typescript/           # TypeScript (27개)
│   ├── typescript.md     # 통합 가이드
│   ├── ts-index.md       # 인덱스
│   └── ts-*.md           # 세부 규칙 25개
│
├── react/                # React (44개)
│   ├── react.md          # 통합 가이드
│   ├── react-index.md    # 인덱스
│   └── react-*.md        # 세부 규칙 42개
│
├── python/               # Python (20개)
│   ├── python.md         # 통합 가이드
│   ├── py-index.md       # 인덱스
│   └── py-*.md           # 세부 규칙 18개
│
├── go/                   # Go (21개)
│   ├── go.md             # 통합 가이드
│   ├── go-index.md       # 인덱스
│   └── go-*.md           # 세부 규칙 19개
│
├── rust/                 # Rust (21개)
│   ├── rust.md           # 통합 가이드
│   ├── rust-index.md     # 인덱스
│   └── rust-*.md         # 세부 규칙 19개
│
└── common/               # 공통 (12개)
    ├── anthropic-official.md  # Claude 공식 가이드
    ├── api-design.md          # API 설계
    ├── clean-architecture.md  # 클린 아키텍처
    ├── database.md            # 데이터베이스
    ├── java.md                # Java
    ├── nextjs.md              # Next.js
    ├── nodejs.md              # Node.js
    ├── project-onboarding.md  # 온보딩
    ├── qa-testing.md          # QA 테스팅
    ├── security.md            # 보안
    ├── tailwind.md            # Tailwind CSS
    └── testing.md             # 테스팅
```

---

## TypeScript (27개)

| 카테고리 | 접두사 | 영향도 | 규칙 수 |
|---------|--------|--------|---------|
| Type System | `ts-types-` | CRITICAL | 7 |
| Validation | `ts-validation-` | HIGH | 1 |
| Error Handling | `ts-error-` | HIGH | 4 |
| Async Patterns | `ts-async-` | HIGH | 5 |
| Framework | `ts-nextjs-` | HIGH | 1 |
| Organization | `ts-org-` | MEDIUM | 4 |
| Anti-patterns | `ts-anti-` | HIGH | 3 |

**참조**: `skills/best-practices/references/typescript/`

---

## React (44개)

| 카테고리 | 접두사 | 영향도 | 규칙 수 |
|---------|--------|--------|---------|
| Async/Waterfalls | `react-async-` | CRITICAL | 5 |
| Bundle Optimization | `react-bundle-` | CRITICAL | 5 |
| Server-Side | `react-server-` | HIGH | 7 |
| Components | `react-components-` | MEDIUM | 4 |
| State Management | `react-state-` | MEDIUM | 4 |
| Re-render | `react-rerender-` | MEDIUM | 7 |
| Side Effects | `react-effects-` | LOW-MEDIUM | 4 |
| JS Performance | `react-js-` | LOW | 6 |

**참조**: `skills/best-practices/references/react/`

---

## Python (20개)

| 카테고리 | 접두사 | 영향도 | 규칙 수 |
|---------|--------|--------|---------|
| Type Hints | `py-types-` | HIGH | 4 |
| Pythonic Code | `py-pythonic-` | HIGH | 4 |
| Context Managers | `py-context-` | HIGH | 3 |
| Error Handling | `py-error-` | HIGH | 4 |
| Anti-patterns | `py-anti-` | CRITICAL | 3 |

**참조**: `skills/best-practices/references/python/`

---

## Go (21개)

| 카테고리 | 접두사 | 영향도 | 규칙 수 |
|---------|--------|--------|---------|
| Error Handling | `go-error-` | CRITICAL | 4 |
| Concurrency | `go-concurrency-` | HIGH | 4 |
| Interface Design | `go-interface-` | HIGH | 4 |
| Organization | `go-org-` | MEDIUM | 4 |
| Anti-patterns | `go-anti-` | CRITICAL | 3 |

**참조**: `skills/best-practices/references/go/`

---

## Rust (21개)

| 카테고리 | 접두사 | 영향도 | 규칙 수 |
|---------|--------|--------|---------|
| Ownership | `rust-ownership-` | CRITICAL | 4 |
| Error Handling | `rust-error-` | CRITICAL | 4 |
| Pattern Matching | `rust-match-` | HIGH | 4 |
| Memory Safety | `rust-memory-` | CRITICAL | 4 |
| Anti-patterns | `rust-anti-` | HIGH | 3 |

**참조**: `skills/best-practices/references/rust/`

---

## 사용법

```bash
# 통합 가이드
Read skills/best-practices/references/typescript/typescript.md

# 인덱스
Read skills/best-practices/references/react/react-index.md

# 세부 규칙
Read skills/best-practices/references/typescript/ts-error-result-pattern.md

# 공통
Read skills/best-practices/references/common/api-design.md
```
