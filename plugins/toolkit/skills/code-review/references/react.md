# React 코드 리뷰 가이드

## 목차
1. [Hook 규칙](#1-hook-규칙)
2. [컴포넌트 설계](#2-컴포넌트-설계)
3. [상태 관리](#3-상태-관리)
4. [렌더링 최적화](#4-렌더링-최적화)

---

## 1. Hook 규칙

### 1.1 최상위에서만 호출

Hook은 컴포넌트 최상위에서만 호출해야 한다. React는 Hook 호출 순서로 상태를 관리하므로, 조건문이나 반복문 안에서 호출하면 렌더링마다 호출 순서가 달라져 상태가 꼬인다.

```tsx
// Bad — 조건부 Hook 호출
function UserProfile({ userId }: { userId?: string }) {
  if (!userId) return null;
  const [user, setUser] = useState<User | null>(null); // Hook 순서 불안정
  useEffect(() => { fetchUser(userId).then(setUser); }, [userId]);
  return <div>{user?.name}</div>;
}

// Good — Hook은 항상 최상위에서 호출
function UserProfile({ userId }: { userId?: string }) {
  const [user, setUser] = useState<User | null>(null);
  useEffect(() => {
    if (!userId) return;
    fetchUser(userId).then(setUser);
  }, [userId]);
  if (!userId) return null;
  return <div>{user?.name}</div>;
}
```

### 1.2 의존성 배열

의존성 배열을 정확히 명시하지 않으면 stale closure(오래된 값 참조) 또는 무한 루프가 발생한다. ESLint의 `react-hooks/exhaustive-deps` 규칙을 활성화하고, 경고를 무시하지 않는다.

```tsx
// Bad — count가 의존성에 빠짐 (항상 초기값 0 참조)
useEffect(() => {
  const id = setInterval(() => setCount(count + 1), 1000);
  return () => clearInterval(id);
}, []); // count 누락

// Good — 함수형 업데이트로 의존성 제거
useEffect(() => {
  const id = setInterval(() => setCount(prev => prev + 1), 1000);
  return () => clearInterval(id);
}, []);
```

### 1.3 커스텀 Hook으로 로직 분리

컴포넌트에 비즈니스 로직이 섞이면 테스트가 어렵고 재사용이 불가능하다. 상태 + 사이드이펙트 로직을 커스텀 Hook으로 추출하면, 컴포넌트는 순수한 렌더링에만 집중할 수 있다.

```tsx
// Bad — 컴포넌트에 로직이 섞임
function OrderList() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  useEffect(() => {
    setLoading(true);
    fetchOrders()
      .then(setOrders)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  // ... 렌더링 로직
}

// Good — 로직을 Hook으로 분리
function useOrders() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  useEffect(() => {
    setLoading(true);
    fetchOrders()
      .then(setOrders)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  return { orders, loading, error };
}

function OrderList() {
  const { orders, loading, error } = useOrders();
  // ... 렌더링에만 집중
}
```

---

## 2. 컴포넌트 설계

### 2.1 Prop drilling 경계

Props를 3단계 이상 전달하면 중간 컴포넌트가 자신과 무관한 props를 전달하는 "전달자" 역할만 하게 된다. 변경 시 모든 중간 단계를 수정해야 하므로 유지보수 비용이 급증한다.

```tsx
// Bad — 3단계 이상 전달
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserBadge user={user} />

// Good — Context로 전달
const UserContext = createContext<User | null>(null);

function App() {
  return (
    <UserContext.Provider value={user}>
      <Layout><Sidebar><UserBadge /></Sidebar></Layout>
    </UserContext.Provider>
  );
}

function UserBadge() {
  const user = useContext(UserContext);
  return <span>{user?.name}</span>;
}
```

### 2.2 컴포넌트 크기

100줄 이상의 컴포넌트는 여러 책임을 담고 있을 가능성이 높다. 렌더링 로직, 이벤트 핸들러, 데이터 변환을 분리하면 각 부분을 독립적으로 테스트하고 재사용할 수 있다.

---

## 3. 상태 관리

### 3.1 파생 상태 지양

다른 상태에서 계산할 수 있는 값을 별도 상태로 관리하면 동기화 버그가 발생한다. 원본 상태가 변경되었는데 파생 상태 업데이트를 빠뜨리면 UI 불일치가 생긴다.

```tsx
// Bad — items에서 파생 가능한 상태를 별도 관리
const [items, setItems] = useState<Item[]>([]);
const [filteredItems, setFilteredItems] = useState<Item[]>([]);
const [itemCount, setItemCount] = useState(0);

// Good — 렌더링 중에 계산
const [items, setItems] = useState<Item[]>([]);
const filteredItems = items.filter(item => item.active);
const itemCount = filteredItems.length;
```

### 3.2 상태 최소화

컴포넌트의 상태는 렌더링에 필요한 최소한의 데이터만 포함해야 한다. 불필요한 상태는 리렌더링을 유발하고, 상태 간 동기화 실수를 증가시킨다.

---

## 4. 렌더링 최적화

### 4.1 useMemo / useCallback

렌더링마다 새로운 객체/함수 참조가 생성되면, 자식 컴포넌트가 `React.memo`로 감싸져 있어도 매번 리렌더링된다. 비용이 큰 계산이나 자식에 전달되는 콜백에 memoization을 적용한다.

```tsx
// Bad — 매 렌더마다 새로운 함수 참조
function Parent({ items }: { items: Item[] }) {
  const sorted = items.sort((a, b) => a.name.localeCompare(b.name));
  const handleClick = (id: string) => selectItem(id);
  return <ChildList items={sorted} onClick={handleClick} />;
}

// Good — 안정적 참조 유지
function Parent({ items }: { items: Item[] }) {
  const sorted = useMemo(
    () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
    [items]
  );
  const handleClick = useCallback((id: string) => selectItem(id), []);
  return <ChildList items={sorted} onClick={handleClick} />;
}
```

### 4.2 key 속성

리스트 렌더링에서 `key`에 인덱스를 사용하면, 항목이 추가/삭제/재정렬될 때 React가 DOM을 잘못 매칭하여 상태가 꼬이거나 불필요한 DOM 조작이 발생한다.

```tsx
// Bad — 인덱스를 key로 사용
{items.map((item, i) => <Item key={i} data={item} />)}

// Good — 고유한 식별자 사용
{items.map(item => <Item key={item.id} data={item} />)}
```
