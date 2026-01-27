---
title: Borrowing with &T and &mut T
impact: CRITICAL
impactDescription: Efficient access without ownership transfer
tags: rust, borrowing, references, mut
---

## Borrowing with &T and &mut T

**Impact: CRITICAL - Efficient access without ownership transfer**

Use references to access data without taking ownership.

**Incorrect:**

```rust
// Unnecessarily takes ownership
fn calculate_length(s: String) -> (String, usize) {
    let len = s.len();
    (s, len)  // Must return ownership
}

// Usage (inconvenient)
let text = String::from("hello");
let (text, len) = calculate_length(text);
```

**Correct:**

```rust
// Immutable reference (&T): multiple concurrent reads allowed
fn calculate_length(s: &String) -> usize {
    s.len()
}

// Mutable reference (&mut T): only one can exist
fn append_suffix(s: &mut String, suffix: &str) {
    s.push_str(suffix);
}

// Usage
let mut text = String::from("hello");
let len = calculate_length(&text);  // immutable reference
append_suffix(&mut text, " world");  // mutable reference
println!("{}", text);  // "hello world"
```

**Why**: Using borrowing allows accessing data without transferring ownership, which is efficient. The borrow checker ensures references are valid.

**Borrowing rules:**
- Multiple `&T` (immutable) OR one `&mut T` (mutable)
- References must always be valid
- Cannot have `&mut T` while `&T` exists

Reference: [The Rust Book - References and Borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)
