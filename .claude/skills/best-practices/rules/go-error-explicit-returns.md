---
title: Explicit Error Returns
impact: CRITICAL
impactDescription: Go idiom, prevents silent failures
tags: go, errors, returns, handling
---

## Explicit Error Returns

**Impact: CRITICAL - Go idiom, prevents silent failures**

Always return errors explicitly and check them at call sites.

**Incorrect:**

```go
// Ignoring errors or using panic
func GetUser(id string) *User {
    user, err := db.QueryUser(id)
    if err != nil {
        panic(err)  // terminates program
    }
    return user
}

// Or ignoring errors
user, _ := db.QueryUser(id)
```

**Correct:**

```go
func GetUser(id string) (*User, error) {
    if id == "" {
        return nil, fmt.Errorf("user ID cannot be empty")
    }

    user, err := db.QueryUser(id)
    if err != nil {
        return nil, fmt.Errorf("failed to query user: %w", err)
    }

    return user, nil
}

// Usage
user, err := GetUser("123")
if err != nil {
    log.Printf("error getting user: %v", err)
    return err
}
// Use user object
```

**Why**: Go encourages explicit error handling. Use panic only for unrecoverable situations (like programming errors), and never ignore errors.

Reference: [Effective Go - Errors](https://go.dev/doc/effective_go#errors)
