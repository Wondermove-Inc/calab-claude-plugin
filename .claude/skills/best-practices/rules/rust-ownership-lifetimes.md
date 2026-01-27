---
title: Lifetime Annotations
impact: HIGH
impactDescription: Prevents dangling references
tags: rust, lifetimes, references, annotations
---

## Lifetime Annotations

**Impact: HIGH - Prevents dangling references**

Use lifetime annotations to specify reference validity periods.

**Incorrect:**

```rust
// Missing lifetime (compile error)
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```

**Correct:**

```rust
// Express reference relationships with explicit lifetimes
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// Store references in structs
struct User<'a> {
    name: &'a str,
    email: &'a str,
}

impl<'a> User<'a> {
    fn new(name: &'a str, email: &'a str) -> Self {
        User { name, email }
    }
}
```

**Why**: Lifetime annotations specify the valid duration of references, preventing dangling references. The compiler uses them to verify reference validity.

**Lifetime rules:**
- `'a` is a lifetime parameter
- `&'a T` means "reference to T that lives at least as long as 'a"
- Return lifetime must match input lifetime

Reference: [The Rust Book - Lifetimes](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html)
