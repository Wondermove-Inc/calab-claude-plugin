---
title: Defer Non-Critical Third-Party Libraries
impact: CRITICAL
impactDescription: Reduces Time to Interactive (TTI) by deferring non-essential code
tags: bundle, third-party, tti, performance
---

## Defer Non-Critical Third-Party Libraries

**Impact: CRITICAL - Reduces Time to Interactive (TTI) by deferring non-essential code**

Non-critical libraries (analytics, error tracking) should not delay Time to Interactive.

**Incorrect (analytics loaded synchronously, blocks rendering):**

```typescript
import { initAnalytics, trackPageView } from 'heavy-analytics-lib'

initAnalytics()
trackPageView()
```

**Correct (analytics loaded after page is interactive):**

```typescript
useEffect(() => {
  const loadAnalytics = async () => {
    const { initAnalytics, trackPageView } = await import('heavy-analytics-lib')
    initAnalytics()
    trackPageView()
  }

  // Defer until idle or after initial render
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => loadAnalytics())
  } else {
    setTimeout(loadAnalytics, 1000)
  }
}, [])
```

**Why**: Non-critical libraries (analytics, error tracking) should not delay Time to Interactive.

Reference: [Loading Third-Party JavaScript](https://web.dev/articles/efficiently-load-third-party-javascript)
