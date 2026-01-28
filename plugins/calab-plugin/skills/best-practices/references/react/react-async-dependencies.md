---
title: Dependency-Based Parallelization
impact: CRITICAL
impactDescription: Maximizes parallelism while respecting data dependencies
tags: async, dependencies, parallelization
---

## Dependency-Based Parallelization

**Impact: CRITICAL - Maximizes parallelism while respecting data dependencies**

Analyze data dependencies and parallelize everything that doesn't have a dependency chain.

**Incorrect (all sequential, even independent operations):**

```typescript
const user = await fetchUser(userId)
const settings = await fetchSettings(userId) // Independent of user
const posts = await fetchPosts(user.id) // Depends on user
```

**Correct (parallelize where possible, sequence where required):**

```typescript
const [user, settings] = await Promise.all([
  fetchUser(userId),
  fetchSettings(userId)
])
const posts = await fetchPosts(user.id) // Must wait for user
```

**Why**: Analyze data dependencies and parallelize everything that doesn't have a dependency chain.

Reference: [Async Patterns](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises)
