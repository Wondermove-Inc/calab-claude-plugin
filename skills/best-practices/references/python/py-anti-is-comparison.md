---
title: Avoid `is` for Value Comparison
impact: MEDIUM
impactDescription: Incorrect comparisons, implementation-dependent behavior
tags: python, anti-pattern, is, comparison, identity
---

## Avoid `is` for Value Comparison

**Impact: MEDIUM - Incorrect comparisons, implementation-dependent behavior**

Use `==` for value comparison, `is` only for identity (None, singletons).

**Incorrect:**

```python
if x is True:  # dangerous - compares identity
    pass

if x is 1:  # dangerous - implementation-dependent
    pass

if name is "John":  # dangerous - string interning varies
    pass
```

**Correct:**

```python
if x:  # recommended for boolean check
    pass

if x == True:  # explicit value comparison (if needed)
    pass

if x == 1:  # value comparison
    pass

if name == "John":  # string comparison
    pass

# is is correct for None
if value is None:
    pass

if value is not None:
    pass
```

**Why**: `is` compares object identity (memory address), not value equality. Small integers (-5 to 256) and some strings are cached by CPython, but this is an implementation detail that shouldn't be relied upon.

**When to use `is`:**
- Comparing to `None`
- Comparing to singleton objects
- Checking object identity explicitly

Reference: [Python Docs - Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)
