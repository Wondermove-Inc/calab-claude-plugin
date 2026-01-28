> **원본**: claude-monitoring-main
> **적용**: calab-claude-plugin v2.3.0+

---
title: React Best Practices Index
impact: N/A
tags: index, summary, anti-patterns
---

# React Best Practices Index

> Version: 19+
> Last Updated: 2026-01-22
> Total Patterns: 42
> Structure: 8 Categories (Priority-Sorted)

## Summary by Priority

| Priority | Category | Patterns | Key Patterns |
|----------|----------|----------|--------------|
| CRITICAL | Eliminating Waterfalls | 5 | Promise.all, defer await, Suspense |
| CRITICAL | Bundle Optimization | 5 | Avoid barrels, dynamic import, preload |
| HIGH | Server-Side | 7 | Auth actions, cache(), after(), streaming |
| MEDIUM | Components | 4 | TypeScript, composition, discriminated unions |
| MEDIUM | State | 4 | Local vs global, reducer, context, derived |
| MEDIUM | Re-renders | 7 | memo, useMemo, useCallback, transitions |
| LOW-MED | Side Effects | 4 | Dependencies, cleanup, race conditions |
| LOW | JS Performance | 6 | Index maps, Sets, immutable methods |

## Pattern Files by Category

### Category 1: Eliminating Waterfalls (CRITICAL)
- `react-async-promise-all.md`
- `react-async-defer-await.md`
- `react-async-suspense-boundaries.md`
- `react-async-parallel.md`
- `react-async-dependencies.md`

### Category 2: Bundle Size Optimization (CRITICAL)
- `react-bundle-barrel-imports.md`
- `react-bundle-dynamic-imports.md`
- `react-bundle-preload.md`
- `react-bundle-conditional.md`
- `react-bundle-defer-third-party.md`

### Category 3: Server-Side Performance (HIGH)
- `react-server-auth-actions.md`
- `react-server-parallel-fetching.md`
- `react-server-cache-react.md`
- `react-server-serialization.md`
- `react-server-after-nonblocking.md`
- `react-server-unstable-cache.md`
- `react-server-streaming.md`

### Category 4: Component Patterns (MEDIUM)
- `react-components-typescript.md`
- `react-components-composition.md`
- `react-components-discriminated-unions.md`
- `react-components-conditional-render.md`

### Category 5: State Management (MEDIUM)
- `react-state-local.md`
- `react-state-reducer.md`
- `react-state-context.md`
- `react-state-derived.md`

### Category 6: Re-render Optimization (MEDIUM)
- `react-rerender-memo.md`
- `react-rerender-usememo.md`
- `react-rerender-usecallback.md`
- `react-rerender-functional-setstate.md`
- `react-rerender-lazy-init.md`
- `react-rerender-transitions.md`
- `react-rerender-avoid-inline-objects.md`

### Category 7: Side Effects (LOW-MEDIUM)
- `react-effects-dependencies.md`
- `react-effects-cleanup.md`
- `react-effects-race-condition.md`
- `react-effects-custom-hooks.md`

### Category 8: JavaScript Performance (LOW)
- `react-js-index-maps.md`
- `react-js-tosorted.md`
- `react-js-early-exit.md`
- `react-js-property-access.md`
- `react-js-set-lookups.md`
- `react-js-passive-events.md`

---

## Anti-Patterns to Avoid

### 1. Mutating State Directly

**Bad**:
```tsx
const [items, setItems] = useState([1, 2, 3])
items.push(4) // Direct mutation - FORBIDDEN
setItems(items) // Won't trigger re-render (same reference)
```

**Good**:
```tsx
setItems([...items, 4]) // New array
// Or
setItems(prev => [...prev, 4])
```

### 2. Using Index as Key for Dynamic Lists

**Bad**:
```tsx
{items.map((item, index) => (
  <li key={index}>{item}</li> // Breaks on reorder/delete
))}
```

**Good**:
```tsx
{items.map(item => (
  <li key={item.id}>{item.name}</li> // Stable identity
))}
```

### 3. Inline Objects/Arrays in JSX

**Bad**:
```tsx
// New array every render
<Select options={['a', 'b', 'c']} />
// New object every render
<div style={{ color: 'red' }} />
```

**Good**:
```tsx
const OPTIONS = ['a', 'b', 'c']
const redStyle = { color: 'red' }

<Select options={OPTIONS} />
<div style={redStyle} />
```

### 4. Unnecessary useEffect for Derived State

**Bad**:
```tsx
const [firstName, setFirstName] = useState('')
const [lastName, setLastName] = useState('')
const [fullName, setFullName] = useState('')

useEffect(() => {
  setFullName(`${firstName} ${lastName}`)
}, [firstName, lastName])
```

**Good**:
```tsx
const [firstName, setFirstName] = useState('')
const [lastName, setLastName] = useState('')
const fullName = `${firstName} ${lastName}` // Just calculate it
```

---

## Key Principles

1. **Parallelize independent operations** (CRITICAL impact)
2. **Load code on demand, not upfront** (CRITICAL impact)
3. **Derive state instead of syncing it**
4. **Use the right state solution for the scope**
5. **Memoize expensive computations and stable references**
6. **Always clean up side effects**
7. **Build indexes for repeated lookups**
