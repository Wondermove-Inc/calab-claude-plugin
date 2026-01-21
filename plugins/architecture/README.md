# Architecture Plugin

> **클린 아키텍처 설계 및 검증**: 4-레이어 구조 자동 생성 + 의존성 규칙 강제 (TypeScript, Go 지원)

---

## 지원 언어

| 언어 | 상태 | 명령어 접미사 |
|------|------|--------------|
| **TypeScript** | ✅ 지원 | `-ts` |
| **Go** | ✅ 지원 | `-go` |

---

## 문제 해결 매트릭스

| 상황 | 문제점 | 솔루션 | TypeScript | Go |
|------|--------|--------|------------|-----|
| **아키텍처 혼란** | 의존성 규칙 위반 | 클린 아키텍처 강제 | `/architecture:clean-init-ts` | `/architecture:clean-init-go` |
| **엔티티 생성** | 일관성 없는 도메인 모델 | 표준화된 엔티티 생성 | `/architecture:clean-entity-ts` | `/architecture:clean-entity-go` |
| **유스케이스 작성** | 비즈니스 로직 분산 | 유스케이스 패턴 적용 | `/architecture:clean-usecase-ts` | `/architecture:clean-usecase-go` |
| **의존성 위반** | 레이어 간 잘못된 참조 | 자동 검증 + 수정 | `/architecture:clean-validate-ts` | `/architecture:clean-validate-go` |

---

## 명령어

### TypeScript

| 명령어 | 옵션 | 자연어 | 설명 |
|--------|------|--------|------|
| `/architecture:clean-init-ts` | - | "TS 클린 아키텍처 만들어줘" | 4-레이어 구조 초기화 |
| `/architecture:clean-entity-ts [name]` | `--with-repository` | "TS 엔티티 만들어줘" | 도메인 엔티티 생성 |
| `/architecture:clean-usecase-ts [name]` | `--entity [name]` | "TS 유스케이스 만들어줘" | 유스케이스 생성 |
| `/architecture:clean-validate-ts` | `--fix` | "TS 아키텍처 검증해줘" | 의존성 규칙 검증 |

### Go

| 명령어 | 옵션 | 자연어 | 설명 |
|--------|------|--------|------|
| `/architecture:clean-init-go` | `--module` | "Go 클린 아키텍처 만들어줘" | Go 4-레이어 구조 초기화 |
| `/architecture:clean-entity-go [name]` | `--with-repository` | "Go 엔티티 만들어줘" | Go 도메인 엔티티 생성 |
| `/architecture:clean-usecase-go [name]` | `--entity [name]` | "Go 유스케이스 만들어줘" | Go 유스케이스 생성 |
| `/architecture:clean-validate-go` | `--fix` | "Go 아키텍처 검증해줘" | Go 의존성 규칙 검증 |

---

## 주요 기능 상세

### 클린 아키텍처 4-레이어

```mermaid
flowchart TB
    subgraph Presentation["Presentation Layer"]
        C["Controllers"]
        P["Presenters"]
    end

    subgraph Application["Application Layer"]
        UC["Use Cases"]
        DTO["DTOs"]
        Port["Ports"]
    end

    subgraph Domain["Domain Layer"]
        E["Entities"]
        VO["Value Objects"]
        RI["Repository Interfaces"]
        DS["Domain Services"]
    end

    subgraph Infrastructure["Infrastructure Layer"]
        Repo["Repository Impl"]
        API["External APIs"]
        DB["Database"]
    end

    Presentation --> Application
    Application --> Domain
    Infrastructure --> Domain

    style Domain fill:#e8f5e9
    style Application fill:#e3f2fd
    style Presentation fill:#fff3e0
    style Infrastructure fill:#fce4ec
```

**레이어별 역할:**

| 레이어 | 역할 | 주요 컴포넌트 |
|--------|------|-------------|
| **Domain** | 핵심 비즈니스 규칙 | Entities, Value Objects, Repository Interfaces |
| **Application** | 유스케이스 구현 | Use Cases, DTOs, Ports |
| **Presentation** | UI/API 처리 | Controllers, Presenters |
| **Infrastructure** | 외부 의존성 | Repository Impl, External APIs, Database |

### 의존성 규칙

```
✅ 올바른 의존성:
   Presentation → Application → Domain ← Infrastructure

❌ 잘못된 의존성:
   Domain → Infrastructure (위반!)
   Domain → Application (위반!)
```

---

## 사용 예시

```bash
# 1. 4-레이어 구조 초기화
/architecture:clean-init

# 2. 도메인 엔티티 생성
/architecture:clean-entity User --with-repository

# 3. 유스케이스 생성
/architecture:clean-usecase CreateUser --entity User

# 4. 의존성 규칙 검증
/architecture:clean-validate --fix
```

### clean-init 실행 결과

```
src/
├── domain/                 # Domain Layer
│   ├── entities/           # 엔티티
│   ├── value-objects/      # 값 객체
│   ├── repositories/       # 리포지토리 인터페이스
│   └── services/           # 도메인 서비스
│
├── application/            # Application Layer
│   ├── use-cases/          # 유스케이스
│   ├── dtos/               # 데이터 전송 객체
│   └── ports/              # 포트 (인터페이스)
│
├── adapters/               # Presentation Layer
│   ├── controllers/        # 컨트롤러
│   └── presenters/         # 프레젠터
│
└── infrastructure/         # Infrastructure Layer
    ├── repositories/       # 리포지토리 구현
    ├── external/           # 외부 API 연동
    └── config/             # 설정
```

### clean-entity 실행 결과

```typescript
// src/domain/entities/User.ts
export class User {
  constructor(
    private readonly id: UserId,
    private name: UserName,
    private email: Email,
    private readonly createdAt: Date
  ) {}

  // Getters
  get getId(): UserId { return this.id; }
  get getName(): UserName { return this.name; }
  get getEmail(): Email { return this.email; }

  // Business methods
  changeName(name: UserName): void {
    this.name = name;
  }

  changeEmail(email: Email): void {
    this.email = email;
  }
}

// src/domain/repositories/UserRepository.ts (--with-repository)
export interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: UserId): Promise<void>;
}
```

### clean-usecase 실행 결과

```typescript
// src/application/use-cases/CreateUser.ts
export interface CreateUserInput {
  name: string;
  email: string;
}

export interface CreateUserOutput {
  id: string;
  name: string;
  email: string;
}

export class CreateUserUseCase {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly idGenerator: IdGenerator
  ) {}

  async execute(input: CreateUserInput): Promise<CreateUserOutput> {
    // 1. Validate
    const email = Email.create(input.email);
    const existingUser = await this.userRepository.findByEmail(email);
    if (existingUser) {
      throw new UserAlreadyExistsError(input.email);
    }

    // 2. Create entity
    const user = new User(
      this.idGenerator.generate(),
      UserName.create(input.name),
      email,
      new Date()
    );

    // 3. Save
    await this.userRepository.save(user);

    // 4. Return output
    return {
      id: user.getId.value,
      name: user.getName.value,
      email: user.getEmail.value,
    };
  }
}
```

### clean-validate 실행 결과

```
🔍 의존성 규칙 검증 중...

══════════════════════════════════════════════════════════════
 검증 결과
══════════════════════════════════════════════════════════════

✅ Domain Layer: 위반 없음
✅ Application Layer: 위반 없음
❌ Presentation Layer: 2개 위반
   - src/adapters/controllers/UserController.ts:5
     → Infrastructure (Prisma) 직접 import
   - src/adapters/controllers/OrderController.ts:12
     → Domain Repository 구현체 직접 import

✅ Infrastructure Layer: 위반 없음

══════════════════════════════════════════════════════════════
 수정 제안 (--fix 옵션으로 자동 수정)
══════════════════════════════════════════════════════════════

1. UserController.ts:5
   Before: import { prisma } from '@/infrastructure/database';
   After:  import { UserRepository } from '@/domain/repositories/UserRepository';

2. OrderController.ts:12
   Before: import { PrismaOrderRepository } from '@/infrastructure/repositories';
   After:  import { OrderRepository } from '@/domain/repositories/OrderRepository';
```

---

## 자동 적용 기능 (패시브 스킬)

| 스킬 | 활성화 조건 | 효과 |
|------|------------|------|
| `clean-architecture-ts` | TypeScript 코드 구현 시 | 4-레이어 구조 강제, 의존성 규칙 검증 |
| `clean-architecture-go` | Go 코드 구현 시 | Go 4-레이어 구조 강제, 의존성 규칙 검증 |

**자동 적용 내용:**
- 새 파일 생성 시 올바른 레이어 위치 제안
- Import 문 작성 시 의존성 규칙 검증
- 코드 리뷰 시 아키텍처 위반 감지

---

## 문서 생성 위치

```
.claude/docs/active/{feature-name}/
├── 03-architecture.md    # 아키텍처 설계 문서
└── 04-erd.md             # ERD 다이어그램
```

---

## 포함 리소스

- **best-practices/**:
  - clean-architecture-ts.md (TypeScript 의존성 규칙, 레이어 가이드)
  - clean-architecture-go.md (Go 의존성 규칙, 레이어 가이드)
  - api-design.md (REST API 설계 원칙)
  - database.md (데이터베이스 설계 원칙)
- **templates/**:
  - architecture-template.md (아키텍처 문서 템플릿)
  - erd-template.md (ERD 템플릿)
  - api-spec-template.md (API 스펙 템플릿)
- **skills/**:
  - clean-architecture-ts/ (TypeScript 클린 아키텍처 스킬)
  - clean-architecture-go/ (Go 클린 아키텍처 스킬)

---

## Go 프로젝트 구조

`/architecture:clean-init-go` 실행 시 생성되는 구조:

```
project/
├── cmd/
│   └── server/
│       └── main.go              # 진입점
├── internal/                     # 비공개 패키지
│   ├── domain/                   # Domain Layer
│   │   ├── entity/              # 엔티티
│   │   ├── valueobject/         # 값 객체
│   │   ├── repository/          # 리포지토리 인터페이스
│   │   └── errors/              # 도메인 에러
│   ├── application/              # Application Layer
│   │   ├── usecase/             # 유스케이스
│   │   ├── dto/                 # 데이터 전송 객체
│   │   └── port/                # 외부 서비스 인터페이스
│   ├── adapters/                 # Adapters Layer
│   │   ├── handler/             # HTTP 핸들러
│   │   ├── repository/          # 리포지토리 구현
│   │   └── gateway/             # 외부 서비스 구현
│   └── infrastructure/           # Infrastructure Layer
│       ├── http/                # HTTP 서버 설정
│       ├── database/            # DB 연결 설정
│       ├── config/              # 환경 설정
│       └── di/                  # 의존성 주입
├── pkg/                          # 공개 패키지
├── go.mod
└── Makefile
```

### Go 의존성 규칙

```
cmd/ → infrastructure → adapters → application → domain
  ↓          ↓              ↓            ↓           ↓
진입점   프레임워크/DB    포트 구현   비즈니스 로직  순수 엔티티

✅ 올바른 의존성:
   infrastructure → adapters → application → domain

❌ 잘못된 의존성:
   domain → infrastructure (위반!)
   application → adapters (위반!)
```
