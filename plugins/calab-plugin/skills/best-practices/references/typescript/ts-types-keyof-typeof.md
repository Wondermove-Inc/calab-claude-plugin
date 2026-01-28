---
title: Extract Union Types with keyof typeof
impact: HIGH
impactDescription: Type-safe key extraction from objects
tags: typescript, types, keyof, typeof, union
---

## Extract Union Types with keyof typeof

**Impact: HIGH - Type-safe key extraction from objects**

Use `keyof typeof` to extract union types from object keys, ensuring type safety when accessing configuration objects.

**Incorrect:**

```typescript
const CONFIG = {
  database: { host: 'localhost', port: 5432 },
  redis: { host: 'localhost', port: 6379 },
  api: { host: 'localhost', port: 3000 }
};

// Accepts any string, no type safety
function getConfig(service: string) {
  return CONFIG[service]; // Error: implicit any
}
```

**Correct:**

```typescript
const CONFIG = {
  database: { host: 'localhost', port: 5432 },
  redis: { host: 'localhost', port: 6379 },
  api: { host: 'localhost', port: 3000 }
} as const;

// Extract keys as union type: 'database' | 'redis' | 'api'
type ServiceName = keyof typeof CONFIG;

function getConfig(service: ServiceName) {
  return CONFIG[service]; // Type-safe access
}

// Also works for values
const ERROR_CODES = {
  NOT_FOUND: 404,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403
} as const;

type ErrorCodeKey = keyof typeof ERROR_CODES; // 'NOT_FOUND' | 'UNAUTHORIZED' | 'FORBIDDEN'
type ErrorCodeValue = typeof ERROR_CODES[ErrorCodeKey]; // 404 | 401 | 403

// Practical pattern: Enum-like object with type safety
const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
} as const;

type LogLevelKey = keyof typeof LogLevel;
type LogLevelValue = typeof LogLevel[LogLevelKey];

function log(level: LogLevelValue, message: string) {
  // Only accepts 0 | 1 | 2 | 3
}
```

**Why**: `keyof typeof` extracts union types from runtime objects, enabling type-safe access patterns. Combined with `as const`, this creates enum-like structures without TypeScript enums, which are better for tree-shaking.

Reference: [TypeScript Handbook - keyof Type Operator](https://www.typescriptlang.org/docs/handbook/2/keyof-types.html)
