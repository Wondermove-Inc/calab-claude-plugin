---
title: Avoid Barrel File Imports
impact: CRITICAL
impactDescription: Reduces import cost by 100-500× (e.g., 1,583 modules → 3 modules)
tags: bundle, imports, tree-shaking
---

## Avoid Barrel File Imports

**Impact: CRITICAL - Reduces import cost by 100-500× (e.g., 1,583 modules → 3 modules)**

Barrel files (index.ts that re-exports) can cause the bundler to include far more code than needed.

**Incorrect (loads 1,583 modules from barrel file):**

```typescript
import { Check, X, Menu } from 'lucide-react'
```

**Correct (loads only 3 modules):**

```typescript
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'
```

**Why**: Barrel files (index.ts that re-exports) can cause the bundler to include far more code than needed.

Reference: [Tree Shaking](https://webpack.js.org/guides/tree-shaking/)
