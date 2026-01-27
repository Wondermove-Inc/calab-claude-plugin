---
title: Generator Expressions
impact: HIGH
impactDescription: Memory-efficient processing of large datasets
tags: python, generators, yield, memory, pythonic
---

## Generator Expressions

**Impact: HIGH - Memory-efficient processing of large datasets**

Use generators for memory-efficient processing of large datasets.

**Incorrect:**

```python
# load everything into memory
def read_large_file(file_path: str) -> list[str]:
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]  # memory waste

# usage
lines = read_large_file('large_file.txt')
for line in lines:
    process(line)
```

**Correct:**

```python
from typing import Generator

# memory-efficient generator
def read_large_file(file_path: str) -> Generator[str, None, None]:
    """Read large file line by line."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

# usage
for line in read_large_file('large_file.txt'):
    process(line)

# Generator expression
sum_of_squares = sum(x**2 for x in range(1000000))
```

**Why**: Generators enable memory-efficient processing of large datasets without loading everything into memory. They produce values lazily, one at a time.

**When to use:**
- Processing large files
- Streaming data
- Infinite sequences
- Chained transformations

Reference: [Python Docs - Generators](https://docs.python.org/3/howto/functional.html#generators)
