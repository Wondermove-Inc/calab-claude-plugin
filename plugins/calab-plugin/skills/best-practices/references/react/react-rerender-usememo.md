---
title: useMemo for Expensive Calculations
impact: MEDIUM
impactDescription: Caches computation results until dependencies change
tags: useMemo, memoization, performance
---

## useMemo for Expensive Calculations

**Impact: MEDIUM - Caches computation results until dependencies change**

useMemo caches the result and only recomputes when dependencies change.

**Incorrect (sorts on every render):**

```tsx
function DataTable({ data }: { data: Item[] }) {
  const sortedData = [...data].sort((a, b) => a.name.localeCompare(b.name))
  // Sorts on every render, even if data hasn't changed
  return <table>{/* ... */}</table>
}
```

**Correct (only sorts when data changes):**

```tsx
function DataTable({ data }: { data: Item[] }) {
  const sortedData = useMemo(
    () => [...data].sort((a, b) => a.name.localeCompare(b.name)),
    [data]
  )
  return <table>{/* ... */}</table>
}
```

**Why**: useMemo caches the result and only recomputes when dependencies change.

Reference: [useMemo](https://react.dev/reference/react/useMemo)
