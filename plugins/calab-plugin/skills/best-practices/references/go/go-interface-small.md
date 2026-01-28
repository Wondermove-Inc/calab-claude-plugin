---
title: Small, Focused Interfaces
impact: HIGH
impactDescription: Easier testing, better composition
tags: go, interfaces, design, composition
---

## Small, Focused Interfaces

**Impact: HIGH - Easier testing, better composition**

Design small interfaces with few methods for better flexibility.

**Incorrect:**

```go
// Interface too large
type FileSystem interface {
    Open(name string) (File, error)
    Create(name string) (File, error)
    Remove(name string) error
    Rename(oldpath, newpath string) error
    Mkdir(name string, perm FileMode) error
    MkdirAll(path string, perm FileMode) error
    // ... many more methods
}
```

**Correct:**

```go
// Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

// Composition
type ReadWriter interface {
    Reader
    Writer
}

type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}
```

**Why**: Small interfaces are easier to test and implement. "Accept interfaces, return structs" - the Go proverb. Composing small interfaces gives you exactly what you need.

**Standard library examples:**
- `io.Reader` (1 method)
- `io.Writer` (1 method)
- `fmt.Stringer` (1 method)
- `error` (1 method)

Reference: [Effective Go - Interfaces](https://go.dev/doc/effective_go#interfaces)
