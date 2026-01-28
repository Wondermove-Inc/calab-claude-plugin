---
title: Safe Abstractions
impact: HIGH
impactDescription: Automatic memory management
tags: rust, memory, abstractions, Vec, Iterator, RAII
---

## Safe Abstractions

**Impact: HIGH - Automatic memory management**

Use Rust's safe abstractions instead of manual memory management.

**Bad (C/C++):**

```c
// Manual memory management
int* arr = malloc(sizeof(int) * 3);
arr[0] = 1;
arr[1] = 2;
arr[2] = 3;
free(arr);  // Manual deallocation (memory leak if missed)
```

**Correct (Rust):**

```rust
// Vec is a memory-safe dynamic array
let mut vec = Vec::new();
vec.push(1);
vec.push(2);
vec.push(3);

// Automatic memory deallocation (Drop trait)
let data = vec![1, 2, 3];
// Memory automatically freed at end of scope

// Safe iteration with Iterator
for item in vec.iter() {
    println!("{}", item);
}

// RAII pattern
{
    let file = File::open("data.txt")?;
    // use file...
} // file automatically closed here
```

**Why**: Rust's standard library provides memory-safe abstractions, automating memory management. The Drop trait ensures cleanup happens automatically.

**Key abstractions:**
| Type | Purpose |
|------|---------|
| `Vec<T>` | Dynamic array |
| `String` | UTF-8 string |
| `Box<T>` | Heap allocation |
| `Rc<T>` | Reference counting |

Reference: [The Rust Book - Smart Pointers](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)
