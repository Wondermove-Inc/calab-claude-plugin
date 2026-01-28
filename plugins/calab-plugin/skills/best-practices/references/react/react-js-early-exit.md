---
title: Early Return in Loops
impact: LOW
impactDescription: Avoids unnecessary iterations
tags: performance, loops, early-return
---

## Early Return in Loops

**Impact: LOW - Avoids unnecessary iterations**

Early returns avoid processing remaining items when the answer is already known.

**Incorrect (continues iterating after finding result):**

```typescript
function findUser(users: User[], id: string): User | undefined {
  let result: User | undefined
  users.forEach(user => {
    if (user.id === id) result = user
    // forEach can't break early
  })
  return result
}
```

**Correct (returns immediately when found):**

```typescript
function findUser(users: User[], id: string): User | undefined {
  for (const user of users) {
    if (user.id === id) return user
  }
  return undefined
}

// Or simply use find()
const user = users.find(u => u.id === id)
```

**Why**: Early returns avoid processing remaining items when the answer is already known.

Reference: [for...of](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of)
