# React 베스트 프랙티스 (2025)

> 이 문서는 React 코드 생성 시 **반드시** 참조해야 합니다.

---

## 1. 컴포넌트 패턴

### 1.1 Function Components (필수)

클래스 컴포넌트 대신 함수형 컴포넌트 사용:

```tsx
// Good
interface UserProfileProps {
  user: User;
  onEdit?: (user: User) => void;
}

const UserProfile: React.FC<UserProfileProps> = ({ user, onEdit }) => {
  return <div>{user.name}</div>;
};

// Bad - 클래스 컴포넌트 사용 금지
class UserProfile extends React.Component { ... }
```

### 1.2 Custom Hooks (로직 분리)

비즈니스 로직은 커스텀 훅으로 분리:

```tsx
// hooks/useUser.ts
/**
 * 사용자 정보를 가져오는 훅
 * @param userId - 사용자 ID
 * @returns 사용자 데이터, 로딩 상태, 에러
 */
export const useUser = (userId: string) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
};

// components/UserProfile.tsx
const UserProfile: React.FC<{ userId: string }> = ({ userId }) => {
  const { user, loading, error } = useUser(userId);

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;
  return <UserCard user={user} />;
};
```

### 1.3 Composition Pattern

상속보다 합성 사용:

```tsx
// Good - 합성
const Card: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="card">{children}</div>
);

const UserCard: React.FC<{ user: User }> = ({ user }) => (
  <Card>
    <Avatar src={user.avatar} />
    <UserInfo user={user} />
  </Card>
);
```

---

## 2. 상태 관리

### 2.1 상태 위치 결정

```
Local State (useState)     → 단일 컴포넌트에서만 사용
Lifted State              → 형제 컴포넌트 간 공유
Context                   → 트리 전체에서 접근 필요
External Store (Zustand)  → 복잡한 전역 상태
Server State (React Query) → API 데이터 캐싱
```

### 2.2 React Query 사용 (서버 상태)

```tsx
/**
 * 사용자 목록을 가져오는 훅
 */
const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000, // 5분
  });
};

/**
 * 사용자 생성 뮤테이션
 */
const useCreateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};
```

### 2.3 Zustand 사용 (전역 상태)

```tsx
interface UserStore {
  user: User | null;
  setUser: (user: User) => void;
  logout: () => void;
}

const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
```

---

## 3. 디렉토리 구조

### Feature-based Structure (권장)

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── SignupForm.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── services/
│   │   │   └── authService.ts
│   │   ├── types/
│   │   │   └── auth.types.ts
│   │   └── index.ts
│   └── users/
│       └── ...
├── shared/
│   ├── components/
│   ├── hooks/
│   └── utils/
└── app/
    └── ...
```

---

## 4. 성능 최적화

### 4.1 메모이제이션

```tsx
// 비싼 계산은 useMemo
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// 콜백은 useCallback
const handleClick = useCallback((id: string) => {
  doSomething(id);
}, [doSomething]);

// 컴포넌트는 React.memo
const ExpensiveComponent = React.memo<{ data: Data }>(({ data }) => {
  return <div>{/* 복잡한 렌더링 */}</div>;
});
```

### 4.2 Code Splitting

```tsx
// 동적 import
const Dashboard = lazy(() => import('./features/dashboard/Dashboard'));

const App = () => (
  <Suspense fallback={<Loading />}>
    <Dashboard />
  </Suspense>
);
```

---

## 5. 타입 정의

### Props 타입

```tsx
interface UserCardProps {
  /** 사용자 정보 */
  user: User;
  /** 수정 버튼 클릭 핸들러 */
  onEdit?: (user: User) => void;
  /** 추가 CSS 클래스 */
  className?: string;
}

const UserCard: React.FC<UserCardProps> = ({ user, onEdit, className }) => {
  // ...
};
```

### Children 타입

```tsx
interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => (
  <div className="layout">{children}</div>
);
```

---

## 6. 에러 처리

### Error Boundary

```tsx
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

---

## 7. 금지 사항

- [ ] 클래스 컴포넌트 사용
- [ ] 인라인 스타일 (Tailwind 사용)
- [ ] 컴포넌트 내 API 직접 호출 (서비스 레이어 사용)
- [ ] any 타입 사용
- [ ] useEffect 남용 (필요한 경우만)
- [ ] Props Drilling 5단계 이상 (Context 사용)
- [ ] index.tsx에 로직 작성 (re-export만)

---

## 8. 체크리스트

코드 생성 시 확인:

- [ ] Function Component 사용
- [ ] Props 타입 정의
- [ ] 비즈니스 로직은 Custom Hook으로 분리
- [ ] 서버 상태는 React Query 사용
- [ ] JSDoc 주석 작성
- [ ] 컴포넌트 500줄 이하
