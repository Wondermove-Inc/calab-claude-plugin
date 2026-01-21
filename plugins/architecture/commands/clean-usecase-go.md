---
description: Go 유스케이스를 생성합니다. 클린 아키텍처 Application 레이어에 유스케이스, DTO, 포트를 생성합니다.
allowed-tools: Write, Edit, Glob, Read
argument-hint: <UseCaseName> [--entity <Entity>]
---

# /architecture:clean-usecase-go - Go 유스케이스 생성

## 설명
클린 아키텍처의 Application 레이어에 새로운 Go 유스케이스를 생성합니다.

## 사용법
```
/architecture:clean-usecase-go <UseCaseName>
/architecture:clean-usecase-go CreateUser
/architecture:clean-usecase-go GetUserByID --entity User
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--entity <name>` | 연관된 엔티티 지정 |
| `--with-dto` | 입출력 DTO 함께 생성 |
| `--with-test` | 유닛 테스트 파일 생성 |

## 실행 순서

### 1. 사용자에게 유스케이스 정보 질문

```
유스케이스 '{UseCaseName}'의 정보를 입력해주세요:
1. 입력 데이터 (Input DTO)
2. 출력 데이터 (Output DTO)
3. 필요한 의존성 (Repository, Service)
4. 비즈니스 규칙
```

### 2. 파일 생성

#### internal/application/usecase/{entity}/create_{entity}.go
```go
package {entity}

import (
	"context"

	"github.com/myorg/myproject/internal/application/dto/{entity}"
	domainEntity "github.com/myorg/myproject/internal/domain/entity"
	"github.com/myorg/myproject/internal/domain/repository"
	"github.com/myorg/myproject/internal/domain/valueobject"
)

// Create{EntityName}UseCase 생성 유스케이스
type Create{EntityName}UseCase struct {
	repo repository.{EntityName}Repository
}

// NewCreate{EntityName}UseCase 유스케이스 생성자
func NewCreate{EntityName}UseCase(repo repository.{EntityName}Repository) *Create{EntityName}UseCase {
	return &Create{EntityName}UseCase{
		repo: repo,
	}
}

// Execute 유스케이스 실행
func (uc *Create{EntityName}UseCase) Execute(ctx context.Context, input dto.Create{EntityName}Input) (*dto.{EntityName}Response, error) {
	// 1. 입력 유효성 검사
	if err := input.Validate(); err != nil {
		return nil, err
	}

	// 2. 값 객체 생성
	email, err := valueobject.NewEmail(input.Email)
	if err != nil {
		return nil, err
	}

	// 3. 엔티티 생성
	entity, err := domainEntity.New{EntityName}(email, input.Name)
	if err != nil {
		return nil, err
	}

	// 4. 영속화
	if err := uc.repo.Save(ctx, entity); err != nil {
		return nil, err
	}

	// 5. 응답 DTO 반환
	return dto.{EntityName}ResponseFrom(entity), nil
}
```

### 3. DTO 파일 생성

#### internal/application/dto/{entity}/create_{entity}_input.go
```go
package {entity}

import (
	"github.com/myorg/myproject/internal/domain/errors"
)

// Create{EntityName}Input 생성 요청 DTO
type Create{EntityName}Input struct {
	Email string `json:"email"`
	Name  string `json:"name"`
}

// Validate 입력 유효성 검사
func (i *Create{EntityName}Input) Validate() error {
	if i.Email == "" {
		return errors.NewValidationError("email", "email is required")
	}
	if i.Name == "" {
		return errors.NewValidationError("name", "name is required")
	}
	if len(i.Name) < 2 {
		return errors.NewValidationError("name", "name must be at least 2 characters")
	}
	return nil
}
```

#### internal/application/dto/{entity}/{entity}_response.go
```go
package {entity}

import (
	"time"

	"github.com/myorg/myproject/internal/domain/entity"
)

// {EntityName}Response 응답 DTO
type {EntityName}Response struct {
	ID        string    `json:"id"`
	Email     string    `json:"email"`
	Name      string    `json:"name"`
	CreatedAt time.Time `json:"createdAt"`
	UpdatedAt time.Time `json:"updatedAt"`
}

// {EntityName}ResponseFrom 엔티티에서 응답 DTO 생성
func {EntityName}ResponseFrom(e *entity.{EntityName}) *{EntityName}Response {
	return &{EntityName}Response{
		ID:        e.ID(),
		Email:     e.Email().String(),
		Name:      e.Name(),
		CreatedAt: e.CreatedAt(),
		UpdatedAt: e.UpdatedAt(),
	}
}

// {EntityName}ListResponse 목록 응답 DTO
type {EntityName}ListResponse struct {
	Items []*{EntityName}Response `json:"items"`
	Total int                     `json:"total"`
}

// {EntityName}ListResponseFrom 엔티티 목록에서 응답 DTO 생성
func {EntityName}ListResponseFrom(entities []*entity.{EntityName}) *{EntityName}ListResponse {
	items := make([]*{EntityName}Response, len(entities))
	for i, e := range entities {
		items[i] = {EntityName}ResponseFrom(e)
	}
	return &{EntityName}ListResponse{
		Items: items,
		Total: len(items),
	}
}
```

### 4. --with-test 옵션 시 테스트 생성

#### internal/application/usecase/{entity}/create_{entity}_test.go
```go
package {entity}_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"

	"github.com/myorg/myproject/internal/application/dto/{entity}"
	usecase "github.com/myorg/myproject/internal/application/usecase/{entity}"
	domainEntity "github.com/myorg/myproject/internal/domain/entity"
)

// MockRepository 모의 리포지토리
type MockRepository struct {
	mock.Mock
}

func (m *MockRepository) FindByID(ctx context.Context, id string) (*domainEntity.{EntityName}, error) {
	args := m.Called(ctx, id)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*domainEntity.{EntityName}), args.Error(1)
}

func (m *MockRepository) FindAll(ctx context.Context) ([]*domainEntity.{EntityName}, error) {
	args := m.Called(ctx)
	return args.Get(0).([]*domainEntity.{EntityName}), args.Error(1)
}

func (m *MockRepository) Save(ctx context.Context, e *domainEntity.{EntityName}) error {
	args := m.Called(ctx, e)
	return args.Error(0)
}

func (m *MockRepository) Delete(ctx context.Context, id string) error {
	args := m.Called(ctx, id)
	return args.Error(0)
}

func TestCreate{EntityName}UseCase_Execute(t *testing.T) {
	tests := []struct {
		name    string
		input   dto.Create{EntityName}Input
		setup   func(*MockRepository)
		wantErr bool
	}{
		{
			name: "성공적으로 생성",
			input: dto.Create{EntityName}Input{
				Email: "test@example.com",
				Name:  "Test User",
			},
			setup: func(m *MockRepository) {
				m.On("Save", mock.Anything, mock.Anything).Return(nil)
			},
			wantErr: false,
		},
		{
			name: "잘못된 이메일",
			input: dto.Create{EntityName}Input{
				Email: "",
				Name:  "Test User",
			},
			setup:   func(m *MockRepository) {},
			wantErr: true,
		},
		{
			name: "이름 너무 짧음",
			input: dto.Create{EntityName}Input{
				Email: "test@example.com",
				Name:  "A",
			},
			setup:   func(m *MockRepository) {},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockRepo := new(MockRepository)
			tt.setup(mockRepo)

			uc := usecase.NewCreate{EntityName}UseCase(mockRepo)
			result, err := uc.Execute(context.Background(), tt.input)

			if tt.wantErr {
				assert.Error(t, err)
				assert.Nil(t, result)
			} else {
				assert.NoError(t, err)
				assert.NotNil(t, result)
				assert.Equal(t, tt.input.Email, result.Email)
				assert.Equal(t, tt.input.Name, result.Name)
			}

			mockRepo.AssertExpectations(t)
		})
	}
}
```

## 출력 예시

```
✅ Go 유스케이스 'CreateUser' 생성 완료

생성된 파일:
- internal/application/usecase/user/create_user.go
- internal/application/dto/user/create_user_input.go
- internal/application/dto/user/user_response.go
- internal/application/usecase/user/create_user_test.go

의존성:
- UserRepository (Domain)

다음 단계:
1. Adapters 레이어에서 Handler 구현
2. Infrastructure에서 DI 컨테이너에 등록
```

## 유스케이스 설계 원칙

1. **단일 책임**: 하나의 유스케이스 = 하나의 비즈니스 규칙
2. **인터페이스 의존**: 구현체가 아닌 인터페이스에 의존
3. **순수 비즈니스 로직**: 프레임워크/인프라 코드 금지
4. **입출력 분리**: DTO를 통한 명확한 경계
5. **테스트 용이성**: 의존성 주입으로 Mock 가능
6. **Context 전파**: 항상 context.Context를 첫 번째 파라미터로

## 참조
- `skills/clean-architecture-go/SKILL.md`
- `best-practices/clean-architecture-go.md`
