---
title: Preload on User Intent
impact: CRITICAL
impactDescription: Zero perceived latency for dynamic imports
tags: bundle, preload, user-intent, performance
---

## Preload on User Intent

**Impact: CRITICAL - Zero perceived latency for dynamic imports**

User intent signals (hover, focus) give us 100-300ms to preload before the click happens.

**Incorrect (no preloading, delay visible on click):**

```tsx
const Editor = dynamic(() => import('./monaco-editor'))

function EditorButton({ onClick }: Props) {
  return <button onClick={onClick}>Open Editor</button>
}
```

**Correct (preload on hover/focus, loaded by click time):**

```tsx
const Editor = dynamic(() => import('./monaco-editor'))

function EditorButton({ onClick }: Props) {
  const preload = () => {
    if (typeof window !== 'undefined') {
      void import('./monaco-editor')
    }
  }

  return (
    <button
      onMouseEnter={preload}
      onFocus={preload}
      onClick={onClick}
    >
      Open Editor
    </button>
  )
}
```

**Why**: User intent signals (hover, focus) give us 100-300ms to preload before the click happens.

Reference: [Resource Hints](https://web.dev/articles/preload-critical-assets)
