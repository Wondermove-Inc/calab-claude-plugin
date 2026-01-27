---
title: Never Ignore Errors
impact: CRITICAL
impactDescription: Hidden bugs, silent failures
tags: go, anti-pattern, errors, blank-identifier
---

## Never Ignore Errors

**Impact: CRITICAL - Hidden bugs, silent failures**

Always handle or explicitly acknowledge errors.

**Incorrect:**

```go
file, _ := os.Open("file.txt")
defer file.Close()

json.Unmarshal(data, &result)  // Error ignored

resp, _ := http.Get(url)  // Error ignored
```

**Correct:**

```go
file, err := os.Open("file.txt")
if err != nil {
    return fmt.Errorf("failed to open file: %w", err)
}
defer file.Close()

if err := json.Unmarshal(data, &result); err != nil {
    return fmt.Errorf("failed to unmarshal: %w", err)
}

resp, err := http.Get(url)
if err != nil {
    return fmt.Errorf("request failed: %w", err)
}
```

**Why**: Ignoring errors hides bugs and causes silent failures. Go's explicit error handling is a feature, not a burden.

**If you truly don't care:**
```go
// Explicitly acknowledge the ignored error
_ = optionalCleanup()  // Still visible in code review
```

**Linter support:**
```bash
# errcheck finds ignored errors
go install github.com/kisielk/errcheck@latest
errcheck ./...
```

Reference: [Effective Go - Errors](https://go.dev/doc/effective_go#errors)
