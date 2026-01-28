# Clean Architecture 베스트 프랙티스

> 이 문서는 Clean Architecture 구현 시 **반드시** 참조해야 합니다.

---

## 1. 개요

### 1.1 4-레이어 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                     │
│            (HTTP Server, DB, Config, DI Container)          │
├─────────────────────────────────────────────────────────────┤
│                      Adapters Layer                         │
│           (Handler/Controller, Repository, Gateway)         │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                        │
│                   (UseCase, DTO, Port)                      │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                           │
│          (Entity, Value Object, Repository Interface)       │
└─────────────────────────────────────────────────────────────┘
                ↑ 의존성 방향 (안쪽으로만)
```

### 1.2 의존성 규칙 (The Dependency Rule)

```
Infrastructure → Adapters → Application → Domain
      ↓              ↓           ↓          ↓
  프레임워크     컨트롤러    비즈니스    순수 엔티티
    /DB        리포지토리    로직
```

**절대 불변의 규칙**: 내부 레이어는 외부 레이어를 절대 참조하지 않습니다.

| 레이어 | 허용된 Import | 금지된 Import |
|--------|---------------|---------------|
| **Domain** | 표준 라이브러리만 | Application, Adapters, Infrastructure |
| **Application** | Domain | Adapters, Infrastructure |
| **Adapters** | Domain, Application | Infrastructure |
| **Infrastructure** | 모두 허용 | - |

---

## 2. 레이어별 역할

### 2.1 Domain Layer (가장 안쪽)

**역할**: 핵심 비즈니스 규칙, 엔티티, 값 객체

**포함 요소**:
- **Entity**: 비즈니스 엔티티 (고유 식별자 보유)
- **Value Object**: 불변 값 객체 (동등성으로 비교)
- **Repository Interface**: 리포지토리 인터페이스 (구현 아님)
- **Domain Error**: 도메인 에러

**규칙**:
- 외부 라이브러리 import 금지 (표준 라이브러리만)
- 프레임워크 코드 참조 금지
- 순수 언어만 사용

### 2.2 Application Layer

**역할**: 비즈니스 유스케이스 구현

**포함 요소**:
- **UseCase**: 비즈니스 로직 조율
- **DTO**: 데이터 전송 객체
- **Port**: 외부 서비스 인터페이스

**규칙**:
- Domain 레이어만 import 가능
- 구현체가 아닌 인터페이스에 의존
- 하나의 유스케이스는 하나의 비즈니스 규칙

### 2.3 Adapters Layer

**역할**: 포트/인터페이스 구현, 데이터 변환

**포함 요소**:
- **Controller/Handler**: HTTP 요청 처리
- **Repository Impl**: 리포지토리 구현
- **Gateway**: 외부 서비스 구현
- **Presenter**: 응답 포맷터

**규칙**:
- Domain, Application만 import 가능
- 포트/인터페이스 구현
- 데이터 변환 담당 (toDomain, toPersistence)

### 2.4 Infrastructure Layer (가장 바깥)

**역할**: 프레임워크 설정, 의존성 조립

**포함 요소**:
- **HTTP Server**: 웹 서버 설정
- **Database**: DB 연결 설정
- **Config**: 환경 설정
- **DI Container**: 의존성 주입

**규칙**:
- 모든 레이어 import 가능
- 프레임워크 설정만 담당
- DI 컨테이너에서 의존성 조립

---

## 3. 디렉토리 구조

### 3.1 Go 프로젝트

```
internal/
├── domain/                    # Domain Layer
│   ├── entity/                # 엔티티
│   ├── valueobject/           # 값 객체
│   ├── repository/            # 리포지토리 인터페이스
│   └── errors/                # 도메인 에러
│
├── application/               # Application Layer
│   ├── usecase/               # 유스케이스
│   ├── dto/                   # 데이터 전송 객체
│   └── port/                  # 외부 서비스 인터페이스
│
├── adapters/                  # Adapters Layer
│   ├── handler/               # HTTP 핸들러
│   ├── repository/            # 리포지토리 구현
│   └── gateway/               # 외부 서비스 구현
│
└── infrastructure/            # Infrastructure Layer
    ├── http/                  # HTTP 서버 설정
    ├── database/              # DB 설정
    ├── config/                # 환경 설정
    └── di/                    # 의존성 주입
```

### 3.2 TypeScript 프로젝트

```
src/
├── domain/                    # Domain Layer
│   ├── entities/              # 엔티티
│   ├── value-objects/         # 값 객체
│   ├── interfaces/            # 리포지토리 인터페이스
│   └── errors/                # 도메인 에러
│
├── application/               # Application Layer
│   ├── use-cases/             # 유스케이스
│   ├── dtos/                  # 데이터 전송 객체
│   └── ports/                 # 외부 서비스 인터페이스
│
├── adapters/                  # Adapters Layer
│   ├── controllers/           # HTTP 컨트롤러
│   ├── repositories/          # 리포지토리 구현
│   └── gateways/              # 외부 서비스 구현
│
└── infrastructure/            # Infrastructure Layer
    ├── http/                  # HTTP 서버 설정
    ├── database/              # DB 설정
    ├── config/                # 환경 설정
    └── di/                    # 의존성 주입
```

---

## 4. 파일명 컨벤션

### 4.1 Go

| 항목 | 컨벤션 | 예시 |
|------|--------|------|
| 엔티티 | snake_case | `user.go`, `order.go` |
| 값 객체 | snake_case | `email.go`, `money.go` |
| 인터페이스 | snake_case | `user_repository.go` |
| 유스케이스 | snake_case | `create_user.go` |
| DTO | snake_case | `create_user_input.go` |
| 핸들러 | snake_case | `user_handler.go` |

### 4.2 TypeScript

| 항목 | 컨벤션 | 예시 |
|------|--------|------|
| 엔티티 | PascalCase | `User.ts`, `Order.ts` |
| 값 객체 | PascalCase | `Email.ts`, `Money.ts` |
| 인터페이스 | I + PascalCase | `IUserRepository.ts` |
| 유스케이스 | PascalCase + UseCase | `CreateUserUseCase.ts` |
| DTO | PascalCase + Dto | `CreateUserDto.ts` |
| 컨트롤러 | PascalCase + Controller | `UserController.ts` |

---

## 5. Domain Layer 구현

### 5.1 Entity

**핵심 패턴**:
- private 필드 + Getter로 캡슐화
- Factory Method (`NewUser`, `create`)로 생성 시 유효성 검사
- Reconstitute 메서드로 DB에서 복원 (검증 없이)
- 비즈니스 메서드에서 상태 변경 + 불변 조건 검사

**Go 예시** (internal/domain/entity/user.go):
```go
type User struct {
    id    string
    email valueobject.Email
    name  string
}

// NewUser 팩토리 메서드 - 생성 시 유효성 검사
func NewUser(email valueobject.Email, name string) (*User, error) {
    if name == "" {
        return nil, errors.NewValidationError("name", "required")
    }
    return &User{id: uuid.New().String(), email: email, name: name}, nil
}

// ReconstituteUser DB에서 복원 - 검증 없이
func ReconstituteUser(id string, email valueobject.Email, name string) *User {
    return &User{id: id, email: email, name: name}
}

// Getter 메서드
func (u *User) ID() string    { return u.id }
func (u *User) Email() valueobject.Email { return u.email }
func (u *User) Name() string  { return u.name }
```

**TypeScript 예시** (src/domain/entities/User.ts):
```typescript
export class User {
  private constructor(private readonly _id: string, private _name: string) {}

  // 팩토리 메서드 - 생성 시 유효성 검사
  static create(props: CreateUserProps): User {
    if (props.name.length < 2) throw new ValidationError('name', 'Min 2 chars');
    return new User(crypto.randomUUID(), props.name);
  }

  // DB에서 복원 - 검증 없이
  static reconstitute(props: UserProps): User {
    return new User(props.id, props.name);
  }

  // Getter 메서드
  get id(): string { return this._id; }
  get name(): string { return this._name; }
}
```

### 5.2 Value Object

**핵심 원칙**:
- 불변성 (Immutability)
- 동등성 비교 (Equality by value)
- 자기 검증 (Self-validation)
- private 생성자 + Factory Method 패턴

### 5.3 Repository Interface

**핵심 원칙**:
- Domain 레이어에 인터페이스 정의
- 구현체는 Adapters 레이어에 위치
- Context 전파 (Go), Promise 반환 (TypeScript)

---

## 6. Application Layer 구현

### 6.1 UseCase

**핵심 패턴**:
- Repository 인터페이스를 생성자 주입
- Execute 메서드에서 비즈니스 흐름 조율
- 입력 검증 → 비즈니스 규칙 검사 → 엔티티 생성 → 저장 → 응답 반환

**Go 예시** (internal/application/usecase/user/create_user.go):
```go
type CreateUserUseCase struct {
    userRepo repository.UserRepository
}

func (uc *CreateUserUseCase) Execute(ctx context.Context, input dto.CreateUserInput) (*dto.UserResponse, error) {
    // 1. 값 객체 생성
    email, err := valueobject.NewEmail(input.Email)
    if err != nil {
        return nil, err
    }

    // 2. 비즈니스 규칙 검사
    existing, err := uc.userRepo.FindByEmail(ctx, email)
    if err != nil && !errors.Is(err, ErrNotFound) {
        return nil, err
    }
    if existing != nil {
        return nil, errors.NewConflictError("email exists")
    }

    // 3. 엔티티 생성
    user, err := entity.NewUser(email, input.Name)
    if err != nil {
        return nil, err
    }

    // 4. 저장
    if err := uc.userRepo.Save(ctx, user); err != nil {
        return nil, err
    }

    return dto.UserResponseFrom(user), nil
}
```

**TypeScript 예시** (src/application/use-cases/user/CreateUserUseCase.ts):
```typescript
export class CreateUserUseCase {
  constructor(private readonly userRepository: IUserRepository) {}

  async execute(input: CreateUserDto): Promise<UserResponseDto> {
    const existing = await this.userRepository.findByEmail(input.email);
    if (existing) throw new ConflictError('email exists');
    const user = User.create({ email: input.email, name: input.name });
    await this.userRepository.save(user);
    return UserResponseDto.from(user);
  }
}
```

### 6.2 DTO

**핵심 원칙**:
- Input DTO: 요청 데이터 + 유효성 검사
- Output DTO: 응답 데이터 + Entity → DTO 변환 메서드
- 레이어 경계에서 데이터 변환 담당

---

## 7. Adapters Layer 구현

### 7.1 HTTP Handler/Controller

**핵심 원칙**:
- UseCase를 주입받아 사용
- HTTP 요청 → DTO 변환 → UseCase 호출 → 응답 반환
- 에러 핸들링은 미들웨어 또는 handleError 메서드로 위임

### 7.2 Repository Implementation

**핵심 원칙**:
- Domain의 Repository 인터페이스 구현
- `toDomain()`: DB 모델 → Entity 변환
- `toPersistence()`: Entity → DB 모델 변환
- Go: `var _ Interface = (*Impl)(nil)` 로 인터페이스 구현 확인

---

## 8. Infrastructure Layer 구현

### 8.1 DI Container

**핵심 원칙**:
- 의존성 조립 순서: Infrastructure → Repository → UseCase → Handler
- 모든 의존성을 한 곳에서 관리
- 인터페이스에 구현체를 바인딩

---

## 9. 체크리스트

### 코드 생성 시 확인

- [ ] 레이어 위치가 올바른가?
- [ ] 의존성 방향이 안쪽으로만 향하는가?
- [ ] 인터페이스가 Domain에 정의되어 있는가?
- [ ] DTO로 레이어 경계가 명확한가?
- [ ] 비즈니스 로직이 엔티티/유스케이스에 있는가?
- [ ] 테스트 가능한 구조인가?

### Go 전용

- [ ] Context가 첫 번째 파라미터인가?
- [ ] 인터페이스 구현 확인 (`var _ Interface = (*Impl)(nil)`)

### TypeScript 전용

- [ ] Path alias 설정이 올바른가?
- [ ] `any` 타입을 남용하지 않았는가?

---

## 10. 금지 사항

| 위반 | 설명 |
|------|------|
| Domain에서 외부 라이브러리 import | 표준 라이브러리만 허용 |
| Application에서 Adapters/Infrastructure import | 인터페이스만 의존 |
| Handler/Controller에서 직접 DB 접근 | UseCase를 통해서만 접근 |
| 엔티티 직접 노출 | DTO로 변환하여 반환 |
| 순환 import | 의존성 방향 위반 |
| Context 미전파 (Go) | 모든 함수에 Context 전달 |
