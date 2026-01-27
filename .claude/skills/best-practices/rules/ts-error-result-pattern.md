---
title: Result Pattern (Option/Either)
impact: HIGH
impactDescription: Forces explicit error handling, improves type safety
tags: typescript, errors, result-pattern, option, either
---

## Result Pattern (Option/Either)

**Impact: HIGH - Forces explicit error handling, improves type safety**

Use Result types to make error handling explicit in the type system.

**Incorrect:**

```typescript
// throws exceptions
function parseJSON<T>(json: string): T {
  return JSON.parse(json) as T; // caller must use try-catch
}
```

**Correct:**

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function parseJSON<T>(json: string): Result<T, SyntaxError> {
  try {
    const value = JSON.parse(json) as T;
    return { ok: true, value };
  } catch (error) {
    return { ok: false, error: error as SyntaxError };
  }
}

// usage
const result = parseJSON<User>('{"name":"John"}');
if (result.ok) {
  console.log(result.value.name);
} else {
  console.error(result.error.message);
}
```

**Why**: The Result pattern forces explicit error handling and enables safe error handling using the type system. Callers cannot forget to handle errors because the return type requires it.

Reference: [TypeScript Handbook - Discriminated Unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)
