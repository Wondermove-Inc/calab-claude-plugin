---
title: Parallel Data Fetching with Promise.all
impact: CRITICAL
impactDescription: Reduces total load time to the duration of the slowest request
tags: async, parallel, data-fetching
---

## Parallel Data Fetching with Promise.all

**Impact: CRITICAL - Reduces total load time to the duration of the slowest request**

When data fetches are independent, they should run in parallel. Total time = max(individual times) instead of sum(individual times).

**Incorrect (sequential data fetching):**

```typescript
async function Dashboard() {
  const metrics = await fetchMetrics()
  const alerts = await fetchAlerts()
  const users = await fetchUsers()
  return <DashboardView metrics={metrics} alerts={alerts} users={users} />
}
```

**Correct (parallel data fetching):**

```typescript
async function Dashboard() {
  const [metrics, alerts, users] = await Promise.all([
    fetchMetrics(),
    fetchAlerts(),
    fetchUsers()
  ])
  return <DashboardView metrics={metrics} alerts={alerts} users={users} />
}
```

**Why**: When data fetches are independent, they should run in parallel. Total time = max(individual times) instead of sum(individual times).

Reference: [Data Fetching Patterns](https://nextjs.org/docs/app/building-your-application/data-fetching/fetching)
