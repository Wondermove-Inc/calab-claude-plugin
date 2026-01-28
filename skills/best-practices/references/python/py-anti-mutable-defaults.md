---
title: Avoid Mutable Default Arguments
impact: CRITICAL
impactDescription: Shared state between calls, unexpected behavior
tags: python, anti-pattern, defaults, mutable
---

## Avoid Mutable Default Arguments

**Impact: CRITICAL - Shared state between calls, unexpected behavior**

Use None as default and create mutable objects inside the function.

**Incorrect:**

```python
def append_to(element, target=[]):  # dangerous: shared across calls
    target.append(element)
    return target

# unexpected behavior
print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] - not [2]!
print(append_to(3))  # [1, 2, 3] - not [3]!
```

**Correct:**

```python
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

# works as expected
print(append_to(1))  # [1]
print(append_to(2))  # [2]
print(append_to(3))  # [3]
```

**Why**: Default argument values are evaluated once when the function is defined, not each time it's called. Mutable defaults (list, dict, set) are shared between all calls.

**Common mutable types to avoid as defaults:**
- `[]` (list)
- `{}` (dict)
- `set()`
- Custom class instances

Reference: [Python Docs - Default Argument Values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values)
