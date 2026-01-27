> **원본**: claude-monitoring-main
> **적용**: calab-claude-plugin v2.3.0+

---
title: Rust Patterns Index
impact: HIGH
version: 2021 Edition
tags: rust, index, patterns
---

## Rust Patterns Index

**19 patterns across 5 categories for Rust 2021 Edition**

### Ownership & Borrowing (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [rust-ownership-transfer](rust-ownership-transfer.md) | HIGH | Ownership transfer |
| [rust-ownership-borrowing](rust-ownership-borrowing.md) | CRITICAL | Borrowing with &T and &mut T |
| [rust-ownership-lifetimes](rust-ownership-lifetimes.md) | HIGH | Lifetime annotations |
| [rust-ownership-clone-copy](rust-ownership-clone-copy.md) | MEDIUM | Clone vs Copy |

### Error Handling (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [rust-error-result](rust-error-result.md) | CRITICAL | Result<T, E> pattern |
| [rust-error-option](rust-error-option.md) | HIGH | Option<T> for nullable values |
| [rust-error-question-mark](rust-error-question-mark.md) | HIGH | ? operator for propagation |
| [rust-error-thiserror](rust-error-thiserror.md) | HIGH | Custom errors with thiserror |

### Pattern Matching (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [rust-match-expressions](rust-match-expressions.md) | HIGH | Match expressions |
| [rust-match-if-let](rust-match-if-let.md) | MEDIUM | if let for single pattern |
| [rust-match-destructuring](rust-match-destructuring.md) | MEDIUM | Destructuring |
| [rust-match-guards](rust-match-guards.md) | MEDIUM | Match guards |

### Memory Safety (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [rust-memory-no-null](rust-memory-no-null.md) | CRITICAL | No null pointers |
| [rust-memory-no-data-races](rust-memory-no-data-races.md) | CRITICAL | No data races |
| [rust-memory-safe-abstractions](rust-memory-safe-abstractions.md) | HIGH | Safe abstractions |
| [rust-memory-unsafe-isolation](rust-memory-unsafe-isolation.md) | HIGH | Unsafe code isolation |

### Anti-patterns (3 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [rust-anti-unnecessary-clone](rust-anti-unnecessary-clone.md) | HIGH | Avoid unnecessary Clone |
| [rust-anti-unwrap-production](rust-anti-unwrap-production.md) | CRITICAL | Avoid unwrap() in production |
| [rust-anti-string-concat-loop](rust-anti-string-concat-loop.md) | MEDIUM | Avoid string concat in loops |

## Key Principles

1. **Ownership**: Clear data flow, prevent memory leaks
2. **Borrowing**: Efficient access without ownership transfer
3. **Lifetimes**: Specify reference validity
4. **Result/Option**: No exceptions, explicit error handling
5. **Pattern Matching**: Handle all cases, compiler-enforced
6. **Memory Safety**: No null, no data races by design
