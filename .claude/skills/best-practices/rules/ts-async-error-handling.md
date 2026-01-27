---
title: Async/Await with Error Handling
impact: HIGH
impactDescription: Partial failure handling, improved process stability
tags: typescript, async, await, error-handling
---

## Async/Await with Error Handling

**Impact: HIGH - Partial failure handling, improved process stability**

Handle errors individually to allow partial failures without stopping the entire process.

**Incorrect:**

```typescript
// Promise chaining without error handling
function processUsers(ids: string[]): Promise<User[]> {
  return Promise.all(ids.map(id => fetchUser(id))); // entire process fails if one fails
}
```

**Correct:**

```typescript
async function processUsers(ids: string[]): Promise<User[]> {
  const users: User[] = [];

  for (const id of ids) {
    try {
      const user = await fetchUser(id);
      users.push(user);
    } catch (error) {
      console.error(`Failed to fetch user ${id}:`, error);
      // one failure doesn't stop the entire process
    }
  }

  return users;
}
```

**Why**: Individual error handling allows partial failures and improves overall process stability. The process continues even if some operations fail.

Reference: [MDN - async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
