---
title: Match Expressions
impact: HIGH
impactDescription: Exhaustive handling, compiler-enforced
tags: rust, match, pattern-matching, exhaustive
---

## Match Expressions

**Impact: HIGH - Exhaustive handling, compiler-enforced**

Use match for exhaustive pattern handling.

**Incorrect:**

```rust
// if-else chain
fn process_message(msg: Message) {
    if matches!(msg, Message::Quit) {
        println!("Quit");
    } else if let Message::Move { x, y } = msg {
        println!("Move to ({}, {})", x, y);
    }
    // Cases may be missed
}
```

**Correct:**

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn process_message(msg: Message) {
    match msg {
        Message::Quit => println!("Quit"),
        Message::Move { x, y } => println!("Move to ({}, {})", x, y),
        Message::Write(text) => println!("Text: {}", text),
        Message::ChangeColor(r, g, b) => println!("Color: ({}, {}, {})", r, g, b),
    }
}

// Number matching
fn classify_number(n: i32) -> &'static str {
    match n {
        0 => "zero",
        1..=9 => "single digit",
        10..=99 => "double digit",
        _ => "large number",
    }
}
```

**Why**: `match` forces handling all cases, preventing bugs. The compiler errors if you miss a variant.

**Match features:**
- Exhaustive (must handle all cases)
- Pattern bindings
- Range patterns (`1..=9`)
- Wildcard (`_`)

Reference: [The Rust Book - Match](https://doc.rust-lang.org/book/ch06-02-match.html)
