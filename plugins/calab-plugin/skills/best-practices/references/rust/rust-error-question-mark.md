---
title: ? Operator for Error Propagation
impact: HIGH
impactDescription: Concise error propagation, clean code
tags: rust, errors, question-mark, propagation
---

## ? Operator for Error Propagation

**Impact: HIGH - Concise error propagation, clean code**

Use the ? operator to propagate errors concisely.

**Incorrect:**

```rust
// Manual error handling (verbose)
fn process_file(path: &str) -> Result<usize, io::Error> {
    let contents = match read_file(path) {
        Ok(c) => c,
        Err(e) => return Err(e),
    };
    let lines = match parse_lines(&contents) {
        Ok(l) => l,
        Err(e) => return Err(e),
    };
    let count = match count_words(&lines) {
        Ok(c) => c,
        Err(e) => return Err(e),
    };
    Ok(count)
}
```

**Correct:**

```rust
use std::io;

fn process_file(path: &str) -> Result<usize, io::Error> {
    let contents = read_file(path)?;  // Automatically propagate error
    let lines = parse_lines(&contents)?;
    let count = count_words(&lines)?;
    Ok(count)
}

// Custom Error with ?
enum MyError {
    Io(io::Error),
    Parse(String),
}

impl From<io::Error> for MyError {
    fn from(err: io::Error) -> Self {
        MyError::Io(err)
    }
}

fn process_data(path: &str) -> Result<Data, MyError> {
    let contents = read_file(path)?;  // io::Error automatically converted to MyError
    let data = parse_data(&contents)
        .map_err(|e| MyError::Parse(e))?;
    Ok(data)
}
```

**Why**: Using the `?` operator allows writing error handling code concisely. It automatically propagates errors and can convert between error types with `From` impl.

Reference: [The Rust Book - Propagating Errors](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator)
