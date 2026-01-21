# Go 클린 아키텍처 베스트 프랙티스

> 이 문서는 Go 프로젝트에서 클린 아키텍처 구현 시 **반드시** 참조해야 합니다.

---

## 1. 레이어 구조

### 1.1 4-레이어 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    cmd/ (진입점)                            │
├─────────────────────────────────────────────────────────────┤
│              internal/infrastructure/                        │
│         (HTTP Server, DB, Config, DI Container)             │
├─────────────────────────────────────────────────────────────┤
│                 internal/adapters/                          │
│          (Handler, Repository 구현, Gateway)                │
├─────────────────────────────────────────────────────────────┤
│               internal/application/                          │
│              (UseCase, DTO, Port)                           │
├─────────────────────────────────────────────────────────────┤
│                 internal/domain/                             │
│        (Entity, Value Object, Repository Interface)         │
└─────────────────────────────────────────────────────────────┘
          ↑ 의존성 방향 (안쪽으로만)
```

### 1.2 의존성 규칙

| 레이어 | 허용된 Import |
|--------|---------------|
| Domain | 표준 라이브러리만 |
| Application | Domain |
| Adapters | Domain, Application |
| Infrastructure | 모든 레이어 |

---

## 2. Domain 레이어

### 2.1 엔티티 (Entity)

```go
// internal/domain/entity/user.go
package entity

import (
    "time"

    "github.com/google/uuid"
    "github.com/myorg/project/internal/domain/errors"
    "github.com/myorg/project/internal/domain/valueobject"
)

// User 사용자 엔티티
type User struct {
    id        string
    email     valueobject.Email
    name      string
    status    UserStatus
    createdAt time.Time
    updatedAt time.Time
}

// NewUser 새 사용자 생성 (Factory Method)
func NewUser(email valueobject.Email, name string) (*User, error) {
    if name == "" {
        return nil, errors.NewValidationError("name", "name is required")
    }

    now := time.Now()
    return &User{
        id:        uuid.New().String(),
        email:     email,
        name:      name,
        status:    UserStatusActive,
        createdAt: now,
        updatedAt: now,
    }, nil
}

// ID getter
func (u *User) ID() string { return u.id }

// Email getter
func (u *User) Email() valueobject.Email { return u.email }

// Name getter
func (u *User) Name() string { return u.name }

// Activate 사용자 활성화 (비즈니스 메서드)
func (u *User) Activate() error {
    if u.status == UserStatusActive {
        return errors.NewValidationError("status", "user is already active")
    }
    u.status = UserStatusActive
    u.updatedAt = time.Now()
    return nil
}
```

### 2.2 값 객체 (Value Object)

```go
// internal/domain/valueobject/email.go
package valueobject

import (
    "regexp"
    "strings"

    "github.com/myorg/project/internal/domain/errors"
)

var emailRegex = regexp.MustCompile(`^[^\s@]+@[^\s@]+\.[^\s@]+$`)

// Email 이메일 값 객체
type Email struct {
    value string
}

// NewEmail 이메일 생성
func NewEmail(value string) (Email, error) {
    normalized := strings.ToLower(strings.TrimSpace(value))
    if normalized == "" {
        return Email{}, errors.NewValidationError("email", "email is required")
    }
    if !emailRegex.MatchString(normalized) {
        return Email{}, errors.NewValidationError("email", "invalid email format")
    }
    return Email{value: normalized}, nil
}

// String 문자열 반환
func (e Email) String() string { return e.value }

// Equals 동등성 비교
func (e Email) Equals(other Email) bool { return e.value == other.value }

// Domain 도메인 추출
func (e Email) Domain() string {
    parts := strings.Split(e.value, "@")
    if len(parts) != 2 {
        return ""
    }
    return parts[1]
}
```

### 2.3 리포지토리 인터페이스

```go
// internal/domain/repository/user_repository.go
package repository

import (
    "context"

    "github.com/myorg/project/internal/domain/entity"
    "github.com/myorg/project/internal/domain/valueobject"
)

// UserRepository 사용자 리포지토리 인터페이스
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*entity.User, error)
    FindByEmail(ctx context.Context, email valueobject.Email) (*entity.User, error)
    FindAll(ctx context.Context, opts ...FindOption) ([]*entity.User, error)
    Save(ctx context.Context, user *entity.User) error
    Delete(ctx context.Context, id string) error
}

// FindOption 조회 옵션
type FindOption func(*findOptions)

type findOptions struct {
    limit  int
    offset int
}

// WithLimit 제한
func WithLimit(limit int) FindOption {
    return func(o *findOptions) { o.limit = limit }
}

// WithOffset 오프셋
func WithOffset(offset int) FindOption {
    return func(o *findOptions) { o.offset = offset }
}
```

---

## 3. Application 레이어

### 3.1 유스케이스 (Use Case)

```go
// internal/application/usecase/user/create_user.go
package user

import (
    "context"

    "github.com/myorg/project/internal/application/dto/user"
    domainEntity "github.com/myorg/project/internal/domain/entity"
    "github.com/myorg/project/internal/domain/errors"
    "github.com/myorg/project/internal/domain/repository"
    "github.com/myorg/project/internal/domain/valueobject"
)

// CreateUserUseCase 사용자 생성 유스케이스
type CreateUserUseCase struct {
    userRepo repository.UserRepository
}

// NewCreateUserUseCase 생성자
func NewCreateUserUseCase(userRepo repository.UserRepository) *CreateUserUseCase {
    return &CreateUserUseCase{userRepo: userRepo}
}

// Execute 실행
func (uc *CreateUserUseCase) Execute(ctx context.Context, input user.CreateUserInput) (*user.UserResponse, error) {
    // 1. 입력 유효성 검사
    if err := input.Validate(); err != nil {
        return nil, err
    }

    // 2. 이메일 값 객체 생성
    email, err := valueobject.NewEmail(input.Email)
    if err != nil {
        return nil, err
    }

    // 3. 이메일 중복 확인 (비즈니스 규칙)
    existing, err := uc.userRepo.FindByEmail(ctx, email)
    if err != nil && !errors.Is(err, errors.ErrNotFound) {
        return nil, err
    }
    if existing != nil {
        return nil, errors.NewValidationError("email", "email already exists")
    }

    // 4. 엔티티 생성
    newUser, err := domainEntity.NewUser(email, input.Name)
    if err != nil {
        return nil, err
    }

    // 5. 저장
    if err := uc.userRepo.Save(ctx, newUser); err != nil {
        return nil, err
    }

    // 6. 응답 반환
    return user.UserResponseFrom(newUser), nil
}
```

### 3.2 DTO (Data Transfer Object)

```go
// internal/application/dto/user/create_user_input.go
package user

import "github.com/myorg/project/internal/domain/errors"

// CreateUserInput 사용자 생성 입력 DTO
type CreateUserInput struct {
    Email string `json:"email"`
    Name  string `json:"name"`
}

// Validate 유효성 검사
func (i *CreateUserInput) Validate() error {
    if i.Email == "" {
        return errors.NewValidationError("email", "email is required")
    }
    if i.Name == "" {
        return errors.NewValidationError("name", "name is required")
    }
    return nil
}
```

```go
// internal/application/dto/user/user_response.go
package user

import (
    "time"

    "github.com/myorg/project/internal/domain/entity"
)

// UserResponse 사용자 응답 DTO
type UserResponse struct {
    ID        string    `json:"id"`
    Email     string    `json:"email"`
    Name      string    `json:"name"`
    CreatedAt time.Time `json:"createdAt"`
}

// UserResponseFrom 엔티티에서 응답 생성
func UserResponseFrom(e *entity.User) *UserResponse {
    return &UserResponse{
        ID:        e.ID(),
        Email:     e.Email().String(),
        Name:      e.Name(),
        CreatedAt: e.CreatedAt(),
    }
}
```

---

## 4. Adapters 레이어

### 4.1 HTTP 핸들러

```go
// internal/adapters/handler/user_handler.go
package handler

import (
    "net/http"

    "github.com/labstack/echo/v4"
    "github.com/myorg/project/internal/application/dto/user"
    userUseCase "github.com/myorg/project/internal/application/usecase/user"
    "github.com/myorg/project/internal/domain/errors"
)

// UserHandler 사용자 핸들러
type UserHandler struct {
    createUser *userUseCase.CreateUserUseCase
    getUser    *userUseCase.GetUserUseCase
}

// NewUserHandler 생성자
func NewUserHandler(
    createUser *userUseCase.CreateUserUseCase,
    getUser *userUseCase.GetUserUseCase,
) *UserHandler {
    return &UserHandler{
        createUser: createUser,
        getUser:    getUser,
    }
}

// Create 사용자 생성
func (h *UserHandler) Create(c echo.Context) error {
    var input user.CreateUserInput
    if err := c.Bind(&input); err != nil {
        return c.JSON(http.StatusBadRequest, ErrorResponse{
            Code:    "INVALID_REQUEST",
            Message: "invalid request body",
        })
    }

    result, err := h.createUser.Execute(c.Request().Context(), input)
    if err != nil {
        return h.handleError(c, err)
    }

    return c.JSON(http.StatusCreated, Response{Data: result})
}

// handleError 에러 처리
func (h *UserHandler) handleError(c echo.Context, err error) error {
    var domainErr *errors.DomainError
    if errors.As(err, &domainErr) {
        switch domainErr.Code {
        case "NOT_FOUND":
            return c.JSON(http.StatusNotFound, ErrorResponse{
                Code:    domainErr.Code,
                Message: domainErr.Message,
            })
        case "VALIDATION":
            return c.JSON(http.StatusBadRequest, ErrorResponse{
                Code:    domainErr.Code,
                Message: domainErr.Message,
            })
        }
    }
    return c.JSON(http.StatusInternalServerError, ErrorResponse{
        Code:    "INTERNAL_ERROR",
        Message: "an error occurred",
    })
}
```

### 4.2 리포지토리 구현체

```go
// internal/adapters/repository/postgres_user_repository.go
package repository

import (
    "context"
    "database/sql"
    stderrors "errors"

    "github.com/myorg/project/internal/domain/entity"
    "github.com/myorg/project/internal/domain/errors"
    "github.com/myorg/project/internal/domain/repository"
    "github.com/myorg/project/internal/domain/valueobject"
)

// PostgresUserRepository PostgreSQL 사용자 리포지토리
type PostgresUserRepository struct {
    db *sql.DB
}

// NewPostgresUserRepository 생성자
func NewPostgresUserRepository(db *sql.DB) *PostgresUserRepository {
    return &PostgresUserRepository{db: db}
}

// 인터페이스 구현 확인
var _ repository.UserRepository = (*PostgresUserRepository)(nil)

// FindByID ID로 사용자 조회
func (r *PostgresUserRepository) FindByID(ctx context.Context, id string) (*entity.User, error) {
    query := `SELECT id, email, name, created_at, updated_at FROM users WHERE id = $1`

    var row userRow
    err := r.db.QueryRowContext(ctx, query, id).Scan(
        &row.ID, &row.Email, &row.Name, &row.CreatedAt, &row.UpdatedAt,
    )
    if err != nil {
        if stderrors.Is(err, sql.ErrNoRows) {
            return nil, errors.NewNotFoundError("user", id)
        }
        return nil, err
    }

    return r.toEntity(&row)
}

// Save 사용자 저장
func (r *PostgresUserRepository) Save(ctx context.Context, user *entity.User) error {
    query := `
        INSERT INTO users (id, email, name, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (id) DO UPDATE SET
            email = EXCLUDED.email,
            name = EXCLUDED.name,
            updated_at = EXCLUDED.updated_at
    `
    _, err := r.db.ExecContext(ctx, query,
        user.ID(),
        user.Email().String(),
        user.Name(),
        user.CreatedAt(),
        user.UpdatedAt(),
    )
    return err
}

// toEntity DB row를 엔티티로 변환
func (r *PostgresUserRepository) toEntity(row *userRow) (*entity.User, error) {
    email, err := valueobject.NewEmail(row.Email)
    if err != nil {
        return nil, err
    }
    return entity.ReconstituteUser(row.ID, email, row.Name, row.CreatedAt, row.UpdatedAt), nil
}
```

---

## 5. Infrastructure 레이어

### 5.1 의존성 주입 컨테이너

```go
// internal/infrastructure/di/container.go
package di

import (
    "github.com/myorg/project/internal/adapters/handler"
    adapterRepo "github.com/myorg/project/internal/adapters/repository"
    userUseCase "github.com/myorg/project/internal/application/usecase/user"
    "github.com/myorg/project/internal/infrastructure/config"
    "github.com/myorg/project/internal/infrastructure/database"
    "github.com/myorg/project/internal/infrastructure/http"
)

// Container 의존성 컨테이너
type Container struct {
    config *config.Config
    server *http.Server

    // Repositories
    userRepo *adapterRepo.PostgresUserRepository

    // Use Cases
    createUserUC *userUseCase.CreateUserUseCase
    getUserUC    *userUseCase.GetUserUseCase

    // Handlers
    userHandler *handler.UserHandler
}

// NewContainer 컨테이너 생성
func NewContainer(cfg *config.Config) (*Container, error) {
    c := &Container{config: cfg}

    // 1. Infrastructure
    db, err := database.NewPostgres(cfg.Database.DSN)
    if err != nil {
        return nil, err
    }

    // 2. Adapters (Repositories)
    c.userRepo = adapterRepo.NewPostgresUserRepository(db)

    // 3. Application (Use Cases)
    c.createUserUC = userUseCase.NewCreateUserUseCase(c.userRepo)
    c.getUserUC = userUseCase.NewGetUserUseCase(c.userRepo)

    // 4. Adapters (Handlers)
    c.userHandler = handler.NewUserHandler(c.createUserUC, c.getUserUC)

    // 5. Infrastructure (HTTP Server)
    c.server = http.NewServer(cfg.Server, c.userHandler)

    return c, nil
}

// Server 서버 반환
func (c *Container) Server() *http.Server {
    return c.server
}
```

---

## 6. 테스트 전략

### 6.1 단위 테스트 (UseCase)

```go
// internal/application/usecase/user/create_user_test.go
func TestCreateUserUseCase_Execute(t *testing.T) {
    tests := []struct {
        name    string
        input   user.CreateUserInput
        setup   func(*MockUserRepository)
        wantErr bool
    }{
        {
            name:  "성공",
            input: user.CreateUserInput{Email: "test@example.com", Name: "Test"},
            setup: func(m *MockUserRepository) {
                m.On("FindByEmail", mock.Anything, mock.Anything).Return(nil, errors.ErrNotFound)
                m.On("Save", mock.Anything, mock.Anything).Return(nil)
            },
            wantErr: false,
        },
        {
            name:  "이메일 중복",
            input: user.CreateUserInput{Email: "existing@example.com", Name: "Test"},
            setup: func(m *MockUserRepository) {
                m.On("FindByEmail", mock.Anything, mock.Anything).Return(&entity.User{}, nil)
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            mockRepo := new(MockUserRepository)
            tt.setup(mockRepo)

            uc := NewCreateUserUseCase(mockRepo)
            _, err := uc.Execute(context.Background(), tt.input)

            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

---

## 7. 체크리스트

### 코드 생성 시 확인

- [ ] 레이어 위치가 올바른가?
- [ ] 의존성 방향이 안쪽으로만 향하는가?
- [ ] Context가 첫 번째 파라미터인가?
- [ ] 인터페이스가 Domain에 정의되어 있는가?
- [ ] DTO로 레이어 경계가 명확한가?
- [ ] 비즈니스 로직이 엔티티/유스케이스에 있는가?
- [ ] 테스트 가능한 구조인가?

---

## 8. 금지 사항

- [ ] Domain에서 외부 라이브러리 import (표준 라이브러리 제외)
- [ ] Application에서 Adapters/Infrastructure import
- [ ] 핸들러에서 직접 DB 접근
- [ ] 엔티티 직접 노출 (DTO 미사용)
- [ ] Context 미전파
- [ ] 순환 import
