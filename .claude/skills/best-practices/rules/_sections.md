# Sections

> **원본**: claude-monitoring-main
> **적용**: calab-claude-plugin v2.3.0+

This file defines all sections, their ordering, impact levels, and descriptions.
The section ID (in parentheses) is the filename prefix used to group rules.

---

## TypeScript Patterns (ts-)

### 1. TypeScript - Type System (ts-types-)

**Impact:** CRITICAL
**Description:** Type safety fundamentals. Avoiding `any`, using unions, generics, const assertions, keyof typeof, and type guards.

### 2. TypeScript - Validation (ts-validation-)

**Impact:** HIGH
**Description:** Schema validation with Zod for runtime validation with inferred types.

### 3. TypeScript - Error Handling (ts-error-)

**Impact:** HIGH
**Description:** Custom errors, Result pattern, proper try-catch, error class hierarchies.

### 4. TypeScript - Async Patterns (ts-async-)

**Impact:** HIGH
**Description:** Async/await patterns, Promise.allSettled, retry with backoff, batch processing.

### 5. TypeScript - Framework Integration (ts-nextjs-)

**Impact:** HIGH
**Description:** Next.js API route typing for type-safe request/response handling.

### 6. TypeScript - Code Organization (ts-org-)

**Impact:** MEDIUM
**Description:** Interface vs Type, barrel exports, path aliases, strict mode.

### 7. TypeScript - Anti-patterns (ts-anti-)

**Impact:** HIGH
**Description:** Type assertion abuse, @ts-ignore, empty interfaces.

---

## Python Patterns (py-)

### 6. Python - Type Hints (py-types-)

**Impact:** HIGH
**Description:** Function/variable annotations, generics, protocols.

### 7. Python - Pythonic Code (py-pythonic-)

**Impact:** HIGH
**Description:** Comprehensions, generators, unpacking, walrus operator.

### 8. Python - Context Managers (py-context-)

**Impact:** HIGH
**Description:** Resource management with `with`, custom managers, contextlib.

### 9. Python - Error Handling (py-error-)

**Impact:** HIGH
**Description:** Exception hierarchy, try-except-else-finally, Result pattern, logging.

### 10. Python - Anti-patterns (py-anti-)

**Impact:** CRITICAL
**Description:** Bare except, mutable defaults, `is` comparison abuse.

---

## Go Patterns (go-)

### 11. Go - Error Handling (go-error-)

**Impact:** CRITICAL
**Description:** Explicit returns, error wrapping, custom types, defer.

### 12. Go - Concurrency (go-concurrency-)

**Impact:** HIGH
**Description:** Goroutines, channels, WaitGroup, context for cancellation.

### 13. Go - Interface Design (go-interface-)

**Impact:** HIGH
**Description:** Small interfaces, implicit implementation, segregation.

### 14. Go - Code Organization (go-org-)

**Impact:** MEDIUM
**Description:** Package structure, internal packages, modules, naming.

### 15. Go - Anti-patterns (go-anti-)

**Impact:** CRITICAL
**Description:** Goroutine leaks, ignoring errors, empty interface abuse.

---

## Rust Patterns (rust-)

### 16. Rust - Ownership & Borrowing (rust-ownership-)

**Impact:** CRITICAL
**Description:** Ownership transfer, borrowing, lifetimes, Clone vs Copy.

### 17. Rust - Error Handling (rust-error-)

**Impact:** CRITICAL
**Description:** Result, Option, ? operator, thiserror.

### 18. Rust - Pattern Matching (rust-match-)

**Impact:** HIGH
**Description:** Match expressions, if let, destructuring, guards.

### 19. Rust - Memory Safety (rust-memory-)

**Impact:** CRITICAL
**Description:** No null, no data races, safe abstractions, unsafe isolation.

### 20. Rust - Anti-patterns (rust-anti-)

**Impact:** HIGH
**Description:** Unnecessary clone, unwrap() in production, string concat loops.

---

## React Patterns (react-)

### 21. React - Eliminating Waterfalls (react-async-)

**Impact:** CRITICAL
**Description:** Waterfalls are the #1 performance killer. Each sequential await adds full network latency.

### 22. React - Bundle Size Optimization (react-bundle-)

**Impact:** CRITICAL
**Description:** Reducing initial bundle size improves Time to Interactive and Largest Contentful Paint.

### 23. React - Server-Side Performance (react-server-)

**Impact:** HIGH
**Description:** Optimizing server-side rendering and data fetching eliminates server-side waterfalls.

### 24. React - Component Patterns (react-components-)

**Impact:** MEDIUM
**Description:** Foundation for clean, maintainable React code with TypeScript.

### 25. React - State Management (react-state-)

**Impact:** MEDIUM
**Description:** Core to React application architecture. Prevents bugs, improves data flow clarity.

### 26. React - Re-render Optimization (react-rerender-)

**Impact:** MEDIUM
**Description:** Reducing unnecessary re-renders minimizes wasted computation.

### 27. React - Side Effects (react-effects-)

**Impact:** LOW-MEDIUM
**Description:** Prevents bugs, memory leaks, and race conditions.

### 28. React - JavaScript Performance (react-js-)

**Impact:** LOW-MEDIUM
**Description:** Micro-optimizations for hot paths can add up to meaningful improvements.
