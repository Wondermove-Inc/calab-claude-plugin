---
title: Walrus Operator (:=)
impact: MEDIUM
impactDescription: Eliminates redundancy, concise code
tags: python, walrus, assignment-expression, pythonic
---

## Walrus Operator (:=)

**Impact: MEDIUM - Eliminates redundancy, concise code**

Use the walrus operator to assign and use values in a single expression.

**Incorrect:**

```python
# redundant calls
user = get_user(user_id)
if user is not None:
    print(f"Found user: {user['name']}")

# creating temporary variables
processed = []
for item in items:
    result = process(item)
    if result is not None:
        processed.append(result)
```

**Correct:**

```python
# eliminating redundancy with walrus operator
if (user := get_user(user_id)) is not None:
    print(f"Found user: {user['name']}")

# leveraging in list comprehension
processed = [result for item in items if (result := process(item)) is not None]

# while loop
while (line := file.readline()):
    process(line)
```

**Why**: The walrus operator eliminates redundancy and makes code more concise. It's especially useful when you need both the result of an expression and a boolean check.

**Common use cases:**
- Conditional checks with assignment
- List comprehensions with filtering
- While loops reading data

Reference: [PEP 572 - Assignment Expressions](https://peps.python.org/pep-0572/)
