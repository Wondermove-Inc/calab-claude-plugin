---
title: React.cache() for Request Deduplication
impact: HIGH
impactDescription: Eliminates duplicate database/API calls within a single request
tags: cache, deduplication, rsc, performance
---

## React.cache() for Request Deduplication

**Impact: HIGH - Eliminates duplicate database/API calls within a single request**

`cache()` deduplicates identical function calls within a single server render pass.

**Incorrect (multiple components call the same function = multiple DB queries):**

```typescript
async function getCurrentUser() {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({ where: { id: session.user.id } })
}

// Called in Header, Sidebar, and MainContent = 3 DB queries
```

**Correct (cached function = 1 DB query):**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({ where: { id: session.user.id } })
})

// Called in Header, Sidebar, and MainContent = 1 DB query (deduplicated)
```

**Why**: `cache()` deduplicates identical function calls within a single server render pass.

Reference: [React cache()](https://react.dev/reference/react/cache)
