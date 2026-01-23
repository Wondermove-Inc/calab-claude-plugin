---
name: best-practices
description: 기술별 베스트 프랙티스를 적용합니다. 코드 작성, 구현, 개발, React, Node.js, TypeScript, 데이터베이스, API 요청 시 자동 활성화. 검증된 패턴과 방법론을 사용합니다.
allowed-tools: Read, Glob
---

# Best Practices Skill

## 목적

각 기술에 대해 검증된 베스트 프랙티스와 디자인 패턴을 적용하여
일관되고 유지보수 가능한 코드를 생성합니다.

## 🚨 자동 활성화 규칙 (필수 적용)

### 1. 키워드 감지 (대소문자 무관)

**프로그래밍 언어 감지 시 해당 best-practices 파일 자동 로드:**

| 감지 키워드 | 로드 파일 |
|------------|----------|
| `python`, `django`, `flask`, `fastapi`, `pydantic`, `pytest` | `python.md` |
| `go`, `golang`, `goroutine`, `gin`, `echo` | `go.md` |
| `rust`, `cargo`, `tokio`, `axum` | `rust.md` |
| `java`, `spring`, `springboot`, `jpa`, `hibernate`, `maven`, `gradle` | `java.md` |
| `react`, `jsx`, `컴포넌트`, `훅`, `hook`, `useState`, `useEffect` | `react.md` |
| `next`, `nextjs`, `app router`, `서버 컴포넌트` | `nextjs.md` |
| `node`, `nodejs`, `express`, `nestjs` | `nodejs.md` |
| `typescript`, `ts`, `타입`, `interface`, `type` | `typescript.md` |
| `tailwind`, `css`, `스타일`, `className`, `디자인 시스템` | `tailwind.md` |
| `test`, `testing`, `테스트`, `jest`, `vitest`, `tdd` | `testing.md` |
| `api`, `rest`, `graphql`, `endpoint`, `swagger` | `api-design.md` |
| `db`, `database`, `sql`, `prisma`, `typeorm`, `데이터베이스` | `database.md` |

### 2. 파일 확장자 감지

**편집/생성하는 파일 확장자에 따라 자동 로드:**

| 확장자 | 로드 파일 |
|--------|----------|
| `.py` | `python.md` |
| `.go` | `go.md` |
| `.rs` | `rust.md` |
| `.java`, `.kt` | `java.md` |
| `.tsx`, `.jsx` | `react.md` + `typescript.md` |
| `.ts` | `typescript.md` + `nodejs.md` |
| `.css`, `.scss` | `tailwind.md` |
| `.test.ts`, `.spec.ts` | `testing.md` |

### 3. 액션 기반 감지

**다음 액션 수행 시 관련 best-practices 자동 로드:**

| 액션 | 로드 파일 |
|------|----------|
| `구현해줘`, `만들어줘`, `작성해줘`, `코드 생성` | 언어 감지 후 해당 파일 |
| `테스트 작성`, `TDD`, `단위 테스트` | `testing.md` |
| `API 설계`, `엔드포인트 추가` | `api-design.md` |
| `스키마 설계`, `ERD`, `마이그레이션` | `database.md` |
| `컴포넌트 만들어`, `UI 구현` | `react.md` + `tailwind.md` |

## 베스트 프랙티스 적용 프로토콜

### 1. 기술 감지 (자동)

```
사용자 입력/파일 확장자 분석
→ 관련 키워드/확장자 감지
→ 해당 베스트 프랙티스 파일 자동 로드
```

### 2. 베스트 프랙티스 로드 (필수)

```
.claude/best-practices/{technology}.md 읽기
→ 패턴, 규칙, 예시 코드 확인
→ 금지 사항 확인
→ 체크리스트 확인
```

### 3. 코드 생성 시 적용

- **파일 구조**: 해당 기술의 권장 구조 사용
- **네이밍**: 기술별 컨벤션 적용
- **패턴**: 검증된 디자인 패턴 사용
- **에러 처리**: 표준 에러 처리 패턴 적용
- **테스트**: 기술별 테스트 패턴 적용
- **금지 사항**: 각 파일의 "금지 사항" 섹션 반드시 준수

## 지원 기술 (12개)

| 기술 | 파일 | 주요 내용 |
|------|------|----------|
| **Python** | `python.md` | Type Hints, Pydantic, FastAPI, pytest |
| **Go** | `go.md` | Error Handling, Context, Concurrency |
| **Rust** | `rust.md` | Ownership, Result/Option, thiserror, Axum |
| **Java** | `java.md` | Hexagonal Architecture, Spring Boot, JPA |
| **React** | `react.md` | 컴포넌트 패턴, 훅, 상태 관리 |
| **Next.js** | `nextjs.md` | App Router, 서버 컴포넌트, 데이터 페칭 |
| **Node.js** | `nodejs.md` | 레이어 아키텍처, 에러 처리, 로깅 |
| **TypeScript** | `typescript.md` | 타입 패턴, 제네릭, 유틸리티 타입 |
| **Tailwind CSS** | `tailwind.md` | 유틸리티 클래스, 반응형, CVA |
| **Database** | `database.md` | 스키마 설계, 쿼리 최적화, 마이그레이션 |
| **API Design** | `api-design.md` | REST/GraphQL, 버저닝, 에러 응답 |
| **Testing** | `testing.md` | TDD, 단위/통합/E2E 테스트 패턴 |

## 출력 형식

### 코드 생성 전 확인 (Silent Mode)

> 사용자에게 매번 알림을 보내지 않고 **자동 적용**합니다.
> 단, 적용한 패턴을 코드 주석이나 응답 말미에 간략히 언급합니다.

```
// Applied: python.md (Type Hints, Pydantic)
// Applied: react.md + tailwind.md (Function Components, CVA)
```

### 코드 생성 체크리스트

코드 생성 시 다음을 확인:

- [ ] 해당 기술의 베스트 프랙티스 파일 로드 완료
- [ ] 해당 기술의 권장 디렉토리 구조 사용
- [ ] 파일당 300줄 이하
- [ ] 모든 함수에 주석 (JSDoc/Docstring)
- [ ] 해당 기술의 네이밍 컨벤션 적용
- [ ] 에러 처리 패턴 적용
- [ ] 타입 정의 완전성
- [ ] **금지 사항 미적용 확인**

## 🚨 Anthropic 공식 가이드라인 (필수 적용)

> 출처: docs.anthropic.com, console.anthropic.com

### 코드 작업 전 필수 행동

```
1. 관련 파일 먼저 읽고 이해 (추측 금지)
2. 코드베이스의 스타일, 컨벤션, 추상화 파악
3. 충분한 컨텍스트 확보 후 답변/수정 제안
```

### 할루시네이션 방지 규칙

- **열어보지 않은 파일 추측 금지**
- **사용자가 언급한 파일 반드시 먼저 읽기**
- **확실하지 않으면 "확인 필요" 인정**
- **근거 없는 주장 절대 금지**

**상세 가이드**: `.claude/best-practices/anthropic-official.md`

## 참조 파일

- `.claude/best-practices/anthropic-official.md` - **Anthropic 공식 가이드라인 (최우선)**
- `.claude/best-practices/` - 기술별 베스트 프랙티스 (15개)
- `.claude/memory/TECH_STACK.md` - 기술 스택 설정
- `.claude/memory/CODE_STYLE.md` - 코드 스타일 규칙
