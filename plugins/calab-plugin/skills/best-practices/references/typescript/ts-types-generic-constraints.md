---
title: Generic Constraints
impact: HIGH
impactDescription: Reusable functions with maintained type safety
tags: typescript, types, generics, constraints, extends
---

## Generic Constraints

**Impact: HIGH - Reusable functions with maintained type safety**

Use `extends` to constrain generic types for type-safe operations.

**Incorrect:**

```typescript
// generic without constraints
function findById<T>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id); // Error: 'id' doesn't exist on T
}
```

**Correct:**

```typescript
interface HasId {
  id: string;
}

function findById<T extends HasId>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// Usage with any type that has an 'id' property
interface User extends HasId {
  name: string;
}

const users: User[] = [{ id: "1", name: "John" }];
const user = findById(users, "1"); // Type: User | undefined
```

**Why**: Using generic constraints allows you to write reusable functions while maintaining type safety. The constraint ensures the generic type has the required properties.

Reference: [TypeScript Handbook - Generic Constraints](https://www.typescriptlang.org/docs/handbook/2/generics.html#generic-constraints)
