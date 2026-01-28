---
title: Race Condition Prevention
impact: LOW-MEDIUM
impactDescription: Prevents displaying stale data from slow requests
tags: useEffect, race-condition, async
---

## Race Condition Prevention

**Impact: LOW-MEDIUM - Prevents displaying stale data from slow requests**

When dependencies change, in-flight requests should be ignored or cancelled.

**Incorrect (race condition possible):**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    // If userId changes quickly, old response might arrive after new one
    fetchUser(userId).then(setUser)
  }, [userId])
}
```

**Correct (cancelled flag prevents stale updates):**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    let cancelled = false

    fetchUser(userId).then(data => {
      if (!cancelled) setUser(data)
    })

    return () => { cancelled = true }
  }, [userId])
}

// Or with AbortController
useEffect(() => {
  const controller = new AbortController()

  fetchUser(userId, { signal: controller.signal })
    .then(setUser)
    .catch(err => {
      if (err.name !== 'AbortError') throw err
    })

  return () => controller.abort()
}, [userId])
```

**Why**: When dependencies change, in-flight requests should be ignored or cancelled.

Reference: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
