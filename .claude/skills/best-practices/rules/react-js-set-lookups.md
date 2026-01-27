---
title: Use Set for Existence Checks
impact: LOW
impactDescription: O(1) vs O(n) for includes checks
tags: performance, set, lookup
---

## Use Set for Existence Checks

**Impact: LOW - O(1) vs O(n) for includes checks**

Set.has() is O(1) while Array.includes() is O(n).

**Incorrect (O(n) per check):**

```typescript
const allowedIds = ['a', 'b', 'c', 'd', 'e']
items.filter(item => allowedIds.includes(item.id)) // O(n²) total
```

**Correct (O(1) per check):**

```typescript
const allowedIds = new Set(['a', 'b', 'c', 'd', 'e'])
items.filter(item => allowedIds.has(item.id)) // O(n) total
```

**Why**: Set.has() is O(1) while Array.includes() is O(n).

Reference: [Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)
