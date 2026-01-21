---
description: Go 프로젝트용 클린 아키텍처 4-레이어 디렉토리 구조를 초기화합니다. 도메인, 애플리케이션, 어댑터, 인프라 레이어를 자동 생성합니다.
allowed-tools: Write, Edit, Bash
---

# /architecture:clean-init-go - Go 클린 아키텍처 초기화

## 설명
Go 프로젝트에 클린 아키텍처 디렉토리 구조와 기본 파일들을 생성합니다.

## 사용법
```
/architecture:clean-init-go
/architecture:clean-init-go --module github.com/myorg/myproject
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--module <name>` | go.mod 모듈 이름 지정 |
| `--with-echo` | Echo 프레임워크 설정 포함 |
| `--with-gin` | Gin 프레임워크 설정 포함 |

## 실행 순서

### 1. 디렉토리 구조 생성

다음 디렉토리 구조를 생성합니다:

```
project/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── domain/
│   │   ├── entity/
│   │   ├── valueobject/
│   │   ├── repository/
│   │   └── errors/
│   ├── application/
│   │   ├── usecase/
│   │   ├── dto/
│   │   └── port/
│   ├── adapters/
│   │   ├── handler/
│   │   ├── repository/
│   │   └── gateway/
│   └── infrastructure/
│       ├── http/
│       ├── database/
│       ├── config/
│       └── di/
├── pkg/
│   └── logger/
├── api/
└── Makefile
```

### 2. 기본 파일 생성

#### cmd/server/main.go

> 💡 아래 `{module}`은 `--module` 옵션으로 지정된 값으로 대체됩니다.

```go
package main

import (
	"log"

	"{module}/internal/infrastructure/config"
	"{module}/internal/infrastructure/di"
)

func main() {
	// 설정 로드
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	// 의존성 주입 컨테이너 초기화
	container, err := di.NewContainer(cfg)
	if err != nil {
		log.Fatalf("failed to initialize container: %v", err)
	}

	// 서버 시작
	if err := container.Server().Start(); err != nil {
		log.Fatalf("failed to start server: %v", err)
	}
}
```

#### internal/domain/errors/errors.go
```go
package errors

import (
	"errors"
	"fmt"
)

// 센티널 에러 정의
var (
	ErrNotFound     = errors.New("resource not found")
	ErrUnauthorized = errors.New("unauthorized access")
	ErrValidation   = errors.New("validation failed")
	ErrConflict     = errors.New("resource conflict")
)

// DomainError 도메인 에러
type DomainError struct {
	Code    string
	Message string
	Err     error
}

func (e *DomainError) Error() string {
	if e.Err != nil {
		return fmt.Sprintf("%s: %v", e.Message, e.Err)
	}
	return e.Message
}

func (e *DomainError) Unwrap() error {
	return e.Err
}

// NewNotFoundError 리소스 미발견 에러
func NewNotFoundError(resource, id string) *DomainError {
	return &DomainError{
		Code:    "NOT_FOUND",
		Message: fmt.Sprintf("%s with id '%s' not found", resource, id),
		Err:     ErrNotFound,
	}
}

// NewValidationError 유효성 검사 에러
func NewValidationError(field, message string) *DomainError {
	return &DomainError{
		Code:    "VALIDATION",
		Message: fmt.Sprintf("validation failed for %s: %s", field, message),
		Err:     ErrValidation,
	}
}
```

#### internal/application/usecase/usecase.go
```go
package usecase

import "context"

// UseCase 유스케이스 인터페이스
type UseCase[TInput any, TOutput any] interface {
	Execute(ctx context.Context, input TInput) (TOutput, error)
}
```

#### internal/infrastructure/config/config.go
```go
package config

import (
	"os"
)

// Config 애플리케이션 설정
type Config struct {
	Server   ServerConfig
	Database DatabaseConfig
}

// ServerConfig HTTP 서버 설정
type ServerConfig struct {
	Port string
	Host string
}

// DatabaseConfig 데이터베이스 설정
type DatabaseConfig struct {
	DSN string
}

// Load 환경변수에서 설정 로드
func Load() (*Config, error) {
	return &Config{
		Server: ServerConfig{
			Port: getEnv("SERVER_PORT", "8080"),
			Host: getEnv("SERVER_HOST", "0.0.0.0"),
		},
		Database: DatabaseConfig{
			DSN: getEnv("DATABASE_DSN", ""),
		},
	}, nil
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
```

#### internal/infrastructure/di/container.go
```go
package di

import (
	"{module}/internal/infrastructure/config"
)

// Container 의존성 주입 컨테이너
type Container struct {
	config *config.Config
	server Server
	// 리포지토리, 유스케이스 등 추가
}

// Server 서버 인터페이스
type Server interface {
	Start() error
}

// NewContainer 컨테이너 생성
func NewContainer(cfg *config.Config) (*Container, error) {
	c := &Container{
		config: cfg,
	}

	// 의존성 초기화 순서:
	// 1. Infrastructure (DB, 외부 서비스)
	// 2. Adapters (리포지토리 구현체)
	// 3. Application (유스케이스)
	// 4. Adapters (핸들러)
	// 5. Infrastructure (HTTP 서버)

	return c, nil
}

// Server 서버 반환
func (c *Container) Server() Server {
	return c.server
}
```

#### Makefile
```makefile
.PHONY: build run test lint clean

# 변수
APP_NAME := server
BUILD_DIR := ./bin

# 빌드
build:
	go build -o $(BUILD_DIR)/$(APP_NAME) ./cmd/server

# 실행
run:
	go run ./cmd/server

# 테스트
test:
	go test -v -race ./...

# 테스트 커버리지
test-coverage:
	go test -v -race -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

# 린트
lint:
	golangci-lint run ./...

# 정리
clean:
	rm -rf $(BUILD_DIR)
	rm -f coverage.out coverage.html

# 의존성 정리
tidy:
	go mod tidy

# 모든 검사
check: lint test
```

### 3. .claude/CLEAN_ARCHITECTURE_GO.md 생성

프로젝트 루트에 Go용 클린 아키텍처 가이드 문서를 생성합니다.

## 출력 예시

```
✅ Go 클린 아키텍처 초기화 완료

생성된 구조:
├── cmd/server/              (진입점)
├── internal/domain/         (엔티티 레이어)
├── internal/application/    (유스케이스 레이어)
├── internal/adapters/       (인터페이스 어댑터 레이어)
├── internal/infrastructure/ (프레임워크 레이어)
└── pkg/                     (공개 패키지)

생성된 파일:
- cmd/server/main.go
- internal/domain/errors/errors.go
- internal/application/usecase/usecase.go
- internal/infrastructure/config/config.go
- internal/infrastructure/di/container.go
- Makefile

다음 단계:
1. /architecture:clean-entity-go User 로 첫 번째 엔티티 생성
2. /architecture:clean-usecase-go CreateUser 로 유스케이스 생성
```

## 참조
- `skills/clean-architecture-go/SKILL.md`
- `best-practices/clean-architecture-go.md`
