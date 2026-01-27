---
title: if let for Single Pattern
impact: MEDIUM
impactDescription: Concise single-pattern handling
tags: rust, if-let, pattern-matching, concise
---

## if let for Single Pattern

**Impact: MEDIUM - Concise single-pattern handling**

Use if let when you only care about one pattern.

**Incorrect:**

```rust
// Handling single pattern with match (verbose)
match config {
    Some(cfg) => println!("Debug mode: {}", cfg.debug),
    None => {}
}
```

**Correct:**

```rust
let config = Some(Config { debug: true });

// if let: when interested in only one pattern
if let Some(cfg) = config {
    println!("Debug mode: {}", cfg.debug);
}

// while let: iterative processing
let mut stack = vec![1, 2, 3];
while let Some(top) = stack.pop() {
    println!("{}", top);
}

// if let with else
if let Some(value) = get_optional() {
    println!("Got: {}", value);
} else {
    println!("Nothing");
}
```

**Why**: Using `if let` allows writing single pattern matching concisely. It's syntactic sugar for a match with one arm and a wildcard.

**When to use:**
- Only handling `Some` case of Option
- Only handling `Ok` case of Result
- Single enum variant

Reference: [The Rust Book - if let](https://doc.rust-lang.org/book/ch06-03-if-let.html)
