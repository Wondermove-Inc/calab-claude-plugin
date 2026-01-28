---
title: Use toSorted() for Immutable Sorting
impact: LOW
impactDescription: Cleaner code, no mutation bugs
tags: performance, immutable, sorting, es2023
---

## Use toSorted() for Immutable Sorting

**Impact: LOW - Cleaner code, no mutation bugs**

Immutable array methods prevent accidental mutation and are more declarative.

**Incorrect (mutates or requires manual copy):**

```typescript
const sorted = users.sort((a, b) => a.name.localeCompare(b.name)) // Mutates!

// Or
const sorted = [...users].sort((a, b) => a.name.localeCompare(b.name)) // Verbose
```

**Correct (toSorted creates new array (ES2023)):**

```typescript
const sorted = users.toSorted((a, b) => a.name.localeCompare(b.name))

// Also: toReversed(), toSpliced(), with()
const reversed = items.toReversed()
const withoutSecond = items.toSpliced(1, 1)
const withReplacement = items.with(0, newFirstItem)
```

**Why**: Immutable array methods prevent accidental mutation and are more declarative.

Reference: [Array.prototype.toSorted()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted)
