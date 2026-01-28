---
title: Using `with` Statement
impact: HIGH
impactDescription: Automatic resource cleanup, prevents memory leaks
tags: python, context-manager, with, resources
---

## Using `with` Statement

**Impact: HIGH - Automatic resource cleanup, prevents memory leaks**

Use context managers for automatic resource management.

**Incorrect:**

```python
# manual resource management
f = open('file.txt', 'r')
try:
    content = f.read()
finally:
    f.close()

# risk of resource leak
conn = connect_to_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
# might forget to call conn.close()
```

**Correct:**

```python
# automatic file closing
with open('file.txt', 'r') as f:
    content = f.read()
# file is automatically closed

# managing multiple resources
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    outfile.write(infile.read())

# database connection
from contextlib import closing

with closing(connect_to_db()) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
```

**Why**: Context managers ensure automatic resource cleanup, preventing memory leaks. Resources are released even if exceptions occur.

Reference: [Python Docs - With Statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)
