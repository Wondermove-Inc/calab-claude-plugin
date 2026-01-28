---
title: Avoid unwrap() in Production
impact: CRITICAL
impactDescription: Panic in production, program termination
tags: rust, anti-pattern, unwrap, expect, error-handling
---

## Avoid unwrap() in Production

**Impact: CRITICAL - Panic in production, program termination**

Use `?`, `expect()`, or proper error handling instead of `unwrap()`.

**Incorrect:**

```rust
let file = File::open("file.txt").unwrap();  // May panic
let data: Config = serde_json::from_str(&contents).unwrap();  // May panic
```

**Correct:**

```rust
// Use ? operator
let file = File::open("file.txt")?;  // Propagate error

// Use expect() with context
let file = File::open("config.json")
    .expect("config.json must exist in project root");

// Use match or if let
let file = match File::open("file.txt") {
    Ok(f) => f,
    Err(e) => {
        eprintln!("Failed to open: {}", e);
        return Err(e.into());
    }
};

// Use unwrap_or / unwrap_or_else
let config = get_config().unwrap_or_default();
let port = env::var("PORT")
    .unwrap_or_else(|_| "8080".to_string());
```

**Why**: `unwrap()` panics on `None`/`Err`, terminating the program. Use proper error handling for production code.

**Alternatives:**
| Method | Behavior |
|--------|----------|
| `?` | Propagate error to caller |
| `expect("msg")` | Panic with message (acceptable for invariants) |
| `unwrap_or(default)` | Use default value |
| `unwrap_or_else(fn)` | Compute default lazily |
| `unwrap_or_default()` | Use Default trait |

Reference: [The Rust Book - To panic! or Not to panic!](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html)
