---
title: Strict Mode Configuration
impact: CRITICAL
impactDescription: Maximum type safety, prevents runtime errors
tags: typescript, strict, tsconfig, configuration
---

## Strict Mode Configuration

**Impact: CRITICAL - Maximum type safety, prevents runtime errors**

Enable strict mode in tsconfig.json for maximum type safety.

**Incorrect:**

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": false  // weakens type checking
  }
}
```

**Correct:**

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

**What each option does:**

| Option | Purpose |
|--------|---------|
| `strict` | Enables all strict type-checking options |
| `noImplicitAny` | Error on expressions with implied `any` |
| `strictNullChecks` | `null` and `undefined` are distinct types |
| `strictFunctionTypes` | Stricter function type checking |
| `strictPropertyInitialization` | Ensure class properties are initialized |

**Why**: Enabling strict mode maximizes type safety and prevents runtime errors in advance. It catches many common bugs at compile time.

Reference: [TypeScript Handbook - Compiler Options](https://www.typescriptlang.org/tsconfig#strict)
