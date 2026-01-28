---
title: Generic Types with TypeVar
impact: HIGH
impactDescription: Reusable code with maintained type safety
tags: python, types, generics, TypeVar, Generic
---

## Generic Types with TypeVar

**Impact: HIGH - Reusable code with maintained type safety**

Use TypeVar and Generic to create reusable, type-safe classes and functions.

**Incorrect:**

```python
# repository without type safety
class Repository:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def get_all(self):
        return self._items.copy()
```

**Correct:**

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Repository(Generic[T]):
    """Generic repository pattern."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        """Add item to repository."""
        self._items.append(item)

    def get_all(self) -> list[T]:
        """Get all items."""
        return self._items.copy()

    def find(self, predicate: callable[[T], bool]) -> T | None:
        """Find first item matching predicate."""
        for item in self._items:
            if predicate(item):
                return item
        return None

# usage
user_repo: Repository[UserData] = Repository()
user_repo.add({"id": "1", "name": "John"})
```

**Why**: Generic types enable writing reusable code while maintaining type safety. The type parameter propagates through the class methods.

Reference: [Python Docs - Generics](https://docs.python.org/3/library/typing.html#generics)
