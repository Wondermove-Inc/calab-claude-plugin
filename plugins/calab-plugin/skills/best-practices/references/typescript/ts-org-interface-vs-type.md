---
title: Interface vs Type
impact: MEDIUM
impactDescription: Clear type intentions, better extensibility
tags: typescript, interface, type, organization
---

## Interface vs Type

**Impact: MEDIUM - Clear type intentions, better extensibility**

Use interface for extensible object structures, type for unions and primitives.

**Incorrect:**

```typescript
// indiscriminate use of Interface and Type
type User = {  // Interface is more suitable
  id: string;
  name: string;
};

interface UserRole {  // Type alias is more suitable
  role: 'admin' | 'user';
}
```

**Correct:**

```typescript
// Interface: extensible object structure
interface User {
  id: string;
  name: string;
}

interface AdminUser extends User {
  permissions: string[];
}

// Type: Union, Intersection, Primitive aliases
type UserId = string;
type UserRole = 'admin' | 'user' | 'guest';
type UserWithRole = User & { role: UserRole };
```

**Why**:
- **Interface** is suitable for defining and extending object structures (supports `extends` and declaration merging)
- **Type** is suitable for Union, Intersection, and Primitive aliases (more flexible for complex types)

Reference: [TypeScript Handbook - Types vs Interfaces](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#differences-between-type-aliases-and-interfaces)
