---
title: Unpacking and Pattern Matching
impact: MEDIUM
impactDescription: Concise, readable code
tags: python, unpacking, pattern-matching, destructuring, pythonic
---

## Unpacking and Pattern Matching

**Impact: MEDIUM - Concise, readable code**

Use unpacking and pattern matching for cleaner data extraction.

**Incorrect:**

```python
# explicit indexing
items = [1, 2, 3, 4, 5]
first = items[0]
rest = items[1:]

# manual dict copying
user = {"id": "1", "name": "John", "age": 30}
user_with_email = user.copy()
user_with_email["email"] = "john@example.com"

# if-elif chain
def process_command(command: dict) -> str:
    if command.get("action") == "create":
        return f"Creating {command['resource']} with {command['data']}"
    elif command.get("action") == "delete":
        return f"Deleting {command['resource']} {command['id']}"
    elif command.get("action") == "list":
        return f"Listing {command['resource']}"
    else:
        return "Unknown command"
```

**Correct:**

```python
# Tuple unpacking
first, *rest = [1, 2, 3, 4, 5]
print(first)  # 1
print(rest)   # [2, 3, 4, 5]

# Dict unpacking
user = {"id": "1", "name": "John", "age": 30}
user_with_email = {**user, "email": "john@example.com"}

# Pattern matching (Python 3.10+)
def process_command(command: dict) -> str:
    match command:
        case {"action": "create", "resource": resource, "data": data}:
            return f"Creating {resource} with {data}"
        case {"action": "delete", "resource": resource, "id": id}:
            return f"Deleting {resource} {id}"
        case {"action": "list", "resource": resource}:
            return f"Listing {resource}"
        case _:
            return "Unknown command"
```

**Why**: Unpacking and pattern matching make code more concise and readable. Pattern matching also ensures exhaustive handling of cases.

Reference: [PEP 634 - Structural Pattern Matching](https://peps.python.org/pep-0634/)
