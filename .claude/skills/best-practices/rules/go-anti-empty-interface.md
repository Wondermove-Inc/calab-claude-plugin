---
title: Avoid Empty Interface Abuse
impact: HIGH
impactDescription: Loss of type safety, runtime errors
tags: go, anti-pattern, interface, any, generics
---

## Avoid Empty Interface Abuse

**Impact: HIGH - Loss of type safety, runtime errors**

Use generics (Go 1.18+) instead of `interface{}` for type-safe code.

**Incorrect:**

```go
func ProcessData(data interface{}) {
    // Loss of type safety
    // Requires type assertions everywhere
    switch v := data.(type) {
    case string:
        // handle string
    case int:
        // handle int
    default:
        // unknown type
    }
}
```

**Correct:**

```go
// Using Generics (Go 1.18+)
func ProcessData[T any](data T) {
    // Type-safe
}

// With constraints
func Max[T constraints.Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

// Usage
result := Max(10, 20)  // Type inferred as int
result := Max("a", "b")  // Type inferred as string
```

**Why**: Empty interface (`interface{}` or `any`) loses type safety and requires runtime type assertions. Generics provide compile-time type safety while maintaining flexibility.

**When empty interface is acceptable:**
- JSON unmarshaling (`map[string]interface{}`)
- Logging parameters
- Existing APIs that require it

Reference: [Go Generics Tutorial](https://go.dev/doc/tutorial/generics)
