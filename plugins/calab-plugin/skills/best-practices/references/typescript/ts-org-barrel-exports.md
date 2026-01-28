---
title: Barrel Exports (Conditional)
impact: MEDIUM
impactDescription: Simplified imports, clear module structure
tags: typescript, exports, barrel, modules, organization
---

## Barrel Exports (Conditional)

**Impact: MEDIUM - Simplified imports, clear module structure**

Use barrel exports for libraries/backend. **Avoid for React/frontend** (see `react-bundle-barrel-imports.md`).

**When to Use (Libraries/Backend):**

```typescript
// user/index.ts (barrel export)
export * from './types';
export * from './service';
export * from './repository';

// usage
import { User, UserService, UserRepository } from '@/domain/user';
```

**When NOT to Use (Frontend/React):**

```typescript
// individual imports (better for tree-shaking)
import { User } from '@/domain/user/types';
import { UserService } from '@/domain/user/service';
import { UserRepository } from '@/domain/user/repository';
```

**Why**:
- **Libraries/Backend**: Barrel exports simplify import paths and clarify module structure
- **Frontend/React**: Barrel exports can break tree-shaking, leading to larger bundles. See `react-bundle-barrel-imports.md` for details.

**Decision Guide:**
| Context | Recommendation |
|---------|---------------|
| npm packages / libraries | ✅ Use barrel exports |
| Backend services | ✅ Use barrel exports |
| React components | ❌ Avoid barrel exports |
| Next.js / frontend | ❌ Avoid barrel exports |

Reference: [TypeScript Handbook - Modules](https://www.typescriptlang.org/docs/handbook/modules.html)
