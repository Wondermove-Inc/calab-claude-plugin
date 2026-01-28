---
title: Custom Error Types with thiserror
impact: HIGH
impactDescription: Structured errors, automatic conversions
tags: rust, errors, thiserror, custom-errors
---

## Custom Error Types with thiserror

**Impact: HIGH - Structured errors, automatic conversions**

Use thiserror crate for ergonomic custom error types.

**Incorrect:**

```rust
// Returns only string
fn process_data(path: &str) -> Result<Data, String> {
    let contents = std::fs::read_to_string(path)
        .map_err(|e| e.to_string())?;  // Loses type information
    // ...
}
```

**Correct:**

```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum DataError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error: {0}")]
    Parse(String),

    #[error("Validation error in field {field}: {message}")]
    Validation { field: String, message: String },

    #[error("Not found: {resource} with ID {id}")]
    NotFound { resource: String, id: String },
}

fn process_data(path: &str) -> Result<Data, DataError> {
    let contents = std::fs::read_to_string(path)?;  // io::Error automatically converted
    let data = serde_json::from_str(&contents)
        .map_err(|e| DataError::Parse(e.to_string()))?;

    if !validate_data(&data) {
        return Err(DataError::Validation {
            field: "age".to_string(),
            message: "must be positive".to_string(),
        });
    }

    Ok(data)
}
```

**Why**: Using custom error types allows structuring error information and increases type safety. thiserror generates boilerplate automatically.

**thiserror features:**
- `#[from]` - Automatic `From` impl
- `#[error("...")]` - Display impl
- Supports named fields in error messages

Reference: [thiserror crate](https://docs.rs/thiserror/latest/thiserror/)
