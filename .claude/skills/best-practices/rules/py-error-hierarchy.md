---
title: Exception Hierarchy
impact: HIGH
impactDescription: Fine-grained error handling, easier debugging
tags: python, errors, exceptions, hierarchy, custom-errors
---

## Exception Hierarchy

**Impact: HIGH - Fine-grained error handling, easier debugging**

Create custom exception hierarchies for granular error handling.

**Incorrect:**

```python
# using generic Exception only
def get_user(user_id):
    if not user_exists(user_id):
        raise Exception("User not found")
    if database_error:
        raise Exception("Database error")

# cannot distinguish error types
try:
    user = get_user(user_id)
except Exception as e:
    print(f"Error: {e}")  # cannot determine error type
```

**Correct:**

```python
class ApplicationError(Exception):
    """Base exception for application errors."""
    pass

class ValidationError(ApplicationError):
    """Raised when validation fails."""

    def __init__(self, message: str, field: str, value: any):
        super().__init__(message)
        self.field = field
        self.value = value

class NotFoundError(ApplicationError):
    """Raised when resource is not found."""

    def __init__(self, message: str, resource: str, identifier: str):
        super().__init__(message)
        self.resource = resource
        self.identifier = identifier

class DatabaseError(ApplicationError):
    """Raised when database operation fails."""
    pass

# usage
try:
    user = get_user(user_id)
except NotFoundError as e:
    print(f"{e.resource} {e.identifier} not found")
except DatabaseError as e:
    print(f"Database error: {e}")
except ApplicationError as e:
    print(f"Application error: {e}")
```

**Why**: Custom exception hierarchies enable fine-grained error handling and easier debugging. Each exception type carries relevant context.

Reference: [Python Docs - User-defined Exceptions](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions)
