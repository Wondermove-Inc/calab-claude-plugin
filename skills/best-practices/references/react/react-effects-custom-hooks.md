---
title: Custom Hooks for Reusable Logic
impact: LOW-MEDIUM
impactDescription: DRY principle, tested once, used everywhere
tags: custom-hooks, reusability, dry
---

## Custom Hooks for Reusable Logic

**Impact: LOW-MEDIUM - DRY principle, tested once, used everywhere**

Custom hooks extract and share stateful logic without duplicating code.

**Incorrect (same fetch logic duplicated in multiple components):**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    let cancelled = false
    setIsLoading(true)
    fetchUser(userId)
      .then(data => { if (!cancelled) setUser(data) })
      .catch(err => { if (!cancelled) setError(err) })
      .finally(() => { if (!cancelled) setIsLoading(false) })
    return () => { cancelled = true }
  }, [userId])

  // ... same pattern repeated in other components
}
```

**Correct (reusable hook):**

```tsx
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    let cancelled = false
    setIsLoading(true)
    fetchUser(userId)
      .then(data => { if (!cancelled) setUser(data) })
      .catch(err => { if (!cancelled) setError(err) })
      .finally(() => { if (!cancelled) setIsLoading(false) })
    return () => { cancelled = true }
  }, [userId])

  return { user, isLoading, error }
}

// Usage - simple and clean
function UserProfile({ userId }: { userId: string }) {
  const { user, isLoading, error } = useUser(userId)
  if (isLoading) return <Spinner />
  if (error) return <Error error={error} />
  return <div>{user?.name}</div>
}
```

**Why**: Custom hooks extract and share stateful logic without duplicating code.

Reference: [Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
