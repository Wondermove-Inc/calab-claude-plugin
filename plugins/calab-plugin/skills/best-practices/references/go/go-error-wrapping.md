---
title: Error Wrapping with %w
impact: HIGH
impactDescription: Preserves error chain, enables errors.Is/As
tags: go, errors, wrapping, fmt
---

## Error Wrapping with %w

**Impact: HIGH - Preserves error chain, enables errors.Is/As**

Use `%w` to wrap errors and preserve the error chain.

**Incorrect:**

```go
// Returns only error string (loses type information)
func ProcessUser(id string) error {
    user, err := GetUser(id)
    if err != nil {
        return fmt.Errorf("process user failed: %v", err)
    }
    return nil
}

// Cannot check original error type
err := ProcessUser("123")
if err != nil {
    // Only string comparison via err.Error() is possible
}
```

**Correct:**

```go
import (
    "errors"
    "fmt"
)

var (
    ErrNotFound = errors.New("resource not found")
    ErrInvalidInput = errors.New("invalid input")
)

func ProcessUser(id string) error {
    user, err := GetUser(id)
    if err != nil {
        // Add context by wrapping error
        return fmt.Errorf("process user failed: %w", err)
    }

    if err := ValidateUser(user); err != nil {
        return fmt.Errorf("validation failed for user %s: %w", id, err)
    }

    return nil
}

// Usage: Check error chain
err := ProcessUser("123")
if err != nil {
    if errors.Is(err, ErrNotFound) {
        // Handle NotFound
    } else if errors.Is(err, ErrInvalidInput) {
        // Handle InvalidInput
    }
}
```

**Why**: Wrapping errors with `%w` allows checking the error chain with `errors.Is()` and `errors.As()`. Context is added while preserving the original error.

Reference: [Go Blog - Working with Errors](https://go.dev/blog/go1.13-errors)
