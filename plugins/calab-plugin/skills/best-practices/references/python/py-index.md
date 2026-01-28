> **원본**: claude-monitoring-main
> **적용**: calab-claude-plugin v2.3.0+

---
title: Python Patterns Index
impact: HIGH
version: 3.10+
tags: python, index, patterns
---

## Python Patterns Index

**18 patterns across 5 categories for Python 3.10+**

### Type Hints (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [py-types-function-annotations](py-types-function-annotations.md) | HIGH | Function type annotations |
| [py-types-variable-annotations](py-types-variable-annotations.md) | MEDIUM | Variable type annotations |
| [py-types-generic-typevar](py-types-generic-typevar.md) | HIGH | Generic types with TypeVar |
| [py-types-protocol](py-types-protocol.md) | HIGH | Protocol for structural typing |

### Pythonic Code (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [py-pythonic-comprehensions](py-pythonic-comprehensions.md) | HIGH | List/dict/set comprehensions |
| [py-pythonic-generators](py-pythonic-generators.md) | HIGH | Generator expressions |
| [py-pythonic-unpacking](py-pythonic-unpacking.md) | MEDIUM | Unpacking and pattern matching |
| [py-pythonic-walrus](py-pythonic-walrus.md) | MEDIUM | Walrus operator (:=) |

### Context Managers (3 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [py-context-with](py-context-with.md) | HIGH | Using `with` statement |
| [py-context-custom](py-context-custom.md) | MEDIUM | Custom context managers |
| [py-context-contextlib](py-context-contextlib.md) | MEDIUM | contextlib utilities |

### Error Handling (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [py-error-hierarchy](py-error-hierarchy.md) | HIGH | Exception hierarchy |
| [py-error-try-except](py-error-try-except.md) | MEDIUM | Try-except-else-finally |
| [py-error-result-pattern](py-error-result-pattern.md) | HIGH | Result pattern with Union |
| [py-error-logging](py-error-logging.md) | HIGH | Logging errors properly |

### Anti-patterns (3 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [py-anti-bare-except](py-anti-bare-except.md) | CRITICAL | Avoid bare except |
| [py-anti-mutable-defaults](py-anti-mutable-defaults.md) | CRITICAL | Avoid mutable default arguments |
| [py-anti-is-comparison](py-anti-is-comparison.md) | MEDIUM | Avoid `is` for value comparison |

## Key Principles

1. **Type Hints**: Functions, variables, Generics, Protocols
2. **Pythonic Code**: Comprehensions and generators over loops
3. **Context Managers**: Safe resource management
4. **Error Handling**: Custom exceptions and Result pattern
5. **Logging**: Proper error tracking in production
6. **Modern Features**: Walrus operator, pattern matching (3.10+)
