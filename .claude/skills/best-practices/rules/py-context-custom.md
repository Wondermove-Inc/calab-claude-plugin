---
title: Custom Context Managers
impact: MEDIUM
impactDescription: Reusable patterns, simplified error handling
tags: python, context-manager, contextmanager, custom
---

## Custom Context Managers

**Impact: MEDIUM - Reusable patterns, simplified error handling**

Create custom context managers for reusable resource patterns.

**Incorrect:**

```python
# manual timing
start = time.time()
try:
    result = expensive_query()
finally:
    elapsed = time.time() - start
    print(f"Query took {elapsed:.2f}s")

# manual transaction management
conn.begin()
try:
    conn.execute("INSERT INTO users ...")
    conn.commit()
except Exception:
    conn.rollback()
    raise
```

**Correct:**

```python
from contextlib import contextmanager
from typing import Generator
import time

@contextmanager
def timer(name: str) -> Generator[None, None, None]:
    """Context manager for timing code blocks."""
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{name} took {elapsed:.2f}s")

# usage
with timer("Database query"):
    result = expensive_query()

# class-based context manager
class DatabaseTransaction:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.connection.begin()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        return False

# usage
with DatabaseTransaction(conn) as db:
    db.execute("INSERT INTO users ...")
```

**Why**: Custom context managers enable reusing common patterns and simplifying error handling. Use `@contextmanager` for simple cases, class-based for complex state.

Reference: [Python Docs - contextlib](https://docs.python.org/3/library/contextlib.html)
