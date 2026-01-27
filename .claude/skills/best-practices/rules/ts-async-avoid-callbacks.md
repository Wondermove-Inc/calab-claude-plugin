---
title: Avoid Callback Hell with Async/Await
impact: MEDIUM
impactDescription: Improved code readability, easier debugging
tags: typescript, async, await, callbacks, readability
---

## Avoid Callback Hell with Async/Await

**Impact: MEDIUM - Improved code readability, easier debugging**

Use async/await to write asynchronous code that reads like synchronous code.

**Incorrect:**

```typescript
// callback hell
function createUserWithProfile(userData: UserData, callback: (err: Error | null, result?: UserProfile) => void) {
  createUser(userData, (err, user) => {
    if (err) return callback(err);
    createProfile(user.id, (err, profile) => {
      if (err) return callback(err);
      initializeSettings(user.id, (err, settings) => {
        if (err) return callback(err);
        callback(null, { user, profile, settings });
      });
    });
  });
}
```

**Correct:**

```typescript
async function createUserWithProfile(userData: UserData): Promise<UserProfile> {
  const user = await createUser(userData);
  const profile = await createProfile(user.id);
  const settings = await initializeSettings(user.id);

  return { user, profile, settings };
}
```

**Why**: Using async/await makes asynchronous code as readable as synchronous code. Error handling is cleaner with try/catch, and the flow of execution is easier to follow.

Reference: [MDN - async/await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises)
