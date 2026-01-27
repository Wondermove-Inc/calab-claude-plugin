---
title: Never Use @ts-ignore
impact: CRITICAL
impactDescription: Hidden bugs, technical debt, unsafe code
tags: typescript, anti-pattern, ts-ignore, ts-expect-error
---

## Never Use @ts-ignore

**Impact: CRITICAL - Hidden bugs, technical debt, unsafe code**

Fundamentally resolve type issues instead of ignoring them.

**Incorrect:**

```typescript
// @ts-ignore
const result = someUnsafeOperation();

// @ts-ignore - I'll fix this later
const data: User = getUnknownData();
```

**Correct:**

```typescript
// fundamentally resolve type issues
const result: ExpectedType = someOperation();

// Or use ts-expect-error with explanation (when truly necessary)
// @ts-expect-error - Third-party library has incorrect types, issue #123 filed
const legacyResult = legacyLibraryCall();
```

**Why**: `@ts-ignore` silences the compiler without fixing the underlying issue. This hides bugs and creates technical debt. If you must suppress an error, use `@ts-expect-error` which will fail if the error is fixed.

**Better alternatives:**
- Fix the actual type issue
- Use type guards for runtime validation
- Extend/augment incorrect library types
- File issues for incorrect @types packages

Reference: [TypeScript Handbook - @ts-expect-error](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-9.html#-ts-expect-error-comments)
