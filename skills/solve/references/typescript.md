# TypeScript 베스트 프랙티스 (2025)

> 이 문서는 TypeScript 코드 생성 시 **반드시** 참조해야 합니다.

---

## 1. 타입 정의 원칙

### 1.1 Strict Mode 필수

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true
  }
}
```

### 1.2 any 사용 금지

```typescript
// Bad
const data: any = fetchData();

// Good
interface ApiResponse<T> {
  data: T;
  status: number;
}
const data: ApiResponse<User> = await fetchData();
```

### 1.3 unknown 사용

외부 데이터는 unknown으로 받고 타입 가드 사용:

```typescript
/**
 * 에러 메시지 추출
 */
const getErrorMessage = (error: unknown): string => {
  if (error instanceof Error) {
    return error.message;
  }
  if (typeof error === 'string') {
    return error;
  }
  return 'Unknown error';
};
```

---

## 2. Interface vs Type

### Interface 사용 (객체 형태)

```typescript
// 객체 형태 정의는 interface
interface User {
  id: string;
  name: string;
  email: string;
}

// 확장 가능
interface Admin extends User {
  permissions: string[];
}
```

### Type 사용 (유니온, 유틸리티)

```typescript
// 유니온 타입
type Status = 'pending' | 'approved' | 'rejected';

// 유틸리티 타입
type UserCreateInput = Omit<User, 'id'>;
type UserUpdateInput = Partial<User>;

// 함수 타입
type Handler = (req: Request, res: Response) => Promise<void>;
```

---

## 3. 제네릭 패턴

### 기본 제네릭

```typescript
/**
 * API 응답 래퍼
 */
interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

/**
 * 페이지네이션 응답
 */
interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
```

### 제네릭 함수

```typescript
/**
 * 배열에서 ID로 항목 찾기
 * @param items - 검색할 배열
 * @param id - 찾을 ID
 * @returns 찾은 항목 또는 undefined
 */
const findById = <T extends { id: string }>(
  items: T[],
  id: string
): T | undefined => {
  return items.find(item => item.id === id);
};
```

### 제네릭 제약

```typescript
/**
 * 숫자 키만 허용하는 레코드
 */
type NumericRecord<T extends Record<string, number>> = T;

/**
 * ID가 있는 타입만 허용
 */
type WithId<T extends { id: string }> = T;
```

---

## 4. 유틸리티 타입 활용

### 자주 사용하는 유틸리티 타입

```typescript
// Partial - 모든 속성 선택적
type UserUpdateDto = Partial<User>;

// Required - 모든 속성 필수
type RequiredUser = Required<User>;

// Pick - 특정 속성만 선택
type UserCredentials = Pick<User, 'email' | 'password'>;

// Omit - 특정 속성 제외
type UserWithoutPassword = Omit<User, 'password'>;

// Record - 키-값 매핑
type UserMap = Record<string, User>;

// Exclude - 유니온에서 제외
type NonAdminRole = Exclude<Role, 'admin' | 'superadmin'>;

// Extract - 유니온에서 추출
type AdminRole = Extract<Role, 'admin' | 'superadmin'>;

// ReturnType - 함수 반환 타입
type FetchResult = ReturnType<typeof fetchUser>;

// Parameters - 함수 파라미터 타입
type FetchParams = Parameters<typeof fetchUser>;
```

### 커스텀 유틸리티 타입

```typescript
/**
 * 특정 키를 필수로 만드는 유틸리티 타입
 */
type RequiredKeys<T, K extends keyof T> = T & Required<Pick<T, K>>;

/**
 * 모든 속성을 readonly로 만드는 유틸리티 타입 (깊은)
 */
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

/**
 * null이 아닌 타입
 */
type NonNullableFields<T> = {
  [P in keyof T]: NonNullable<T[P]>;
};
```

---

## 5. 타입 가드

### typeof 가드

```typescript
const processValue = (value: string | number): string => {
  if (typeof value === 'string') {
    return value.toUpperCase();
  }
  return value.toString();
};
```

### instanceof 가드

```typescript
const handleError = (error: Error | string): void => {
  if (error instanceof Error) {
    console.error(error.message);
  } else {
    console.error(error);
  }
};
```

### in 가드

```typescript
interface Dog {
  bark(): void;
}

interface Cat {
  meow(): void;
}

const speak = (animal: Dog | Cat): void => {
  if ('bark' in animal) {
    animal.bark();
  } else {
    animal.meow();
  }
};
```

### 커스텀 타입 가드

```typescript
/**
 * User 타입 가드
 */
const isUser = (obj: unknown): obj is User => {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'email' in obj
  );
};

// 사용
if (isUser(data)) {
  console.log(data.email); // 타입 안전
}
```

---

## 6. Enum vs Union

### Union 타입 권장

```typescript
// Good - Union 타입
type Status = 'pending' | 'approved' | 'rejected';

// 값과 타입이 일치
const status: Status = 'pending';

// 타입 안전한 객체
const StatusLabel: Record<Status, string> = {
  pending: '대기중',
  approved: '승인됨',
  rejected: '거절됨',
};
```

### Enum 사용 (숫자 값 필요 시)

```typescript
// 숫자 값이 필요한 경우
enum HttpStatus {
  OK = 200,
  CREATED = 201,
  BAD_REQUEST = 400,
  NOT_FOUND = 404,
}
```

---

## 7. 함수 타입

### 함수 시그니처

```typescript
// 함수 타입
type Comparator<T> = (a: T, b: T) => number;

// 오버로드
function parse(input: string): number;
function parse(input: number): string;
function parse(input: string | number): string | number {
  if (typeof input === 'string') {
    return parseInt(input, 10);
  }
  return input.toString();
}
```

### Async 함수 타입

```typescript
type AsyncHandler<T> = () => Promise<T>;
type AsyncCallback<T, R> = (data: T) => Promise<R>;
```

---

## 8. 금지 사항

- [ ] any 타입 사용
- [ ] as 타입 단언 남용 (타입 가드 사용)
- [ ] Non-null assertion (!) 남용
- [ ] 암시적 any
- [ ] 타입 없는 함수 파라미터
- [ ] 타입 없는 함수 반환값

---

## 9. 체크리스트

코드 생성 시 확인:

- [ ] strict mode 활성화
- [ ] any 미사용
- [ ] 명시적 타입 정의
- [ ] 타입 가드 사용
- [ ] 유틸리티 타입 활용
- [ ] JSDoc 주석 작성
