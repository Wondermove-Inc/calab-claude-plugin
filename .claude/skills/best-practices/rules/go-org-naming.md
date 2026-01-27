---
title: Naming Conventions
impact: MEDIUM
impactDescription: Readability, consistency with standard library
tags: go, naming, conventions, style
---

## Naming Conventions

**Impact: MEDIUM - Readability, consistency with standard library**

Follow Go naming conventions for consistency.

**Incorrect:**

```go
// Unclear name
package usr

// Name too long
type UserRepositoryInterfaceImplementation struct {}

// Does not follow Go conventions
func Get_User(id string) (*User, error) {}
```

**Correct:**

```go
// Package name: lowercase, short and clear
package user

// Interface: noun or ends with -er
type Reader interface {}
type UserRepository interface {}

// Struct: PascalCase
type UserService struct {}

// Variables/functions: camelCase (internal), PascalCase (exported)
func getUserByID(id string) (*User, error) {}
func GetUser(id string) (*User, error) {}

// Constants: PascalCase or ALL_CAPS
const MaxRetries = 3
const DEFAULT_TIMEOUT = 5 * time.Second
```

**Why**: Following Go naming conventions improves code readability and maintains consistency with the standard library.

**Naming rules:**

| Element | Convention | Example |
|---------|------------|---------|
| Package | lowercase, short | `user`, `http` |
| Interface | -er suffix or noun | `Reader`, `UserRepo` |
| Exported | PascalCase | `GetUser` |
| Unexported | camelCase | `getUserByID` |
| Acronyms | All caps | `HTTP`, `URL`, `ID` |

Reference: [Effective Go - Names](https://go.dev/doc/effective_go#names)
