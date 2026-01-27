---
title: Function Type Annotations
impact: HIGH
impactDescription: IDE support, early bug detection with mypy
tags: python, types, annotations, functions
---

## Function Type Annotations

**Impact: HIGH - IDE support, early bug detection with mypy**

Annotate function parameters and return types for better tooling support.

**Incorrect:**

```python
# no type hints
def get_user(user_id):
    # implementation
    pass

def process_users(user_ids):
    return [get_user(uid) for uid in user_ids if get_user(uid) is not None]
```

**Correct:**

```python
from typing import Optional

def get_user(user_id: str) -> Optional[dict]:
    """Fetch user by ID.

    Args:
        user_id: The unique identifier for the user

    Returns:
        User dictionary if found, None otherwise
    """
    # implementation
    pass

def process_users(user_ids: list[str]) -> list[dict]:
    """Process multiple users.

    Args:
        user_ids: List of user IDs to process

    Returns:
        List of processed user dictionaries
    """
    return [get_user(uid) for uid in user_ids if get_user(uid) is not None]
```

**Why**: Type hints enable IDE auto-completion and type checking tools (mypy) to detect bugs early in development.

Reference: [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
