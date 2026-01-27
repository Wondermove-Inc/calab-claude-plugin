---
title: Package Structure
impact: HIGH
impactDescription: Clear organization, proper encapsulation
tags: go, packages, structure, organization
---

## Package Structure

**Impact: HIGH - Clear organization, proper encapsulation**

Follow standard Go project layout conventions.

**Correct:**

```
project/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── domain/
│   │   ├── user.go
│   │   └── repository.go
│   ├── application/
│   │   └── service.go
│   ├── adapters/
│   │   ├── handler.go
│   │   └── postgres.go
│   └── infrastructure/
│       ├── database.go
│       └── config.go
├── pkg/
│   └── logger/
│       └── logger.go
└── go.mod
```

**Directory purposes:**

| Directory | Purpose |
|-----------|---------|
| `cmd/` | Entry points for executables |
| `internal/` | Packages that cannot be imported externally |
| `pkg/` | Public packages usable externally |
| `domain/` | Business logic and entities |
| `application/` | Use cases and services |
| `adapters/` | External interfaces (HTTP, DB) |
| `infrastructure/` | Configuration, logging, etc. |

**Why**: Following conventions makes the codebase predictable and maintainable. `internal/` provides compile-time encapsulation.

Reference: [Standard Go Project Layout](https://github.com/golang-standards/project-layout)
