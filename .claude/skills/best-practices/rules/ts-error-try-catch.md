---
title: Error Handling in Try-Catch
impact: MEDIUM
impactDescription: Proper error recovery, improved debugging
tags: typescript, errors, try-catch, instanceof
---

## Error Handling in Try-Catch

**Impact: MEDIUM - Proper error recovery, improved debugging**

Use `instanceof` to handle different error types appropriately.

**Incorrect:**

```typescript
// handles error without type checking
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    return await response.json();
  } catch (error) {
    console.error(error); // only logs error
    throw error;
  }
}
```

**Correct:**

```typescript
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new NotFoundError('User not found', 'user', id);
    }
    return await response.json();
  } catch (error) {
    if (error instanceof NotFoundError) {
      // handle specific error
      throw error;
    } else if (error instanceof TypeError) {
      // handle network error
      throw new Error('Network error');
    } else {
      // handle unexpected error
      throw new Error('Unknown error');
    }
  }
}
```

**Why**: Proper handling of each error type improves application stability and debugging efficiency. Different errors may require different recovery strategies.

Reference: [MDN - try...catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch)
