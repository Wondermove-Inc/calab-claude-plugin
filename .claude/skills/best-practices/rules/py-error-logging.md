---
title: Logging Errors Properly
impact: HIGH
impactDescription: Systematic error recording, easier production debugging
tags: python, errors, logging, production
---

## Logging Errors Properly

**Impact: HIGH - Systematic error recording, easier production debugging**

Use the logging module instead of print for error reporting.

**Incorrect:**

```python
# error output with print
def process_users(user_ids: list[str]) -> list[dict]:
    results = []

    for user_id in user_ids:
        try:
            user = get_user(user_id)
            results.append(user)
        except Exception as e:
            print(f"Error: {e}")  # no logging level, no stack trace

    return results
```

**Correct:**

```python
import logging

logger = logging.getLogger(__name__)

def process_users(user_ids: list[str]) -> list[dict]:
    """Process multiple users with error logging."""
    results = []

    for user_id in user_ids:
        try:
            user = get_user(user_id)
            results.append(user)
        except NotFoundError:
            logger.warning(f"User {user_id} not found", exc_info=True)
        except DatabaseError:
            logger.error(f"Database error for user {user_id}", exc_info=True)
        except Exception:
            logger.exception(f"Unexpected error for user {user_id}")

    return results
```

**Why**: The logging module enables systematic error recording and easier debugging in production environments. It supports log levels, formatters, and handlers.

**Logging levels:**
| Level | Use case |
|-------|----------|
| `DEBUG` | Detailed debugging |
| `INFO` | General information |
| `WARNING` | Something unexpected |
| `ERROR` | Error occurred |
| `CRITICAL` | System failure |

Reference: [Python Docs - logging](https://docs.python.org/3/library/logging.html)
