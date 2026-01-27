---
title: React.memo for Expensive Components
impact: MEDIUM
impactDescription: Prevents re-render when props unchanged
tags: memo, performance, re-render
---

## React.memo for Expensive Components

**Impact: MEDIUM - Prevents re-render when props unchanged**

memo performs shallow prop comparison and skips re-render if props are equal.

**Incorrect (re-renders on every parent render):**

```tsx
export function UserList({ users, onUserClick }: UserListProps) {
  console.log('UserList rendered') // Logs every time parent re-renders
  return (
    <ul>
      {users.map(user => (
        <li key={user.id} onClick={() => onUserClick(user.id)}>
          {user.name}
        </li>
      ))}
    </ul>
  )
}
```

**Correct (only re-renders when props change):**

```tsx
export const UserList = React.memo(function UserList({
  users,
  onUserClick
}: UserListProps) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id} onClick={() => onUserClick(user.id)}>
          {user.name}
        </li>
      ))}
    </ul>
  )
})
```

**Why**: memo performs shallow prop comparison and skips re-render if props are equal.

Reference: [memo](https://react.dev/reference/react/memo)
