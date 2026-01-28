---
title: useState for Local State
impact: MEDIUM
impactDescription: Simpler code, fewer dependencies
tags: state, useState, local-state
---

## useState for Local State

**Impact: MEDIUM - Simpler code, fewer dependencies**

Not all state needs to be global. Local state is simpler and has no external dependencies.

**Incorrect (using global state for local concerns):**

```tsx
function SearchInput() {
  const dispatch = useDispatch()
  const { query, results, isLoading } = useSelector(state => state.search)

  const handleSearch = (value: string) => {
    dispatch(setQuery(value))
    dispatch(fetchResults(value))
  }

  return <input value={query} onChange={(e) => handleSearch(e.target.value)} />
}
```

**Correct (local state for local concerns):**

```tsx
function SearchInput() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (value: string) => {
    setQuery(value)
    setIsLoading(true)
    try {
      const data = await searchUsers(value)
      setResults(data)
    } finally {
      setIsLoading(false)
    }
  }

  return <input value={query} onChange={(e) => handleSearch(e.target.value)} />
}
```

**Why**: Not all state needs to be global. Local state is simpler and has no external dependencies.

Reference: [State: A Component's Memory](https://react.dev/learn/state-a-components-memory)
