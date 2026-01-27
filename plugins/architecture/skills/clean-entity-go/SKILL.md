---
name: architecture:clean-entity-go
description: Go 도메인 엔티티를 생성합니다. 클린 아키텍처 Domain 레이어에 엔티티, 값 객체, 리포지토리 인터페이스를 생성합니다.
allowed-tools: Write, Edit, Glob
argument-hint: <EntityName> [--with-repository]
user-invocable: true
---

# /architecture:clean-entity-go - Go 도메인 엔티티 생성

## 설명
클린 아키텍처의 Domain 레이어에 새로운 Go 엔티티를 생성합니다.

## 사용법
```
/architecture:clean-entity-go <EntityName>
/architecture:clean-entity-go User
/architecture:clean-entity-go Product --with-repository
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--with-repository` | 리포지토리 인터페이스도 함께 생성 |
| `--with-value-objects` | 관련 값 객체 생성 |

## 실행 순서

### 1. 사용자에게 엔티티 속성 질문

```
엔티티 '{EntityName}'의 속성을 정의해주세요:
1. 필수 속성 (예: email, name)
2. 선택 속성 (예: bio, avatar)
3. 값 객체로 분리할 속성 (예: Email, Money)
```

### 2. 파일 생성

#### internal/domain/entity/{entity}.go

> `{module}`은 go.mod의 모듈명으로 대체됩니다.

```go
package entity

import (
	"time"

	"github.com/google/uuid"
	"{module}/internal/domain/errors"
	"{module}/internal/domain/valueobject"
)

// {EntityName} 도메인 엔티티
type {EntityName} struct {
	id        string
	email     valueobject.Email
	name      string
	createdAt time.Time
	updatedAt time.Time
}

// New{EntityName} 새 엔티티 생성 (Factory Method)
func New{EntityName}(email valueobject.Email, name string) (*{EntityName}, error) {
	if name == "" {
		return nil, errors.NewValidationError("name", "name is required")
	}
	if len(name) < 2 {
		return nil, errors.NewValidationError("name", "name must be at least 2 characters")
	}

	now := time.Now()
	return &{EntityName}{
		id:        uuid.New().String(),
		email:     email,
		name:      name,
		createdAt: now,
		updatedAt: now,
	}, nil
}

// Reconstitute DB에서 엔티티 복원
func Reconstitute{EntityName}(id string, email valueobject.Email, name string, createdAt, updatedAt time.Time) *{EntityName} {
	return &{EntityName}{
		id:        id,
		email:     email,
		name:      name,
		createdAt: createdAt,
		updatedAt: updatedAt,
	}
}

// Getters (불변성 유지)

// ID 엔티티 ID 반환
func (e *{EntityName}) ID() string {
	return e.id
}

// Email 이메일 반환
func (e *{EntityName}) Email() valueobject.Email {
	return e.email
}

// Name 이름 반환
func (e *{EntityName}) Name() string {
	return e.name
}

// CreatedAt 생성 시간 반환
func (e *{EntityName}) CreatedAt() time.Time {
	return e.createdAt
}

// UpdatedAt 수정 시간 반환
func (e *{EntityName}) UpdatedAt() time.Time {
	return e.updatedAt
}

// Business Methods

// UpdateName 이름 변경
func (e *{EntityName}) UpdateName(name string) error {
	if len(name) < 2 {
		return errors.NewValidationError("name", "name must be at least 2 characters")
	}
	e.name = name
	e.updatedAt = time.Now()
	return nil
}

// Equals 동등성 비교
func (e *{EntityName}) Equals(other *{EntityName}) bool {
	if other == nil {
		return false
	}
	return e.id == other.id
}
```

### 3. --with-repository 옵션 시 추가 생성

#### internal/domain/repository/{entity}_repository.go
```go
package repository

import (
	"context"

	"{module}/internal/domain/entity"
)

// {EntityName}Repository 리포지토리 인터페이스
type {EntityName}Repository interface {
	// FindByID ID로 엔티티 조회
	FindByID(ctx context.Context, id string) (*entity.{EntityName}, error)

	// FindAll 모든 엔티티 조회
	FindAll(ctx context.Context) ([]*entity.{EntityName}, error)

	// Save 엔티티 저장 (생성 또는 수정)
	Save(ctx context.Context, e *entity.{EntityName}) error

	// Delete 엔티티 삭제
	Delete(ctx context.Context, id string) error
}
```

### 4. --with-value-objects 옵션 시 추가 생성

#### internal/domain/valueobject/email.go
```go
package valueobject

import (
	"regexp"

	"{module}/internal/domain/errors"
)

var emailRegex = regexp.MustCompile(`^[^\s@]+@[^\s@]+\.[^\s@]+$`)

// Email 이메일 값 객체
type Email struct {
	value string
}

// NewEmail 이메일 값 객체 생성
func NewEmail(value string) (Email, error) {
	if value == "" {
		return Email{}, errors.NewValidationError("email", "email is required")
	}
	if !emailRegex.MatchString(value) {
		return Email{}, errors.NewValidationError("email", "invalid email format")
	}
	return Email{value: value}, nil
}

// String 문자열 반환
func (e Email) String() string {
	return e.value
}

// Equals 동등성 비교
func (e Email) Equals(other Email) bool {
	return e.value == other.value
}

// IsZero 빈 값 확인
func (e Email) IsZero() bool {
	return e.value == ""
}
```

## 출력 예시

```
Go 엔티티 'User' 생성 완료

생성된 파일:
- internal/domain/entity/user.go
- internal/domain/repository/user_repository.go
- internal/domain/valueobject/email.go

엔티티 구조:
- id: string (UUID)
- email: Email (Value Object)
- name: string
- createdAt: time.Time
- updatedAt: time.Time

다음 단계:
1. /architecture:clean-usecase-go CreateUser 로 유스케이스 생성
2. Adapters 레이어에서 리포지토리 구현
```

## 엔티티 설계 원칙

1. **불변성**: 가능한 불변 속성 사용 (private 필드 + getter)
2. **캡슐화**: 비공개 필드 + 공개 메서드
3. **비즈니스 로직**: 엔티티 내부에서 처리
4. **검증**: 생성 시점에 유효성 검사 (생성자에서)
5. **프레임워크 독립**: 순수 Go만 사용 (표준 라이브러리 + uuid만)

## 참조
- `skills/clean-architecture-go/SKILL.md`
- `best-practices/clean-architecture-go.md`
