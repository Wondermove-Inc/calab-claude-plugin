# Testing 베스트 프랙티스 (2025)

> 이 문서는 테스트 코드 작성 시 **반드시** 참조해야 합니다.

---

## 1. 테스트 피라미드

```
        /\
       /  \        E2E Tests (10%)
      /----\       - 핵심 사용자 시나리오
     /      \
    /--------\     Integration Tests (20%)
   /          \    - API, DB 통합
  /------------\
 /              \  Unit Tests (70%)
/                \ - 함수, 컴포넌트 단위
```

---

## 2. 테스트 구조 (AAA 패턴)

```typescript
describe('UserService', () => {
  describe('findById', () => {
    it('should return user when exists', async () => {
      // Arrange (준비)
      const userId = 'test-user-id';
      const mockUser = { id: userId, name: 'Test User' };
      jest.spyOn(userRepository, 'findById').mockResolvedValue(mockUser);

      // Act (실행)
      const result = await userService.findById(userId);

      // Assert (검증)
      expect(result).toEqual(mockUser);
      expect(userRepository.findById).toHaveBeenCalledWith(userId);
    });

    it('should throw NotFoundException when user not exists', async () => {
      // Arrange
      jest.spyOn(userRepository, 'findById').mockResolvedValue(null);

      // Act & Assert
      await expect(userService.findById('invalid-id'))
        .rejects
        .toThrow(NotFoundException);
    });
  });
});
```

---

## 3. 네이밍 규칙

### describe/it 네이밍

```typescript
// describe: 테스트 대상
describe('UserService', () => {
  describe('createUser', () => {
    // it: should [expected behavior] when [condition]
    it('should create user when valid data provided', () => {});
    it('should throw ValidationError when email is invalid', () => {});
    it('should hash password before saving', () => {});
  });
});
```

### 테스트 파일 네이밍

```
user.service.ts      → user.service.test.ts (단위 테스트)
user.service.ts      → user.service.spec.ts (대안)
user.controller.ts   → user.controller.integration.test.ts (통합 테스트)
```

---

## 4. 단위 테스트 (Unit Tests)

### 함수 테스트

```typescript
// utils/format.test.ts
import { formatCurrency, formatDate } from './format';

describe('formatCurrency', () => {
  it('should format number as USD currency', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56');
  });

  it('should handle zero', () => {
    expect(formatCurrency(0)).toBe('$0.00');
  });

  it('should handle negative numbers', () => {
    expect(formatCurrency(-100)).toBe('-$100.00');
  });
});
```

### React 컴포넌트 테스트

```typescript
// components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('should render children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Custom Hook 테스트

```typescript
// hooks/useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('should initialize with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('should initialize with custom value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('should increment count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

---

## 5. 통합 테스트 (Integration Tests)

### API 테스트

```typescript
// features/users/users.integration.test.ts
import request from 'supertest';
import { app } from '../../app';
import { prisma } from '../../lib/prisma';

describe('Users API', () => {
  beforeEach(async () => {
    await prisma.user.deleteMany();
  });

  describe('GET /api/users', () => {
    it('should return empty array when no users', async () => {
      const response = await request(app)
        .get('/api/users')
        .expect(200);

      expect(response.body.data).toEqual([]);
    });

    it('should return users list', async () => {
      // Arrange
      await prisma.user.create({
        data: { email: 'test@example.com', name: 'Test' },
      });

      // Act
      const response = await request(app)
        .get('/api/users')
        .expect(200);

      // Assert
      expect(response.body.data).toHaveLength(1);
      expect(response.body.data[0].email).toBe('test@example.com');
    });
  });

  describe('POST /api/users', () => {
    it('should create user with valid data', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'new@example.com', name: 'New User' })
        .expect(201);

      expect(response.body.data.email).toBe('new@example.com');
    });

    it('should return 400 with invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'invalid', name: 'Test' })
        .expect(400);

      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });
});
```

---

## 6. Mocking

### 모듈 Mocking

```typescript
// Mock 전체 모듈
jest.mock('../services/emailService', () => ({
  sendEmail: jest.fn().mockResolvedValue(true),
}));

// 사용
import { sendEmail } from '../services/emailService';

it('should send welcome email', async () => {
  await userService.createUser({ email: 'test@example.com' });
  expect(sendEmail).toHaveBeenCalledWith(
    'test@example.com',
    'Welcome!'
  );
});
```

### 부분 Mocking

```typescript
jest.mock('../lib/prisma', () => ({
  prisma: {
    user: {
      findUnique: jest.fn(),
      create: jest.fn(),
    },
  },
}));
```

### Spy

```typescript
const findByIdSpy = jest.spyOn(userRepository, 'findById');
findByIdSpy.mockResolvedValue(mockUser);

// 검증
expect(findByIdSpy).toHaveBeenCalledWith('user-id');

// 복원
findByIdSpy.mockRestore();
```

---

## 7. 테스트 데이터

### Factory 패턴

```typescript
// tests/factories/user.factory.ts

/**
 * 테스트용 사용자 데이터 생성
 */
export const createMockUser = (overrides?: Partial<User>): User => ({
  id: 'test-user-id',
  email: 'test@example.com',
  name: 'Test User',
  createdAt: new Date('2024-01-01'),
  updatedAt: new Date('2024-01-01'),
  deletedAt: null,
  ...overrides,
});

// 사용
const user = createMockUser({ name: 'Custom Name' });
```

### Fixture

```typescript
// tests/fixtures/users.json
[
  { "id": "1", "email": "user1@example.com", "name": "User 1" },
  { "id": "2", "email": "user2@example.com", "name": "User 2" }
]

// 사용
import users from '../fixtures/users.json';
```

---

## 8. E2E 테스트 (Playwright)

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should login with valid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message'))
      .toContainText('Invalid credentials');
  });
});
```

---

## 9. 금지 사항

- [ ] 테스트 간 의존성 (순서 의존)
- [ ] 실제 외부 API 호출
- [ ] 하드코딩된 날짜/시간
- [ ] sleep/delay 사용 (waitFor 사용)
- [ ] 스냅샷 남용
- [ ] 테스트 없는 코드 배포

---

## 10. 체크리스트

테스트 작성 시 확인:

- [ ] AAA 패턴 준수
- [ ] 명확한 테스트 이름
- [ ] 테스트 격리 (독립적 실행)
- [ ] Mock/Stub 적절히 사용
- [ ] 에지 케이스 테스트
- [ ] 에러 케이스 테스트
- [ ] 커버리지 80% 이상
