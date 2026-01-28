---
title: Batch Processing with Promise.allSettled
impact: MEDIUM
impactDescription: Handle partial failures in bulk operations
tags: typescript, async, batch, allSettled, bulk
---

## Batch Processing with Promise.allSettled

**Impact: MEDIUM - Handle partial failures in bulk operations**

Use `Promise.allSettled` for batch operations where you need to handle partial failures without stopping the entire process.

**Incorrect:**

```typescript
// Promise.all fails fast - one rejection stops everything
async function processUsers(userIds: string[]) {
  const results = await Promise.all(
    userIds.map(id => processUser(id))
  );
  return results; // Never reached if any user fails
}

// No concurrency control - can overwhelm external services
async function processAllAtOnce(userIds: string[]) {
  // Launches ALL requests simultaneously
  return Promise.allSettled(userIds.map(id => processUser(id)));
}
```

**Correct:**

```typescript
interface BatchResult<T> {
  succeeded: T[];
  failed: Array<{ item: unknown; error: Error }>;
}

// Semaphore for actual concurrency limiting
class Semaphore {
  private queue: Array<() => void> = [];
  private running = 0;

  constructor(private maxConcurrent: number) {}

  async acquire(): Promise<void> {
    if (this.running < this.maxConcurrent) {
      this.running++;
      return;
    }
    return new Promise(resolve => this.queue.push(resolve));
  }

  release(): void {
    this.running--;
    const next = this.queue.shift();
    if (next) {
      this.running++;
      next();
    }
  }
}

async function processBatch<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  options: { concurrency?: number } = {}
): Promise<BatchResult<R>> {
  const { concurrency = 5 } = options;
  const semaphore = new Semaphore(concurrency);

  const promises = items.map(async (item) => {
    await semaphore.acquire();
    try {
      return await processor(item);
    } finally {
      semaphore.release();
    }
  });

  const results = await Promise.allSettled(promises);

  const succeeded: R[] = [];
  const failed: Array<{ item: T; error: Error }> = [];

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      succeeded.push(result.value);
    } else {
      failed.push({
        item: items[index],
        error: result.reason instanceof Error
          ? result.reason
          : new Error(String(result.reason))
      });
    }
  });

  return { succeeded, failed };
}

// Usage
async function syncAllUsers() {
  const userIds = await getAllUserIds(); // e.g., 1000 users

  // Only 5 concurrent requests at a time
  const { succeeded, failed } = await processBatch(
    userIds,
    async (userId) => {
      const userData = await fetchUserData(userId);
      await updateLocalCache(userId, userData);
      return { userId, synced: true };
    },
    { concurrency: 5 }
  );

  console.log(`Synced ${succeeded.length}/${userIds.length} users`);

  if (failed.length > 0) {
    console.error(`Failed to sync ${failed.length} users:`,
      failed.map(f => f.item)
    );
  }

  return { succeeded, failed };
}

// Alternative: Using p-limit library (recommended for production)
// npm install p-limit
import pLimit from 'p-limit';

async function processBatchWithPLimit<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  concurrency = 5
): Promise<BatchResult<R>> {
  const limit = pLimit(concurrency);

  const results = await Promise.allSettled(
    items.map(item => limit(() => processor(item)))
  );

  // ... same result processing as above
}
```

**Why**: `Promise.allSettled` waits for all promises regardless of outcome, returning both fulfilled and rejected results. Combined with proper concurrency control (semaphore or p-limit), this prevents overwhelming external services while ensuring partial failures don't stop the entire batch.

Reference: [MDN - Promise.allSettled](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled)
