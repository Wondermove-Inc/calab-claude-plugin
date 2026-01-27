---
title: Unsafe Code Isolation
impact: HIGH
impactDescription: Minimize and contain unsafe code
tags: rust, unsafe, memory, isolation, FFI
---

## Unsafe Code Isolation

**Impact: HIGH - Minimize and contain unsafe code**

Minimize unsafe blocks and wrap them in safe abstractions.

**Incorrect:**

```rust
// Overusing unsafe
pub fn process_data(data: &mut [i32]) {
    unsafe {
        // Lots of unsafe code
        // Difficult to guarantee memory safety
    }
}
```

**Correct:**

```rust
// Minimize and isolate unsafe code
fn split_at_mut(slice: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = slice.len();
    let ptr = slice.as_mut_ptr();

    assert!(mid <= len);

    unsafe {
        (
            std::slice::from_raw_parts_mut(ptr, mid),
            std::slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}

// Safe wrapper
pub fn safe_split_at_mut(slice: &mut [i32], mid: usize) -> Result<(&mut [i32], &mut [i32]), String> {
    if mid > slice.len() {
        return Err("Index out of bounds".to_string());
    }
    Ok(split_at_mut(slice, mid))
}
```

**Why**: Minimizing `unsafe` code and wrapping it with safe wrappers maintains memory safety. The unsafe block is a signal that extra care is needed.

**When unsafe is needed:**
- FFI (Foreign Function Interface)
- Low-level optimizations
- Hardware access
- Building safe abstractions

Reference: [The Rust Book - Unsafe Rust](https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html)
