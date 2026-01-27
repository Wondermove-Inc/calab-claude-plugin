---
title: Conditional Module Loading
impact: CRITICAL
impactDescription: Prevents loading unused code paths
tags: bundle, conditional, dynamic-import
---

## Conditional Module Loading

**Impact: CRITICAL - Prevents loading unused code paths**

When code paths are mutually exclusive, use dynamic imports to load only what's needed.

**Incorrect (both formatters always loaded):**

```typescript
import { formatMarkdown } from './markdown-formatter'
import { formatCode } from './code-formatter'

function format(content: string, type: 'markdown' | 'code') {
  return type === 'markdown' ? formatMarkdown(content) : formatCode(content)
}
```

**Correct (only needed formatter is loaded):**

```typescript
async function format(content: string, type: 'markdown' | 'code') {
  if (type === 'markdown') {
    const { formatMarkdown } = await import('./markdown-formatter')
    return formatMarkdown(content)
  }
  const { formatCode } = await import('./code-formatter')
  return formatCode(content)
}
```

**Why**: When code paths are mutually exclusive, use dynamic imports to load only what's needed.

Reference: [Code Splitting](https://webpack.js.org/guides/code-splitting/)
