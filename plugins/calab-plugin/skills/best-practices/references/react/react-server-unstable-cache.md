---
title: Use unstable_cache for Cross-Request Caching
impact: HIGH
impactDescription: Reduces database load, sub-millisecond response for cached data
tags: cache, cross-request, performance, next.js
---

## Use unstable_cache for Cross-Request Caching

**Impact: HIGH - Reduces database load, sub-millisecond response for cached data**

Data that doesn't change frequently should be cached across requests.

**Incorrect (fetches from DB on every request):**

```typescript
async function getPopularPosts() {
  return await db.post.findMany({
    orderBy: { views: 'desc' },
    take: 10
  })
}
```

**Correct (cached with revalidation):**

```typescript
import { unstable_cache } from 'next/cache'

const getPopularPosts = unstable_cache(
  async () => {
    return await db.post.findMany({
      orderBy: { views: 'desc' },
      take: 10
    })
  },
  ['popular-posts'],
  { revalidate: 3600, tags: ['posts'] } // Cache for 1 hour
)
```

**Why**: Data that doesn't change frequently should be cached across requests.

Reference: [Next.js unstable_cache](https://nextjs.org/docs/app/api-reference/functions/unstable_cache)
