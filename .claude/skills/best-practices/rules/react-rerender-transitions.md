---
title: useTransition for Non-Urgent Updates
impact: MEDIUM
impactDescription: Keeps UI responsive during heavy updates
tags: useTransition, concurrent, performance
---

## useTransition for Non-Urgent Updates

**Impact: MEDIUM - Keeps UI responsive during heavy updates**

startTransition marks updates as interruptible, allowing urgent updates to take priority.

**Incorrect (scroll handler blocks main thread):**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handler = () => setScrollY(window.scrollY) // Urgent update
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

**Correct (scroll updates marked as non-urgent):**

```tsx
import { startTransition } from 'react'

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY)) // Non-urgent
    }
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

**Why**: startTransition marks updates as interruptible, allowing urgent updates to take priority.

Reference: [useTransition](https://react.dev/reference/react/useTransition)
