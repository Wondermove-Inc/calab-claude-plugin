---
title: Custom Error Types
impact: HIGH
impactDescription: Granular error handling, easier debugging
tags: typescript, errors, custom-errors, error-handling
---

## Custom Error Types

**Impact: HIGH - Granular error handling, easier debugging**

Create custom error classes with relevant context for better error handling.

**Incorrect:**

```typescript
// only uses generic Error
function validateUser(user: unknown): User {
  if (typeof user !== 'object') {
    throw new Error('Invalid user');
  }
}
```

**Correct:**

```typescript
class ValidationError extends Error {
  constructor(
    message: string,
    public field: string,
    public value: unknown
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

class NotFoundError extends Error {
  constructor(
    message: string,
    public resource: string,
    public id: string
  ) {
    super(message);
    this.name = 'NotFoundError';
  }
}

function validateUser(user: unknown): User {
  if (typeof user !== 'object' || user === null) {
    throw new ValidationError('Invalid user object', 'user', user);
  }
  // validation logic
}
```

**Why**: Using custom error types allows for more granular error handling logic and easier debugging. Error handlers can use `instanceof` to handle specific error types differently.

Reference: [MDN - Custom Errors](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error#custom_error_types)
