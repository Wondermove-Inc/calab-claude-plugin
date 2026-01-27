---
title: Intersection Types for Composition
impact: MEDIUM
impactDescription: Improved code reusability, follows DRY principle
tags: typescript, types, intersection, composition, DRY
---

## Intersection Types for Composition

**Impact: MEDIUM - Improved code reusability, follows DRY principle**

Use intersection types to compose types from reusable parts.

**Incorrect:**

```typescript
// duplicated property definition
interface User {
  name: string;
  email: string;
  createdAt: Date;
  updatedAt: Date;
}
```

**Correct:**

```typescript
interface Timestamped {
  createdAt: Date;
  updatedAt: Date;
}

interface UserData {
  name: string;
  email: string;
}

type User = UserData & Timestamped;

const user: User = {
  name: "John",
  email: "john@example.com",
  createdAt: new Date(),
  updatedAt: new Date()
};
```

**Why**: Using intersection types improves code reusability and follows the DRY principle. Common patterns like timestamps, audit fields, or metadata can be composed into any type.

Reference: [TypeScript Handbook - Intersection Types](https://www.typescriptlang.org/docs/handbook/2/objects.html#intersection-types)
