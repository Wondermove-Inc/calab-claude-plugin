---
title: Strategic Suspense Boundaries
impact: CRITICAL
impactDescription: Layout renders immediately, data-dependent sections stream in
tags: suspense, streaming, ssr, performance
---

## Strategic Suspense Boundaries

**Impact: CRITICAL - Layout renders immediately, data-dependent sections stream in**

Use Suspense boundaries to allow static shell to render immediately while data-dependent components load asynchronously.

**Incorrect (entire page blocked until data loads):**

```tsx
async function Page() {
  const data = await fetchData() // Blocks everything
  return (
    <div>
      <Sidebar />
      <DataDisplay data={data} />
      <Footer />
    </div>
  )
}
```

**Correct (layout renders immediately):**

```tsx
function Page() {
  return (
    <div>
      <Sidebar />
      <Suspense fallback={<Skeleton />}>
        <DataDisplay />
      </Suspense>
      <Footer />
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData()
  return <div>{data.content}</div>
}
```

**Why**: Suspense boundaries allow the static shell to render immediately while data-dependent components load asynchronously.

Reference: [React Suspense](https://react.dev/reference/react/Suspense)
