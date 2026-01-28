---
title: Protocol for Structural Typing
impact: HIGH
impactDescription: Duck typing with type safety
tags: python, types, Protocol, structural-typing, duck-typing
---

## Protocol for Structural Typing

**Impact: HIGH - Duck typing with type safety**

Use Protocol for structural typing that works with Python's duck typing.

**Incorrect:**

```python
# forced inheritance (ignoring duck typing)
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self) -> str:
        pass

# all classes must inherit Drawable
class Circle(Drawable):
    def draw(self) -> str:
        return "Drawing circle"
```

**Correct:**

```python
from typing import Protocol

class Drawable(Protocol):
    """Protocol for drawable objects."""

    def draw(self) -> str:
        """Draw the object."""
        ...

class Circle:
    def draw(self) -> str:
        return "Drawing circle"

class Square:
    def draw(self) -> str:
        return "Drawing square"

def render(obj: Drawable) -> None:
    """Render any drawable object."""
    print(obj.draw())

# usage - no inheritance required
render(Circle())  # OK
render(Square())  # OK
```

**Why**: Protocols leverage Python's duck typing while still enabling type checking. Classes don't need to explicitly inherit from the Protocol - they just need to implement the required methods.

Reference: [PEP 544 - Protocols: Structural Subtyping](https://peps.python.org/pep-0544/)
