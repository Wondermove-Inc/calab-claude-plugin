# Hexagonal Architecture (Ports & Adapters) 베스트 프랙티스

> 이 문서는 Hexagonal Architecture 구현 시 **반드시** 참조해야 합니다.

---

## 1. 개요

### 1.1 핵심 개념

Hexagonal Architecture(육각형 아키텍처)는 **Ports and Adapters Architecture**라고도 불립니다.
애플리케이션의 핵심 비즈니스 로직을 외부 시스템(DB, UI, 외부 API)으로부터 완전히 격리시킵니다.

```
┌──────────────────────────────────────────────────────────────────┐
│                      Driving Adapters (Input)                    │
│              (REST Handler, CLI, gRPC, Message Consumer)         │
├──────────────────────────────────────────────────────────────────┤
│                        Driving Ports (Input)                     │
│                    (UseCase Interfaces)                          │
├──────────────────────────────────────────────────────────────────┤
│                         Application Core                         │
│            (Domain Entities + Application Services)              │
├──────────────────────────────────────────────────────────────────┤
│                       Driven Ports (Output)                      │
│             (Repository, Gateway, Notifier Interfaces)           │
├──────────────────────────────────────────────────────────────────┤
│                      Driven Adapters (Output)                    │
│          (PostgreSQL, Redis, HTTP Client, SMTP, Kafka)           │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Clean Architecture와의 차이점

| 관점 | Clean Architecture | Hexagonal Architecture |
|------|-------------------|----------------------|
| 레이어 수 | 4개 (Domain, Application, Adapters, Infrastructure) | 2개 (Core, Adapters) + Ports |
| 초점 | 레이어 간 의존성 방향 | Port/Adapter 대칭 구조 |
| 용어 | UseCase, Repository | Port, Adapter |
| 적합한 경우 | 복잡한 도메인 | 다양한 외부 시스템 연동 |

---

## 2. 구조

### 2.1 디렉토리 구조 (Go)

```
internal/
├── core/                           # Application Core
│   ├── domain/                     # 도메인 모델
│   │   ├── entity/                 # 엔티티
│   │   ├── valueobject/            # 값 객체
│   │   └── event/                  # 도메인 이벤트
│   │
│   ├── service/                    # 애플리케이션 서비스
│   │   └── user_service.go
│   │
│   └── port/                       # 포트 정의
│       ├── driving/                # Driving Ports (Input)
│       │   └── user_service.go     # UseCase 인터페이스
│       └── driven/                 # Driven Ports (Output)
│           ├── user_repository.go  # 영속화 포트
│           ├── email_sender.go     # 알림 포트
│           └── payment_gateway.go  # 외부 서비스 포트
│
├── adapter/                        # 어댑터
│   ├── driving/                    # Driving Adapters (Input)
│   │   ├── http/                   # REST API
│   │   │   ├── handler/
│   │   │   └── router.go
│   │   ├── grpc/                   # gRPC
│   │   └── cli/                    # CLI 커맨드
│   │
│   └── driven/                     # Driven Adapters (Output)
│       ├── persistence/            # 영속화
│       │   ├── postgres/
│       │   └── redis/
│       ├── notification/           # 알림
│       │   └── smtp/
│       └── external/               # 외부 서비스
│           └── stripe/
│
└── config/                         # 설정 및 DI
    ├── config.go
    └── wire.go                     # 의존성 주입
```

### 2.2 디렉토리 구조 (TypeScript)

```
src/
├── core/                           # Application Core
│   ├── domain/                     # 도메인 모델
│   │   ├── entities/               # 엔티티
│   │   ├── value-objects/          # 값 객체
│   │   └── events/                 # 도메인 이벤트
│   │
│   ├── services/                   # 애플리케이션 서비스
│   │   └── UserService.ts
│   │
│   └── ports/                      # 포트 정의
│       ├── driving/                # Driving Ports (Input)
│       │   └── IUserService.ts
│       └── driven/                 # Driven Ports (Output)
│           ├── IUserRepository.ts
│           ├── IEmailSender.ts
│           └── IPaymentGateway.ts
│
├── adapters/                       # 어댑터
│   ├── driving/                    # Driving Adapters (Input)
│   │   ├── http/                   # REST API (Express/Fastify)
│   │   ├── graphql/                # GraphQL
│   │   └── cli/                    # CLI
│   │
│   └── driven/                     # Driven Adapters (Output)
│       ├── persistence/            # 영속화
│       │   ├── prisma/
│       │   └── redis/
│       ├── notification/           # 알림
│       │   └── nodemailer/
│       └── external/               # 외부 서비스
│           └── stripe/
│
└── config/                         # 설정 및 DI
    └── container.ts
```

---

## 3. Port 정의

### 3.1 Driving Port (Input Port)

Driving Port는 **애플리케이션이 제공하는 기능**을 정의합니다.
외부에서 애플리케이션을 **호출**할 때 사용합니다.

**핵심 원칙:**
- UseCase 인터페이스 정의 (CRUD 메서드)
- Input DTO를 함께 정의
- Core 내부에 위치 (`core/port/driving/`)
- 도메인 언어 사용 (기술적 용어 X)

### 3.2 Driven Port (Output Port)

Driven Port는 **애플리케이션이 필요로 하는 외부 기능**을 정의합니다.
애플리케이션에서 **외부를 호출**할 때 사용합니다.

**핵심 원칙:**
- Repository, Gateway, Sender 등 외부 의존성 인터페이스 정의
- Core 내부에 위치 (`core/port/driven/`)
- 기술 구현과 무관한 도메인 용어 사용
- 각 외부 시스템마다 별도 Port 정의

---

## 4. Application Core

### 4.1 Domain Entity

**핵심 원칙:**
- Clean Architecture의 Entity와 동일한 패턴
- private 필드 + Getter로 캡슐화
- Factory Method로 생성 시 유효성 검사
- 비즈니스 메서드에서 상태 변경

### 4.2 Application Service

Application Service는 **Driving Port를 구현**하고 **Driven Port를 사용**합니다.

**핵심 패턴:**
- Driving Port 인터페이스 구현
- Driven Port를 생성자 주입
- 비즈니스 흐름 조율 (유효성 검사 → 비즈니스 규칙 → 엔티티 생성 → 저장)

**Go 예시** (internal/core/service/user_service.go):
```go
type UserService struct {
    userRepo    driven.UserRepository
    emailSender driven.EmailSender
}

var _ driving.UserService = (*UserService)(nil)  // Driving Port 구현 확인

func (s *UserService) CreateUser(ctx context.Context, input driving.CreateUserInput) (*entity.User, error) {
    // 1. 값 객체 생성
    email, err := valueobject.NewEmail(input.Email)
    if err != nil {
        return nil, err
    }

    // 2. 비즈니스 규칙 검사
    existing, err := s.userRepo.FindByEmail(ctx, email)
    if err != nil && !errors.Is(err, ErrNotFound) {
        return nil, err
    }
    if existing != nil {
        return nil, ErrEmailAlreadyExists
    }

    // 3. 엔티티 생성
    user, err := entity.NewUser(email, input.Name)
    if err != nil {
        return nil, err
    }

    // 4. 저장
    if err := s.userRepo.Save(ctx, user); err != nil {
        return nil, err
    }

    // 5. 부수 효과 (이메일 발송)
    if err := s.emailSender.Send(ctx, email.String(), "Welcome!", "Welcome!"); err != nil {
        // 로깅 후 계속 진행 또는 에러 반환 (비즈니스 규칙에 따라)
        return nil, err
    }

    return user, nil
}
```

**TypeScript 예시** (src/core/services/UserService.ts):
```typescript
export class UserService implements IUserService {
  constructor(
    private readonly userRepository: IUserRepository,
    private readonly emailSender: IEmailSender,
  ) {}

  async createUser(input: CreateUserInput): Promise<User> {
    const existing = await this.userRepository.findByEmail(Email.create(input.email));
    if (existing) throw new EmailAlreadyExistsError();
    const user = User.create(input.email, input.name);
    await this.userRepository.save(user);
    await this.emailSender.send(input.email, 'Welcome!', 'Welcome!');
    return user;
  }
}
```

---

## 5. Adapter 구현

### 5.1 Driving Adapter (HTTP Handler)

**핵심 원칙:**
- Driving Port(UseCase 인터페이스)를 주입받아 호출
- HTTP 요청 → Input DTO 변환 → Port 호출 → 응답 변환
- 비즈니스 로직 없음 (변환과 호출만)

### 5.2 Driven Adapter (Repository)

**핵심 원칙:**
- Driven Port 인터페이스 구현
- `var _ Port = (*Impl)(nil)` 로 구현 확인 (Go)
- DB 모델 ↔ Entity 변환 담당
- 기술 구현 세부사항 캡슐화

**Go 예시** (internal/adapter/driven/persistence/postgres/user_repository.go):
```go
type UserRepository struct {
    db *sql.DB
}

var _ driven.UserRepository = (*UserRepository)(nil)  // Driven Port 구현 확인

func (r *UserRepository) Save(ctx context.Context, user *entity.User) error {
    query := `INSERT INTO users (id, email, name) VALUES ($1, $2, $3)
              ON CONFLICT (id) DO UPDATE SET email = EXCLUDED.email, name = EXCLUDED.name`
    _, err := r.db.ExecContext(ctx, query, user.ID(), user.Email().String(), user.Name())
    return err
}
```

---

## 6. 의존성 주입

**핵심 원칙:**
- 조립 순서: Driven Adapters → Application Services → Driving Adapters
- Port 인터페이스에 구현체 바인딩
- Go: Wire, 수동 DI / TypeScript: TSyringe, InversifyJS

---

## 7. 어댑터 교체

Hexagonal Architecture의 강점은 **어댑터 교체가 용이**하다는 것입니다.

**활용 사례:**
- **테스트**: InMemory Adapter로 외부 시스템 없이 테스트
- **환경별**: 설정에 따라 Postgres/MongoDB/Memory 어댑터 교체
- **마이그레이션**: 기존 어댑터를 새 어댑터로 점진적 교체

---

## 8. 체크리스트

### Port 정의 시
- [ ] Driving Port에 UseCase 인터페이스를 정의했는가?
- [ ] Driven Port에 외부 의존성 인터페이스를 정의했는가?
- [ ] Port가 Core 내부에 위치하는가?
- [ ] Port가 도메인 언어를 사용하는가? (기술적 용어 X)

### Adapter 구현 시
- [ ] Driving Adapter가 Driving Port를 호출하는가?
- [ ] Driven Adapter가 Driven Port를 구현하는가?
- [ ] Adapter가 Core를 import하는가? (Core가 Adapter를 import하면 안됨)
- [ ] 어댑터 교체가 가능한 구조인가?

### 테스트 시
- [ ] Mock Adapter로 Application Service를 테스트할 수 있는가?
- [ ] 외부 시스템 없이 테스트가 가능한가?

---

## 9. 금지 사항

- [ ] Core에서 Adapter import
- [ ] Entity에서 외부 라이브러리 의존
- [ ] Port 없이 직접 Adapter 호출
- [ ] Adapter 간 직접 통신
- [ ] Driving Adapter에서 비즈니스 로직 구현
