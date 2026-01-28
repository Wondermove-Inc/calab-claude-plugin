---
title: Interface Segregation
impact: HIGH
impactDescription: Clear dependencies, minimal coupling
tags: go, interfaces, segregation, SOLID
---

## Interface Segregation

**Impact: HIGH - Clear dependencies, minimal coupling**

Require only the methods you need from the caller.

**Incorrect:**

```go
// Interface containing all methods
type UserRepository interface {
    GetUser(id string) (*User, error)
    ListUsers() ([]*User, error)
    SaveUser(user *User) error
    DeleteUser(id string) error
}

// Requires full interface when only read is needed
func DisplayUser(repo UserRepository, id string) error {
    user, err := repo.GetUser(id)
    if err != nil {
        return err
    }
    fmt.Println(user)
    return nil
}
```

**Correct:**

```go
// Segregate interfaces by role
type UserReader interface {
    GetUser(id string) (*User, error)
    ListUsers() ([]*User, error)
}

type UserWriter interface {
    SaveUser(user *User) error
    DeleteUser(id string) error
}

// Read-only function
func DisplayUser(reader UserReader, id string) error {
    user, err := reader.GetUser(id)
    if err != nil {
        return err
    }
    fmt.Println(user)
    return nil
}

// Read/Write function
func UpdateUser(repo interface {
    UserReader
    UserWriter
}, id string, updates map[string]interface{}) error {
    user, err := repo.GetUser(id)
    if err != nil {
        return err
    }
    // Update
    return repo.SaveUser(user)
}
```

**Why**: Requiring only necessary methods makes dependencies clear and testing easier. Functions declare exactly what they need.

Reference: [SOLID in Go](https://dave.cheney.net/2016/08/20/solid-go-design)
