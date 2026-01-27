---
title: Discriminated Unions for Props
impact: MEDIUM
impactDescription: Ensures type-safe props combinations
tags: typescript, discriminated-unions, type-safety
---

## Discriminated Unions for Props

**Impact: MEDIUM - Ensures type-safe props combinations**

Discriminated unions make invalid states unrepresentable in the type system.

**Incorrect (invalid prop combinations possible):**

```tsx
interface ButtonProps {
  variant: 'link' | 'button'
  href?: string
  onClick?: () => void
}

function Button({ variant, href, onClick }: ButtonProps) {
  if (variant === 'link') {
    return <a href={href}>{children}</a> // href might be undefined!
  }
  return <button onClick={onClick}>{children}</button> // onClick might be undefined!
}
```

**Correct (type-safe prop combinations):**

```tsx
type ButtonProps =
  | { variant: 'link'; href: string; onClick?: never }
  | { variant: 'button'; href?: never; onClick: () => void }

function Button(props: ButtonProps & { children: React.ReactNode }) {
  if (props.variant === 'link') {
    return <a href={props.href}>{props.children}</a> // href guaranteed
  }
  return <button onClick={props.onClick}>{props.children}</button> // onClick guaranteed
}
```

**Why**: Discriminated unions make invalid states unrepresentable in the type system.

Reference: [TypeScript Discriminated Unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)
