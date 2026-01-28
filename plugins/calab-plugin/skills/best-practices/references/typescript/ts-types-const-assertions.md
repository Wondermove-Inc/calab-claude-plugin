---
title: Use const Assertions for Literal Types
impact: HIGH
impactDescription: Enables precise literal types, improves type inference
tags: typescript, types, const, literal-types, inference
---

## Use const Assertions for Literal Types

**Impact: HIGH - Enables precise literal types, improves type inference**

Use `as const` to create readonly literal types instead of widened primitive types.

**Incorrect:**

```typescript
// Type is widened to { status: string; code: number }
const response = {
  status: 'success',
  code: 200
};

// Type is string[]
const STATUSES = ['pending', 'active', 'archived'];

function setStatus(status: string) {} // Too permissive
```

**Correct:**

```typescript
// Type is { readonly status: 'success'; readonly code: 200 }
const response = {
  status: 'success',
  code: 200
} as const;

// Type is readonly ['pending', 'active', 'archived']
const STATUSES = ['pending', 'active', 'archived'] as const;

// Extract union type: 'pending' | 'active' | 'archived'
type Status = typeof STATUSES[number];

function setStatus(status: Status) {} // Only accepts valid statuses

// Works with object keys too
const HTTP_CODES = {
  OK: 200,
  NOT_FOUND: 404,
  SERVER_ERROR: 500
} as const;

type HttpCode = typeof HTTP_CODES[keyof typeof HTTP_CODES]; // 200 | 404 | 500
```

**Why**: `as const` preserves literal types and makes objects/arrays readonly. This enables TypeScript to infer precise types, catching typos and invalid values at compile time rather than runtime.

Reference: [TypeScript Handbook - const assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#literal-types)
