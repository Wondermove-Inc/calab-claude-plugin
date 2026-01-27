---
title: Avoid Bare Except
impact: CRITICAL
impactDescription: Catches KeyboardInterrupt, SystemExit, hides bugs
tags: python, anti-pattern, except, errors
---

## Avoid Bare Except

**Impact: CRITICAL - Catches KeyboardInterrupt, SystemExit, hides bugs**

Always specify the exception type in except clauses.

**Incorrect:**

```python
try:
    risky_operation()
except:  # catches all exceptions (including KeyboardInterrupt, SystemExit)
    pass
```

**Correct:**

```python
try:
    risky_operation()
except Exception as e:  # explicit exception type
    logger.error(f"Operation failed: {e}")
```

**Why**: Bare `except:` catches everything including `KeyboardInterrupt` (Ctrl+C) and `SystemExit`, making it impossible to stop the program normally. It also silently hides bugs.

**Exception hierarchy:**
```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── ValueError
    ├── TypeError
    └── ... (all other exceptions)
```

Using `except Exception` catches normal exceptions but allows system-level exceptions to propagate.

Reference: [PEP 8 - Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations)
