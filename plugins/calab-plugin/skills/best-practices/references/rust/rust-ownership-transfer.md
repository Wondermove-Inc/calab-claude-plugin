---
title: Ownership Transfer
impact: HIGH
impactDescription: Memory safety, predictable data flow
tags: rust, ownership, move, memory
---

## Ownership Transfer

**Impact: HIGH - Memory safety, predictable data flow**

Transfer ownership intentionally and return owned data when needed.

**Incorrect:**

```rust
fn process_string(s: String) {
    let processed = s.to_uppercase();
    // Does not return processed (memory waste)
}

// Usage
let original = String::from("hello");
process_string(original);
// original unusable, result cannot be received
```

**Correct:**

```rust
fn process_string(s: String) -> String {
    // Takes ownership of s, processes and returns it
    let processed = s.to_uppercase();
    processed  // ownership transferred
}

// Usage
let original = String::from("hello");
let result = process_string(original);
// original can no longer be used
println!("{}", result);
```

**Why**: Clearly managing ownership prevents memory leaks and makes data flow predictable. The compiler enforces ownership rules at compile time.

**Ownership rules:**
1. Each value has exactly one owner
2. When owner goes out of scope, value is dropped
3. Ownership can be transferred (moved)

Reference: [The Rust Book - Ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)
