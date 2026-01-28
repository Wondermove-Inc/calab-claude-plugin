---
title: Error Class Hierarchies
impact: HIGH
impactDescription: Typed error handling with inheritance
tags: typescript, error, class, inheritance, hierarchy
---

## Error Class Hierarchies

**Impact: HIGH - Typed error handling with inheritance**

Create structured error hierarchies using class inheritance for domain-specific error handling with proper typing.

**Incorrect:**

```typescript
// Flat error types - hard to categorize
class NotFoundError extends Error {}
class UnauthorizedError extends Error {}
class ValidationError extends Error {}
class DatabaseError extends Error {}

// No way to catch "all HTTP errors" vs "all system errors"
try {
  await fetchUser(id);
} catch (error) {
  // Have to check each type individually
  if (error instanceof NotFoundError) { /* ... */ }
  if (error instanceof UnauthorizedError) { /* ... */ }
  // etc.
}
```

**Correct:**

```typescript
// Base application error
abstract class AppError extends Error {
  abstract readonly code: string;
  abstract readonly statusCode: number;

  constructor(message: string, public readonly cause?: Error) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace?.(this, this.constructor);
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      ...(process.env.NODE_ENV === 'development' && { stack: this.stack })
    };
  }
}

// HTTP Error hierarchy
abstract class HttpError extends AppError {
  abstract readonly statusCode: number;
}

class NotFoundError extends HttpError {
  readonly code = 'NOT_FOUND';
  readonly statusCode = 404;

  constructor(resource: string, id: string) {
    super(`${resource} with id '${id}' not found`);
  }
}

class UnauthorizedError extends HttpError {
  readonly code = 'UNAUTHORIZED';
  readonly statusCode = 401;
}

class ValidationError extends HttpError {
  readonly code = 'VALIDATION_ERROR';
  readonly statusCode = 400;

  constructor(public readonly fieldErrors: Record<string, string[]>) {
    super('Validation failed');
  }
}

// System Error hierarchy
abstract class SystemError extends AppError {
  readonly statusCode = 500;
}

class DatabaseError extends SystemError {
  readonly code = 'DATABASE_ERROR';

  constructor(operation: string, cause?: Error) {
    super(`Database operation '${operation}' failed`, cause);
  }
}

// Usage with hierarchical catching
async function handleRequest() {
  try {
    await processRequest();
  } catch (error) {
    if (error instanceof HttpError) {
      // Handle all HTTP errors uniformly
      return Response.json(error.toJSON(), { status: error.statusCode });
    }
    if (error instanceof SystemError) {
      // Log and return generic error
      console.error('System error:', error);
      return Response.json({ code: 'INTERNAL_ERROR' }, { status: 500 });
    }
    throw error; // Re-throw unknown errors
  }
}
```

**Why**: Error hierarchies enable catching errors at different granularity levels. Catch `HttpError` for all client-facing errors, or catch specific types like `NotFoundError`. This pattern provides type-safe error handling while reducing boilerplate.

Reference: [MDN - Custom Error Types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error#custom_error_types)
