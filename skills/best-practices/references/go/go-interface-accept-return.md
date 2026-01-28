---
title: Accept Interfaces, Return Structs
impact: HIGH
impactDescription: Flexible inputs, concrete outputs
tags: go, interfaces, design, proverb
---

## Accept Interfaces, Return Structs

**Impact: HIGH - Flexible inputs, concrete outputs**

Accept interfaces for flexibility, return concrete types for clarity.

**Incorrect:**

```go
// Returning interface (unnecessary)
type UserServiceInterface interface {
    GetUser(id string) (*User, error)
}

func NewUserService(repo UserRepository) UserServiceInterface {
    return &UserService{
        repo: repo,
    }
}
```

**Correct:**

```go
// Accept interfaces, return concrete types
func NewUserService(repo UserRepository) *UserService {
    return &UserService{
        repo: repo,
    }
}

type UserService struct {
    repo UserRepository
}

func (s *UserService) GetUser(id string) (*User, error) {
    return s.repo.GetUser(id)
}
```

**Why**: Returning concrete types allows callers to receive as interface if needed and makes adding methods easier. Interfaces should be defined by consumers, not producers.

**Go proverb**: "Accept interfaces, return structs"

| Parameter | Return |
|-----------|--------|
| Interface (flexible) | Struct (concrete) |
| Caller decides what to pass | Caller decides how to use |

Reference: [Go Proverbs](https://go-proverbs.github.io/)
