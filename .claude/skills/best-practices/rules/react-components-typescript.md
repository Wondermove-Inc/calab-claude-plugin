---
title: Functional Components with TypeScript
impact: MEDIUM
impactDescription: Prevents prop-related bugs, enables IDE auto-completion
tags: typescript, props, type-safety
---

## Functional Components with TypeScript

**Impact: MEDIUM - Prevents prop-related bugs, enables IDE auto-completion**

TypeScript props interfaces catch errors at compile time and provide documentation.

**Incorrect (no props types defined):**

```tsx
export function UserCard({ user, onEdit, className }) {
  return (
    <div className={className}>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  )
}
```

**Correct (typed props interface):**

```tsx
interface UserCardProps {
  user: User
  onEdit?: (userId: string) => void
  className?: string
}

export function UserCard({ user, onEdit, className }: UserCardProps) {
  return (
    <div className={className}>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      {onEdit && (
        <button onClick={() => onEdit(user.id)}>Edit</button>
      )}
    </div>
  )
}
```

**Why**: TypeScript props interfaces catch errors at compile time and provide documentation.

Reference: [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
