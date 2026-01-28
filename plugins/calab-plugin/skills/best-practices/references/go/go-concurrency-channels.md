---
title: Channels and Select
impact: HIGH
impactDescription: Non-blocking operations, graceful shutdown
tags: go, concurrency, channels, select
---

## Channels and Select

**Impact: HIGH - Non-blocking operations, graceful shutdown**

Use select to handle multiple channels and implement graceful shutdown.

**Incorrect:**

```go
// Blocking without select
func Worker(jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        result := ProcessJob(job)
        results <- result  // Cannot receive shutdown signal
    }
}
```

**Correct:**

```go
func Worker(jobs <-chan Job, results chan<- Result, done <-chan struct{}) {
    for {
        select {
        case job, ok := <-jobs:
            if !ok {
                return  // Channel closed
            }
            result := ProcessJob(job)
            results <- result
        case <-done:
            return  // Shutdown signal
        }
    }
}

// Usage
jobs := make(chan Job, 100)
results := make(chan Result, 100)
done := make(chan struct{})

// Start worker
go Worker(jobs, results, done)

// Send jobs
jobs <- Job{ID: "1"}

// Send shutdown signal
close(done)
```

**Why**: Using `select` allows handling multiple channels simultaneously and implementing graceful shutdown. Workers can respond to both work and shutdown signals.

Reference: [Go Tour - Select](https://go.dev/tour/concurrency/5)
