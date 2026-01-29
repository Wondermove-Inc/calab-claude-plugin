# /clean --validate - 아키텍처 규칙 검증

> **클린 아키텍처 의존성 규칙 및 구조 검증**

## 사용법

```bash
/clean --validate           # 검증만
/clean --validate --fix     # 검증 + 자동 수정
```

## 실행 절차

### Step 1: 디렉토리 구조 검증

```
✅ 필수 디렉토리 확인:
[ ] src/domain/
[ ] src/application/
[ ] src/adapters/
[ ] src/infrastructure/
[ ] src/shared/

❌ 누락된 디렉토리:
• src/domain/value-objects/ 없음
```

### Step 2: 의존성 규칙 검증

**허용된 의존성:**

| 레이어 | 허용된 import |
|--------|--------------|
| Domain | 없음 (외부 의존성 금지) |
| Application | @domain/* |
| Adapters | @domain/*, @application/* |
| Infrastructure | @domain/*, @application/*, @adapters/* |

**검증 방법:**

```typescript
// 각 파일의 import 문 분석
import { User } from '@domain/entities/User';  // ✅ OK
import { PrismaClient } from '@prisma/client';  // ❌ Domain에서 금지
```

### Step 3: 파일 위치 검증

| 파일 유형 | 올바른 위치 |
|----------|------------|
| Entity | src/domain/entities/ |
| Value Object | src/domain/value-objects/ |
| Repository Interface | src/domain/interfaces/ |
| UseCase | src/application/use-cases/ |
| DTO | src/application/dtos/ |
| Controller | src/adapters/controllers/ |
| Repository Impl | src/adapters/repositories/ |
| Config | src/infrastructure/config/ |

### Step 4: 인터페이스 분리 검증

```typescript
// ✅ Good - 인터페이스에 의존
constructor(private readonly userRepo: IUserRepository) {}

// ❌ Bad - 구현체에 직접 의존
constructor(private readonly userRepo: PrismaUserRepository) {}
```

### Step 5: DTO 사용 검증

```typescript
// ✅ Good - DTO로 반환
execute(): Promise<UserOutputDto> {}

// ❌ Bad - Entity 직접 반환
execute(): Promise<User> {}
```

### Step 6: 검증 결과 출력

```
============================================
 CLEAN VALIDATE 결과
============================================

 📁 디렉토리 구조: ✅ OK

 📦 의존성 규칙:
 ┌────────────────────────────────────────┐
 │ 검사 파일: 45개                         │
 │ 위반 사항: 3개                          │
 └────────────────────────────────────────┘

 ❌ 위반 사항:

 1. src/domain/entities/User.ts:5
    └── 금지된 import: import { PrismaClient } from '@prisma/client'
    └── Domain은 외부 라이브러리에 의존할 수 없습니다.

 2. src/application/use-cases/CreateUser.ts:8
    └── 금지된 import: import { UserController } from '@adapters/controllers'
    └── Application은 Adapters에 의존할 수 없습니다.

 3. src/application/services/UserService.ts
    └── 잘못된 위치: Service는 use-cases/에 위치해야 합니다.

 📊 통계:
 • Domain 위반: 1개
 • Application 위반: 2개
 • Adapters 위반: 0개
 • Infrastructure 위반: 0개

============================================
 --fix 옵션으로 자동 수정 가능
============================================
```

### Step 7: 자동 수정 (`--fix`)

```
============================================
 CLEAN VALIDATE --fix 결과
============================================

 🔧 자동 수정된 항목:

 1. ✅ src/domain/entities/User.ts
    └── PrismaClient import 제거됨
    └── 도메인 순수성 유지

 2. ✅ src/application/use-cases/CreateUser.ts
    └── UserController import 제거됨
    └── 의존성 역전 필요 → 인터페이스 생성됨

 3. ✅ src/application/services/UserService.ts
    └── src/application/use-cases/UserService.ts로 이동됨

 ⚠️ 수동 수정 필요:

 1. src/domain/entities/User.ts
    └── Prisma 관련 로직을 Infrastructure로 이동 필요

============================================
 수동 수정 후 다시 /clean --validate 실행
============================================
```

## 의존성 규칙 상세

### Domain Layer (핵심)
```
✅ 허용:
- 같은 Domain 내 다른 파일
- 기본 JavaScript/TypeScript 타입

❌ 금지:
- @application/*
- @adapters/*
- @infrastructure/*
- 외부 라이브러리 (Prisma, Express 등)
```

### Application Layer
```
✅ 허용:
- @domain/*

❌ 금지:
- @adapters/*
- @infrastructure/*
```

### Adapters Layer
```
✅ 허용:
- @domain/*
- @application/*

❌ 금지:
- @infrastructure/* (DI 컨테이너 제외)
```

### Infrastructure Layer
```
✅ 허용:
- 모든 레이어
- 외부 라이브러리
```

## 수동 검증 도구

```bash
# madge를 사용한 순환 의존성 검사
npx madge --circular src/

# 시각화
npx madge --image graph.svg src/
```

## 검증 체크리스트

- [ ] 모든 엔티티는 domain/entities/에 위치
- [ ] 값 객체는 domain/value-objects/에 위치
- [ ] 유스케이스는 IUseCase 인터페이스 구현
- [ ] 유스케이스는 DTO로 입출력
- [ ] 리포지토리는 인터페이스에 의존
- [ ] Domain에 외부 의존성 없음
- [ ] 순환 의존성 없음
