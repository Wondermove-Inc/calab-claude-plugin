---
title: contextlib Utilities
impact: MEDIUM
impactDescription: Simplified complex resource management
tags: python, context-manager, contextlib, suppress, ExitStack
---

## contextlib Utilities

**Impact: MEDIUM - Simplified complex resource management**

Use contextlib utilities for common context management patterns.

**Incorrect:**

```python
# exception handling
try:
    os.remove('temp_file.txt')
except FileNotFoundError:
    pass

# manual redirection
original_stdout = sys.stdout
sys.stdout = io.StringIO()
try:
    print("This goes to StringIO")
    content = sys.stdout.getvalue()
finally:
    sys.stdout = original_stdout
```

**Correct:**

```python
from contextlib import suppress, redirect_stdout, ExitStack
import io
import os

# suppressing exceptions
with suppress(FileNotFoundError):
    os.remove('temp_file.txt')

# stdout redirection
output = io.StringIO()
with redirect_stdout(output):
    print("This goes to StringIO")
content = output.getvalue()

# dynamic context managers
with ExitStack() as stack:
    files = [stack.enter_context(open(fname)) for fname in file_names]
    # all files automatically closed
```

**Why**: contextlib utilities simplify complex resource management scenarios. They provide battle-tested implementations of common patterns.

**Key utilities:**
| Utility | Purpose |
|---------|---------|
| `suppress` | Ignore specific exceptions |
| `redirect_stdout` | Capture print output |
| `ExitStack` | Dynamic number of context managers |
| `closing` | Add close() to any object |

Reference: [Python Docs - contextlib](https://docs.python.org/3/library/contextlib.html)
