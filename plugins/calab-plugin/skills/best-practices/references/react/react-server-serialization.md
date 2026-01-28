---
title: Minimize RSC Serialization Overhead
impact: HIGH
impactDescription: Reduces RSC payload size and parsing time
tags: rsc, serialization, performance
---

## Minimize RSC Serialization Overhead

**Impact: HIGH - Reduces RSC payload size and parsing time**

Everything passed from Server to Client Components must be serialized. Pass minimal data.

**Incorrect (passing entire objects when only specific fields needed):**

```tsx
async function UserPage() {
  const user = await getFullUserWithAllRelations() // 50+ fields
  return <UserCard user={user} />
}
```

**Correct (pass only what's needed):**

```tsx
async function UserPage() {
  const user = await getFullUserWithAllRelations()
  return (
    <UserCard
      name={user.name}
      avatar={user.avatar}
      email={user.email}
    />
  )
}
```

**Why**: Everything passed from Server to Client Components must be serialized. Pass minimal data.

Reference: [RSC Payload](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
