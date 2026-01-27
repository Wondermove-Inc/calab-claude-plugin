---
title: Option<T> for Nullable Values
impact: HIGH
impactDescription: No null pointer errors, compile-time safety
tags: rust, errors, Option, null-safety
---

## Option<T> for Nullable Values

**Impact: HIGH - No null pointer errors, compile-time safety**

Use Option to represent values that may or may not exist.

**Incorrect:**

```rust
// Using panic instead of null pointer
fn find_user(id: u32) -> User {
    if user_exists(id) {
        User { id, name: String::from("John") }
    } else {
        panic!("User not found");  // Terminates program
    }
}
```

**Correct:**

```rust
fn find_user(id: u32) -> Option<User> {
    // Returns Some if user found, None otherwise
    if user_exists(id) {
        Some(User { id, name: String::from("John") })
    } else {
        None
    }
}

// Usage: if let
if let Some(user) = find_user(1) {
    println!("Found: {}", user.name);
} else {
    println!("User not found");
}

// Usage: match
match find_user(1) {
    Some(user) => println!("Found: {}", user.name),
    None => println!("User not found"),
}

// Usage: unwrap_or
let user = find_user(1).unwrap_or(User::default());
```

**Why**: Using `Option<T>` prevents null pointer errors at compile time. The compiler forces you to handle the `None` case.

**Option variants:**
- `Some(T)` - Value exists
- `None` - Value doesn't exist

Reference: [The Rust Book - Option](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html#the-option-enum-and-its-advantages-over-null-values)
