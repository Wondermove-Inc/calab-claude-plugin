---
title: useEffect Dependency Array
impact: LOW-MEDIUM
impactDescription: Prevents stale closures and missing updates
tags: useEffect, dependencies, stale-closure
---

## useEffect Dependency Array

**Impact: LOW-MEDIUM - Prevents stale closures and missing updates**

Effects re-run when dependencies change. Missing dependencies cause stale data bugs.

**Incorrect (missing dependency):**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, []) // Missing userId dependency!
}
```

**Correct (all dependencies declared):**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    let cancelled = false

    fetchUser(userId).then(data => {
      if (!cancelled) setUser(data)
    })

    return () => { cancelled = true }
  }, [userId]) // Correct dependency
}
```

**Why**: Effects re-run when dependencies change. Missing dependencies cause stale data bugs.

Reference: [useEffect](https://react.dev/reference/react/useEffect)
