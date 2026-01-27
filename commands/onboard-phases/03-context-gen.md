---
description: 온보딩 Phase 4 - 컨텍스트 문서 자동 생성 단계입니다.
allowed-tools: Read, Write, Glob, Grep
---

# Phase 4: 컨텍스트 문서 생성

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**. 에이전트를 적극 활용하고, 파일이 크면 분할해서 읽어라.

---

## 4.1 PROJECT_SUMMARY.md

**필수 섹션:**

```markdown
# 프로젝트 요약

## 개요
- **프로젝트명**:
- **설명**: 한 문장 설명
- **주요 기능**: 3-5개 핵심 기능

## 기술 스택

### Frontend
| 기술 | 버전 | 용도 |
|------|------|------|
| Next.js | 14.x | SSR/SSG 프레임워크 |
| React | 18.x | UI 라이브러리 |
| TypeScript | 5.x | 타입 시스템 |
| Tailwind CSS | 3.x | 스타일링 |
| React Query | 5.x | 서버 상태 관리 |

### Backend
| 기술 | 버전 | 용도 |
|------|------|------|
| Node.js | 20.x | 런타임 |
| Prisma | 5.x | ORM |
| PostgreSQL | 15.x | 데이터베이스 |

## 디렉토리 구조
src/
├── app/              # Next.js App Router
├── components/       # 재사용 컴포넌트
├── lib/              # 유틸리티
├── types/            # 타입 정의
└── prisma/           # DB 스키마

## 개발 명령어
| 명령어 | 설명 |
|--------|------|
| `npm run dev` | 개발 서버 시작 |
| `npm run build` | 프로덕션 빌드 |
| `npm run test` | 테스트 실행 |
```

---

## 4.2 ARCHITECTURE.md

**필수 섹션:**

```markdown
# 아키텍처 문서

## 시스템 개요 (C4 Level 1)
(System Context 다이어그램)

## 컨테이너 다이어그램 (C4 Level 2)
(Container 다이어그램)

## 레이어 구조
### 프레젠테이션 레이어
- **역할**: UI 렌더링, 사용자 입력 처리
- **위치**: `src/app/`, `src/components/`

### 애플리케이션 레이어
- **역할**: 유스케이스 구현
- **위치**: `src/lib/services/`

### 도메인 레이어
- **역할**: 핵심 비즈니스 규칙
- **위치**: `src/lib/domain/`

### 인프라 레이어
- **역할**: 외부 시스템 연동
- **위치**: `src/lib/infrastructure/`

## 데이터 흐름
(Sequence 다이어그램)

## 상태 관리
| 상태 유형 | 관리 방법 | 위치 |
|----------|----------|------|
| 서버 상태 | React Query | `src/lib/hooks/` |
| 클라이언트 상태 | Zustand | `src/lib/stores/` |

## 인증/인가
(인증 흐름 다이어그램)

## 아키텍처 결정 기록 (ADR)
(주요 기술 결정 기록)
```

---

## 4.3 CODE_PATTERNS.md

**필수 섹션:**

```markdown
# 코드 패턴

## 컴포넌트 패턴

### 표준 컴포넌트 구조
- Props 인터페이스 정의
- memo 사용 패턴
- 스타일링 방식

### 페이지 컴포넌트 구조
- 메타데이터 정의
- Suspense 사용
- 서버 컴포넌트 패턴

## API 패턴

### API Route 표준 구조
- 요청 스키마 (Zod)
- 인증 검증
- 에러 처리
- 응답 형식

### 표준 응답 형식
{
  "data": { ... },
  "meta": { "page": 1, "limit": 10, "total": 100 }
}

## 훅 패턴
- 쿼리 키 팩토리
- useQuery 패턴
- useMutation 패턴

## 에러 처리 패턴
- 커스텀 에러 클래스
- AppError, ValidationError, NotFoundError

## 테스트 패턴
- 컴포넌트 테스트
- API 테스트
```

---

## 4.4 CONVENTIONS.md

**필수 섹션:**

```markdown
# 코딩 컨벤션

## 파일/폴더 명명 규칙
| 유형 | 규칙 | 예시 |
|------|------|------|
| 컴포넌트 파일 | PascalCase | `UserCard.tsx` |
| 유틸리티 파일 | camelCase | `formatDate.ts` |
| 훅 파일 | camelCase (use 접두사) | `useAuth.ts` |

## 코드 명명 규칙
| 유형 | 규칙 | 예시 |
|------|------|------|
| 컴포넌트 | PascalCase | `UserCard` |
| 함수/변수 | camelCase | `getUserById` |
| 상수 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |

## Import 순서
1. React/Next.js
2. 외부 라이브러리
3. 내부 절대 경로
4. 상대 경로
5. 타입
6. 스타일

## 주석 규칙
- JSDoc 형식
- 왜(Why) 설명 우선
- TODO/FIXME 규칙

## Git 커밋 메시지 규칙
- 형식: `<type>(<scope>): <subject>`
- 타입: feat, fix, docs, style, refactor, test, chore

## 브랜치 규칙
| 브랜치 | 용도 |
|--------|------|
| `main` | 프로덕션 배포 |
| `develop` | 개발 통합 |
| `feature/xxx` | 새 기능 개발 |
```

---

## 4.5 DOMAIN_KNOWLEDGE.md

**사용자 입력 수집 템플릿:**

```markdown
# 도메인 지식

## 비즈니스 개요
### 프로젝트가 해결하는 문제
(사용자 입력 필요)

### 대상 사용자
| 사용자 유형 | 역할 | 주요 니즈 |
|------------|------|----------|
| (입력) | (입력) | (입력) |

## 핵심 도메인 개념

### 엔티티 (Entities)
| 엔티티 | 설명 | 주요 속성 |
|--------|------|----------|
| (입력) | (입력) | (입력) |

### 값 객체 (Value Objects)
| 값 객체 | 설명 | 제약 조건 |
|---------|------|----------|
| (입력) | (입력) | (입력) |

## 비즈니스 규칙

### 불변 규칙 (Invariants)
1. (입력)

### 정책 (Policies)
1. (입력)

## 도메인 용어 사전
| 용어 | 정의 | 영문 |
|------|------|------|
| (입력) | (입력) | (입력) |

## 도메인 이벤트
| 이벤트 | 트리거 | 후속 액션 |
|--------|--------|----------|
| (입력) | (입력) | (입력) |
```
