---
title: List/Dict/Set Comprehensions
impact: HIGH
impactDescription: Concise, readable, often faster than loops
tags: python, comprehensions, list, dict, set, pythonic
---

## List/Dict/Set Comprehensions

**Impact: HIGH - Concise, readable, often faster than loops**

Use comprehensions instead of imperative loops for transformations.

**Incorrect:**

```python
# imperative style
squared = []
for x in range(10):
    squared.append(x**2)

evens = []
for x in range(10):
    if x % 2 == 0:
        evens.append(x)

user_names = {}
for user in users:
    user_names[user["id"]] = user["name"]
```

**Correct:**

```python
# List comprehension
squared = [x**2 for x in range(10)]

# Conditional comprehension
evens = [x for x in range(10) if x % 2 == 0]

# Nested comprehension
matrix = [[i * j for j in range(3)] for i in range(3)]

# Dict comprehension
user_names = {user["id"]: user["name"] for user in users}

# Set comprehension
unique_ids = {user["id"] for user in users}
```

**Why**: Comprehensions are more concise, readable, and often faster than imperative loops. They express the transformation intent clearly.

**When to use loops instead:**
- Side effects (printing, API calls)
- Complex logic with multiple statements
- When early exit (break) is needed

Reference: [Python Docs - List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
