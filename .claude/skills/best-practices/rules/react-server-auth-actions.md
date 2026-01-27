---
title: Authenticate Server Actions
impact: HIGH
impactDescription: Prevents unauthorized access, essential security pattern
tags: server-actions, authentication, security
---

## Authenticate Server Actions

**Impact: HIGH - Prevents unauthorized access, essential security pattern**

Server Actions are public HTTP endpoints. Always authenticate and authorize before performing mutations.

**Incorrect (no authentication check):**

```typescript
'use server'

export async function deleteUser(userId: string) {
  await db.user.delete({ where: { id: userId } })
}
```

**Correct (authentication and authorization):**

```typescript
'use server'

export async function deleteUser(userId: string) {
  const session = await verifySession()
  if (!session) {
    throw new Error('Must be logged in')
  }
  if (session.user.role !== 'admin' && session.user.id !== userId) {
    throw new Error('Cannot delete other users')
  }
  await db.user.delete({ where: { id: userId } })
}
```

**Why**: Server Actions are public HTTP endpoints. Always authenticate and authorize before performing mutations.

Reference: [Next.js Server Actions Security](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations#security)
