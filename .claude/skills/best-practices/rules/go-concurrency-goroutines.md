---
title: Goroutines with Error Handling
impact: HIGH
impactDescription: Safe concurrent execution, error propagation
tags: go, concurrency, goroutines, errors, channels
---

## Goroutines with Error Handling

**Impact: HIGH - Safe concurrent execution, error propagation**

Pass errors from goroutines through channels for proper handling.

**Incorrect:**

```go
// No error handling
func ProcessUsers(userIDs []string) []*User {
    var users []*User
    for _, id := range userIDs {
        go func() {
            user, _ := GetUser(id)  // Ignoring errors
            users = append(users, user)  // race condition
        }()
    }
    return users
}
```

**Correct:**

```go
func ProcessUsers(userIDs []string) error {
    errCh := make(chan error, len(userIDs))
    resultCh := make(chan *User, len(userIDs))

    for _, id := range userIDs {
        go func(userID string) {
            user, err := GetUser(userID)
            if err != nil {
                errCh <- err
                return
            }
            resultCh <- user
        }(id)  // Note: variable capture
    }

    // Collect results
    var users []*User
    for i := 0; i < len(userIDs); i++ {
        select {
        case user := <-resultCh:
            users = append(users, user)
        case err := <-errCh:
            return fmt.Errorf("processing failed: %w", err)
        }
    }

    return nil
}
```

**Why**: Errors from goroutines should be passed through channels for handling. Be careful with variable capture (pass as parameter) and race conditions (use channels or mutex).

Reference: [Go Blog - Share Memory By Communicating](https://go.dev/blog/codelab-share)
