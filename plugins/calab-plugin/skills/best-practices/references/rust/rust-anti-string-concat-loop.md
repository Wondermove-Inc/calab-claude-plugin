---
title: Avoid String Concatenation in Loops
impact: MEDIUM
impactDescription: Quadratic time complexity, memory reallocation
tags: rust, anti-pattern, string, performance, loops
---

## Avoid String Concatenation in Loops

**Impact: MEDIUM - Quadratic time complexity, memory reallocation**

Use `push_str()` for in-place modification or collect iterators.

**Incorrect:**

```rust
let mut result = String::new();
for i in 0..1000 {
    result = result + &i.to_string();  // Reallocates every iteration
}
```

**Correct:**

```rust
// Use push_str for in-place modification
let mut result = String::new();
for i in 0..1000 {
    result.push_str(&i.to_string());  // In-place modification
}

// Pre-allocate capacity
let mut result = String::with_capacity(4000);
for i in 0..1000 {
    result.push_str(&i.to_string());
}

// Use collect for cleaner code
let result: String = (0..1000)
    .map(|i| i.to_string())
    .collect();

// Use join for separator
let parts: Vec<String> = (0..100).map(|i| i.to_string()).collect();
let result = parts.join(", ");
```

**Why**: String concatenation with `+` creates a new String each time. `push_str()` modifies in place, avoiding repeated allocation.

**Performance:**
| Method | Complexity |
|--------|------------|
| `+` in loop | O(n²) |
| `push_str()` | O(n) amortized |
| `collect()` | O(n) |

Reference: [Rust Performance Book](https://nnethercote.github.io/perf-book/type-sizes.html)
