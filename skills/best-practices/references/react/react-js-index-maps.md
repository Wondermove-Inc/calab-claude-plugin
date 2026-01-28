---
title: Build Index Maps for Lookups
impact: LOW
impactDescription: O(n²) to O(n) for join operations
tags: performance, map, lookup, algorithms
---

## Build Index Maps for Lookups

**Impact: LOW - O(n²) to O(n) for join operations**

For repeated lookups, build an index first. Map lookup is O(1) vs array find O(n).

**Incorrect (O(n²) - find() called for each order):**

```typescript
function enrichOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId) // O(n) per order
  }))
}
```

**Correct (O(n) - Map lookup is O(1)):**

```typescript
function enrichOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))
  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId) // O(1) per order
  }))
}
```

**Why**: For repeated lookups, build an index first. Map lookup is O(1) vs array find O(n).

Reference: [Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
