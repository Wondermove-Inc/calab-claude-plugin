---
title: Defer Await Until Needed
impact: CRITICAL
impactDescription: Eliminates unnecessary blocking, enables early returns
tags: async, early-return, optimization
---

## Defer Await Until Needed

**Impact: CRITICAL - Eliminates unnecessary blocking, enables early returns**

Perform validation and early returns before starting async operations to avoid unnecessary work.

**Incorrect (blocks on await even when skipProcessing is true):**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  const userData = await fetchUserData(userId)
  if (skipProcessing) return { skipped: true }
  return processUserData(userData)
}
```

**Correct (early return before await):**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  if (skipProcessing) return { skipped: true }
  const userData = await fetchUserData(userId)
  return processUserData(userData)
}
```

**Why**: Perform validation and early returns before starting async operations to avoid unnecessary work.

Reference: [Async/Await Best Practices](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises)
