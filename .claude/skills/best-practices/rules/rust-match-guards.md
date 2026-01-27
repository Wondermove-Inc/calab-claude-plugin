---
title: Match Guards
impact: MEDIUM
impactDescription: Conditional pattern matching
tags: rust, match, guards, pattern-matching
---

## Match Guards

**Impact: MEDIUM - Conditional pattern matching**

Use match guards to add conditions to patterns.

**Incorrect:**

```rust
// Nested if-else
fn check_number(num: Option<i32>) {
    if let Some(x) = num {
        if x < 0 {
            println!("Negative: {}", x);
        } else if x == 0 {
            println!("Zero");
        } else {
            println!("Positive: {}", x);
        }
    } else {
        println!("No number");
    }
}
```

**Correct:**

```rust
fn check_number(num: Option<i32>) {
    match num {
        Some(x) if x < 0 => println!("Negative: {}", x),
        Some(x) if x == 0 => println!("Zero"),
        Some(x) => println!("Positive: {}", x),
        None => println!("No number"),
    }
}

// Complex conditions
fn compare(x: i32, y: i32) {
    match (x, y) {
        (a, b) if a == b => println!("Equal"),
        (a, b) if a > b => println!("x is greater"),
        _ => println!("y is greater"),
    }
}
```

**Why**: Using match guards allows adding conditions to patterns, making code more expressive. The guard is evaluated after the pattern matches.

**Syntax:** `pattern if condition => expression`

Reference: [The Rust Book - Match Guards](https://doc.rust-lang.org/book/ch18-03-pattern-syntax.html#extra-conditionals-with-match-guards)
