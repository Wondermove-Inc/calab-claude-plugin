---
title: Defer for Cleanup
impact: HIGH
impactDescription: Guaranteed cleanup, prevents resource leaks
tags: go, defer, cleanup, resources
---

## Defer for Cleanup

**Impact: HIGH - Guaranteed cleanup, prevents resource leaks**

Use defer to ensure resources are cleaned up regardless of errors.

**Incorrect:**

```go
// Manual cleanup (may be missed on error)
func ProcessFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return err
    }

    scanner := bufio.NewScanner(f)
    for scanner.Scan() {
        line := scanner.Text()
        // Process line
    }

    f.Close()  // Not executed if error occurs
    return nil
}
```

**Correct:**

```go
func ProcessFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return fmt.Errorf("failed to open file: %w", err)
    }
    defer f.Close()  // Automatically executes when function returns

    // Process file
    scanner := bufio.NewScanner(f)
    for scanner.Scan() {
        line := scanner.Text()
        // Process line
    }

    if err := scanner.Err(); err != nil {
        return fmt.Errorf("scan error: %w", err)
    }

    return nil
}
```

**Why**: Using `defer` ensures resources are cleaned up regardless of whether an error occurs. The deferred function runs when the surrounding function returns.

**Common defer patterns:**
- Close files: `defer f.Close()`
- Unlock mutexes: `defer mu.Unlock()`
- Close database connections: `defer db.Close()`
- Release resources: `defer release()`

Reference: [Go Blog - Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)
