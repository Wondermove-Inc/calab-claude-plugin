---
title: No Null Pointers
impact: CRITICAL
impactDescription: Compile-time null safety
tags: rust, memory, null, Option, safety
---

## No Null Pointers

**Impact: CRITICAL - Compile-time null safety**

Rust has no null - use Option<T> for nullable values.

**Bad (C/C++):**

```c
// Null pointer (does not exist in Rust)
Config* get_config() {
    if (config_exists()) {
        return load_config();
    } else {
        return NULL;  // Null pointer
    }
}

// Usage: Null check may be missed
Config* config = get_config();
use_config(config);  // Segmentation fault possible
```

**Correct (Rust):**

```rust
// Represent nullable with Option<T>
fn get_config() -> Option<Config> {
    if config_exists() {
        Some(Config::load())
    } else {
        None
    }
}

// Usage: Compiler forces None check
let config = get_config();
match config {
    Some(c) => use_config(c),
    None => use_default_config(),
}

// Or with unwrap_or
let config = get_config().unwrap_or_default();
```

**Why**: Rust has no null pointers, preventing null pointer dereference errors at compile time. The type system forces you to handle the absence of a value.

**The billion dollar mistake avoided:**
> "I call it my billion-dollar mistake... the null reference" - Tony Hoare

Reference: [The Rust Book - Option](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html#the-option-enum-and-its-advantages-over-null-values)
