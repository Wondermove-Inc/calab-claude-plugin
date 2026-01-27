---
title: Functional setState Updates
impact: MEDIUM
impactDescription: Removes dependency on current state, stable callback
tags: setState, functional-updates, performance
---

## Functional setState Updates

**Impact: MEDIUM - Removes dependency on current state, stable callback**

Functional updates receive current state as argument, eliminating closure dependencies.

**Incorrect (depends on items, callback changes when items changes):**

```tsx
const addItems = useCallback((newItems: Item[]) => {
  setItems([...items, ...newItems])
}, [items]) // Dependency on items
```

**Correct (no dependency needed, callback never changes):**

```tsx
const addItems = useCallback((newItems: Item[]) => {
  setItems(curr => [...curr, ...newItems])
}, []) // No dependencies
```

**Why**: Functional updates receive current state as argument, eliminating closure dependencies.

Reference: [Updating state based on previous state](https://react.dev/reference/react/useState#updating-state-based-on-the-previous-state)
