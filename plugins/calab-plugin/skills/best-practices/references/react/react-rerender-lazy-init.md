---
title: Lazy State Initialization
impact: MEDIUM
impactDescription: Expensive initialization runs only once
tags: useState, lazy-initialization, performance
---

## Lazy State Initialization

**Impact: MEDIUM - Expensive initialization runs only once**

Passing a function to useState defers execution to initial render only.

**Incorrect (buildSearchIndex runs on every render):**

```tsx
function SearchComponent({ items }: Props) {
  const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items))
  // buildSearchIndex(items) called every render, result discarded after first
}
```

**Correct (buildSearchIndex runs only on mount):**

```tsx
function SearchComponent({ items }: Props) {
  const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items))
  // Arrow function only called on initial render
}
```

**Why**: Passing a function to useState defers execution to initial render only.

Reference: [Avoiding recreating the initial state](https://react.dev/reference/react/useState#avoiding-recreating-the-initial-state)
