---
title: after() for Non-Blocking Operations
impact: HIGH
impactDescription: Returns response immediately while background tasks continue
tags: after, non-blocking, performance, next.js
---

## after() for Non-Blocking Operations

**Impact: HIGH - Returns response immediately while background tasks continue**

`after()` schedules work to run after the response is sent, improving perceived performance.

**Incorrect (user waits for logging to complete):**

```typescript
export async function POST(request: Request) {
  const data = await updateDatabase(request)
  await logUserAction({ // User waits for this
    userAgent: (await headers()).get('user-agent'),
    action: 'update'
  })
  return Response.json({ status: 'success' })
}
```

**Correct (response sent immediately, logging runs after):**

```typescript
import { after } from 'next/server'

export async function POST(request: Request) {
  const data = await updateDatabase(request)

  after(async () => {
    // Runs after response is sent
    await logUserAction({
      userAgent: (await headers()).get('user-agent'),
      action: 'update'
    })
  })

  return Response.json({ status: 'success' })
}
```

**Why**: `after()` schedules work to run after the response is sent, improving perceived performance.

Reference: [Next.js after()](https://nextjs.org/docs/app/api-reference/functions/after)
