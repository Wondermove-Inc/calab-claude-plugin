---
title: Custom Error Types
impact: HIGH
impactDescription: Structured error information, type-based handling
tags: go, errors, custom-errors, error-interface
---

## Custom Error Types

**Impact: HIGH - Structured error information, type-based handling**

Create custom error types with relevant context for granular handling.

**Incorrect:**

```go
// Returns only string
func GetUser(id string) (*User, error) {
    user, err := db.QueryUser(id)
    if err != nil {
        if err == sql.ErrNoRows {
            return nil, errors.New("user not found")
        }
        return nil, err
    }
    return user, nil
}
```

**Correct:**

```go
type ValidationError struct {
    Field string
    Value interface{}
    Msg   string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s (value: %v)", e.Field, e.Msg, e.Value)
}

type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}

func GetUser(id string) (*User, error) {
    user, err := db.QueryUser(id)
    if err != nil {
        if err == sql.ErrNoRows {
            return nil, &NotFoundError{Resource: "user", ID: id}
        }
        return nil, fmt.Errorf("database error: %w", err)
    }
    return user, nil
}

// Usage: Type checking
user, err := GetUser("123")
if err != nil {
    var notFoundErr *NotFoundError
    if errors.As(err, &notFoundErr) {
        log.Printf("user not found: %s", notFoundErr.ID)
    }
}
```

**Why**: Using custom error types allows structuring error information and enables type-based error handling with `errors.As()`.

Reference: [Go Blog - Error handling and Go](https://go.dev/blog/error-handling-and-go)
