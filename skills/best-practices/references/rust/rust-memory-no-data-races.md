---
title: No Data Races
impact: CRITICAL
impactDescription: Thread safety at compile time
tags: rust, memory, concurrency, data-races, Arc, Mutex
---

## No Data Races

**Impact: CRITICAL - Thread safety at compile time**

Rust's ownership rules prevent data races at compile time.

**Bad (C/C++):**

```c
// Data race (Rust compiler prevents this)
int counter = 0;

void increment() {
    counter++;  // Data race
}

// Problem occurs when called concurrently from multiple threads
```

**Correct (Rust):**

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());
```

**Why**: Rust's ownership and borrowing rules prevent data races at compile time. You cannot have multiple mutable references, which eliminates a whole class of bugs.

**Thread-safe types:**
| Type | Purpose |
|------|---------|
| `Arc<T>` | Atomic reference counting for shared ownership |
| `Mutex<T>` | Mutual exclusion for mutable access |
| `RwLock<T>` | Read-write lock (multiple readers, single writer) |

Reference: [The Rust Book - Fearless Concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html)
