---
title: Variable Type Annotations
impact: MEDIUM
impactDescription: Clarifies code intent, improves type checking accuracy
tags: python, types, annotations, variables, TypeAlias
---

## Variable Type Annotations

**Impact: MEDIUM - Clarifies code intent, improves type checking accuracy**

Use explicit variable annotations for complex types.

**Incorrect:**

```python
# relying on type inference only
user_id = "user_123"
users = []
user_map = {}
```

**Correct:**

```python
from typing import TypeAlias

UserId: TypeAlias = str
UserData: TypeAlias = dict[str, str | int]

# explicit variable types
user_id: UserId = "user_123"
users: list[UserData] = []
user_map: dict[UserId, UserData] = {}

# complex types
from typing import Union, Literal

Status: TypeAlias = Literal["active", "inactive", "pending"]
Result: TypeAlias = Union[UserData, None]
```

**Why**: Explicit type annotations clarify code intent and improve type checking accuracy. They're especially valuable for empty collections and complex nested types.

Reference: [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
