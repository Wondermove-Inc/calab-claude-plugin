---
title: Avoid Type Assertion Abuse
impact: HIGH
impactDescription: Runtime errors from unchecked types
tags: typescript, anti-pattern, type-assertion, type-guard
---

## Avoid Type Assertion Abuse

**Impact: HIGH - Runtime errors from unchecked types**

Use type guards instead of type assertions to validate types at runtime.

**Incorrect:**

```typescript
const user = data as User; // assertion without type validation
```

**Correct:**

```typescript
function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    'name' in data
  );
}

if (isUser(data)) {
  const user = data; // safely verified with type guard
  console.log(user.name);
}
```

**Why**: Type assertions bypass TypeScript's type checking. If the data doesn't match the asserted type at runtime, you'll get errors. Type guards validate at runtime and narrow the type safely.

**When assertions are acceptable:**
- DOM element types that TypeScript can't infer
- API responses with known schemas (paired with validation)
- Test code where you control the input

Reference: [TypeScript Handbook - Type Guards](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates)
