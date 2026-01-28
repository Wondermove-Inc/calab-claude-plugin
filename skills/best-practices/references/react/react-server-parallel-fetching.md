---
title: Parallel Component Composition
impact: HIGH
impactDescription: Server components fetch in parallel when composed as siblings
tags: rsc, server-components, parallel, composition
---

## Parallel Component Composition

**Impact: HIGH - Server components fetch in parallel when composed as siblings**

React Server Components that are siblings automatically fetch in parallel.

**Incorrect (sequential fetching in single component):**

```tsx
async function Page() {
  const header = await fetchHeader()
  const sidebar = await fetchSidebarItems()
  return (
    <div>
      <Header data={header} />
      <Sidebar items={sidebar} />
    </div>
  )
}
```

**Correct (parallel fetching via component composition):**

```tsx
async function Header() {
  const data = await fetchHeader()
  return <header>{data.title}</header>
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}

export default function Page() {
  return (
    <div>
      <Header />  {/* Fetches in parallel */}
      <Sidebar /> {/* with this */}
    </div>
  )
}
```

**Why**: React Server Components that are siblings automatically fetch in parallel.

Reference: [React Server Components](https://react.dev/reference/rsc/server-components)
