---
title: Union Types & Type Narrowing
impact: HIGH
impactDescription: Prevents runtime errors, ensures type safety
tags: typescript, types, union, narrowing, discriminated-unions
---

## Union Types & Type Narrowing

**Impact: HIGH - Prevents runtime errors, ensures type safety**

Use union types with type guards for safe property access.

**Incorrect:**

```typescript
// access without type guard
function handleResult(result: any): void {
  console.log(result.data); // possible runtime error
}
```

**Correct:**

```typescript
type Result<T> = { success: true; data: T } | { success: false; error: string };

function handleResult<T>(result: Result<T>): void {
  // Type narrowing
  if (result.success) {
    console.log(result.data); // TypeScript knows 'data' exists
  } else {
    console.error(result.error); // TypeScript knows 'error' exists
  }
}
```

**Why**: Using union types and type narrowing prevents runtime errors and ensures type safety. TypeScript can infer the correct type within each branch.

Reference: [TypeScript Handbook - Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
