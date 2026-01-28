---
title: Component Composition over Props Drilling
impact: MEDIUM
impactDescription: Reduces coupling, increases flexibility
tags: composition, props, patterns
---

## Component Composition over Props Drilling

**Impact: MEDIUM - Reduces coupling, increases flexibility**

Composition allows consumers to customize structure and content without adding more props.

**Incorrect (props drilling makes component inflexible):**

```tsx
interface CardProps {
  title: string
  content: string
  headerClassName?: string
  bodyClassName?: string
}

function Card({ title, content, headerClassName, bodyClassName }: CardProps) {
  return (
    <div className="card">
      <div className={headerClassName}><h2>{title}</h2></div>
      <div className={bodyClassName}><p>{content}</p></div>
    </div>
  )
}
```

**Correct (composition pattern):**

```tsx
function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={`card ${className}`}>{children}</div>
}

function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>
}

function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="card-body">{children}</div>
}

// Usage - highly flexible
<Card>
  <CardHeader><h2>Title</h2></CardHeader>
  <CardBody><p>Any content here</p></CardBody>
</Card>
```

**Why**: Composition allows consumers to customize structure and content without adding more props.

Reference: [Composition vs Inheritance](https://react.dev/learn/thinking-in-react)
