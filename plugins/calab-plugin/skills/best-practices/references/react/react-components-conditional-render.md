---
title: Explicit Conditional Rendering
impact: MEDIUM
impactDescription: Prevents rendering falsy values like 0
tags: conditional, rendering, jsx
---

## Explicit Conditional Rendering

**Impact: MEDIUM - Prevents rendering falsy values like 0**

`&&` with numbers can render `0` because `0 && <JSX>` evaluates to `0`, which React renders.

**Incorrect (renders "0" when count is 0):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}
```

**Correct (explicit boolean check):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}
```

**Why**: `&&` with numbers can render `0` because `0 && <JSX>` evaluates to `0`, which React renders.

Reference: [Conditional Rendering](https://react.dev/learn/conditional-rendering)
