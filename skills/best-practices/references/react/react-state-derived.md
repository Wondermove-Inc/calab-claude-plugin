---
title: Derive State Instead of Syncing
impact: MEDIUM
impactDescription: Eliminates sync bugs, reduces state count
tags: state, derived-state, anti-pattern
---

## Derive State Instead of Syncing

**Impact: MEDIUM - Eliminates sync bugs, reduces state count**

Derived state calculated during render is always in sync and requires no effect.

**Incorrect (derived state stored and synced):**

```tsx
function TodoList({ todos }: { todos: Todo[] }) {
  const [completedCount, setCompletedCount] = useState(0)
  const [pendingCount, setPendingCount] = useState(0)

  useEffect(() => {
    const completed = todos.filter(t => t.completed).length
    setCompletedCount(completed)
    setPendingCount(todos.length - completed)
  }, [todos])

  return <div>Completed: {completedCount}, Pending: {pendingCount}</div>
}
```

**Correct (calculate derived values during render):**

```tsx
function TodoList({ todos }: { todos: Todo[] }) {
  const completedCount = todos.filter(t => t.completed).length
  const pendingCount = todos.length - completedCount

  return <div>Completed: {completedCount}, Pending: {pendingCount}</div>
}
```

**Why**: Derived state calculated during render is always in sync and requires no effect.

Reference: [Choosing the State Structure](https://react.dev/learn/choosing-the-state-structure)
