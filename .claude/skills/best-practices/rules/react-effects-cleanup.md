---
title: Cleanup Functions
impact: LOW-MEDIUM
impactDescription: Prevents memory leaks and stale updates
tags: useEffect, cleanup, memory-leak
---

## Cleanup Functions

**Impact: LOW-MEDIUM - Prevents memory leaks and stale updates**

Cleanup functions run before the next effect and on unmount, preventing leaks.

**Incorrect (no cleanup, intervals accumulate):**

```tsx
function Timer() {
  const [seconds, setSeconds] = useState(0)

  useEffect(() => {
    setInterval(() => setSeconds(s => s + 1), 1000)
    // Memory leak: interval continues after unmount
  }, [])
}
```

**Correct (cleanup on unmount):**

```tsx
function Timer() {
  const [seconds, setSeconds] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => setSeconds(s => s + 1), 1000)
    return () => clearInterval(interval) // Cleanup
  }, [])
}
```

**Why**: Cleanup functions run before the next effect and on unmount, preventing leaks.

Reference: [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)
