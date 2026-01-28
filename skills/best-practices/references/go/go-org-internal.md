---
title: Internal Packages
impact: HIGH
impactDescription: API protection, encapsulation
tags: go, packages, internal, encapsulation
---

## Internal Packages

**Impact: HIGH - API protection, encapsulation**

Use `internal/` to prevent external imports of private packages.

**Incorrect:**

```go
// domain/user.go (can be imported externally)
package domain

type User struct {
    ID    string
    Name  string
    Email string
}

// From external project
import "myproject/domain"  // Unintended access possible
```

**Correct:**

```go
// internal/domain/user.go (cannot be imported externally)
package domain

type User struct {
    ID    string
    Name  string
    Email string
}

// internal/adapters/handler.go
package adapters

import "myproject/internal/domain"  // OK

func GetUserHandler(w http.ResponseWriter, r *http.Request) {
    user := &domain.User{}
    // Process
}
```

**Why**: Using the `internal/` directory restricts packages to the project internally, protecting the API. External projects cannot import anything under `internal/`.

**Go compiler enforces:**
```
myproject/internal/domain  →  Only myproject/* can import
myproject/pkg/logger       →  Anyone can import
```

Reference: [Go Docs - Internal Packages](https://go.dev/doc/go1.4#internalpackages)
