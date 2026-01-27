---
title: Try-Except-Else-Finally
impact: MEDIUM
impactDescription: Clear error handling logic, proper cleanup
tags: python, errors, try, except, else, finally
---

## Try-Except-Else-Finally

**Impact: MEDIUM - Clear error handling logic, proper cleanup**

Use the else block to minimize try block scope.

**Incorrect:**

```python
# all logic in try block without else
def process_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as f:
            data = f.read()
        print(f"Successfully read {file_path}")
        result = parse_data(data)  # parse_data errors also caught by except
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        print(f"Finished processing {file_path}")
```

**Correct:**

```python
def process_file(file_path: str) -> dict:
    """Process file and return result."""
    try:
        with open(file_path, 'r') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    except PermissionError:
        print(f"Permission denied: {file_path}")
        raise
    else:
        # runs only when no exception occurred
        print(f"Successfully read {file_path}")
        return parse_data(data)
    finally:
        # always runs
        print(f"Finished processing {file_path}")
```

**Why**: Using the else block minimizes the try block scope and clarifies error handling logic. Errors in the else block are not caught by the except clauses.

**Block purposes:**
| Block | When it runs |
|-------|-------------|
| `try` | Code that might raise exceptions |
| `except` | When specific exception occurs |
| `else` | When no exception occurred |
| `finally` | Always (cleanup) |

Reference: [Python Docs - Handling Exceptions](https://docs.python.org/3/tutorial/errors.html#handling-exceptions)
