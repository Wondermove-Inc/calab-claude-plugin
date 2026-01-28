---
title: useCallback for Stable Function References
impact: MEDIUM
impactDescription: Prevents child re-renders due to new function references
tags: useCallback, performance, re-render
---

## useCallback for Stable Function References

**Impact: MEDIUM - Prevents child re-renders due to new function references**

useCallback returns the same function reference unless dependencies change.

**Incorrect (new function reference on every render):**

```tsx
function UserSearch() {
  const [query, setQuery] = useState('')

  // Created fresh on every render
  const handleSearch = async (value: string) => {
    setQuery(value)
    await searchUsers(value)
  }

  // SearchInput re-renders every time (if it uses memo)
  return <SearchInput onSearch={handleSearch} />
}
```

**Correct (stable function reference):**

```tsx
function UserSearch() {
  const [query, setQuery] = useState('')

  const handleSearch = useCallback(async (value: string) => {
    setQuery(value)
    await searchUsers(value)
  }, []) // Empty deps = never changes

  return <SearchInput onSearch={handleSearch} />
}

const SearchInput = React.memo(function SearchInput({
  onSearch
}: {
  onSearch: (v: string) => void
}) {
  return <input onChange={(e) => onSearch(e.target.value)} />
})
```

**Why**: useCallback returns the same function reference unless dependencies change.

Reference: [useCallback](https://react.dev/reference/react/useCallback)
