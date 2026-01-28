---
title: Promise.all() for Independent Operations
impact: CRITICAL
impactDescription: 2-10× improvement through parallel execution
tags: async, parallelization, promises, waterfalls
---

## Promise.all() for Independent Operations

**Impact: CRITICAL - 2-10× improvement through parallel execution**

When async operations have no interdependencies, execute them concurrently.

**Incorrect (sequential execution, 3 round trips):**

```typescript
// Sequential: 3 round trips, ~900ms total
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**Correct (parallel execution, 1 round trip):**

```typescript
// Parallel: 1 round trip, ~300ms total
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

**Why**: Sequential awaits create a "waterfall" where each request waits for the previous one to complete. Independent operations should always run in parallel.

Reference: [Promise.all() - MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)
