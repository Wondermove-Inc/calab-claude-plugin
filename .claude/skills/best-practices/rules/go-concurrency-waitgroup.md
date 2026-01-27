---
title: WaitGroup for Synchronization
impact: HIGH
impactDescription: Reliable goroutine completion tracking
tags: go, concurrency, waitgroup, sync
---

## WaitGroup for Synchronization

**Impact: HIGH - Reliable goroutine completion tracking**

Use WaitGroup to wait for all goroutines to complete.

**Incorrect:**

```go
// Using sleep without WaitGroup (unreliable)
func ProcessAllUsers(userIDs []string) {
    for _, id := range userIDs {
        go func(userID string) {
            ProcessUser(userID)
        }(id)
    }
    time.Sleep(5 * time.Second)  // Uncertain if time is sufficient
}
```

**Correct:**

```go
import "sync"

func ProcessAllUsers(userIDs []string) error {
    var wg sync.WaitGroup
    errCh := make(chan error, len(userIDs))

    for _, id := range userIDs {
        wg.Add(1)
        go func(userID string) {
            defer wg.Done()

            if err := ProcessUser(userID); err != nil {
                errCh <- err
            }
        }(id)
    }

    // Wait for all goroutines to complete
    wg.Wait()
    close(errCh)

    // Collect errors
    for err := range errCh {
        if err != nil {
            return fmt.Errorf("processing failed: %w", err)
        }
    }

    return nil
}
```

**Why**: Using WaitGroup ensures all goroutines complete reliably. It's the standard way to synchronize concurrent operations in Go.

**Key pattern:**
1. `wg.Add(1)` before starting goroutine
2. `defer wg.Done()` at goroutine start
3. `wg.Wait()` to block until all done

Reference: [Go Docs - sync.WaitGroup](https://pkg.go.dev/sync#WaitGroup)
