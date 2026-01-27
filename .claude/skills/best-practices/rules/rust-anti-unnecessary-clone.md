---
title: Avoid Unnecessary Clone
impact: HIGH
impactDescription: Performance, memory efficiency
tags: rust, anti-pattern, clone, borrowing, performance
---

## Avoid Unnecessary Clone

**Impact: HIGH - Performance, memory efficiency**

Prefer borrowing over cloning when possible.

**Incorrect:**

```rust
fn process(s: String) {
    let s2 = s.clone();  // Unnecessary clone
    println!("{}", s2);
}

// Clone in a loop
fn process_all(items: Vec<String>) {
    for item in items.iter() {
        let owned = item.clone();  // Cloning each item
        do_something(owned);
    }
}
```

**Correct:**

```rust
fn process(s: &String) {
    println!("{}", s);  // Borrowing
}

// Use references
fn process_all(items: &[String]) {
    for item in items {
        do_something(item);  // Pass reference
    }
}

// Clone only when ownership is truly needed
fn take_ownership(s: String) -> String {
    // Actually needs ownership
    s.to_uppercase()
}
```

**Why**: `clone()` is expensive - it allocates memory and copies data. Use borrowing when you don't need ownership.

**When clone is acceptable:**
- Actually need separate ownership
- Type is cheap to clone (small, Copy types)
- Simplifying complex lifetime situations

Reference: [The Rust Book - References and Borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)
