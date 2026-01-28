---
title: Retry Pattern with Exponential Backoff
impact: MEDIUM
impactDescription: Resilient async operations
tags: typescript, async, retry, backoff, resilience
---

## Retry Pattern with Exponential Backoff

**Impact: MEDIUM - Resilient async operations**

Implement retry logic with exponential backoff for transient failures in network requests and external service calls.

**Incorrect:**

```typescript
// No retry - fails on first transient error
async function fetchData(url: string) {
  const response = await fetch(url);
  return response.json();
}

// Simple retry without backoff - can overwhelm services
async function fetchWithRetry(url: string) {
  for (let i = 0; i < 3; i++) {
    try {
      return await fetch(url);
    } catch {
      // Immediate retry - no delay
      continue;
    }
  }
  throw new Error('Failed after retries');
}
```

**Correct:**

```typescript
interface RetryOptions {
  maxAttempts?: number;
  baseDelayMs?: number;
  maxDelayMs?: number;
  shouldRetry?: (error: unknown, attempt: number) => boolean;
}

const defaultOptions: Required<RetryOptions> = {
  maxAttempts: 3,
  baseDelayMs: 1000,
  maxDelayMs: 30000,
  shouldRetry: (error) => {
    // Retry on network errors and 5xx responses
    if (error instanceof TypeError) return true; // Network error
    if (error instanceof Response) return error.status >= 500;
    return false;
  }
};

async function withRetry<T>(
  operation: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const opts = { ...defaultOptions, ...options };
  let lastError: unknown;

  for (let attempt = 1; attempt <= opts.maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;

      if (attempt === opts.maxAttempts || !opts.shouldRetry(error, attempt)) {
        throw error;
      }

      // Exponential backoff with jitter
      const delay = Math.min(
        opts.baseDelayMs * Math.pow(2, attempt - 1) + Math.random() * 100,
        opts.maxDelayMs
      );

      console.warn(`Attempt ${attempt} failed, retrying in ${delay}ms...`);
      await sleep(delay);
    }
  }

  throw lastError;
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Usage
async function fetchUserData(userId: string) {
  return withRetry(
    async () => {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw response;
      return response.json();
    },
    {
      maxAttempts: 3,
      baseDelayMs: 500,
      shouldRetry: (error) => {
        if (error instanceof Response) {
          // Retry 5xx, rate limits (429), but not 4xx
          return error.status >= 500 || error.status === 429;
        }
        return true; // Retry network errors
      }
    }
  );
}
```

**Why**: Transient failures (network blips, temporary overload) are common in distributed systems. Exponential backoff prevents overwhelming recovering services while jitter prevents thundering herd problems when many clients retry simultaneously.

Reference: [AWS - Exponential Backoff](https://docs.aws.amazon.com/general/latest/gr/api-retries.html)
