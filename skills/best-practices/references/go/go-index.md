> **원본**: claude-monitoring-main
> **적용**: calab-claude-plugin v2.3.0+

---
title: Go Patterns Index
impact: HIGH
version: 1.21+
tags: go, index, patterns
---

## Go Patterns Index

**19 patterns across 5 categories for Go 1.21+**

### Error Handling (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [go-error-explicit-returns](go-error-explicit-returns.md) | CRITICAL | Explicit error returns |
| [go-error-wrapping](go-error-wrapping.md) | HIGH | Error wrapping with %w |
| [go-error-custom-types](go-error-custom-types.md) | HIGH | Custom error types |
| [go-error-defer](go-error-defer.md) | HIGH | Defer for cleanup |

### Concurrency (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [go-concurrency-goroutines](go-concurrency-goroutines.md) | HIGH | Goroutines with error handling |
| [go-concurrency-channels](go-concurrency-channels.md) | HIGH | Channels and select |
| [go-concurrency-waitgroup](go-concurrency-waitgroup.md) | HIGH | WaitGroup for synchronization |
| [go-concurrency-context](go-concurrency-context.md) | CRITICAL | Context for cancellation |

### Interface Design (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [go-interface-small](go-interface-small.md) | HIGH | Small, focused interfaces |
| [go-interface-implicit](go-interface-implicit.md) | MEDIUM | Implicit implementation |
| [go-interface-segregation](go-interface-segregation.md) | HIGH | Interface segregation |
| [go-interface-accept-return](go-interface-accept-return.md) | HIGH | Accept interfaces, return structs |

### Code Organization (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [go-org-package-structure](go-org-package-structure.md) | HIGH | Package structure |
| [go-org-internal](go-org-internal.md) | HIGH | Internal packages |
| [go-org-modules](go-org-modules.md) | MEDIUM | Module management |
| [go-org-naming](go-org-naming.md) | MEDIUM | Naming conventions |

### Anti-patterns (3 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [go-anti-goroutine-leaks](go-anti-goroutine-leaks.md) | CRITICAL | Avoid goroutine leaks |
| [go-anti-ignoring-errors](go-anti-ignoring-errors.md) | CRITICAL | Never ignore errors |
| [go-anti-empty-interface](go-anti-empty-interface.md) | HIGH | Avoid empty interface abuse |

## Key Principles

1. **Explicit Error Handling**: Return errors, use `%w` for wrapping
2. **Safe Concurrency**: Goroutines + Channels + Select + WaitGroup
3. **Context Everywhere**: Timeout and cancellation with Context
4. **Small Interfaces**: "Accept interfaces, return structs"
5. **Internal Packages**: Protect APIs with `internal/` directory
6. **Defer Cleanup**: Always use defer for resource cleanup
