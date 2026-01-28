---
title: Result Pattern with Union
impact: HIGH
impactDescription: Forces explicit error handling, improves type safety
tags: python, errors, result-pattern, union, dataclass
---

## Result Pattern with Union

**Impact: HIGH - Forces explicit error handling, improves type safety**

Use Result types to make error handling explicit.

**Incorrect:**

```python
# exception-only handling
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

# usage (caller must use try-catch)
try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Error: {e}")
```

**Correct:**

```python
from typing import Union, TypeAlias
from dataclasses import dataclass

@dataclass
class Success:
    value: any

@dataclass
class Failure:
    error: str

Result: TypeAlias = Union[Success, Failure]

def divide(a: float, b: float) -> Result:
    """Divide two numbers, returning Result."""
    if b == 0:
        return Failure("Division by zero")
    return Success(a / b)

# usage
result = divide(10, 2)
match result:
    case Success(value):
        print(f"Result: {value}")
    case Failure(error):
        print(f"Error: {error}")
```

**Why**: The Result pattern forces explicit error handling and improves type safety. Callers cannot forget to handle errors because the return type requires it.

**When to use:**
- Expected error conditions
- APIs where errors are part of normal flow
- When exceptions feel too heavy

Reference: [Python Docs - Union Types](https://docs.python.org/3/library/typing.html#typing.Union)
