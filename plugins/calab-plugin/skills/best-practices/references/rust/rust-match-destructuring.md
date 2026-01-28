---
title: Destructuring
impact: MEDIUM
impactDescription: Concise data extraction
tags: rust, destructuring, pattern-matching, structs
---

## Destructuring

**Impact: MEDIUM - Concise data extraction**

Use destructuring to extract values from complex types.

**Incorrect:**

```rust
// Manual field access
let x = point.x;
let y = point.y;
println!("x: {}, y: {}", x, y);
```

**Correct:**

```rust
struct Point {
    x: i32,
    y: i32,
}

let point = Point { x: 10, y: 20 };

// Struct destructuring
let Point { x, y } = point;
println!("x: {}, y: {}", x, y);

// Tuple destructuring
let (a, b, c) = (1, 2, 3);

// Nested destructuring
match point {
    Point { x: 0, y } => println!("On y-axis at {}", y),
    Point { x, y: 0 } => println!("On x-axis at {}", x),
    Point { x, y } => println!("At ({}, {})", x, y),
}

// Function parameter destructuring
fn print_point(&Point { x, y }: &Point) {
    println!("({}, {})", x, y);
}
```

**Why**: Using destructuring allows decomposing data structures concisely. It works in let statements, function parameters, and match arms.

Reference: [The Rust Book - Destructuring](https://doc.rust-lang.org/book/ch18-03-pattern-syntax.html#destructuring-to-break-apart-values)
