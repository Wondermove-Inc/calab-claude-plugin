---
title: Path Aliases
impact: MEDIUM
impactDescription: Concise imports, easier refactoring
tags: typescript, paths, aliases, tsconfig, organization
---

## Path Aliases

**Impact: MEDIUM - Concise imports, easier refactoring**

Configure path aliases in tsconfig.json for cleaner imports.

**Incorrect:**

```typescript
// using relative paths
import { User } from '../../../domain/user';
import { CreateUserUseCase } from '../../application/usecases';
```

**Correct:**

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/domain/*": ["src/domain/*"],
      "@/application/*": ["src/application/*"]
    }
  }
}

// usage
import { User } from '@/domain/user';
import { CreateUserUseCase } from '@/application/usecases';
```

**Why**: Using path aliases makes import paths concise and minimizes changes when moving files. It also makes the codebase structure clearer in imports.

**Note**: Ensure your bundler (webpack, vite, etc.) is configured to resolve these aliases as well.

Reference: [TypeScript Handbook - Module Resolution](https://www.typescriptlang.org/docs/handbook/module-resolution.html)
