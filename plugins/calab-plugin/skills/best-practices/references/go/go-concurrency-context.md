---
title: Context for Cancellation
impact: CRITICAL
impactDescription: Timeout handling, resource cleanup
tags: go, concurrency, context, timeout, cancellation
---

## Context for Cancellation

**Impact: CRITICAL - Timeout handling, resource cleanup**

Use Context for timeouts, cancellation, and request-scoped values.

**Incorrect:**

```go
// Infinite wait without Context
func FetchUsers(ids []string) ([]*User, error) {
    results := make([]*User, 0, len(ids))

    for _, id := range ids {
        user, err := GetUser(id)  // May wait indefinitely
        if err != nil {
            return nil, err
        }
        results = append(results, user)
    }

    return results, nil
}
```

**Correct:**

```go
import "context"

func FetchUsers(ctx context.Context, ids []string) ([]*User, error) {
    results := make([]*User, 0, len(ids))

    for _, id := range ids {
        select {
        case <-ctx.Done():
            return nil, ctx.Err()  // Cancelled
        default:
            user, err := GetUserWithContext(ctx, id)
            if err != nil {
                return nil, err
            }
            results = append(results, user)
        }
    }

    return results, nil
}

// Usage
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

users, err := FetchUsers(ctx, ids)
if err != nil {
    if errors.Is(err, context.DeadlineExceeded) {
        log.Println("timeout")
    }
}
```

**Why**: Using Context makes it easy to implement timeout and cancellation. It propagates through the call stack, allowing coordinated cleanup.

**Context types:**
| Function | Purpose |
|----------|---------|
| `context.WithTimeout` | Deadline after duration |
| `context.WithDeadline` | Deadline at specific time |
| `context.WithCancel` | Manual cancellation |
| `context.WithValue` | Request-scoped values |

Reference: [Go Blog - Context](https://go.dev/blog/context)
