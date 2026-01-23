# Phase 1-2: 프로젝트 스캔 및 코드 패턴 분석

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**. 에이전트를 적극 활용하고, 파일이 크면 분할해서 읽어라.

---

## Phase 1: 프로젝트 스캔 (Discovery)

### 1.1 설정 파일 분석

**필수 분석 대상:**

| 파일 | 추출 정보 |
|------|----------|
| `package.json` | 기술 스택, 스크립트, 의존성 버전 |
| `tsconfig.json` | TypeScript 설정, Path alias |
| `.env.example` | 환경 변수 목록 |
| `docker-compose.yml` | 서비스 구성 |
| `prisma/schema.prisma` | DB 스키마, 엔티티 관계 |

**분석 명령어:**

```bash
# 프로젝트 루트 구조
ls -la

# 소스 디렉토리 구조 (3레벨까지)
find src -type d -maxdepth 3 | head -50

# 주요 설정 파일
cat package.json
cat tsconfig.json
```

### 1.2 기술 스택 식별

**분석 항목:**

```yaml
Frontend:
  - Framework: (React, Next.js, Vue, Angular)
  - State: (Redux, Zustand, Recoil, Context)
  - Styling: (CSS Modules, Tailwind, Styled-components)
  - Testing: (Jest, Vitest, RTL, Cypress)

Backend:
  - Runtime: (Node.js, Deno, Bun)
  - Framework: (Express, Fastify, NestJS, Hono)
  - ORM: (Prisma, TypeORM, Drizzle, Knex)
  - Auth: (NextAuth, Passport, JWT)

Database:
  - Primary: (PostgreSQL, MySQL, MongoDB)
  - Cache: (Redis, Memcached)
  - Search: (Elasticsearch, Algolia)

Infrastructure:
  - Container: (Docker, Podman)
  - CI/CD: (GitHub Actions, GitLab CI, Jenkins)
  - Cloud: (AWS, GCP, Azure, Vercel)
```

### 1.3 디렉토리 구조 매핑

**구조 유형 식별:**

| 패턴 | 특징 | 예시 |
|------|------|------|
| **Feature-based** | 기능별 폴더 | `features/auth/`, `features/user/` |
| **Layer-based** | 레이어별 폴더 | `controllers/`, `services/`, `repositories/` |
| **Domain-based** | 도메인별 폴더 | `domain/user/`, `domain/order/` |
| **Hybrid** | 혼합 구조 | `app/`, `lib/`, `components/` |

---

## Phase 2: 코드 패턴 분석 (Pattern Extraction)

### 2.1 대표 파일 선정

**분석할 파일 수:**

| 카테고리 | 파일 수 | 선정 기준 |
|----------|---------|----------|
| 컴포넌트 | 3-5개 | 가장 큰 파일, 재사용 컴포넌트 |
| API 라우트 | 2-3개 | CRUD 완비된 엔드포인트 |
| 서비스/유틸 | 2-3개 | 핵심 비즈니스 로직 |
| 타입 정의 | 1-2개 | 공통 타입, 엔티티 타입 |

### 2.2 패턴 추출 체크리스트

**컴포넌트 패턴:**

```typescript
// 추출할 패턴들
□ Props 정의 방식 (interface vs type)
□ 기본값 처리 (defaultProps vs 구조분해)
□ 상태 관리 (useState, useReducer, 외부 상태)
□ 부수효과 (useEffect 패턴)
□ 에러 바운더리 사용 여부
□ 메모이제이션 (useMemo, useCallback, React.memo)
□ 스타일링 방식
□ 테스트 패턴 (단위/통합)
```

**API 패턴:**

```typescript
// 추출할 패턴들
□ 라우터 구조 (Express, Fastify, Next.js API Routes)
□ 미들웨어 체인
□ 인증/인가 처리
□ 요청 검증 (Zod, Joi, class-validator)
□ 응답 형식 (표준화된 JSON 구조)
□ 에러 처리 (커스텀 에러 클래스)
□ 로깅 전략
□ 페이지네이션 패턴
```

**에러 처리 패턴:**

```typescript
// 추출할 패턴들
□ 커스텀 에러 클래스 존재 여부
□ 전역 에러 핸들러
□ 사용자 에러 vs 시스템 에러 구분
□ 에러 코드 체계
□ 로깅 레벨 (debug, info, warn, error)
```

### 2.3 Import 순서 분석

**표준 순서 추출:**

```typescript
// 1. 외부 라이브러리 (node_modules)
import React from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. 내부 모듈 (절대 경로)
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';

// 3. 상대 경로 모듈
import { UserCard } from './UserCard';
import { formatDate } from '../utils';

// 4. 타입 (type-only imports)
import type { User } from '@/types';

// 5. 스타일
import styles from './styles.module.css';
```
