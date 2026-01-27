---
title: Passive Event Listeners
impact: LOW
impactDescription: Eliminates scroll/touch delay (100-300ms improvement)
tags: performance, events, scrolling, touch
---

## Passive Event Listeners

**Impact: LOW - Eliminates scroll/touch delay (100-300ms improvement)**

Passive listeners tell the browser that preventDefault won't be called, enabling immediate scrolling.

**Incorrect (browser waits to see if preventDefault will be called):**

```typescript
document.addEventListener('touchstart', handleTouch)
document.addEventListener('wheel', handleScroll)
```

**Correct (browser can scroll immediately):**

```typescript
document.addEventListener('touchstart', handleTouch, { passive: true })
document.addEventListener('wheel', handleScroll, { passive: true })
```

**Why**: Passive listeners tell the browser that preventDefault won't be called, enabling immediate scrolling.

Reference: [Improving scroll performance with passive listeners](https://web.dev/articles/passive-listeners)
