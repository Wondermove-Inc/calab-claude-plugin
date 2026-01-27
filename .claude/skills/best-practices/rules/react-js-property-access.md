---
title: Avoid Repeated Property Access
impact: LOW
impactDescription: Reduces property lookup overhead in hot paths
tags: performance, destructuring, optimization
---

## Avoid Repeated Property Access

**Impact: LOW - Reduces property lookup overhead in hot paths**

Destructuring once is faster than repeated property chain traversal.

**Incorrect (repeated deep property access):**

```typescript
function processItems(data: Data) {
  for (const item of data.response.items) {
    console.log(data.response.metadata.version) // Looked up each iteration
    processItem(item, data.response.metadata.format)
  }
}
```

**Correct (cache property access):**

```typescript
function processItems(data: Data) {
  const { items, metadata } = data.response
  const { version, format } = metadata

  for (const item of items) {
    console.log(version)
    processItem(item, format)
  }
}
```

**Why**: Destructuring once is faster than repeated property chain traversal.

Reference: [Destructuring assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)
