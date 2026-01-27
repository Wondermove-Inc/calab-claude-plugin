> **원본**: claude-monitoring-main
> **적용**: calab-claude-plugin v2.3.0+

---
title: TypeScript Patterns Index
impact: HIGH
version: 5.0+
tags: typescript, index, patterns
---

## TypeScript Patterns Index

**25 patterns across 7 categories for TypeScript 5.0+**

### Type System (7 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [ts-types-avoid-any](ts-types-avoid-any.md) | CRITICAL | Avoid `any` type, use explicit types |
| [ts-types-union-narrowing](ts-types-union-narrowing.md) | HIGH | Union types with type narrowing |
| [ts-types-intersection](ts-types-intersection.md) | MEDIUM | Intersection types for composition |
| [ts-types-generic-constraints](ts-types-generic-constraints.md) | HIGH | Generic constraints for type safety |
| [ts-types-const-assertions](ts-types-const-assertions.md) | HIGH | `as const` for literal types |
| [ts-types-keyof-typeof](ts-types-keyof-typeof.md) | HIGH | `keyof typeof` for union extraction |
| [ts-types-type-guards](ts-types-type-guards.md) | HIGH | `is` predicate type guards |

### Validation (1 pattern)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [ts-validation-zod-schema](ts-validation-zod-schema.md) | HIGH | Zod schema validation with type inference |

### Error Handling (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [ts-error-custom-types](ts-error-custom-types.md) | HIGH | Custom error types for granular handling |
| [ts-error-result-pattern](ts-error-result-pattern.md) | HIGH | Result pattern (Option/Either) |
| [ts-error-try-catch](ts-error-try-catch.md) | MEDIUM | Proper try-catch with type checking |
| [ts-error-class-hierarchies](ts-error-class-hierarchies.md) | HIGH | Error class hierarchies with inheritance |

### Async Patterns (5 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [ts-async-error-handling](ts-async-error-handling.md) | HIGH | Async/await with error handling |
| [ts-async-all-settled](ts-async-all-settled.md) | HIGH | Promise.allSettled for parallel ops |
| [ts-async-avoid-callbacks](ts-async-avoid-callbacks.md) | MEDIUM | Avoid callback hell |
| [ts-async-retry-pattern](ts-async-retry-pattern.md) | MEDIUM | Retry with exponential backoff |
| [ts-async-batch-processing](ts-async-batch-processing.md) | MEDIUM | Batch processing with allSettled |

### Framework Integration (1 pattern)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [ts-nextjs-api-route-typing](ts-nextjs-api-route-typing.md) | HIGH | Next.js API route type safety |

### Code Organization (4 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [ts-org-interface-vs-type](ts-org-interface-vs-type.md) | MEDIUM | Interface vs Type usage |
| [ts-org-barrel-exports](ts-org-barrel-exports.md) | MEDIUM | Barrel exports (conditional) |
| [ts-org-path-aliases](ts-org-path-aliases.md) | MEDIUM | Path aliases in tsconfig |
| [ts-org-strict-mode](ts-org-strict-mode.md) | CRITICAL | Strict mode configuration |

### Anti-patterns (3 patterns)

| Pattern | Impact | Description |
|---------|--------|-------------|
| [ts-anti-type-assertion](ts-anti-type-assertion.md) | HIGH | Avoid type assertion abuse |
| [ts-anti-ignore-errors](ts-anti-ignore-errors.md) | CRITICAL | Never use @ts-ignore |
| [ts-anti-empty-interfaces](ts-anti-empty-interfaces.md) | LOW | Avoid empty interfaces |

## Key Principles

1. **Type Safety First**: Avoid `any`, use explicit type definitions
2. **Literal Types**: Use `as const` for precise type inference
3. **Type Guards**: Use `is` predicates for runtime type narrowing
4. **Schema Validation**: Use Zod for runtime validation with type inference
5. **Error Hierarchies**: Create structured error classes for granular handling
6. **Union & Generics**: Utilize union types, intersection types, and generic constraints
7. **Safe Async**: Retry patterns, batch processing, proper error handling
8. **Framework Types**: Type API routes and external boundaries properly
9. **Interface vs Type**: Use interface for objects, type for unions/primitives
10. **Strict Mode**: Enable strict mode for maximum type safety
