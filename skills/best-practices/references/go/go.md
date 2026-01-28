# Go 베스트 프랙티스 (2025)

> 이 문서는 Go(Golang) 코드 생성 시 **반드시** 참조해야 합니다.

---

## 1. 에러 처리 (Error Handling)

### 1.1 기본 에러 처리 패턴

```go
// 에러는 항상 확인하고 처리
func ReadConfig(filename string) (*Config, error) {
    data, err := os.ReadFile(filename)
    if err != nil {
        return nil, fmt.Errorf("reading config file: %w", err)
    }

    var config Config
    if err := json.Unmarshal(data, &config); err != nil {
        return nil, fmt.Errorf("parsing config: %w", err)
    }

    return &config, nil
}
```

### 1.2 에러 래핑 (Error Wrapping)

```go
import (
    "errors"
    "fmt"
)

// 센티널 에러 정의
var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized access")
    ErrValidation   = errors.New("validation failed")
)

// 에러 래핑 (컨텍스트 추가)
func FindUser(id string) (*User, error) {
    user, err := db.FindByID(id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
        }
        return nil, fmt.Errorf("finding user %s: %w", id, err)
    }
    return user, nil
}

// 에러 확인
func HandleUser(id string) {
    user, err := FindUser(id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            // 404 처리
        }
        // 기타 에러 처리
    }
}
```

### 1.3 커스텀 에러 타입

```go
// AppError 커스텀 에러
type AppError struct {
    Code    string
    Message string
    Err     error
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Err)
    }
    return e.Message
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// 생성 헬퍼
func NewNotFoundError(resource, id string) *AppError {
    return &AppError{
        Code:    "NOT_FOUND",
        Message: fmt.Sprintf("%s with id '%s' not found", resource, id),
    }
}

// 타입 확인
func HandleError(err error) {
    var appErr *AppError
    if errors.As(err, &appErr) {
        switch appErr.Code {
        case "NOT_FOUND":
            // 404 처리
        case "VALIDATION":
            // 400 처리
        }
    }
}
```

---

## 2. 프로젝트 구조

### 2.1 표준 레이아웃

```
project/
├── cmd/
│   └── server/
│       └── main.go              # 진입점
├── internal/                     # 비공개 패키지
│   ├── config/
│   │   └── config.go
│   ├── domain/                   # 도메인 모델
│   │   ├── user.go
│   │   └── errors.go
│   ├── service/                  # 비즈니스 로직
│   │   └── user_service.go
│   ├── repository/               # 데이터 접근
│   │   └── user_repository.go
│   └── handler/                  # HTTP 핸들러
│       └── user_handler.go
├── pkg/                          # 공개 패키지
│   └── logger/
│       └── logger.go
├── api/                          # API 스펙
│   └── openapi.yaml
├── go.mod
├── go.sum
└── Makefile
```

### 2.2 패키지 네이밍

```go
// Good - 짧고 명확한 이름
package user
package config
package handler

// Bad - util, common, helper 등 모호한 이름
package util    // ❌
package common  // ❌
package helpers // ❌
```

---

## 3. 인터페이스

### 3.1 작은 인터페이스

```go
// Good - 작고 집중된 인터페이스
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// 조합
type ReadWriter interface {
    Reader
    Writer
}
```

### 3.2 의존성 주입

```go
// Repository 인터페이스 (서비스에서 정의)
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

// Service 구현
type UserService struct {
    repo UserRepository
}

func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}

func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    return s.repo.FindByID(ctx, id)
}

// 테스트용 Mock
type MockUserRepository struct {
    users map[string]*User
}

func (m *MockUserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    if user, ok := m.users[id]; ok {
        return user, nil
    }
    return nil, ErrNotFound
}
```

---

## 4. Context 사용

### 4.1 Context 전파

```go
import "context"

// 항상 첫 번째 파라미터로 context.Context 전달
func (s *UserService) CreateUser(ctx context.Context, input CreateUserInput) (*User, error) {
    // 타임아웃 확인
    if err := ctx.Err(); err != nil {
        return nil, fmt.Errorf("context error: %w", err)
    }

    user := &User{
        ID:    uuid.New().String(),
        Email: input.Email,
        Name:  input.Name,
    }

    if err := s.repo.Save(ctx, user); err != nil {
        return nil, fmt.Errorf("saving user: %w", err)
    }

    return user, nil
}

// HTTP 핸들러에서 context 사용
func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    // 타임아웃 추가
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    user, err := h.service.CreateUser(ctx, input)
    if err != nil {
        // 에러 처리
    }
}
```

---

## 5. 동시성 (Concurrency)

### 5.1 Goroutine 패턴

```go
// WaitGroup으로 goroutine 대기
func ProcessItems(items []Item) error {
    var wg sync.WaitGroup
    errChan := make(chan error, len(items))

    for _, item := range items {
        wg.Add(1)
        go func(item Item) {
            defer wg.Done()
            if err := process(item); err != nil {
                errChan <- err
            }
        }(item)
    }

    wg.Wait()
    close(errChan)

    // 첫 번째 에러 반환
    for err := range errChan {
        return err
    }
    return nil
}
```

### 5.2 Channel 패턴

```go
// Worker Pool 패턴
func WorkerPool(ctx context.Context, jobs <-chan Job, workers int) <-chan Result {
    results := make(chan Result, workers)

    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                select {
                case <-ctx.Done():
                    return
                case results <- process(job):
                }
            }
        }()
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}
```

### 5.3 sync.Mutex 사용

```go
type SafeCounter struct {
    mu    sync.RWMutex
    value int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *SafeCounter) Value() int {
    c.mu.RLock()
    defer c.mu.RUnlock()
    return c.value
}
```

---

## 6. HTTP 서버 (Echo/Gin)

### 6.1 Echo 프레임워크

```go
package main

import (
    "net/http"

    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func main() {
    e := echo.New()

    // 미들웨어
    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    e.Use(middleware.RequestID())

    // 라우트
    api := e.Group("/api/v1")
    {
        api.GET("/users", listUsers)
        api.GET("/users/:id", getUser)
        api.POST("/users", createUser)
    }

    e.Logger.Fatal(e.Start(":8080"))
}

// Handler - 구조화된 응답
func getUser(c echo.Context) error {
    id := c.Param("id")

    user, err := userService.FindByID(c.Request().Context(), id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return c.JSON(http.StatusNotFound, ErrorResponse{
                Code:    "NOT_FOUND",
                Message: "User not found",
            })
        }
        return c.JSON(http.StatusInternalServerError, ErrorResponse{
            Code:    "INTERNAL_ERROR",
            Message: "An error occurred",
        })
    }

    return c.JSON(http.StatusOK, Response{
        Data: user,
    })
}

// 응답 구조체
type Response struct {
    Data interface{} `json:"data"`
}

type ErrorResponse struct {
    Code    string `json:"code"`
    Message string `json:"message"`
}
```

---

## 7. 테스트

### 7.1 테이블 기반 테스트

```go
func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name     string
        price    float64
        rate     float64
        expected float64
        wantErr  bool
    }{
        {
            name:     "10% discount",
            price:    100,
            rate:     0.1,
            expected: 90,
            wantErr:  false,
        },
        {
            name:     "invalid rate",
            price:    100,
            rate:     1.5,
            expected: 0,
            wantErr:  true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := CalculateDiscount(tt.price, tt.rate)

            if (err != nil) != tt.wantErr {
                t.Errorf("wantErr %v, got error %v", tt.wantErr, err)
            }
            if result != tt.expected {
                t.Errorf("expected %v, got %v", tt.expected, result)
            }
        })
    }
}
```

### 7.2 Mock 테스트

```go
// testify/mock 사용
import "github.com/stretchr/testify/mock"

type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func TestUserService_GetUser(t *testing.T) {
    mockRepo := new(MockUserRepository)
    service := NewUserService(mockRepo)

    expectedUser := &User{ID: "1", Name: "Test"}
    mockRepo.On("FindByID", mock.Anything, "1").Return(expectedUser, nil)

    user, err := service.GetUser(context.Background(), "1")

    assert.NoError(t, err)
    assert.Equal(t, expectedUser, user)
    mockRepo.AssertExpectations(t)
}
```

---

## 8. 금지 사항

- [ ] 에러 무시 (`_ = someFunction()`)
- [ ] panic 남용 (복구 불가능한 상황에만)
- [ ] init() 함수 과다 사용
- [ ] 전역 변수
- [ ] 불필요한 interface{} (any) 사용
- [ ] naked return (이름 있는 반환값)
- [ ] context.Background() 남용 (전파 필수)
- [ ] data race (go vet -race 검사 필수)

---

## 9. 체크리스트

코드 생성 시 확인:

- [ ] 모든 에러 처리 및 래핑
- [ ] Context 첫 번째 파라미터
- [ ] 작은 인터페이스 정의
- [ ] 테이블 기반 테스트
- [ ] golangci-lint 통과
- [ ] go vet -race 통과
- [ ] 명확한 패키지 구조
- [ ] 파일 500줄 이하
