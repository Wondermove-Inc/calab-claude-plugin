---
title: Implicit Interface Implementation
impact: MEDIUM
impactDescription: Loose coupling, easier testing with mocks
tags: go, interfaces, implicit, decoupling
---

## Implicit Interface Implementation

**Impact: MEDIUM - Loose coupling, easier testing with mocks**

Leverage Go's implicit interface implementation for loose coupling.

**Incorrect:**

```go
// Depends on concrete type
func ProcessUser(repo *PostgresUserRepo, id string) error {
    user, err := repo.GetUser(id)
    if err != nil {
        return err
    }
    return repo.SaveUser(user)
}
```

**Correct:**

```go
type UserRepository interface {
    GetUser(id string) (*User, error)
    SaveUser(user *User) error
}

// Implicit implementation (no explicit declaration needed)
type PostgresUserRepo struct {
    db *sql.DB
}

func (r *PostgresUserRepo) GetUser(id string) (*User, error) {
    // Implementation
    return nil, nil
}

func (r *PostgresUserRepo) SaveUser(user *User) error {
    // Implementation
    return nil
}

// Usage: Accept interface type
func ProcessUser(repo UserRepository, id string) error {
    user, err := repo.GetUser(id)
    if err != nil {
        return err
    }
    // Process
    return repo.SaveUser(user)
}
```

**Why**: Depending on interfaces makes it easy to inject mock implementations for testing. No explicit "implements" declaration needed - if the type has the methods, it implements the interface.

Reference: [Go Tour - Interfaces](https://go.dev/tour/methods/9)
