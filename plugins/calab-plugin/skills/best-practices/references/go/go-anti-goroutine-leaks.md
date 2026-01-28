---
title: Avoid Goroutine Leaks
impact: CRITICAL
impactDescription: Memory leaks, resource exhaustion
tags: go, anti-pattern, goroutines, leaks, context
---

## Avoid Goroutine Leaks

**Impact: CRITICAL - Memory leaks, resource exhaustion**

Always provide exit conditions for goroutines.

**Incorrect:**

```go
func ProcessData() {
    go func() {
        for {
            // No exit condition
            time.Sleep(1 * time.Second)
        }
    }()
}
```

**Correct:**

```go
func ProcessData(ctx context.Context) {
    go func() {
        ticker := time.NewTicker(1 * time.Second)
        defer ticker.Stop()

        for {
            select {
            case <-ticker.C:
                // Process
            case <-ctx.Done():
                return
            }
        }
    }()
}
```

**Why**: Goroutines without exit conditions run forever, consuming memory and CPU. Always use context, done channels, or other mechanisms to signal shutdown.

**Common leak patterns:**
- Infinite loops without exit
- Blocked channel sends/receives
- Missing context cancellation
- Forgetting to close channels

**Detection:**
```go
// In tests, check goroutine count
import "runtime"
before := runtime.NumGoroutine()
// ... run code ...
after := runtime.NumGoroutine()
if after > before {
    // Potential leak
}
```

Reference: [Go Blog - Concurrency is not Parallelism](https://go.dev/blog/waza-talk)
