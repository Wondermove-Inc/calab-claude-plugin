---
title: Result<T, E> Pattern
impact: CRITICAL
impactDescription: Safe error handling, no exceptions
tags: rust, errors, Result, error-handling
---

## Result<T, E> Pattern

**Impact: CRITICAL - Safe error handling, no exceptions**

Use Result for operations that can fail.

**Incorrect:**

```rust
// Using panic (terminates program)
fn read_file(path: &str) -> String {
    let mut file = File::open(path).unwrap();  // panic!
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    contents
}
```

**Correct:**

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;  // Propagate error with ? operator
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// Usage
match read_file("file.txt") {
    Ok(contents) => println!("{}", contents),
    Err(e) => eprintln!("Error: {}", e),
}
```

**Why**: Using `Result<T, E>` allows safe error handling and lets callers handle errors. Unlike exceptions, errors are explicit in the type system.

**Result variants:**
- `Ok(T)` - Success with value
- `Err(E)` - Failure with error

Reference: [The Rust Book - Error Handling](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html)
