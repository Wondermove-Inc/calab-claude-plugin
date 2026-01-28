---
title: Streaming with Loading UI
impact: HIGH
impactDescription: Shows meaningful content immediately while data loads
tags: streaming, suspense, loading, ux
---

## Streaming with Loading UI

**Impact: HIGH - Shows meaningful content immediately while data loads**

Streaming allows fast sections to render while slow sections load, improving perceived performance.

**Incorrect (entire page waits for slow data):**

```tsx
async function DashboardPage() {
  const [quickData, slowData] = await Promise.all([
    fetchQuickData(),
    fetchSlowData() // Takes 3 seconds
  ])
  return <Dashboard quick={quickData} slow={slowData} />
}
```

**Correct (quick data shows immediately, slow data streams in):**

```tsx
import { Suspense } from 'react'

async function QuickSection() {
  const data = await fetchQuickData()
  return <QuickDisplay data={data} />
}

async function SlowSection() {
  const data = await fetchSlowData()
  return <SlowDisplay data={data} />
}

export default function DashboardPage() {
  return (
    <div>
      <Suspense fallback={<QuickSkeleton />}>
        <QuickSection />
      </Suspense>
      <Suspense fallback={<SlowSkeleton />}>
        <SlowSection />
      </Suspense>
    </div>
  )
}
```

**Why**: Streaming allows fast sections to render while slow sections load, improving perceived performance.

Reference: [Next.js Streaming](https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming)
