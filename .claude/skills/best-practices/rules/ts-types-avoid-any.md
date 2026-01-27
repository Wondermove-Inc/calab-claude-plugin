---
title: Avoid `any` Type
impact: CRITICAL
impactDescription: Type safety loss, runtime errors, disabled IDE support
tags: typescript, types, any, type-safety
---

## Avoid `any` Type

**Impact: CRITICAL - Type safety loss, runtime errors, disabled IDE support**

Explicit types prevent bugs and enable IDE support.

**Incorrect:**

```typescript
// uses any (loses type safety)
function getUser(id: any): any {
  // implementation
}
```

**Correct:**

```typescript
// explicit type definition
interface User {
  id: string;
  name: string;
  email: string;
}

function getUser(id: string): User {
  // implementation
}
```

**Why**: `any` disables TypeScript's type checking. Using explicit types allows you to catch errors at compile time.

Reference: [TypeScript Handbook - Do's and Don'ts](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
