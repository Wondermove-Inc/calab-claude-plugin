---
title: Dynamic Import for Heavy Components
impact: CRITICAL
impactDescription: Removes heavy dependencies from initial bundle (100KB-2MB savings typical)
tags: bundle, dynamic-import, code-splitting
---

## Dynamic Import for Heavy Components

**Impact: CRITICAL - Removes heavy dependencies from initial bundle (100KB-2MB savings typical)**

Heavy components should be loaded on-demand, not included in the initial JavaScript bundle.

**Incorrect (Monaco (2MB) loads on initial page load):**

```typescript
import { MonacoEditor } from './monaco-editor'

function CodePage() {
  return <MonacoEditor />
}
```

**Correct (Monaco loads only when component renders):**

```typescript
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false, loading: () => <EditorSkeleton /> }
)

function CodePage() {
  return <MonacoEditor />
}
```

**Why**: Heavy components should be loaded on-demand, not included in the initial JavaScript bundle.

Reference: [Next.js Dynamic Imports](https://nextjs.org/docs/app/building-your-application/optimizing/lazy-loading)
