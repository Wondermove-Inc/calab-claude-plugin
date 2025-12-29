# 코딩 컨벤션

> 이 문서는 `/onboard` 명령어로 자동 생성됩니다.
> 모든 코드 작성 시 이 컨벤션을 준수하세요.

---

## 네이밍 규칙

### 파일/폴더

| 대상 | 규칙 | 예시 |
|------|------|------|
| 컴포넌트 | PascalCase | `UserProfile.tsx` |
| 훅 | camelCase + use 접두사 | `useAuth.ts` |
| 유틸리티 | camelCase | `formatDate.ts` |
| 타입 | PascalCase | `UserTypes.ts` |
| 상수 | UPPER_SNAKE_CASE | `API_ENDPOINTS.ts` |
| 폴더 | kebab-case | `user-profile/` |

### 변수/함수

| 대상 | 규칙 | 예시 |
|------|------|------|
| 변수 | camelCase | `userName`, `isLoading` |
| 함수 | camelCase + 동사 | `getUserById`, `handleClick` |
| 상수 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 타입/인터페이스 | PascalCase | `UserProfile`, `IRepository` |
| Enum | PascalCase | `UserStatus`, `OrderType` |

### Boolean 네이밍

```typescript
// Good
isLoading, hasError, canEdit, shouldRender

// Bad
loading, error, edit, render
```

---

## 파일 구조 규칙

### 컴포넌트 폴더

```
ComponentName/
├── index.ts              # export
├── ComponentName.tsx     # 컴포넌트
├── ComponentName.test.tsx # 테스트
├── ComponentName.styles.ts # 스타일 (styled-components)
└── types.ts              # 타입 정의
```

### 기능 폴더 (Feature)

```
feature-name/
├── components/
├── hooks/
├── services/
├── types/
├── utils/
└── index.ts
```

---

## Import 순서

```typescript
// 1. React/Next.js
import React from 'react';
import { useRouter } from 'next/router';

// 2. 외부 라이브러리
import { useQuery } from '@tanstack/react-query';
import clsx from 'clsx';

// 3. 내부 모듈 (절대 경로)
import { Button } from '@/components/ui';
import { useAuth } from '@/hooks/useAuth';
import { UserService } from '@/services/user';

// 4. 상대 경로 import
import { UserCard } from './UserCard';
import { formatUserName } from './utils';

// 5. 타입 import
import type { User, UserRole } from '@/types';

// 6. 스타일
import styles from './Component.module.css';
```

---

## 주석 규칙

### 함수 주석 (JSDoc)

```typescript
/**
 * 사용자 정보를 조회합니다.
 *
 * @param userId - 사용자 ID
 * @returns 사용자 정보 객체
 * @throws {NotFoundError} 사용자를 찾을 수 없는 경우
 */
async function getUserById(userId: string): Promise<User> {
  // ...
}
```

### 인라인 주석

```typescript
// 단일 라인 설명
const result = calculate(); // 계산 결과

/*
 * 복잡한 로직 설명
 * 여러 줄이 필요한 경우
 */
```

### TODO/FIXME

```typescript
// TODO: 이 기능 구현 필요
// FIXME: 버그 수정 필요
// NOTE: 참고 사항
// HACK: 임시 해결책
```

---

## Git 커밋 메시지

### 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

| Type | 설명 |
|------|------|
| feat | 새 기능 |
| fix | 버그 수정 |
| docs | 문서 변경 |
| style | 코드 포맷팅 |
| refactor | 리팩토링 |
| test | 테스트 추가/수정 |
| chore | 빌드, 설정 변경 |

### 예시

```
feat(auth): 로그인 기능 구현

- JWT 토큰 기반 인증 추가
- 리프레시 토큰 처리 구현
- 로그아웃 기능 추가

Closes #123
```

---

## 코드 스타일

### 함수 정의

```typescript
// 선호: 화살표 함수
const handleClick = () => { ... };

// 비선호: function 키워드
function handleClick() { ... }
```

### 조건문

```typescript
// 선호: 얼리 리턴
if (!user) return null;
if (!user.isActive) return <Inactive />;
return <Dashboard />;

// 비선호: 중첩 조건
if (user) {
  if (user.isActive) {
    return <Dashboard />;
  } else {
    return <Inactive />;
  }
}
return null;
```

### 삼항 연산자

```typescript
// 단순한 경우만 사용
const status = isActive ? 'active' : 'inactive';

// 복잡한 경우 if/else 사용
```

---

## 금지 사항

| 항목 | 이유 |
|------|------|
| `any` 타입 | 타입 안전성 저하 |
| `console.log` | 프로덕션 코드 오염 |
| 하드코딩된 비밀키 | 보안 위험 |
| 매직 넘버 | 가독성 저하 |
| 300줄 초과 파일 | 유지보수 어려움 |

---

*이 문서는 /onboard 명령어로 자동 생성되었습니다.*
*갱신: /context-refresh*
