---
title: Module Management
impact: MEDIUM
impactDescription: Clean dependencies, reproducible builds
tags: go, modules, go.mod, dependencies
---

## Module Management

**Impact: MEDIUM - Clean dependencies, reproducible builds**

Keep go.mod clean and use go mod tidy regularly.

**Incorrect:**

```go
// Unnecessary dependencies in go.mod
require (
    github.com/lib/pq v1.10.9
    github.com/unused/package v1.0.0  // Not used
)
```

**Correct:**

```go
// go.mod
module github.com/user/myproject

go 1.21

require (
    github.com/lib/pq v1.10.9
    github.com/stretchr/testify v1.8.4
)

// Specify only minimum versions, manage exact versions with go.sum
```

**Why**: Run `go mod tidy` to remove unused dependencies and maintain clean module management.

**Common commands:**

| Command | Purpose |
|---------|---------|
| `go mod init` | Initialize new module |
| `go mod tidy` | Add missing, remove unused deps |
| `go mod download` | Download dependencies |
| `go mod verify` | Verify dependencies |
| `go mod graph` | Print dependency graph |

**Best practices:**
- Run `go mod tidy` before committing
- Check in both `go.mod` and `go.sum`
- Use `go get -u` carefully (updates dependencies)

Reference: [Go Docs - Modules](https://go.dev/ref/mod)
