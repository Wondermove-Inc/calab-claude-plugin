---
title: Clone vs Copy
impact: MEDIUM
impactDescription: Performance awareness, intentional copying
tags: rust, clone, copy, traits, performance
---

## Clone vs Copy

**Impact: MEDIUM - Performance awareness, intentional copying**

Understand the difference between Copy (implicit) and Clone (explicit).

**Incorrect:**

```rust
// Unnecessary clone
let s1 = String::from("hello");
let s2 = s1.clone();  // Could use reference instead of clone
let len = s2.len();
```

**Correct:**

```rust
// Copy trait (small types stored on stack)
let x: i32 = 5;
let y = x;  // Copy
println!("{}, {}", x, y);  // Both can be used

// Clone trait (large types stored on heap)
let s1 = String::from("hello");
let s2 = s1.clone();  // Explicit copy
println!("{}, {}", s1, s2);

// Use reference without Clone (more efficient)
let s1 = String::from("hello");
let s2 = &s1;
println!("{}, {}", s1, s2);
```

**Why**: `clone()` is expensive (heap allocation), so use it only when necessary. Prefer borrowing when possible.

**Copy vs Clone:**

| Trait | Behavior | Types |
|-------|----------|-------|
| `Copy` | Implicit bitwise copy | `i32`, `bool`, `char`, `&T` |
| `Clone` | Explicit, can be expensive | `String`, `Vec`, `Box` |

Reference: [The Rust Book - Copy and Clone](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html#ways-variables-and-data-interact-clone)
