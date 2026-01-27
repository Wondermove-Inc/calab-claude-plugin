---
title: Promise.allSettled for Parallel Operations
impact: HIGH
impactDescription: Receive all results even with partial failures
tags: typescript, async, promise, allSettled, parallel
---

## Promise.allSettled for Parallel Operations

**Impact: HIGH - Receive all results even with partial failures**

Use `Promise.allSettled` or Result pattern to handle parallel operations with potential failures.

**Incorrect:**

```typescript
// risk of total failure with Promise.all
async function fetchAllUsers(ids: string[]): Promise<User[]> {
  return await Promise.all(ids.map(id => fetchUser(id))); // entire process fails if one fails
}
```

**Correct:**

```typescript
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };

async function fetchAllUsers(ids: string[]): Promise<Result<User>[]> {
  const promises = ids.map(id =>
    fetchUser(id)
      .then(user => ({ ok: true as const, value: user }))
      .catch(error => ({ ok: false as const, error: error as Error }))
  );

  return await Promise.all(promises);
}

// usage
const results = await fetchAllUsers(['1', '2', '3']);
const successful = results.filter(r => r.ok);
const failed = results.filter(r => !r.ok);
```

**Why**: Using `Promise.allSettled` or the Result pattern allows you to receive all results even if some fail. This is essential for batch operations where partial success is acceptable.

Reference: [MDN - Promise.allSettled()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled)
