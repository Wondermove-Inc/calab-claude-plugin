---
title: Context API for Shared State
impact: MEDIUM
impactDescription: Eliminates props drilling for truly global state
tags: state, context, props-drilling
---

## Context API for Shared State

**Impact: MEDIUM - Eliminates props drilling for truly global state**

Context provides state to any descendant without explicit props at each level.

**Incorrect (props drilling through many levels):**

```tsx
function App() {
  const [user, setUser] = useState(null)
  return <Layout user={user} setUser={setUser} />
}

function Layout({ user, setUser }) {
  return <Header user={user} setUser={setUser} />
}

function Header({ user, setUser }) {
  return <UserMenu user={user} setUser={setUser} />
}
```

**Correct (context for cross-cutting concerns):**

```tsx
const AuthContext = createContext<AuthContextType | undefined>(undefined)

function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const value = useMemo(() => ({
    user,
    login: async (creds: Credentials) => { /* ... */ },
    logout: () => setUser(null)
  }), [user])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}

// Usage - no drilling
function UserMenu() {
  const { user, logout } = useAuth()
  return <button onClick={logout}>{user?.name}</button>
}
```

**Why**: Context provides state to any descendant without explicit props at each level.

Reference: [Passing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context)
