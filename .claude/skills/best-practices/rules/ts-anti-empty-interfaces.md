---
title: Avoid Empty Interfaces
impact: LOW
impactDescription: Unclear intent, potential type errors
tags: typescript, anti-pattern, interface, empty-type
---

## Avoid Empty Interfaces

**Impact: LOW - Unclear intent, potential type errors**

Use explicit types to express empty objects or remove unnecessary interfaces.

**Incorrect:**

```typescript
interface Props {}  // meaningless interface

function Component(props: Props) {
  // ...
}
```

**Correct:**

```typescript
// Option 1: Explicitly express empty type
type Props = Record<string, never>;

// Option 2: Omit interface entirely for components with no props
function Component() {
  // ...
}

// Option 3: Use object type if truly any object is allowed
type AnyObject = Record<string, unknown>;
```

**Why**: Empty interfaces accept any object type, which is rarely the intended behavior. Being explicit about the type's purpose improves code clarity and catches errors.

**Common scenarios:**
| Scenario | Solution |
|----------|----------|
| Component with no props | Omit props parameter |
| Placeholder for future props | Add TODO comment, use `Record<string, never>` |
| Accept any object | Use `Record<string, unknown>` |

Reference: [TypeScript Handbook - Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html)
