---
title: Avoid Creating Objects in Render
impact: MEDIUM
impactDescription: Prevents unnecessary re-renders of memoized children
tags: inline-objects, re-render, performance
---

## Avoid Creating Objects in Render

**Impact: MEDIUM - Prevents unnecessary re-renders of memoized children**

Object literals create new references every render, defeating memo comparisons.

**Incorrect (new object created every render):**

```tsx
function Parent() {
  return <Child style={{ color: 'red', fontSize: 14 }} />
}
```

**Correct (stable object reference):**

```tsx
const childStyle = { color: 'red', fontSize: 14 }

function Parent() {
  return <Child style={childStyle} />
}

// Or with useMemo for dynamic values
function Parent({ color }: { color: string }) {
  const style = useMemo(() => ({ color, fontSize: 14 }), [color])
  return <Child style={style} />
}
```

**Why**: Object literals create new references every render, defeating memo comparisons.

Reference: [Optimizing Performance](https://legacy.reactjs.org/docs/optimizing-performance.html)
