# Next.js 베스트 프랙티스 (2025)

> 이 문서는 Next.js 14+ App Router 코드 생성 시 **반드시** 참조해야 합니다.

---

## 1. App Router 구조

### 디렉토리 구조

```
app/
├── (auth)/                    # Route Group (URL에 미반영)
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── dashboard/
│   ├── layout.tsx             # 레이아웃
│   ├── page.tsx              # 페이지
│   ├── loading.tsx           # 로딩 UI
│   ├── error.tsx             # 에러 UI
│   └── [id]/                 # 동적 라우트
│       └── page.tsx
├── api/                       # Route Handlers
│   └── users/
│       └── route.ts
├── layout.tsx                 # Root 레이아웃
└── page.tsx                   # 홈페이지
```

---

## 2. Server Components vs Client Components

### Server Components (기본값)

```tsx
// app/users/page.tsx
// 'use client' 없으면 Server Component

/**
 * 사용자 목록 페이지 (Server Component)
 * 서버에서 데이터 fetch 후 렌더링
 */
export default async function UsersPage() {
  const users = await fetchUsers(); // 서버에서 직접 fetch

  return (
    <div>
      <h1>Users</h1>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

### Client Components

```tsx
// components/UserForm.tsx
'use client';

import { useState } from 'react';

/**
 * 사용자 폼 (Client Component)
 * 상호작용이 필요한 경우 사용
 */
export default function UserForm() {
  const [name, setName] = useState('');

  return (
    <form>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
    </form>
  );
}
```

### 언제 Client Component 사용?

```
필요한 경우:
- useState, useEffect 등 훅 사용
- 이벤트 핸들러 (onClick, onChange)
- 브라우저 API 사용 (localStorage, window)
- 클라이언트 전용 라이브러리

불필요한 경우:
- 데이터 표시만
- 정적 콘텐츠
- 서버에서 데이터 fetch
```

---

## 3. 데이터 Fetching

### Server Component에서 Fetch

```tsx
// app/users/page.tsx

/**
 * 사용자 데이터 fetch
 */
async function getUsers(): Promise<User[]> {
  const res = await fetch('https://api.example.com/users', {
    cache: 'force-cache', // 기본값: 정적 데이터
    // cache: 'no-store',  // 동적 데이터
    // next: { revalidate: 3600 } // ISR: 1시간마다 재검증
  });

  if (!res.ok) {
    throw new Error('Failed to fetch users');
  }

  return res.json();
}

export default async function UsersPage() {
  const users = await getUsers();
  return <UserList users={users} />;
}
```

### Parallel Data Fetching

```tsx
/**
 * 병렬 데이터 fetch로 성능 최적화
 */
export default async function DashboardPage() {
  // 병렬 fetch
  const [users, products, orders] = await Promise.all([
    getUsers(),
    getProducts(),
    getOrders(),
  ]);

  return (
    <Dashboard users={users} products={products} orders={orders} />
  );
}
```

---

## 4. Server Actions

```tsx
// app/users/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

/**
 * 사용자 생성 Server Action
 * @param formData - 폼 데이터
 */
export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  // 데이터 검증
  if (!name || !email) {
    return { error: 'Name and email are required' };
  }

  // DB 저장
  await prisma.user.create({
    data: { name, email },
  });

  // 캐시 무효화
  revalidatePath('/users');

  return { success: true };
}

// 컴포넌트에서 사용
// app/users/new/page.tsx
import { createUser } from '../actions';

export default function NewUserPage() {
  return (
    <form action={createUser}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

---

## 5. Route Handlers (API Routes)

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

/**
 * 사용자 목록 조회
 */
export async function GET() {
  const users = await prisma.user.findMany();
  return NextResponse.json(users);
}

/**
 * 사용자 생성
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const user = await prisma.user.create({
      data: body,
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 500 }
    );
  }
}
```

### Dynamic Route Handler

```tsx
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

interface Params {
  params: { id: string };
}

/**
 * 특정 사용자 조회
 */
export async function GET(request: NextRequest, { params }: Params) {
  const user = await prisma.user.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(user);
}
```

---

## 6. 메타데이터

### 정적 메타데이터

```tsx
// app/about/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company',
};

export default function AboutPage() {
  return <div>About</div>;
}
```

### 동적 메타데이터

```tsx
// app/users/[id]/page.tsx
import { Metadata } from 'next';

interface Props {
  params: { id: string };
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const user = await getUser(params.id);

  return {
    title: user.name,
    description: `Profile of ${user.name}`,
  };
}

export default async function UserPage({ params }: Props) {
  const user = await getUser(params.id);
  return <UserProfile user={user} />;
}
```

---

## 7. 로딩 & 에러 처리

### Loading UI

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
    </div>
  );
}
```

### Error UI

```tsx
// app/dashboard/error.tsx
'use client';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error, reset }: ErrorProps) {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

---

## 8. 금지 사항

- [ ] 불필요한 'use client' 사용
- [ ] Server Component에서 useState/useEffect
- [ ] API Route에서 직접 DB 접근 (서비스 레이어 사용)
- [ ] 클라이언트에서 민감 환경변수 접근
- [ ] 과도한 동적 렌더링 (가능하면 정적 생성)
- [ ] Image 컴포넌트 대신 img 태그 사용

---

## 9. 체크리스트

코드 생성 시 확인:

- [ ] Server vs Client Component 적절히 구분
- [ ] 데이터 fetching은 Server Component에서
- [ ] Server Actions로 뮤테이션
- [ ] 메타데이터 설정
- [ ] loading.tsx, error.tsx 추가
- [ ] Next/Image 컴포넌트 사용
- [ ] JSDoc 주석 작성
